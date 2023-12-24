# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import subprocess
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#app = Flask(__name__)
app = Flask(__name__, template_folder='/home/knight/桌面/College-Class/软件定义网络/SDN-Traffic-Data-Collection-For-Analysis/tempates')
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_network", methods=["POST"])
def start_network():
    # 请确保在安全的环境中运行这些命令
    os.system("sudo python topology.py && sudo ryu-manager controller.py")
    return jsonify(message="Network started successfully")

@app.route("/run_script/<host_id>", methods=["POST"])
def run_script(host_id):
    script = "script" + host_id[-1] + ".sh"
    # 请确保在安全的环境中运行这些命令
    os.system("bash ./" + script)
    return jsonify(message="Script for host " + host_id + " executed successfully")

@app.route("/get_file/<file_id>", methods=["GET"])
def get_file(file_id):
    file_name = "h" + file_id[-1] + "file.txt"
    try:
        with open(file_name, 'r') as file:
            content = file.read()
        return jsonify(content=content)
    except FileNotFoundError:
        return jsonify(error="File not found"), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2003,debug=True)