from main import db

from datetime import datetime

from models.ContainerMainSensor import ContainerMainSensor

class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    barcode = db.Column(db.String)
    name = db.Column(db.String)
    key = db.Column(db.String, unique=True, nullable=False)

    main_sensor_sensor = db.relationship("ContainerMainSensor", uselist=False, backref="container", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Container {}>".format(self.id)

    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

    def init_sensors(self):
        if self.id is None:
            db.session.add(self)
            db.session.flush()

        if self.main_sensor_sensor is None:
            self.main_sensor_sensor = ContainerMainSensor( container = self)

        db.session.commit()
