import paho.mqtt.client as mqtt
import threading
import json
import time

from models import *

from config import configuration

CONFIGURATION = 'development'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

{% for device in project.devices %}

def send_data_{{device.get_name_camel_case()}}(client):
    i = 0
    increment = 1
    points = ['52.517711, 13.376964', '52.517463, 13.377093', '52.517176, 13.377232', '52.516758, 13.377253',
              '52.516418, 13.376910', '52.516033, 13.377028', '52.515883, 13.377361', '52.515615, 13.377543',
              '52.515191, 13.377532', '52.514786, 13.377478']

    LIMIT = len(points)

    while True:

        message = {}
        message['key'] = '{{device.get_name_camel_case()}}-x'

        {% for sensor in device.sensors %}
        message['{{sensor.get_name_camel_case()}}_sensor'] = {}
        {% for data in sensor.data_fields %}
        {% if data.type|string == 'String' and data.name != 'key' %}
        message['{{sensor.get_name_camel_case()}}_sensor']['{{data.name}}'] = 'test'
        {% elif data.type|string == 'Boolean' %}
        message['{{sensor.get_name_camel_case()}}_sensor']['{{data.name}}'] = True if i % 2 == 0 else False
        {% elif data.type|string == 'Integer' %}
        message['{{sensor.get_name_camel_case()}}_sensor']['{{data.name}}'] = i
        {% elif data.type|string == 'Float' %}
        message['{{sensor.get_name_camel_case()}}_sensor']['{{data.name}}'] = i**2
        {% elif data.type|string == 'Point' %}
        message['{{sensor.get_name_camel_case()}}_sensor']['{{data.name}}'] = points[i]
        {% endif %}

        {% endfor %}
        {% endfor %}

        i += increment

        if i == LIMIT:
            increment = -1
            i += increment

        if i < 0:
            increment = 1
            i += increment

        client.publish('{{device.project.get_name_camel_case()}}/data/{{device.get_name_camel_case()}}',
                       json.dumps(message))  # publish
        print('Sending data to {}.'.format('{{device.get_name_camel_case()}}'))

        time.sleep(15)


def register_device_{{device.get_name_camel_case()}}(client):
    message = {}

    message['key'] = '{{device.get_name_camel_case()}}-x'

    {% for field in device.fields %}
    {% if field.type|string == 'String' and field.name != 'key' %}
    message['{{field.name}}'] = 'test'
    {% elif field.type|string == 'Boolean' %}
    message['{{field.name}}'] = True
    {% elif field.type|string == 'Integer' %}
    message['{{field.name}}'] = 1
    {% elif field.type|string == 'Float' %}
    message['{{field.name}}'] = 1.0
    {% endif %}
    {% endfor %}

    client.publish('{{device.project.get_name_camel_case()}}/register/{{device.get_name_camel_case()}}', json.dumps(message)) #publish
    print('Sending message to register a {}.'.format('{{device.get_name_camel_case()}}'))

    mqtt_thread = threading.Thread(target=send_data_{{device.get_name_camel_case()}}, args=[client])
    mqtt_thread.daemon = True
    mqtt_thread.start()
{% endfor %}

class DevicesSimulator:
    def __init__(self):
        self.client = mqtt.Client(client_id='{{project.name}}.Simulator')

    def start_mqtt_thread(self):
        self.client.on_connect = on_connect

        if (configuration[CONFIGURATION].MQTT_USERNAME != '' and configuration[
            CONFIGURATION].MQTT_PASSWORD != ''):
            self.client.username_pw_set(configuration[CONFIGURATION].MQTT_USERNAME,
                                   password=configuration[CONFIGURATION].MQTT_PASSWORD)

        self.client.connect(configuration[CONFIGURATION].MQTT_BROKER_URL,
                            configuration[CONFIGURATION].MQTT_BROKER_PORT)

        {% for device in project.devices %}
        register_device_{{device.get_name_camel_case()}}(self.client)
        {% endfor %}

    def start(self):
        self.mqtt_thread = threading.Thread(target=self.start_mqtt_thread)
        self.mqtt_thread.start()

        print('Running Simulator...')

    def stop(self):
        self.client.loop_stop()

devicesSimulator = DevicesSimulator()
devicesSimulator.start()

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    print('Stopping Simulator...')
    devicesSimulator.stop()
