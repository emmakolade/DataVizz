from django.urls import path

from .views import FileUploadView, FileRetrieveView, FileDisplayView
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('file/<int:id>/', FileRetrieveView.as_view(), name='retrieve'),
    path('<int:id>/display/', FileDisplayView.as_view(), name='display'),
]
