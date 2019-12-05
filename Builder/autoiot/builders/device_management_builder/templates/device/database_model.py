from main import db

from datetime import datetime

{% for sensor in device.sensors %}
from models.{{device.name + sensor.name}} import {{device.name + sensor.name}}
{% endfor %}

class {{device.name}}(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    {% for field in device.fields %}
    {% if field.name == 'key' %}
    {{field.name}} = db.Column(db.{{field.type}}, unique=True, nullable=False)
    {% else %}
    {{field.name}} = db.Column(db.{{field.type}})
    {% endif %}
    {% endfor %}

    {% for sensor in device.sensors %}
    {{sensor.get_name_camel_case()}}_sensor = db.relationship("{{device.name + sensor.name}}", uselist=False, backref="{{device.get_name_camel_case()}}", cascade="all, delete-orphan")
    {% endfor %}

    def __repr__(self):
        return "<{{device.name}} {}>".format(self.id)

    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

    {% if device.sensors %}
    def init_sensors(self):
        if self.id is None:
            db.session.add(self)
            db.session.flush()

        {% for sensor in device.sensors %}
        if self.{{sensor.get_name_camel_case()}}_sensor is None:
            self.{{sensor.get_name_camel_case()}}_sensor = {{device.name + sensor.name}}( {{device.get_name_camel_case()}} = self)
        {% endfor %}

        db.session.commit()
    {% endif %}
