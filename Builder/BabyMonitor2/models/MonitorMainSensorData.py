from main import db

from datetime import datetime

from geoalchemy2 import Geometry


class MonitorMainSensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sleeping = db.Column(db.Boolean)

    breathing = db.Column(db.Boolean)

    time_no_breathing = db.Column(db.Integer)

    crying = db.Column(db.Boolean)


    monitor_main_sensor_id = db.Column(db.Integer, db.ForeignKey("monitor_main_sensor.id"))

    def __repr__(self):
        return "<MonitorMainSensorData {}>".format(self.id)

    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

