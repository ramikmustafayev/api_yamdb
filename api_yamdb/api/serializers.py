from rest_framework import serializers
from users.models import User
from reviews.models import Category,Genre,Title,Review,Comment
from datetime import datetime
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator


class TokenObtainSerializer(serializers.Serializer):
    token_class = RefreshToken
    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username']=serializers.CharField()
        self.fields['confirmation_code']=serializers.CharField()
    
    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


    def validate(self, attrs):
        data={}
        username=attrs['username']
        confirmation_code=attrs['confirmation_code']
        user=get_object_or_404(User,username=username)
       
        if user.confirmation_code!=confirmation_code:
            raise serializers.ValidationError('Неправильный код подтверждения')
       
        refresh=self.get_token(user)
        data['token']=str(refresh.access_token)
        return data
        

class AuthSerializer(serializers.Serializer):
    username=serializers.CharField(style={'base_template':'input.html'})
    email=serializers.EmailField(style={'base_template':'input.html'})

    def validate_username(self,username):
        if username=='me':
            raise serializers.ValidationError("Нельзя создать пользователя с именем 'me'")

        if User.objects.filter(username=username).exists():
             raise serializers.ValidationError("Пользователь с таким именем уже существует")  

        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с такой почтой уже существует")
        return email

    
    
    def create(self, validated_data): 
        user=User.objects.create_user(**validated_data)
        confirmation_code=default_token_generator.make_token(user)
        user.confirmation_code=confirmation_code
        user.save()
        email=validated_data['email']
        
        send_mail(
            'Регистрация на сайте YaMDB',
                f'Ваш код подтверждения {confirmation_code} .',
                'no-reply@YaMDB.fake',
                [f'{email}'],
                 fail_silently=False )
        
        return {}

        
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=('username','email','first_name','last_name','bio','role')

    def validate_username(self,data):
        if data=='me':
            raise serializers.ValidationError("Нельзя создать пользователя с именем 'me'")
        return data

    def update(self, instance:User, validated_data):
        role=instance.role
        
        if role=='user':
            if validated_data.get('role')!='user':
                validated_data['role']='user'
        return super().update(instance, validated_data)

    
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields=('name','slug')

class TitlesReadSerializer(serializers.ModelSerializer):
    category=CategoriesSerializer(read_only=True)  
    genre= GenresSerializer(many=True, read_only=True) 
    rating=serializers.IntegerField(source='average_rating',read_only=True)
    class Meta:
        model=Title
        fields=['id','name','year','rating','description','genre','category']

   
class TitlesWriteSerializer(serializers.ModelSerializer):
    category=serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')
    genre= serializers.SlugRelatedField(queryset=Genre.objects.all(), many=True, slug_field='slug')
    class Meta:
        model=Title
        fields=['id','name','year','description','genre','category']
        extra_kwargs = {"description": {"required": False, "allow_null": True}}

    def validate_year(self, data):
        year=datetime.now().year
        if data>year:
            raise serializers.ValidationError("Нельзя добавить ещё не вышедшие фильмы")
        return data


class ReviewsSerializer(serializers.ModelSerializer):
    author=serializers.StringRelatedField(read_only=True)
    score=serializers.IntegerField(max_value=10, min_value=1)
    class Meta:
        model=Review
        exclude=['title']
    
    def create(self, validated_data):
        author=validated_data.get('author')
        title=validated_data.get('title')
    
        if Review.objects.filter(author=author).filter(title=title).exists():
            raise serializers.ValidationError("One Film-one review")

        return super().create(validated_data)

class CommentsSerializer(serializers.ModelSerializer):
    author=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Comment
        exclude=['review']

