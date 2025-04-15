from re import S
from flask import abort, jsonify, request

from app import create_app, db
from app.database import SensorData
from app.environment import PORT

app = create_app()


@app.route("/")
def hello_world():
    return "Hello, world!"


@app.route("/sensor-data", methods=["POST"])
def post_sensor_data():
    data = request.get_json()
    if not data:
        abort(400)
    sensor_data = SensorData(**data)
    db.session.add(sensor_data)
    db.session.commit()
    return jsonify({"id": sensor_data.id}), 201


@app.route("/sensor-data", methods=["GET"])
def get_sensor_data():
    sensor_data = SensorData.query.all()
    return jsonify([d.to_dict()for d in sensor_data]), 200


if __name__ == "__main__":
    app.run(port=PORT)
