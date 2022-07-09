from django.urls import path
from .views import site
from .views import api

app_name = 'posts'

urlpatterns = [
    path('', site.PostListViewHome.as_view(), name='home'),
    path('posts/search/', site.PostListViewSearch.as_view(), name='search'),
    path(
        'posts/tags/<slug:slug>/',
        site.PostListViewTag.as_view(),
        name='tag'
    ),
    path('posts/category/<int:category_id>/', site.category, name='category'),
    path('posts/<int:pk>/', site.PostDetail.as_view(), name='post'),
    path(
        'posts/api/v1/',
        site.PostHomeListViewApi.as_view(),
        name='home_view_api'
    ),
    path(
        'posts/api/v1/<int:pk>/',
        site.PostDetailViewApi.as_view(),
        name='post_view_api'
    ),
    path('posts/theory/', site.theory, name='theory'),
    path(
        'posts/api/v2/',
        api.PostAPIv2List.as_view(),
        name='posts_api_v2'
    ),
    path(
        'posts/api/v2/<int:pk>/',
        api.PostAPIv2Detail.as_view(),
        name='posts_api_v2_detail'
    ),
]
