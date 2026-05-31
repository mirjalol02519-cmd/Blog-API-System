from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, ProfileView, ProfileUpdateView,
    PostListCreateView, PostDetailUpdateDeleteView,
    CommentListCreateView, CommentDetailUpdateDeleteView,
    LikePostView, UnlikePostView
)

urlpatterns = [
    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/profile/update/', ProfileUpdateView.as_view(), name='profile_update'),

    # Post endpoints
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<intpk>/', PostDetailUpdateDeleteView.as_view(), name='post_detail_update_delete'),

    # Comment endpoints
    path('comments/', CommentListCreateView.as_view(), name='comment_list_create'),
    path('comments/<intpk>/', CommentDetailUpdateDeleteView.as_view(), name='comment_detail_update_delete'),

    # Like endpoints
    path('likes/like/', LikePostView.as_view(), name='like_post'),
    path('likes/unlike/<int:post_id>/', UnlikePostView.as_view(), name='unlike_post'),
]