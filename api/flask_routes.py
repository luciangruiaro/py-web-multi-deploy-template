from flask import Flask, render_template, request, jsonify
from service.hello_service import HelloService
from helpers.utils import format_response


def create_flask_app(config, template_dir=None, static_dir=None):
    app = Flask(__name__, static_folder=static_dir or 'static', template_folder=template_dir or 'templates')
    app.config.update(config)
    app.state = type('State', (), {'config': config})()

    hello_service = HelloService(config)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/hello', methods=['GET'])
    def hello_get():
        return jsonify(format_response("Hello GET", hello_service.say_hello()))

    @app.route('/hello', methods=['POST'])
    def hello_post():
        data = request.json
        return jsonify(format_response("Hello POST", hello_service.process_data(data)))

    return app
