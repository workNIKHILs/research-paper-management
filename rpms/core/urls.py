from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('publications/', views.publication_list, name='publication_list'),
    path('self-upload/', views.self_upload, name='self_upload'),
    path('upload/', views.upload_publication, name='upload_publication'),
    path('upload/confirm/', views.upload_confirm, name='upload_confirm'),
    path('export/', views.export_page, name='export_page'),
    path('export/download/', views.export_download, name='export_download'),
]