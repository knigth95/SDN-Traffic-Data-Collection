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

@app.route('/')
def index():
    return render_template('index.html')  # You need to create an index.html file under templates directory

@app.route('/start_ryu', methods=['GET'])
def start_ryu():
    try:
        subprocess.Popen(['ryu-manager', 'controller.py'])
        return jsonify(status="success", message="RYU Controller started")
    except Exception as e:
        return jsonify(status="error", message=str(e))

@app.route('/start_mininet', methods=['GET'])
def start_mininet():
    try:
        subprocess.Popen(['mn', '--custom', 'topology.py', '--topo', 'mytopo'])
        return jsonify(status="success", message="Mininet started")
    except Exception as e:
        return jsonify(status="error", message=str(e))

@app.route('/start_script/<int:host_number>', methods=['GET'])
def start_script(host_number):
    try:
        subprocess.Popen(['xterm', '-e', f'bash ./script{host_number}.sh'])
        return jsonify(status="success", message=f"Host{host_number} script started")
    except Exception as e:
        return jsonify(status="error", message=str(e))

@app.route('/stop_script/<int:host_number>', methods=['GET'])
def stop_script(host_number):
    # This requires properly writing the scripts to handle 'stop' signal
    return jsonify(status="error", message="Not implemented")

@app.route('/view_file/<int:host_number>', methods=['GET'])
def view_file(host_number):
    try:
        file_path = os.path.join(app.root_path, f'h{host_number}file.txt')
        with open(file_path, 'r') as file: 
            file_content = file.read()
        return jsonify(status="success", content=file_content)
    except Exception as e:
        return jsonify(status="error", message=str(e))

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=2003, debug=True, use_reloader=True)
    except Exception as e:
        print("An exception occurred: {}".format(e))
    finally:
        release_resources()