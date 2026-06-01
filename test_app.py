import unittest
from unittest.mock import patch
from app import app

class TestIndexRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('app.render_template')
    def test_get_request_initial_state(self, mock_render):
        mock_render.return_value = "OK"
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        mock_render.assert_called_once_with('index.html', result=None)

    @patch('app.render_template')
    def test_valid_calculation_and_rounding(self, mock_render):
        response = self.client.post('/', data={'p': '1000', 'r': '5', 't': '2'})
        self.assertEqual(response.status_code, 200)
        mock_render.assert_called_once_with('index.html', result=1102.5)

    @patch('app.render_template')
    def test_invalid_non_numeric_input(self, mock_render):
        response = self.client.post('/', data={'p': 'abc', 'r': '5', 't': '2'})
        self.assertEqual(response.status_code, 200)
        mock_render.assert_called_once_with('index.html', result='Введите корректные числа!')

    @patch('app.render_template')
    def test_invalid_boundary_values(self, mock_render):
        response = self.client.post('/', data={'p': '100', 'r': '5', 't': '150'})
        self.assertEqual(response.status_code, 200)
        mock_render.assert_called_once_with('index.html', result='Введите корректные числа!')

if __name__ == '__main__':
    unittest.main()