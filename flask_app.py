from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('run_script')
def handle_run_script(data):
    script_args = data.get('args', [])
    process = subprocess.Popen(
        script_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for stdout_line in iter(process.stdout.readline, ""):
        emit('script_output', {'output': stdout_line.strip()}, broadcast=True)

    process.stdout.close()
    process.wait()

if __name__ == '__main__':
    socketio.run(app,host = ("0.0.0.0"), debug=True)
