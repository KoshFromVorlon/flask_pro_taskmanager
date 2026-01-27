def test_home_page_redirect(client):
    """Главная должна перекидывать на логин, если не вошел"""
    response = client.get('/')
    assert response.status_code == 302  # 302 - это редирект
    assert '/login' in response.headers['Location']


def test_login_page_loads(client):
    """Страница логина должна открываться (код 200)"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"TaskMaster Pro" in response.data  # Проверяем, есть ли название на странице


def test_register_process(client, app):
    """Проверяем регистрацию нового пользователя"""
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpassword'
    }, follow_redirects=True)

    # После регистрации нас должно перекинуть на главную и показать флеш-сообщение
    assert response.status_code == 200
    # Ищем текст из translations.py (ключ flash_register_success)
    # Внимание: тут текст зависит от языка по умолчанию (RU)
    assert "Регистрация успешна!".encode('utf-8') in response.data

    with app.app_context():
        from app.models import User
        assert User.query.filter_by(username='newuser').first() is not None
