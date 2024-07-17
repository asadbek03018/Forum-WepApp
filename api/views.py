
import logging

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status

# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from forum.models import Forum
from .serializers import ForumSerializer, UserSignupSerializer

logger = logging.getLogger(__name__)

# class Forums(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)



class ForumsListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    all_forums = Forum.objects.all()
    queryset = all_forums
    serializer_class = ForumSerializer




class GetForumsbyCategory(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ForumSerializer

    def get_object(self, slug):
        return Forum.objects.filter(category__slug=slug)

    def get(self, request, slug, format=None):
        try:
            forums = self.get_object(slug)
            if forums.exists():
                serializer = self.serializer_class(forums, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Forumlar mavjud emas!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving forums for category {slug}: {e}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, slug=None):
        serializer = ForumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetForumByCategoryAndSlug(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ForumSerializer

    def get_object(self, category_slug, slug):
        try:
            return Forum.objects.get(category__slug=category_slug, forum_slug=slug)
        except Forum.DoesNotExist:
            return None

    def get(self, request, category_slug, slug, format=None):
        forum = self.get_object(category_slug, slug)
        if forum is not None:
            serializer = self.serializer_class(forum)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Forum mavjud emas!'}, status=status.HTTP_404_NOT_FOUND)


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)
            if user:
                serializer = UserSignupSerializer(user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)