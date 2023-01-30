from rest_framework import serializers
from .models import DataFile
import pandas as pd


class DataFileSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        file = validated_data.pop('file')
        data_file = DataFile.objects.create(**validated_data)
        data_file.file.save(file.name, file)
        data_file.save()
        return data_file

    class Meta:
        model = DataFile
        fields = ['id', 'file', 'timestamp']
