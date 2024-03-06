import unittest
from flask_testing import TestCase
from video_app.app import app, UPLOAD_FOLDER  # Adjust the import based on your app structure

class AppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    def test_homepage(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('upload.html')

    def test_upload_file(self):
        with open('path/to/your/test/file.txt', 'rb') as file:
            response = self.client.post('/', data={'file': (file, 'test_file.txt')})
            self.assert_redirects(response, '/')

            # Add more assertions based on your application's behavior

if __name__ == '__main__':
    unittest.main()
