from django.urls import path, include
from rest_framework.routers import DefaultRouter,SimpleRouter
from .views import UserViewSet, CategoriesViewSet, GenresViewSet,TitleViewSet,ReviewViewSet, CommentViewSet, SignUp,LogIn
from rest_framework_simplejwt.views import TokenObtainPairView
    
router =DefaultRouter()
router.register('users', UserViewSet)
router.register('categories',CategoriesViewSet)
router.register('genres',GenresViewSet)
router.register('titles',TitleViewSet)

router2=DefaultRouter()
router2.register('reviews',ReviewViewSet,basename='review')

router3=DefaultRouter()
router3.register('comments',CommentViewSet,basename='comment')



urlpatterns = [
    path('api/v1/auth/signup/', SignUp.as_view()),
    path('api/v1/auth/token/', LogIn.as_view(), name='token_obtain' ),
    path('api/v1/', include(router.urls)),
    path('api/v1/titles/<int:title_id>/', include(router2.urls)),
    path('api/v1/titles/<int:title_id>/reviews/<int:review_id>/',include(router3.urls))
]
