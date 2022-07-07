from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.PostListViewHome.as_view(), name='home'),
    path('posts/search/', views.PostListViewSearch.as_view(), name='search'),
    path(
        'posts/tags/<slug:slug>/',
        views.PostListViewTag.as_view(),
        name='tag'
    ),
    path('posts/category/<int:category_id>/', views.category, name='category'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post'),
    path(
        'posts/api/v1/',
        views.PostHomeListViewApi.as_view(),
        name='home_view_api'
    ),
    path(
        'posts/api/v1/<int:pk>/',
        views.PostDetailViewApi.as_view(),
        name='post_view_api'
    ),
    path('posts/theory/', views.theory, name='theory'),
]
