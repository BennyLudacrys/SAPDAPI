from . import views
from .views import PersonListAPIView, PersonDetailAPIView
from django.urls import path

urlpatterns = [
    path('', PersonListAPIView.as_view(), name="list-posts"),
    path('<int:id>', PersonDetailAPIView.as_view(), name="detail-posts"),
    path('<int:post_id>/detection/', views.get_posts_by_user, name='detection'),
    path('<int:user_id>/posts/', views.get_posts_by_user, name='get_posts_by_user'),
    path('posts/<int:post_id>/', views.get_post, name='get_post'),
    path('allPosts/', views.get_all_posts, name='get_all_posts'),
    path('posts/<int:post_id>/change-status/', views.PersonDetailAPIView.change_status, name='change_post_status'),

]
