from django.db.models import Q
from . import permissions
from rest_framework import filters

# Create your views here.
from rest_framework import generics
import rest_framework
from Blog.serializers import (
    Article_Serializer,
    ArticleCreate_Serializer,
    ArticleList_Serializer,
    Comment_serializer, 
    CommentCreate_serializer, 
    CategorySerailizer,
    CategorytDetailSerializer,
    Reply_Serializer,

    UserAccountSerializer,
    UserProfileSerializer,
)

from Blog.models import Article, Category, Comment, Reply
from Users.models import CustomUsers, UserProfile



class SearchView(generics.ListAPIView):

    serializer_class= Article_Serializer
    def get_queryset(self):
        q= self.request.GET.get("q")
        if q != None:
            return Article.objects.filter(Q(title__icontains= q)|Q(snippet__icontains= q)|Q(Author__username__icontains=q)|Q(body__icontains=q) )
        return Article.objects.none()




class ArticleCreateApiView(generics.CreateAPIView):
    queryset=Article.objects.all()
    serializer_class=ArticleCreate_Serializer
    permission_classes=[ rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly]


    def perform_create(self, serializer):
        user= self.request.user
        return super().perform_create(serializer.save(Author=user))


class ArticleDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= Article_Serializer
    permission_classes=[ rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return Article.objects.all().select_related('Author').prefetch_related('Category', "comments")




class ArticleListApiView(generics.ListAPIView):

    serializer_class= ArticleList_Serializer
    filter_backends=[filters.SearchFilter, filters.OrderingFilter]
    search_fields=["Category__name", "title"]
    
    def get_queryset(self):
        return Article.objects.all().defer("body").select_related('Author')


class CommentDetailview(generics.RetrieveDestroyAPIView):
    serializer_class= Comment_serializer
    permission_classes=[permissions.IsCommentOwner,]

    def get_queryset(self):
        return Comment.objects.all().select_related('name').prefetch_related("replies", "name__userprofile").defer("name__userprofile__bio")



class CommentCreateApiView(generics.CreateAPIView):
    queryset= Comment.objects.all()
    serializer_class= CommentCreate_serializer
    permission_classes=[rest_framework.permissions.IsAuthenticated]


    def perform_create(self, serializer):
        return super().perform_create(serializer.save(name=self.request.user))

class CategoryListApi(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerailizer
    permission_classes=[ rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly]


class CategoryDetailApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=CategorytDetailSerializer
    permission_classes=[rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly]
    lookup_field="slug"

    def get_queryset(self):

        return Category.objects.all().prefetch_related('category')



class UserProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class=UserProfileSerializer
    permission_classes=[rest_framework.permissions.IsAuthenticated, permissions.IsUserProfileOwner]


    def get_queryset(self):
        return UserProfile.objects.all().select_related('user').prefetch_related('user__userarticle', 'user__user_comments')
    
    


class UserAccountSettingView(generics.DestroyAPIView):
    serializer_class=UserAccountSerializer
    lookup_field="username"
    permission_classes=[permissions.IsAccountOwner]


    def get_queryset(self):
        username= self.kwargs["username"]
        return CustomUsers.objects.filter(username=username)




class UserListView(generics.ListAPIView):
    queryset=CustomUsers.objects.all()
    serializer_class=UserAccountSerializer
    permission_classes=[rest_framework.permissions.IsAdminUser]
    

class ReplyCreateApiView(generics.CreateAPIView):
    queryset=Reply.objects.all()
    serializer_class= Reply_Serializer

    def perform_create(self, serializer):
        return super().perform_create(serializer.save(name=self.request.user))
    
class ReplyDeleteApiView(generics.RetrieveDestroyAPIView):
    serializer_class= Reply_Serializer
    permission_classes=[permissions.IsCommentOwner,]

    def get_queryset(self):
        return Reply.objects.all().select_related("name", "Comment")





    
        

