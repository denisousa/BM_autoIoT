from main import db

from datetime import datetime

from geoalchemy2 import Geometry
{% if device.project.database.type == 'postgre' %}
from shapely import wkb
{% endif %}

{% set sensor_name = device.name + sensor.name %}
{% set metric_name = device.name + sensor.name + 'Data' %}

class {{metric_name}}(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    {% for field in sensor.data_fields %}
    {% if field.type|string == 'Point' %}
    {% if device.project.database.type == 'postgre'%}
    {{field.name}}_raw_point = db.Column(Geometry('POINT'))
    {% else %}
    {{field.name}}_raw_point_x = db.Column(db.Float)
    {{field.name}}_raw_point_y = db.Column(db.Float)
    {% endif %}
    {% else %}
    {{field.name}} = db.Column(db.{{field.type}})
    {% endif %}

    {% endfor %}

    {{str_converter(sensor_name).camel()}}_id = db.Column(db.Integer, db.ForeignKey("{{str_converter(sensor_name).camel()}}.id"))

    def __repr__(self):
        return "<{{device.name + sensor.name + 'Data'}} {}>".format(self.id)

    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

    {% for field in sensor.data_fields %}
    {% if field.type|string == 'Point' %}
    #This property is used to check if "{{field.name}}_raw_point" is a POINT type attr.
    @property
    def {{field.name}}(self):

        # Remove this point class when database type is postgre
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y


        {% if device.project.database.type == 'postgre' %}
        if hasattr(self, '{{field.name}}_raw_point') and (not self.{{field.name}}_raw_point is None):
            return wkb.loads(bytes(self.{{field.name}}_raw_point.data))
        {% endif %}

        if hasattr(self, '{{field.name}}_raw_point_x') and (not self.{{field.name}}_raw_point_x is None):
            return Point(self.{{field.name}}_raw_point_x, self.{{field.name}}_raw_point_y)
        else:
            return None
    {% endif %}
    {% endfor %}
