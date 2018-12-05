from django.urls import path
from .views import upload_file, OCRDetails

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('ocr_details/<int:pk>/', OCRDetails.as_view(), name='ocr_details')

]
