from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.contrib.auth.models import User

from .models import Category, Post, Comment, Like
from .serializers import (
    UserRegisterSerializer, UserSerializer, CategorySerializer,
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer,
    CommentSerializer, LikeSerializer
)
from .permissions import IsAuthorOrReadOnly


# 1. AUTHENTICATION (REGISTRATION, LOGIN, PROFILE)

class RegisterView(generics.CreateAPIView):
    # User registration API
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny] # Everyone can use


class LoginView(ObtainAuthToken):
    # User login API to get authentication token
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        }, status=status.HTTP_200_OK)
    


class LogoutView(APIView):
    # Logout API (delete token, user logout)
    permission_classes = [permissions.IsAuthenticated] # Only for authenticated users
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Muvafaqqiyatli tizimdan chiqdingiz"}, status=status.HTTP_200_OK)
    

class ProfileView(generics.RetrieveAPIView):
    # User profile detail API (view profile data)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class ProfileUpdateView(generics.UpdateAPIView):
    # User profile update API (edit profile data)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    


# 2. POST API (LIST, DETAIL, CREATE, UPDATE, DELETE)
class PostListCreateView(generics.ListAPIView):
    # View posts (all) and create Post (only loggedin users)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filter, Serach and Ordering settings
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Optimize likes_count and comments_count using annotations
        return Post.objects.select_related('author', 'category').annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )
    
    def get_serializer_class(self):
        # Use different serializers for create and retrieve
        if self.request.method == 'POST':
            return PostCreateUpdateSerializer
        return PostListSerializer
    
    def perfrom_create(self, serializer):
        # Set the post author to the current user
        serializer.save(author=self.request.user)


class PostDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update, and delete a post
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly] # only author can delete/edit
    

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    


# COMMENT API (LIST, CREATE, UPDATE, DELETE)

class CommentListCreateView(generics.ListAPIView):
    # List comments and create new comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # Edit comment and delete
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly] # Only comment owner can edit



# LIKE API (PUT LIKE AND REMOVE)
class LikePostView(generics.CreateAPIView):
    # API (Put like for post)
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UnlikePostView(APIView):
    # Delete
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        # search like
        like = Like.objects.filter(user=request.user, post_id=post_id)

        if like.exists():
            like.delete()
            return Response({"message": "Like olib tashlandi"}, status=status.HTTP_204_NO_CONTENT)
        
        else:
            return Response({"error": "Siz bu postga like bosmagansiz!"}, status=status.HTTP_400_BAD_REQUEST)