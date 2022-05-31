from django.urls import path

from . import views


urlpatterns = [
    # Home page
    path('', views.Index.as_view(), name='index'),
    
    # Document operations
    path('documents/', views.DocumentsView.as_view(), name='list_documents'),
    path('document/<int:pk>/', views.DocumentPageView.as_view(), name='document_page'),
    path('document/<int:pk>/update/', views.DocumentUpdateView.as_view(), name='document_update'),
    path('document/<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document_delete'),
    path('document/create/', views.DocumentCreateView.as_view(), name='document_create'),
    path('document/<int:pk>/finish/', views.finish_document, name='document_finish'),
    
    # Generate pdf
    path('document/<int:pk>/generate_pdf/', views.ViewPDF.as_view(), name='document_pdf'),
]