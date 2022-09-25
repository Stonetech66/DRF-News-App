from django.urls import include, path

from Blog.serializers import UserEditProfileSerializer
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from . import views
from rest_framework.schemas import get_schema_view

from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view


API_TITLE="BLOG API"
schema_view=get_swagger_view(title=API_TITLE)




app_name="api"
urlpatterns= [

    path('', views.ArticleListApiView.as_view(), name= 'article-list'),
    path('<int:pk>/', views.ArticleDetailApiView.as_view(), name= 'articleapi-detail'),
    path('create/', views.ArticleCreateApiView.as_view(), name= 'articlecreate'),
    path("comment/<int:pk>/", views.CommentDetailview.as_view(), name= "comment-detail"),
    path("comment/create/", views.CommentCreateApiView.as_view(), name= "comment-create"),
    path("categories/", views.CategoryListApi.as_view(), name="category-list"),
    path("category/<slug:slug>/", views.CategoryDetailApi.as_view(), name="category-detail"),
    path("user/<str:username>/account/delete/", views.UserAccountSettingView.as_view(), name="account-delete"),
    path("user/<str:pk>/profile", views.UserProfileApiView.as_view(), name="user-api-profile"),
    path("article/create/", views.ArticleCreateApiView.as_view(), name="articleapi-create"),
    path("user/list/", views.UserListView.as_view(), name="all-users"),
    path("reply/create/", views.ReplyCreateApiView.as_view(), name="reply-create"), 
    path("", include('dj_rest_auth.urls')),
    path("signup/", include('dj_rest_auth.registration.urls')),
    path("reply/<int:pk>/", views.ReplyDeleteApiView.as_view(), name="reply-api-delete"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("docs/", schema_view, name="schema"),
    path("blog/docs/", include_docs_urls(title=API_TITLE), name="api-docs"),
    path("password/reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="rest_password_reset_confirm")

]
