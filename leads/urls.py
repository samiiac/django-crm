
from django.urls import path
from .views import (lead_list,lead_detail,lead_create,lead_update,
LeadDetailView,LeadListView,LeadCreateView,LeadUpdateView,LeadDeleteView
,AssignAgentView,CategoryListView,CategoryDetailView,LeadCategoryUpdateView,CategoryCreateView,CategoryDeleteView)

urlpatterns = [
    path('',LeadListView.as_view(),name='leads-list'),
    path('<int:pk>/',LeadDetailView.as_view(),name='leads-detail'),
    path('create-lead/',LeadCreateView.as_view(),name='leads-create'),
    path('update-lead/<int:pk>/',LeadUpdateView.as_view(),name='leads-update'),
    path('delete-lead/<int:pk>/',LeadDeleteView.as_view(),name='leads-delete'),
    path('assign-agent/<int:pk>/',AssignAgentView.as_view(),name='assign-agent'),
    path('category/',CategoryListView.as_view(),name='category-list'),
    path('category/<int:pk>/',CategoryDetailView.as_view(),name = 'category-detail'),
    path('update-category/<int:pk>/',LeadCategoryUpdateView.as_view(),name='update-category'),
    path('delete-category/<int:pk>/',CategoryDeleteView.as_view(),name='delete-category'),
    path('create-category',CategoryCreateView.as_view(),name='create-category')
]