from rest_framework.test import APITestCase

from system.models import Post

class PostCreateTestCase(APITestCase):
    def test_create_post(self):
        initial_post_count = Post.objects.count()
        post_attrs = {"title":"VA the la het","content":"HFSFDFDFD"}

        response = self.client.post('/api/v1/post/new', post_attrs)
        if response.status_code != 201:
            print(response.data)
        self.assertEqual(
            Post.objects.count(),
            initial_post_count + 1,
        )
        for attr, expected_value in post_attrs.items():
            self.assertEqual(response.data[attr], expected_value)