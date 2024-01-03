# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import os
import subprocess
import signal
import sys

app = Flask(__name__, template_folder='./tempates')

# 释放资源的函数
def release_resources():
    # 在这里可以执行必要的资源释放操作
    print("Releasing resources...")

def signal_handler(signal, frame):
    release_resources()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_ryu', methods=['POST'])
def ryu_start():
    try:
        # 根据不同操作系统打开一个新的终端窗口来运行ryu-manager
        if sys.platform == "win32":
            subprocess.Popen('start cmd /k ryu-manager controller.py', shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen("osascript -e 'tell app \"Terminal\" to do script \"ryu-manager controller.py\"'", shell=True)
        elif sys.platform.startswith('linux'):
            subprocess.Popen('gnome-terminal -- bash -c "ryu-manager controller.py"', shell=True)
        else:
            raise EnvironmentError("Unsupported platform")

        return jsonify({'message': 'RYU is starting...'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start_mininet', methods=['POST'])
def mininet_start():
    try:
        
        password = 'bsj'
        if sys.platform == "win32":
            subprocess.Popen("start cmd /k python3 topology.py", shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen("osascript -e 'tell app \"Terminal\" to do script \"python3 topology.py\"'", shell=True)
        elif sys.platform.startswith('linux'):
            #subprocess.Popen(f"echo {password} | sudo -S python3 topology.py", shell=True)
            #subprocess.Popen(f'gnome-terminal -- bash -c "echo {password} | sudo -S python3 topology.py; exec bash"', shell=True)
            subprocess.Popen(f'gnome-terminal -- bash -c "sudo python3 topology.py; exec bash;read -r"', shell=True)
        else:
            raise EnvironmentError("Unsupported platform")
        
        return jsonify({'message': 'Mininet is starting...'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/open_xterm/<host_id>', methods=['POST'])
def open_xterm(host_id):
    try:
        script_name = 'script{}.sh'.format(host_id)
        subprocess.Popen(['xterm', '-title', 'h{}'.format(host_id), '-e', 'bash ./{}'.format(script_name)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'message': 'Xterm for h{} is opened.'.format(host_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop_script/<host_id>', methods=['POST'])
def stop_script(host_id):
    try:
        script_name = 'script{}.sh'.format(host_id)
        subprocess.Popen(['xterm', '-title', 'Stop Host {}'.format(host_id), '-e', 'bash ./{} stop'.format(script_name)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'message': 'Stopping script for Host {}...'.format(host_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/show_file/<file_id>', methods=['GET'])
def show_file(file_id):
    try:
        filename = 'h{}file.txt'.format(file_id)
        with open(filename, 'r') as file:
            content = file.read()
        return jsonify({'file_content': content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2003, debug=True, use_reloader=True)