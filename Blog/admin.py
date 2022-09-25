from django.contrib import admin
from .models import Article, Comment, Category, Reply
# Register your models here.


class commentinline(admin.StackedInline):
	model= Comment
	

class ArticleAdmin(admin.ModelAdmin):
	inlines= [ commentinline, ]
	list_filter=["Author", "date_published"]


class replyInline(admin.TabularInline):
	model=Reply

class CommentInlines(admin.ModelAdmin):
	inlines=[replyInline,]
	list_filter=["date_published", "Article", "name"]
	



admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentInlines)
admin.site.register(Category)
admin.site.register(Reply)
