# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import os
import subprocess
import signal
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

def release_resources():
    print("Releasing bound ports and other resources...")
    # 在这里可以添加关闭数据库连接、停止后台线程等操作
    # 对于端口，Flask内置的开发服务器将在程序退出时自动释放端口
    # 对于其他服务器或应用程序占用的端口，可以在此执行必要的释放操作
    # 例如：subprocess.Popen(['fuser', '-k', '2003/tcp'])

# 通过信号处理确保意外终止时调用资源释放函数
def signal_handler(signal, frame):
    release_resources()
    sys.exit(0)


# 绑定信号处理函数
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

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
    try:
        app.run(host='0.0.0.0', port=2003, debug=True, use_reloader=True)
    except Exception as e:
        print("An exception occurred: {}".format(e))
    finally:
        release_resources()