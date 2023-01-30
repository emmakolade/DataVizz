

from django.urls import path

from .views import FileUploadView, FileRetrieveView, FileDisplayView, FileDownloadView
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('file/<int:id>/', FileRetrieveView.as_view(), name='retrieve'),
    path('display/<int:id>/', FileDisplayView.as_view(), name='display'),
    path('download/<int:id>/',
         FileDownloadView.as_view(), name='download_file'),
]
