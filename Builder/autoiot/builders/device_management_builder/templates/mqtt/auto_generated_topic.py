'''
This is a example of message to update this sensor value
{{sample_message}}
'''

from main import db
import json

{% for model in models %}
from models.{{model['name']}} import {{model['name']}}
{% endfor %}

def {{str_converter(model['name']).camel()}}_{{str_converter(sensor['name']).camel()}}_sensor(client, userdata, msg):
    message = json.loads(msg.payload)

    {{str_converter(model['name']).camel()}} = {{model['name']}}.query.filter_by({{model['key']}}=message[message['key']]).first()

    if {{str_converter(model['name']).camel()}} is not None:
        {{str_converter(model['name']).camel()}}.{{str_converter(sensor['name']).camel()}}_sensor.add_metric({% for metric in sensor['metrics'] %}{{metric}}=message['metrics']['{{metric}}']{{ "," if not loop.last }}{% endfor %})