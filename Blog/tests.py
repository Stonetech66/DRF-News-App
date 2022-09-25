from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Article, Comment, Reply
from django.contrib.auth.models import Permission
# Create your tests here.
class Blogtest(TestCase):
	def setUp(self):
	
		self.user= get_user_model().objects.create_user(
		username= 'rince',
		email= 'gidi@gmail.com',
		password= "qwerty1234")

		self.post= Article.objects.create(Author= self.user, title= "po", body= "hope")

		self.comment = Comment.objects.create(Article= self.post, name= self.user, comment= "no")

		self.permission= Permission.objects.get(codename= 'special_articlecreate')

		self.reply= Reply.objects.create(Comment=self.comment, name=self.user, body="this is very nice")

	def test_Article_content(self):
		resp=Article.objects.get(id=1)
		art= f"{resp.title}"
		g= f"{resp.body}"
		a= f"{resp.Author}"
		self.assertEqual(art, "po")
		self.assertEqual(g, "hope")
		self.assertEqual(a, "rince")


	def test_get_absolute_url(self):
		self.assertEqual(self.post.get_absolute_url(), '/articles/1')

	def test_string_representation(self):
		resp= Article(title= "pork")
		self.assertEqual(str(resp), resp.title[:20])


	def test_Article_login_list_view(self):
		self.client.login(email='gidi@gmail.com', password= "qwerty1234")
		resp= self.client.get(reverse("ArticleListview"))
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, "Latest News")
		self.assertTemplateUsed(resp, "ArticleListview.html")
		





	def test_Article_detail_view(self):
		self.client.login(email='gidi@gmail.com', password= "qwerty1234")
		resp= self.client.get(self.post.get_absolute_url())
		noresp= self.client.get('/Books/1234411/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(noresp.status_code, 404)
		self.assertTemplateUsed('ArticleDetailView.html')
		self.assertContains(resp, "no")

	def test_aricle_logout_detail_view(self):
		self.client.logout()
		resp= self.client.get(self.post.get_absolute_url())
		self.assertEqual(resp.status_code, 302)
		self.assertRedirects(resp, '%s?next=/articles/1'% (reverse('account_login')))



	def test_Article_create_view(self):
		self.client.login(email='gidi@gmail.com', password= "qwerty1234")
		self.user.user_permissions.add(self.permission)
		resp= self.client.post(reverse("ArticleCreateview"), {"title":"hope", "snippet":"insis", "Author":self.user})
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed("ArticleCreateview.html")
		self.assertContains(resp, "hope")

		

	def test_Article_update_view(self):
		resp= self.client.post(reverse("ArticleUpdateview", args= "1"), {"title":"hope", "snippet":"insis", "Author":self.user})
		self.assertEqual(resp.status_code, 302)
		

	def test_Article_delete_view(self):
		self.client.login(email='gidi@gmail.com', password= "qwerty1234")
		resp= self.client.post(reverse("ArticleDeleteview", args= "1"))
		self.assertEqual(resp.status_code, 302)

	def test_logout_user_can_delete_article(self):
		self.client.logout
		response= self.client.post(reverse("ArticleDeleteview", args="1"))
		self.assertEqual(response.status_code, 302)


	def test_user_delete_reply(self):
		self.client.login(email='gidi@gmail.com', password= "qwerty1234")
		response= self.client.post(reverse("reply-delete", args="1"))
		self.assertEqual(response.status_code, 302)

	def test_loggedout_user_cant_delete_reply(self):
		self.client.logout()
		response= self.client.post(reverse("reply-delete", args="1"))
		self.assertEqual(response.status_code, 302)

	def test_reply_detail(self):
		self.client.login(email='gidi@gmail.com', password= "qwerty1234")
		response= self.client.get(reverse("comment-replies", args="1"))
		noresponse= self.client.get('comment/182823/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(noresponse.status_code, 404)

	def test_user_delete_comment(self):
		self.client.login(email='gidi@gmail.com', password= "qwerty1234")
		response= self.client.post(reverse("Commentdelete", args="1"))
		self.assertEqual(response.status_code, 302)

	

