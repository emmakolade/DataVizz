from rest_framework import serializers
from .models import DataFile
import pandas as pd


class DataFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataFile
        fields = ['id', 'file', 'timestamp']

