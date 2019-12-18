import paho.mqtt.client as mqtt
import threading
import json

from models import *

from config import configuration

CONFIGURATION = 'development'

#MQTT Manager

def on_connect(client, userdata, flags, rc):
    '''
        This method is triggered when the application connects with the MQTT Broker.
    :param client: MQTT client
    :param userdata:
    :param flags:
    :param rc: Connection status code
    :return: None.
    '''

    print("Connected with result code " + str(rc))

    # Subscribe to topics
    client.subscribe('container_management_project/register/container')
    client.subscribe('container_management_project/update/container')
    client.subscribe('container_management_project/data/container')

def container_management_project_register_container(client, userdata, msg):
    '''
    Callback function triggered when a message arrives in the topic "container_management_project/register/container"
    '''
    
    try:
        message = json.loads(msg.payload)
        device = Container.query.filter_by(key=message['key']).first()
    
        if not device: #Device is not in the database
            print('Creating new device.')
            device = Container()
            device.key = message['key']
    
            
            if 'barcode' in message:
                device.barcode = message['barcode']
            
            if 'name' in message:
                device.name = message['name']
            
            if 'key' in message:
                device.key = message['key']
            
    
            db.session.add(device)
            db.session.commit()
    
            device.init_sensors()
        else:
            print('Device already in the database.')
    
    except Exception as e:
        print(e)
            
def container_management_project_update_container(client, userdata, msg):
    '''
    Callback function triggered when a message arrives in the topic "container_management_project/update/container"
    '''
    
    try:
        message = json.loads(msg.payload)
        device = Container.query.filter_by(key=message['key']).first()
    
        if device: #Device in the database
            print('Updating device.')
            
            device.key = message['key']
    
            
            if 'barcode' in message:
                device.barcode = message['barcode']
            
            if 'name' in message:
                device.name = message['name']
            
            if 'key' in message:
                device.key = message['key']
            
    
            db.session.add(device)
            db.session.commit()
    
        else: #Device not in the database
            print('Device not in the database.')
    
    except Exception as e:
        print(e)
            
def container_management_project_data_container(client, userdata, msg):
    '''
    Callback function triggered when a message arrives in the topic "container_management_project/data/container"
    '''
    
    try:
        message = json.loads(msg.payload)
        device = Container.query.filter_by(key=message['key']).first()
    
        if device: #Device in the database
            print('Adding data to device.')                
    
            
            if 'main_sensor_sensor' in message:
                device.main_sensor_sensor.add_metric_from_dict(message['main_sensor_sensor'])
            
    
            db.session.add(device)
            db.session.commit()
    
        else: #Device not in the database
            print('Device not in the database.')
    
    except Exception as e:
        print(e)
            

#MQTT Manager class responsible for the communication between application and MQTT Broker.
class MQTTManager:
    def __init__(self):
        self.client = mqtt.Client(client_id='Container Management Project.1574706806.2212186')

    def start_mqtt_thread(self):
        self.client.on_connect = on_connect

        if (configuration[CONFIGURATION].MQTT_USERNAME != '' and configuration[
            CONFIGURATION].MQTT_PASSWORD != ''):
            self.client.username_pw_set(configuration[CONFIGURATION].MQTT_USERNAME,
                                        password=configuration[CONFIGURATION].MQTT_PASSWORD)

        self.client.connect(configuration[CONFIGURATION].MQTT_BROKER_URL,
                            configuration[CONFIGURATION].MQTT_BROKER_PORT)

        # Register callback functions to each topic
        self.client.message_callback_add('container_management_project/register/container', container_management_project_register_container)
        self.client.message_callback_add('container_management_project/update/container', container_management_project_update_container)
        self.client.message_callback_add('container_management_project/data/container', container_management_project_data_container)

        self.client.loop_start()

    def start(self):
        self.mqtt_thread = threading.Thread(target=self.start_mqtt_thread)
        self.mqtt_thread.start()

    def stop(self):
        self.client.loop_stop()