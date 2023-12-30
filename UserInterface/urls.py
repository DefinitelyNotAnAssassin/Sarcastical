from django.urls import path    

from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),
    path('translate', views.translate, name = "translate"),
    path('help', views.TheRelationshipSaviourView, name = "The Relationship Saviour"),
    
    
]