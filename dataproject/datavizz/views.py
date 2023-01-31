from django.shortcuts import render
import xlrd
from rest_framework import status, generics, serializers
from .models import DataFile
from rest_framework import viewsets
from .serializers import DataFileSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.http import FileResponse, HttpResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer

# Create your views here.


class FileUploadView(generics.CreateAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    parser_classes = (MultiPartParser, FileUploadParser, FormParser)
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        file = self.request.data['file']
        if file.size > 10485760:  # 10MB
            raise serializers.ValidationError('file must be less than 10mb')
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class FileRetrieveView(generics.RetrieveAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.file.path
        # check if file is csv or excel file
        valid_extension = ['.csv', '.xls', '.xlsx']
        if not any(file.endswith(ext) for ext in valid_extension):
            raise ValueError(
                f'file must have one of the following extensions: {", ".join(valid_extension)}')
        # use pandas to clean
        if file.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.endswith('.xls') or file.endswith('.xlsx'):
            df = pd.read_excel(file)

        # handle missing values differently based on the type of data in each column
        for column in df.columns:
            if df[column].dtype == 'float64':
                df[column].fillna(df[column].mean(), inplace=True)
            elif df[column].dtype == 'int64':
                df[column].fillna(df[column].median(), inplace=True)
            else:
                df[column].fillna('Unknown', inplace=True)

        # remove or replace outliers in the data
        for column in df.columns:
            if df[column].dtype == 'float64' or df[column].dtype == 'int64':
                q1 = df[column].quantile(0.25)
                q3 = df[column].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - (1.5 * iqr)
                upper_bound = q3 + (1.5 * iqr)
                df = df[(df[column] >= lower_bound) &
                        (df[column] <= upper_bound)]

        # handle data that is in the wrong format
        for column in df.columns:
            if df[column].dtype == 'object':
                try:
                    df[column] = pd.to_datetime(df[column])
                except ValueError:
                    pass

        # handle data that is in the wrong range
        for column in df.columns:
            if df[column].dtype == 'int64':
                df = df[(df[column] >= 0) & (df[column] <= 120)]

        # handle data that is not consistent
        for column in df.columns:
            if df[column].dtype == 'object':
                df[column] = df[column].str.lower().str.strip()
                df[column] = df[column].astype('category')

        df = df.drop_duplicates()  # removes duplicate rows
        df = df.dropna(axis='columns', how='all')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


# function to handle file download and display
def display_and_download(file):
    if file.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.endswith('.xls') or file.endswith('.xlsx'):
        data = pd.read_excel(file)

    x = None
    y = None

    for colunm in data.columns:
        if x is None:
            x = data[colunm]
        elif y is None:
            y = data[colunm]
        else:
            break

    if x is None or y is None:
        return None
    plt.plot(x, y)
    return plt


class FileDisplayView(generics.RetrieveAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.file.path
        plot = display_and_download(file)
        if plot is None:
            return Response("No suitable x and y values found in DataFrame")
        plot.show()
        return Response("data displayed")

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class FileDownloadView(generics.RetrieveAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.file.path
        plot = display_and_download(file)
        if plot is None:
            return Response("No suitable x and y values found in DataFrame")
        plot.savefig('data.pdf')
        response = FileResponse(open('data.pdf', 'rb'),
                                content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=data.pdf'
        # with open('data.pdf', 'rb') as pdf:
        #     response = HttpResponse(pdf.read(), content_type='application/pdf')
        #     response['Content-Disposition'] = 'inline;filename=data.pdf'
        return Response("data downloaded as pdf")

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


'''
def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.file.path
        # check if file is csv or excel file
        valid_extension = ['.csv', '.xls', '.xlsx']
        if not any(file.endswith(ext) for ext in valid_extension):
            raise ValueError(
                f'file must have one of the following extensions: {", ".join(valid_extension)}')
        # use pandas to clean
        if file.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.endswith('.xls') or file.endswith('.xlsx'):
            df = pd.read_excel(file)

        # perform additional cleaning and procesing on the Dataframe
        df = df.dropna()  # remove rows with missing values
        df = df.drop_duplicates()  # removes duplicate rows
        df = df.dropna(axis='columns', how='all')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
'''
