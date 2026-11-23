from flask import Blueprint, jsonify

deploy_hook = Blueprint('deploy', __name__)

@deploy_hook.route("/deploy", methods=["POST"])
def deploy():
    return jsonify({"deploy message": "success"})


