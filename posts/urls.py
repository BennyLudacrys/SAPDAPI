from . import views
from .views import PersonListAPIView, PersonDetailAPIView, get_free_posts
from django.urls import path

from comments.views import CommentListCreateAPIView, CommentDetailAPIView

urlpatterns = [
    path('', PersonListAPIView.as_view(), name="list-posts"),
    path('<int:id>', PersonDetailAPIView.as_view(), name="detail-posts"),
    path('<int:post_id>/detection/', views.get_posts_by_user, name='detection'),
    path('<int:user_id>/posts/', views.get_posts_by_user, name='get_posts_by_user'),
    path('posts/<int:post_id>/', views.get_post, name='get_post'),
    path('allPosts/', views.get_all_posts, name='get_all_posts'),
    path('posts/<int:post_id>/change-status/', views.change_statuss, name='change_post_status'),
    path('posts/<int:post_id>/change-status/', views.PersonDetailAPIView.change_status, name='change_post_status'),
    path('free-posts/', views.get_free_posts, name='get_free_posts'),
    path('get-post/', views.get_posts_by_status, name='get_post'),

    path('<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('<int:post_id>/comments/<int:id>/', CommentDetailAPIView.as_view(), name='comment-detail'),


]
