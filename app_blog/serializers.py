from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Post, Comment, Like


# 1. AUTH & USER SERIALIZERS
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Bu username allaqachon bor!")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['username']



# 2. CATEGORY SERIALIZER
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']



# 3. COMMENT SERIALIZER
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') # Comment author's name

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_at']



# 4. LIKE SERIALIZER
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'post', 'user']

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        post = attrs.get('post')

        # Prevent duplicate likes (user cannot like twice)
        if Like.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError("Siz bu postga allaqachon like bosgansiz!")
        
        return attrs



# 5. POST SERIALIZERS
class PostListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = serializers.ReadOnlyField(source='category.name')
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'author', 'category', 'likes_count', 'comments_count', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'author', 'category', 'likes_count', 'comments', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'category']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Post sarlavhasi kamida 5 ta belgidan iborat bo'lishi kerak!")
        return value