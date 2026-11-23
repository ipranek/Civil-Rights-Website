from flask import Blueprint, jsonify
import subprocess
import os
import pathlib

deploy_hook = Blueprint('deploy', __name__)
FOLDER_DIR = os.path.dirname(os.path.abspath(__file__))

@deploy_hook.route("/deploy", methods=["POST"])
def deploy():
    #pull first
    result = subprocess.run(["git", "-C", FOLDER_DIR,"pull"], capture_output=True, text=True)
    if result.returncode == 0:
        #touch only if pull is successful
        wsgi_path = os.environ.get("WSGI_PATH")    
        if wsgi_path is not None:
            pathlib.Path(wsgi_path).touch() 
        return jsonify({"message": "successpull", "output": result.stdout})
    else:
        return jsonify({"message": "error", "output": result.stderr}), 500

    