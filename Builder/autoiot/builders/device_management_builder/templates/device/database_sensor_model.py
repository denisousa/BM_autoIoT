from main import db

from datetime import datetime

{% set sensor_name = device.name + sensor.name %}
{% set metric_name = device.name + sensor.name + 'Data' %}

{% if sensor.data_fields %}
from models.{{metric_name}} import {{metric_name}}
{% endif %}

class {{sensor_name}}(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    {% for field in sensor.fields %}
    {{field.name}} = db.Column(db.{{field.type}})
    {% endfor %}

    {{device.get_name_camel_case()}}_id = db.Column(db.Integer, db.ForeignKey("{{device.get_name_camel_case()}}.id"))

    metrics = db.relationship("{{metric_name}}", backref="{{str_converter(sensor_name).camel()}}", lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return "<{{device.name + sensor.name}} {}>".format(self.id)

    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

    {% if sensor.data_fields %}
    def add_metric(self{% for field in sensor.data_fields %}, {{field.name}}{% endfor %}):
        new_metric = {{metric_name}}({{str_converter(sensor_name).camel()}}=self)

        {% for field in sensor.data_fields %}
        new_metric.{{field.name}} = {{field.name}}
        {% endfor %}

        db.session.add(new_metric)
        db.session.commit()

    def add_metric_from_dict(self, D):
        try:
            new_metric = {{metric_name}}({{str_converter(sensor_name).camel()}}=self)

            print(D)

            for k, v in D.items():
                #if type(getattr({{metric_name}}, k)) == property :
                {% if sensor.device.project.database.type == 'postgre' %}
                if hasattr(new_metric, k + '_raw_point'):
                {% else %}
                if hasattr(new_metric, k + '_raw_point_x'):
                {% endif %}
                    print('Probably a position attr. Trying to set as a POINT attr.')

                    k = k + '_raw_point'

                    x, y = v.split(',')
                    x.strip()
                    y.strip()

                    {% if sensor.device.project.database.type == 'postgre' %}
                    setattr(new_metric, k, "POINT({} {})".format(x,y))
                    {% else %}
                    setattr(new_metric, k + '_x', float(x))
                    setattr(new_metric, k + '_y', float(y))
                    {% endif %}
                else:
                    setattr(new_metric, k, v)

            db.session.add(new_metric)
            db.session.commit()
        except Exception as e:
            print('Error inserting metric!', e)

    {% endif %}



    def number_of_metrics(self):
        return self.metrics.count()

    def get_metrics_to_plot(self, axis, metric_name):
        metrics = self.metrics.filter(getattr({{metric_name}}, metric_name) != None).order_by({{metric_name}}.created_at.desc()).limit(30).all()

        if axis == 'x':
            result = [metric.created_at.isoformat() for metric in metrics]
        else:
            result = [getattr(metric, metric_name) for metric in metrics]

        return result

    def get_last_metric_data(self, metric_name):
        
        if not hasattr({{metric_name}}, metric_name):
            return None
        
        metric = self.metrics.filter(getattr({{metric_name}}, metric_name) != None).order_by({{metric_name}}.created_at.desc()).first()

        return metric