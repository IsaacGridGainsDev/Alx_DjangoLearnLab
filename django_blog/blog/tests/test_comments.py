# blog/tests/test_comments.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", password="pw")
        self.other = User.objects.create_user(username="other", password="pw")
        self.post = Post.objects.create(title="P", content="C", author=self.user)

    def test_create_comment_requires_login(self):
        url = reverse("post-detail", args=[self.post.pk])
        # anonymous POST -> redirect to login
        resp = self.client.post(url, {"content": "Hello"})
        self.assertNotEqual(resp.status_code, 200)
        # login and post
        self.client.login(username="other", password="pw")
        resp = self.client.post(url, {"content": "Hello"})
        # after successful post, detail view should redirect back to post detail
        self.assertIn(resp.status_code, (302, 303))
        self.assertTrue(Comment.objects.filter(post=self.post, author=self.other, content="Hello").exists())

    def test_edit_comment_only_author(self):
        c = Comment.objects.create(post=self.post, author=self.other, content="X")
        edit_url = reverse("comment-edit", args=[c.pk])
        # not logged in
        resp = self.client.get(edit_url)
        self.assertNotEqual(resp.status_code, 200)
        # logged in as different user => cannot edit
        self.client.login(username="author", password="pw")
        resp = self.client.get(edit_url)
        self.assertNotEqual(resp.status_code, 200)
        # logged in as comment author => can edit
        self.client.login(username="other", password="pw")
        resp = self.client.get(edit_url)
        self.assertEqual(resp.status_code, 200)
        resp2 = self.client.post(edit_url, {"content": "Updated"})
        self.assertIn(resp2.status_code, (302, 303))
        c.refresh_from_db()
        self.assertEqual(c.content, "Updated")

    def test_delete_comment_only_author(self):
        c = Comment.objects.create(post=self.post, author=self.other, content="ToDelete")
        del_url = reverse("comment-delete", args=[c.pk])
        # other user can't delete
        self.client.login(username="author", password="pw")
        resp = self.client.post(del_url)
        self.assertNotEqual(resp.status_code, 302)  # no redirect / no deletion
        self.assertTrue(Comment.objects.filter(pk=c.pk).exists())
        # author can delete
        self.client.login(username="other", password="pw")
        resp = self.client.post(del_url)
        self.assertIn(resp.status_code, (302, 303))
        self.assertFalse(Comment.objects.filter(pk=c.pk).exists())
