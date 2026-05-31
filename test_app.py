import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


@patch('app.render_template')
class TestIndexRoute:

    def test_get_request_returns_200(self, mock_render, client):
        mock_render.return_value = "OK"
        response = client.get('/')
        assert response.status_code == 200
        mock_render.assert_called_once_with('index.html', result=None)

    def test_post_valid_data_returns_correct_result(self, mock_render, client):
        response = client.post('/', data={'p': '1000', 'r': '5', 't': '2'})
        assert response.status_code == 200
        mock_render.assert_called_once_with('index.html', result=1102.5)

    def test_post_valid_data_rounding(self, mock_render, client):
        response = client.post('/', data={'p': '100', 'r': '3', 't': '10'})
        assert response.status_code == 200
        mock_render.assert_called_once_with('index.html', result=134.39)

    def test_post_invalid_non_digits(self, mock_render, client):
        response = client.post('/', data={'p': 'abc', 'r': '0', 't': '2'})
        assert response.status_code == 200
        mock_render.assert_called_once_with('index.html', result='Введите корректные числа!')

    def test_post_valid_t_149(self, mock_render, client):
        response = client.post('/', data={'p': '1', 'r': '1', 't': '149'})
        assert response.status_code == 200
        call_kwargs = mock_render.call_args.kwargs
        assert call_kwargs['result'] != 'Введите корректные числа!'
        assert isinstance(call_kwargs['result'], float)