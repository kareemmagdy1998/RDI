from django.urls import path
from .views import ConvertPDFToImageView, FileUploadView, ImageListView, PDFDeleteView, PDFListView, ImageDetailView, PDFDetailView, ImageDeleteView, RotateImageView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('images/', ImageListView.as_view(), name='image-list'),
    path('pdfs/', PDFListView.as_view(), name='pdf-list'),
    path('images/<int:id>/', ImageDetailView.as_view(), name='image-detail'),
    path('pdfs/<int:id>/', PDFDetailView.as_view(), name='pdf-detail'),
    path('images/<int:id>/delete/', ImageDeleteView.as_view(), name='image-delete'),
    path('pdfs/<int:id>/delete/', PDFDeleteView.as_view(), name='pdf-delete'),
    path('rotate/', RotateImageView.as_view(), name='rotate-image'),
    path('convert-pdf-to-image/', ConvertPDFToImageView.as_view(), name='convert-pdf-to-image'),
]