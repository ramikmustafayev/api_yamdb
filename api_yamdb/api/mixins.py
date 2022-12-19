from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrModeratorOrAuthor

class ReviewCommentMixin(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action=='list' or self.action=='retrieve':
            return (IsAuthenticatedOrReadOnly(),)
        elif self.action=='create':
            return (IsAuthenticated(),)
        return [IsAuthenticated(),IsAdminOrModeratorOrAuthor()]   


        