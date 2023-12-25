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

app = Flask(__name__, template_folder='./tempates')


# 用于存储子进程的字典
subprocesses = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_ryu', methods=['POST'])
def start_ryu():
    proc = subprocess.Popen(['gnome-terminal', '--', 'ryu-manager', 'controller.py'])
    subprocesses['ryu'] = proc
    return jsonify(success=True)

@app.route('/start_mininet', methods=['POST'])
def start_mininet():
    # 下面的 'sudo' 密码方式不是一个安全的做法，应仅作为示例。请寻找更合适的解决方案。
    proc = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'echo 123456 | sudo -S python topology.py'])
    subprocesses['mininet'] = proc
    return jsonify(success=True)

@app.route('/show_topo', methods=['GET'])
def show_topo():
    # 实际的拓扑数据应该由其他逻辑产生或从其他地方读取
    topo_data = '<svg>Your SVG topology diagram here.</svg>'
    return jsonify(topology=topo_data)

@app.route('/start_script/<int:host_id>', methods=['POST'])
def start_script(host_id):
    script_name = 'script{}.sh'.format(host_id)
    proc = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'xterm -hold -e bash ./scripts/{}'.format(script_name)])
    subprocesses['h{}}'.format(host_id)] = proc
    return jsonify(success=True)

@app.route('/stop_script/<int:host_id>', methods=['POST'])
def stop_script(host_id):
    proc = subprocesses.get('h{}'.format(host_id))
    if proc:
        proc.send_signal(signal.SIGINT) # or signal.SIGKILL
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/file_content/<int:file_id>', methods=['GET'])
def file_content(file_id):
    file_name = 'h{}file.txt'.format(file_id)
    try:
        with open(file_name, 'r') as f:
            file_content = f.read()
        return jsonify({'file_content':file_content}),200
        #return send_file(file_name, as_attachment=False)
    except FileNotFoundError:
        return jsonify(error='File not found'), 404

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=2004, debug=True,use_reloader=True)
    except Exception as e:
        print('Error occurred: {}'.format(e))
    finally:
        release_resources()