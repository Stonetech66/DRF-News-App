from Blog.countries import Countries
from Blog.models import Article, Comment, Category,Reply
from Users.models import CustomUsers, UserProfile
from  rest_framework import serializers, reverse
from Users.models import UserProfile
from Users.models import Genders
from dateutil.relativedelta import *
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.reverse import reverse


from . import validators

class UserSerializer(serializers.Serializer):
    user_url=  serializers.HyperlinkedIdentityField(view_name="api:user-api-profile")
    username=serializers.CharField(read_only=True)
    profile_pic=serializers.ImageField(source="userprofile.profile_pic", read_only=True)


class inlineUserSerializer(serializers.Serializer):
    user_url=  serializers.HyperlinkedIdentityField(view_name="api:user-api-profile")
    username=serializers.CharField(read_only=True)




""""""
class ArticleList_Serializer(serializers.ModelSerializer):
    owner=inlineUserSerializer(source="Author", read_only=True)
    url=  serializers.HyperlinkedIdentityField(view_name="api:articleapi-detail")
    class Meta:
        model= Article
        fields= [
            "owner",
            "date_published",
            "snippet",
            "url",
            "header_image",
            "title",
            "body"

        ]
        read_only_fields= [  
            "owner",
            "date_published",
            "snippet",]

class ArticleCreate_Serializer(serializers.ModelSerializer):
    class Meta:
        model= Article
        fields= [
            "title",
            "snippet",
            "Category",
            "body",
            "header_image",   
        ]
    def  validate(self, attrs):
        name= attrs["title"]
        if Article.objects.filter(title__iexact=name):
            raise serializers.ValidationError("Article already exists")
        return super().validate(attrs)
 

class CategorySerailizer(serializers.ModelSerializer):
    url= serializers.HyperlinkedIdentityField(view_name="api:category-detail", lookup_field="slug")

    class Meta:
        model= Category
        fields=[
            "name", 
            "url",

        ]

    def  validate(self, attrs):
        name= attrs["name"]
        if Category.objects.filter(name__iexact=name):
            raise serializers.ValidationError("Category already exits")
        return super().validate(attrs)

class CommentSerializer(serializers.Serializer):
    owner=UserSerializer(source="name", read_only=True)
    comment= serializers.CharField(read_only=True)
    comment_url= serializers.HyperlinkedIdentityField(view_name="api:comment-detail")
    date_published=serializers.DateTimeField(read_only=True)





class Article_Serializer(serializers.ModelSerializer):
    owner=inlineUserSerializer(source="Author", read_only=True)
    comments= CommentSerializer(source="comments.all", many=True, read_only=True)
    url=  serializers.HyperlinkedIdentityField(view_name="api:articleapi-detail")
    category=CategorySerailizer(source="Category",read_only=True, many=True)
    comment_count=serializers.IntegerField(source="comments.count", read_only=True)
    class Meta:
        model= Article
        fields= [
            "owner",
            "date_published",
            "title",
            "snippet",
            "url",
            "category",
            "Category",
            "body",
            "header_image",
            "comment_count",
            "comments"
            
        ]

    def get_comment_url(self):

        return reverse("api:comment-create")




class inline_reply_serializer(serializers.Serializer):
    name= serializers.CharField(read_only=True)
    profile_pic= serializers.ImageField(source="name.userprofile.profile_pic")
    date_published= serializers.DateTimeField(read_only=True)
    body=serializers.CharField(read_only=True)
    url= serializers.HyperlinkedIdentityField(view_name='api:reply-api-delete')
    



class Comment_serializer(serializers.ModelSerializer):
    owner=UserSerializer(source="name", read_only=True)
    comment=serializers.CharField()
    replies= inline_reply_serializer(source="replies.all", read_only=True,many=True)
    reply_count= serializers.IntegerField(source="replies.count", read_only=True)

    class Meta:
        model= Comment
        fields= [
            "owner",     
            "comment",
            "date_published",
            "replies"
           

    ]

class CommentCreate_serializer(serializers.ModelSerializer):
    article=serializers.CharField(source="Article.title", read_only=True)
    class Meta:
        model= Comment
        fields= [    
            "Article",
            "article",
            "comment",
           
    ]
    

class CategorytDetailSerializer(serializers.ModelSerializer):
    articles=ArticleList_Serializer(source="category.all", read_only=True, many=True)
    article_count=serializers.IntegerField(source="category.count", read_only=True)
    class Meta:
        model= Category
        fields=[
            "article_count",
            "name",
 
            "articles",

        ]

class UserEditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields= [
            "profile_pic",
			"bio",
            
        ]
   




class UserProfileSerializer(serializers.ModelSerializer):
    Country= serializers.CharField(source="country.country", read_only=True)
    articles=ArticleList_Serializer(source="user.userarticle.all", many=True, read_only=True)
    comments=CommentSerializer(source="user.user_comments", many=True, read_only=True)
    comment_count=serializers.IntegerField(source="user.user_comments.count", read_only=True)
    article_count=serializers.IntegerField(source="user.userarticle.count", read_only=True)
    owner= serializers.CharField(source="user.username", read_only=True)
    verified= serializers.BooleanField(read_only=True)
    class Meta:
        model=UserProfile
        fields= [
            "owner",
            "verified",
            "profile_pic",
			"bio",
			"Country",
            "comment_count",
            "article_count",
            "articles",
            "comments",
            
        ]


class UserAccountSerializer(serializers.ModelSerializer):
    Birth_date=serializers.DateField(validators=[validators.validate_Birth_date])
    class Meta:
        model= CustomUsers
        fields= [
            "Fullname",
            "username",
            "email",
            "gender",
            "country",
            "Birth_date"
        ]
    

    
class Reply_Serializer(serializers.ModelSerializer):
    owner=serializers.CharField(source="name.username", read_only=True)
    class Meta:
        model= Reply
        fields=[
           "Comment", 
           "body", 
            "owner",

            
        ]

class RegisterSerailizer(RegisterSerializer):
    Birth_date= serializers.DateField(validators=[validators.validate_Birth_date])
    Fullname= serializers.CharField(max_length=70)
    country= serializers.ChoiceField(choices=Countries)
    gender=serializers.ChoiceField(choices=Genders)
    email=serializers.EmailField()




    def save(self, request):
        user= super().save(request)
        user.Birth_date= self.data.get("Birth_date")
        user.Fullname= self.data.get("Fullname")
        user.country= self.data.get("country")
        user.gender=self.data.get("gender")

        user.save()
        return user
