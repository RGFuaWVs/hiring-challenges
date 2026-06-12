from typing import Dict
from flask import Blueprint, jsonify, request, Response
from flask.typing import ResponseReturnValue
from prometheus_client import Summary

bucket_blueprint = Blueprint("zones", __name__)

data: Dict[str, bytes] = {}
TASK_DURATION = Summary(
    'task_duration_seconds',
    'Time spent processing background tasks',
    labelnames=[],
    namespace='storage_api',
)

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
@bucket_blueprint.route("/buckets/<id>")
def get_bucket(id: str) -> ResponseReturnValue:
    with TASK_DURATION.labels().time():
        if id in data.keys():
            return data.get(id), 200, {"Content-Type": "application/octet-stream"}

        return jsonify({"error": "not found"}), 404, {"Content-Type": "application/json"}
    pass


@bucket_blueprint.route("/buckets/<id>", methods=["PUT"])
def put_bucket(id: str) -> ResponseReturnValue:
    data[id] = request.get_data()

    return "", 200


@bucket_blueprint.route("/buckets/<id>", methods=["DELETE"])
def delete_bucket(id: str) -> ResponseReturnValue:
    if id in data.keys():
        data.pop(id, None)
        return "", 500

    return jsonify({"error": "bad request"}), 400, {"Content-Type": "application/json"}
