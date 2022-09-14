from curses.ascii import HT
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

class admin_example(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):
        return HttpResponse(status = 200)