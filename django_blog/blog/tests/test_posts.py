# blog/tests/test_posts.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

class PostCRUDTests(TestCase):
    def setUp(self):
        # create two users
        self.u1 = User.objects.create_user(username="author1", password="pass1")
        self.u2 = User.objects.create_user(username="other", password="pass2")
        # create a post by u1
        self.post = Post.objects.create(title="Test Post", content="Content here", author=self.u1)

    def test_list_and_detail_accessible(self):
        # list
        resp = self.client.get(reverse("post-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.title)
        # detail
        resp = self.client.get(reverse("post-detail", args=[self.post.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.content)

    def test_create_requires_login(self):
        resp = self.client.get(reverse("post-create"))
        # redirect to login
        self.assertNotEqual(resp.status_code, 200)
        # login and access
        self.client.login(username="author1", password="pass1")
        resp = self.client.get(reverse("post-create"))
        self.assertEqual(resp.status_code, 200)
        # create post
        resp = self.client.post(reverse("post-create"), {"title": "New", "content": "Body"})
        self.assertIn(resp.status_code, (302, 303))
        self.assertTrue(Post.objects.filter(title="New").exists())

    def test_update_only_author(self):
        url = reverse("post-edit", args=[self.post.pk])
        # other user cannot edit
        self.client.login(username="other", password="pass2")
        resp = self.client.get(url)
        # should be forbidden or redirected (UserPassesTestMixin returns 403 by default)
        self.assertNotEqual(resp.status_code, 200)
        # author can edit
        self.client.login(username="author1", password="pass1")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(url, {"title": "Changed", "content": "New body"})
        self.assertIn(resp.status_code, (302, 303))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Changed")

    def test_delete_only_author(self):
        url = reverse("post-delete", args=[self.post.pk])
        # other user cannot delete
        self.client.login(username="other", password="pass2")
        resp = self.client.post(url)
        self.assertNotEqual(resp.status_code, 302)  # not deleted/redirected
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
        # author can delete
        self.client.login(username="author1", password="pass1")
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (302, 303))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
