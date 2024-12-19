from flask import Flask, send_from_directory, Blueprint, Response
import os

app = Flask(__name__)
bp = Blueprint('demo-plugin', __name__)

@bp.route('/', methods=['GET'])
def plugin():
    return send_from_directory('./', 'plugin.yaml')

@bp.route('/permissions.json', methods=['GET'])
def permissions():
    return send_from_directory('./', 'permissions.json')


app.register_blueprint(bp, url_prefix='/demo-namespace/demo-plugin')

if __name__ == '__main__':
    app.run(port=5001)