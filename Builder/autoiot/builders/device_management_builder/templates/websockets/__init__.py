{% for device in project.devices %}
from .{{device.name}}Socket import *
{% endfor %}