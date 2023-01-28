from rest_framework import status, generics, serializers
from .models import DataFile
from .serializers import DataFileSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response


from django.http import FileResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd

# Create your views here.


class FileUploadView(generics.CreateAPIView):
    serializer_class = DataFileSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        file = self.request.data['file']
        if file.size > 10485760:  # 10MB
            raise serializers.ValidationError('file must be less than 10mb')
        serializer.save()


class FileRetrieveView(generics.RetrieveAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    lookup_field = 'file'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.file_path
        # check if file is csv or excel file
        valid_extension = ['.csv', '.xls', 'xlsx']
        if not any(file_path.endswith(ext) for ext in valid_extension):
            raise ValueError(
                f'file must have one of the following extensions: {", ".join(valid_extension)}')
        # use pandas to clean
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)

        # perform additional cleaning and procesing on the Dataframe
        df = df.dropna()  # remove rows with missing values
        df = df.drop_duplicates()  # removes duplicate rows
        df = df.dropna(subset=df.columns, how='all')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# def retrieve(self, request, *args, **kwargs):
#        instance = self.get_object()
#        file_path = instance.file.path
#        # check if file is csv or excel file
#        if not (file_path.endswith('.csv') or file_path.endswith('.xlsx')):
#             raise ValueError('File must be csv or excel')
#         # use pandas to clean and process the uploaded file
#         data = pd.read_csv(file_path) if file_path.endswith(
#             '.csv') else pd.read_excel(file_path)
#         cleaned_data = data.dropna()
#         return Response(cleaned_data.to_json())
