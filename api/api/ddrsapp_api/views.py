from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from api.ddrsapp_api.serializers import UserSerializer, GroupSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]