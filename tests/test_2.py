import os
import tempfile
import unittest
from flask import Flask
from app import app, allowed_file

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_allowed_file(self):
        self.assertTrue(allowed_file("example.txt"))
        self.assertTrue(allowed_file("example.pdf"))
        self.assertTrue(allowed_file("example.mp4"))
        self.assertTrue(allowed_file("example.mov"))
        self.assertTrue(allowed_file("example.avi"))
        self.assertFalse(allowed_file("example.jpg"))
        self.assertFalse(allowed_file("example.doc"))

    def test_upload_form(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload Video', response.data)

    def test_upload_invalid_file_type(self):
        response = self.app.post('/', data={'compressionPercentage': 50}, follow_redirects=True)
        self.assertIn(b'Invalid file type or no file selected', response.data)

    def test_upload_valid_file(self):
        # Create a temporary file for testing
        _, temp_file_path = tempfile.mkstemp(suffix='.mp4')
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write("dummy content")

        with open(temp_file_path, 'rb') as temp_file:
            response = self.app.post('/', data={'compressionPercentage': 50},
                                     content_type='multipart/form-data',
                                     data={'videoFile': (temp_file, 'test_video.mp4')},
                                     follow_redirects=True)

        self.assertIn(b'Video successfully uploaded', response.data)
        self.assertIn(b'Original size:', response.data)
        self.assertIn(b'Compressed size:', response.data)

if __name__ == '__main__':
    unittest.main()
