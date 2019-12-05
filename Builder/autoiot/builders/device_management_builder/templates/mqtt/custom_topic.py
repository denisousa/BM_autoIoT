from main import db
import json

{% for model in models %}
from models.{{model['name']}} import {{model['name']}}
{% endfor %}

def {{function_name}}(client, userdata, msg):
    message = json.loads(msg.payload)
{% for line in code.split('\n') %}
    {{line}}
{% endfor %}