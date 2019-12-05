{% for device in project.devices %}
from .{{device.name}} import *

{% for sensor in device.sensors %}
from .{{device.name}}{{sensor.name}} import *
from .{{device.name}}{{sensor.name}}Data import *
{% endfor %}

{% endfor %}