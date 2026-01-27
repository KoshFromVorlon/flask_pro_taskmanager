from app import create_app

app = create_app()

if __name__ == '__main__':
    # host='0.0.0.0' нужен, чтобы сайт был доступен из контейнера (если запускать python run.py)
    app.run(debug=True, host='0.0.0.0', port=5000)