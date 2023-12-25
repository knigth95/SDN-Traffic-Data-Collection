# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import os
import subprocess
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

app = Flask(__name__, template_folder='/home/knight/桌面/College-Class/软件定义网络/SDN-Traffic-Data-Collection-For-Analysis/tempates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    try:
        # 注意：在生产环境中，请避免使用subprocess来运行有sudo权限的命令，这是一个示例。
        password = 'bsj'  # 切勿在生产代码中硬编码密码!
        command = 'echo "{}" | sudo -S python3 topology.py && ryu-manager controller.py'.format(password)
        subprocess.Popen(command, shell=True)
        return jsonify({'message': 'Network is starting...'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/open_xterm/<host_id>', methods=['POST'])
def open_xterm(host_id):
    try:
        # 在mininet主机上打开xterm
        subprocess.Popen('xterm -title "Host {}" -e mininet/util/m h{}'.format(host_id, host_id), shell=True)
        return jsonify({'message': 'Xterm for Host {} is opened.'.format(host_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/script/<host_id>', methods=['POST'])
def script(host_id):
    action = request.form['action']  # "start" or "stop"
    script_name = 'script{}.sh'.format(host_id)
    try:
        if action == 'start':
            subprocess.Popen(['/bin/bash', script_name], cwd=os.getcwd())
        elif action == 'stop':
            subprocess.Popen(['/bin/bash', script_name, 'stop'], cwd=os.getcwd())
        return jsonify({'message': 'Action {} for script {} executed.'.format(action, script_name)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/show_file/<file_id>', methods=['GET'])
def show_file(file_id):
    filename = 'h{}file.txt'.format(file_id)
    try:
        with open(filename, 'r') as f:
            file_content = f.read()
        return jsonify({'file_content': file_content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2003,debug=True)