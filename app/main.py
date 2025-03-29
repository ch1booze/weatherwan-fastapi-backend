import json

from flask import abort, jsonify, request

from app import create_app, db
from app.database import Telemetry

app = create_app()


@app.route("/")
def hello_world():
    return "Hello, world!"


@app.route("/telemetry", methods=["POST"])
def store_telemetry():
    """Handles incoming telemetry data from IoT nodes."""
    telemetry_data = request.get_json()

    if (
        not telemetry_data
        or "node" not in telemetry_data
        or "data" not in telemetry_data
    ):
        abort(400, description="Invalid payload. 'node' and 'data' are required.")

    try:
        data = json.dumps(telemetry_data["data"])
    except (TypeError, ValueError):
        abort(400, description="Invalid data format.")

    telemetry = Telemetry(node=telemetry_data["node"], data=data)

    try:
        db.session.add(telemetry)
        db.session.commit()
    except Exception:
        db.session.rollback()
        abort(500, description="Database error.")

    return jsonify({"message": "Telemetry stored successfully"}), 201


if __name__ == "__main__":
    app.run()
