# blog/tests/test_tags_search.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

class TagSearchTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user(username="u", password="pw")
        # create posts with tags
        p1 = Post.objects.create(title="Django tips", content="Some tips", author=self.u)
        p1.tags.add("django", "python")
        p2 = Post.objects.create(title="Flask vs Django", content="Comparisons", author=self.u)
        p2.tags.add("flask", "python")
        p3 = Post.objects.create(title="Random post", content="Unrelated", author=self.u)
        p3.tags.add("misc")

    def test_posts_by_tag(self):
        resp = self.client.get(reverse("posts-by-tag", args=["python"]))
        self.assertEqual(resp.status_code, 200)
        # both p1 and p2 should appear
        self.assertContains(resp, "Django tips")
        self.assertContains(resp, "Flask vs Django")
        # p3 shouldn't
        self.assertNotContains(resp, "Random post")

    def test_search_title(self):
        resp = self.client.get(reverse("post-list") + "?q=Flask")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Flask vs Django")
        self.assertNotContains(resp, "Random post")

    def test_search_content(self):
        resp = self.client.get(reverse("post-list") + "?q=tips")
        self.assertContains(resp, "Django tips")

    def test_search_by_tag_via_q(self):
        # search via q=python should match posts tagged 'python'
        resp = self.client.get(reverse("post-list") + "?q=python")
        self.assertContains(resp, "Django tips")
        self.assertContains(resp, "Flask vs Django")
