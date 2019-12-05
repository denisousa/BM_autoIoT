from main import db

from datetime import datetime

from models.Smart_LightMainSensor import Smart_LightMainSensor

class Smart_Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String)
    barcode = db.Column(db.String)
    key = db.Column(db.String, unique=True, nullable=False)

    main_sensor_sensor = db.relationship("Smart_LightMainSensor", uselist=False, backref="smart__light", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Smart_Light {}>".format(self.id)

    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

    def init_sensors(self):
        if self.id is None:
            db.session.add(self)
            db.session.flush()

        if self.main_sensor_sensor is None:
            self.main_sensor_sensor = Smart_LightMainSensor( smart__light = self)

        db.session.commit()
