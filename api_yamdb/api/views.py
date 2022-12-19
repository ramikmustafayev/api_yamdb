from django.shortcuts import render
from .serializers import (UserSerializer, CategoriesSerializer,GenresSerializer,TitlesWriteSerializer,
TitlesReadSerializer,ReviewsSerializer,CommentsSerializer,TokenObtainSerializer,AuthSerializer)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from .permissions import IsAdmin
from rest_framework import status
from users.models import User
from reviews.models import Category,Genre, Title,Review, Comment
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import TitleFilter
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .mixins import ReviewCommentMixin

class LogIn(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


class SignUp(APIView):
    permission_classes=(AllowAny,)
    def post(self, request):
        ser=AuthSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            valid_data={'email':request.data['email'], 'username':request.data['username']}
            return Response(valid_data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserViewSet(ModelViewSet):
    lookup_field='username'
    serializer_class=UserSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes=[IsAuthenticated,IsAdmin]
    search_fields = ('username',) 
    pagination_class=PageNumberPagination
    queryset=User.objects.all()

    @action(methods=['GET','PATCH'],detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method=="PATCH":
            ser=self.get_serializer(request.user,data=request.data, partial=True)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_200_OK)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)     
        ser=self.get_serializer(request.user)
        return Response(ser.data)
        
 
class CategoriesViewSet(ModelViewSet):
    lookup_field='slug'
    serializer_class=CategoriesSerializer
    pagination_class=PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 
    queryset=Category.objects.all()

    def get_permissions(self):
        if self.action=='list':
            return (IsAuthenticatedOrReadOnly(),)
        return (IsAuthenticated(),IsAdmin())

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenresViewSet(ModelViewSet):
    lookup_field='slug'
    serializer_class=GenresSerializer
    queryset=Genre.objects.all()
    pagination_class=PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 

    def get_permissions(self):
        if self.action=='list':
            return (IsAuthenticatedOrReadOnly(),)
        return (IsAuthenticated(),IsAdmin())

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(ModelViewSet):
    queryset=Title.objects.all().annotate(average_rating=Avg('reviews__score'))
    pagination_class=PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class=TitleFilter

    def get_serializer_class(self):
        if self.action=='retrieve' or self.action=='list':
            return TitlesReadSerializer
        return TitlesWriteSerializer

    def get_permissions(self):
        if self.action=='list' or self.action=='retrieve':
            return (IsAuthenticatedOrReadOnly(),)
        return (IsAuthenticated(),IsAdmin())

  
class ReviewViewSet(ReviewCommentMixin, ModelViewSet):
    serializer_class=ReviewsSerializer
    pagination_class=PageNumberPagination

    def perform_create(self, serializer):
        title=get_object_or_404(Title,id=self.kwargs['title_id'])
        return serializer.save(author=self.request.user,title=title)

    def get_queryset(self):
        return Review.objects.filter(title_id=self.kwargs['title_id'])


class CommentViewSet(ReviewCommentMixin, ModelViewSet):
    serializer_class=CommentsSerializer
    pagination_class=PageNumberPagination

    def perform_create(self, serializer):
        review=get_object_or_404(Review,title_id=self.kwargs['title_id'],id=self.kwargs['review_id'])
        return serializer.save(author=self.request.user, review=review)
    
    def get_queryset(self):
        reviews=Review.objects.filter(title_id=self.kwargs['title_id']).filter(id=self.kwargs['review_id']) 
        return Comment.objects.filter(review=reviews.first())