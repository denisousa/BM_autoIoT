from main import db

from datetime import datetime


class SmartTV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String)
    barcode = db.Column(db.String)
    key = db.Column(db.String, unique=True, nullable=False)


    def __repr__(self):
        return "<SmartTV {}>".format(self.id)

    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

