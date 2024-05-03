import unittest
from app import app, db, URL
import os

class URLShortenerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_shorten_url(self):
        response = self.client.post('/shorten', json={'url': 'https://www.example.com'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue('shortcode' in response.get_json())

    def test_redirect_to_url(self):
        with self.app.app_context():
            url = URL(url='https://www.example.com', shortcode='test123')
            db.session.add(url)
            db.session.commit()

        response = self.client.get('/test123')
        self.assertEqual(response.status_code, 302)

    def test_get_stats(self):
        with self.app.app_context():
            url = URL(url='https://www.example.com', shortcode='test123')
            db.session.add(url)
            db.session.commit()

        response = self.client.get('/test123/stats')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('created' in response.get_json())
        self.assertTrue('lastRedirect' in response.get_json())
        self.assertTrue('redirectCount' in response.get_json())

if __name__ == '__main__':
    unittest.main()
