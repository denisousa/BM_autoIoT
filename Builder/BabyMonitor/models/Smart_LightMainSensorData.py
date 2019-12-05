from main import db

from datetime import datetime

from geoalchemy2 import Geometry


class Smart_LightMainSensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    timeoff = db.Column(db.Boolean)

    presence = db.Column(db.Boolean)


    smart__light_main_sensor_id = db.Column(db.Integer, db.ForeignKey("smart__light_main_sensor.id"))

    def __repr__(self):
        return "<Smart_LightMainSensorData {}>".format(self.id)

    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

