import time
from typing import Dict
from flask import Blueprint, jsonify, request, Response
from flask.typing import ResponseReturnValue
from prometheus_client import Summary

bucket_blueprint = Blueprint("zones", __name__)

data: Dict[str, bytes] = {}

REQUEST_TIME = Summary(
    'request_processing_seconds',
    'Time spent processing request',
    labelnames=['path', 'method', 'status_code'],
    namespace='storage_api',
)

# Decorate function with metric.
@bucket_blueprint.route("/buckets/<id>")
def get_bucket(id: str) -> ResponseReturnValue:
    start = time.perf_counter()
    
    if id in data.keys():
        REQUEST_TIME.labels(path=f"/buckets/{id}", method="GET", status_code=200).observe(time.perf_counter() - start)
        return data.get(id), 200, {"Content-Type": "application/octet-stream"}
        
    REQUEST_TIME.labels(path=f"/buckets/{id}", method="GET", status_code=404).observe(time.perf_counter() - start)
    return jsonify({"error": "not found"}), 404, {"Content-Type": "application/json"}


@bucket_blueprint.route("/buckets/<id>", methods=["PUT"])
def put_bucket(id: str) -> ResponseReturnValue:
    with REQUEST_TIME.labels(path=f"/buckets/{id}", method="PUT", status_code=200).time():
        data[id] = request.get_data()

        return "", 200
    pass


@bucket_blueprint.route("/buckets/<id>", methods=["DELETE"])
def delete_bucket(id: str) -> ResponseReturnValue:
    start = time.perf_counter()

    if id in data.keys():
        data.pop(id, None)
        REQUEST_TIME.labels(path=f"/buckets/{id}", method="DELETE", status_code=500).observe(time.perf_counter() - start)
        return "", 500

    REQUEST_TIME.labels(path=f"/buckets/{id}", method="DELETE", status_code=400).observe(time.perf_counter() - start)
    return jsonify({"error": "bad request"}), 400, {"Content-Type": "application/json"}