from django.urls import path
from .import views

app_name = 'comments'

urlpatterns = [
    path('add_comment/<int:pk>', views.add_comment, name='add_comment')
]