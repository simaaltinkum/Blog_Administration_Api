from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import RegisterSerializer, BlogSerializer


class UserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if kwargs.get('action') == 'register':
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Kayıt başarılı!",
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif kwargs.get('action') == 'login':
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "message": "Giriş başarılı!",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "error": "Kullanıcı hesabı aktif değil"
                    }, status=status.HTTP_403_FORBIDDEN)

            else:
                return Response({
                    "error": "Geçersiz kullanıcı adı veya şifre"
                }, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        }, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        user.username = request.data.get('username')
        user.email = request.data.get('email')
        user.save()
        return Response({
            "message": "Profil güncellendi!"
        }, status=HTTP_200_OK)


class BlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        blog_posts = BlogSerializer.objects.all()
        serializer = BlogSerializer(blog_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                "message": "Yeni blog yazısı oluşturuldu!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        blog_post = BlogSerializer.objects.get(id=kwargs.get('id'))
        serializer = BlogSerializer(blog_post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        blog_post = BlogSerializer.objects.get(id=kwargs.get('id'))
        serializer = BlogSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Blog yazısı güncellendi!",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        blog_post = BlogSerializer.objects.get(id=kwargs.get('id'))
        blog_post.delete()
        return Response({
            "message": "Blog yazısı silindi!"
        }, status=status.HTTP_204_NO_CONTENT)
