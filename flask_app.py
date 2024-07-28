from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess

from main import *

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('run_asset_enumeration')
def handle_asset_enumeration(data):
    domain = data['domain']
    emit('message', {'status': 'running', 'message': 'Asset enumeration started'})
    result = main(domain)
    
    if result == 'success':
        emit('message', {'status': 'success', 'message': 'Asset enumeration completed successfully'})
    else:
        emit('message', {'status': 'error', 'message': 'Asset enumeration failed'})

@socketio.on('run_spider')
def handle_spider(data):
    urls = data['domain']
    allowed_domains = data['allowed_domains']

    emit('message', {'status': 'running', 'message': 'Spider script started'})

    try:
        # somehow importing the endpoint module and calling the spider here didn't work.
        process = subprocess.Popen(
            f'python3 endpoint.py --url {urls} --allowed_domains {allowed_domains}',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True
        )
        result = 'success'
    except Exception as e:
        print(e)
        result = 'failed'

    stdout, stderr = process.communicate()

    if stderr != None:
        print(stderr)
        result = 'failed'

    if result == 'success':
        emit('message', {'status': 'success', 'message': 'Spider script completed successfully'})
    else:
        emit('message', {'status': 'error', 'message': 'Spider script failed'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
