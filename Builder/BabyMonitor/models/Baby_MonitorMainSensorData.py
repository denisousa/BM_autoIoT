from main import db

from datetime import datetime

from geoalchemy2 import Geometry


class Baby_MonitorMainSensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    temperature = db.Column(db.Float)

    breathing = db.Column(db.Boolean)

    sleeping = db.Column(db.Boolean)


    baby__monitor_main_sensor_id = db.Column(db.Integer, db.ForeignKey("baby__monitor_main_sensor.id"))

    def __repr__(self):
        return "<Baby_MonitorMainSensorData {}>".format(self.id)

    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

