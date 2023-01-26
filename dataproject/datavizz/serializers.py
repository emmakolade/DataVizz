from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from .models import Data
import pandas as pd


class DataSerializer(serializers.ModelSerializer):
    data_file = serializers.FileField(required=True,
                                      upload_to='uploads/', validators=[FileExtensionValidator(['csv', 'xlsx'])])

    class Meta:
        model = Data
        fields = ['name', 'value', 'date', 'category', 'data_file']

    def create(self, validated_data):

        data_file = validated_data.pop('data_file')
        if data_file.name.endswith('.csv'):
            df = pd.read_csv(data_file)
        elif data_file.name.endswith('.xlsx'):
            df = pd.read_excel(data_file)
        else:
            raise serializers.ValidationError("file format not supported.")

        # clean and process the data

        for index, row in df.iterrows():
            data = Data(name=row['name'], value=row['value'],
                        date=row['date'], category=row['category'])
