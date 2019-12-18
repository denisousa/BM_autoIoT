from main import db

from datetime import datetime

from geoalchemy2 import Geometry


class ContainerMainSensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    temperature = db.Column(db.Float)

    position_raw_point_x = db.Column(db.Float)
    position_raw_point_y = db.Column(db.Float)

    filing_status = db.Column(db.Integer)


    container_main_sensor_id = db.Column(db.Integer, db.ForeignKey("container_main_sensor.id"))

    def __repr__(self):
        return "<ContainerMainSensorData {}>".format(self.id)

    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

    #This property is used to check if "position_raw_point" is a POINT type attr.
    @property
    def position(self):

        # Remove this point class when database type is postgre
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y



        if hasattr(self, 'position_raw_point_x') and (not self.position_raw_point_x is None):
            return Point(self.position_raw_point_x, self.position_raw_point_y)
        else:
            return None
