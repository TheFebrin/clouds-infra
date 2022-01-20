from flask import Flask
from views import views

app = Flask(__name__)

app.register_blueprint(views, url_prefix='/')


def main():
    app.run(host='0.0.0.1', port=4444, debug=True)

if __name__ == '__main__':
    print('Start server')
    main()

