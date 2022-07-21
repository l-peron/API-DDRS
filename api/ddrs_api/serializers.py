from rest_framework import serializers
from ddrs_api.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name_text']
