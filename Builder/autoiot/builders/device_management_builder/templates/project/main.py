from flask import Flask, Blueprint, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import configuration
from flask_login import LoginManager, current_user
import importlib
from flask_restless import APIManager
#from flask_restless_swagger import SwagAPIManager as APIManager

from flask_socketio import SocketIO

{% if project.database.type == 'postgre' %}
from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from shapely.geometry import Point, mapping, shape
{% endif %}

import os
import sys

CONFIGURATION = 'development'

# Creating the main app object
app = Flask(__name__)

# Load configuration from the config file
app.config.from_object(configuration[CONFIGURATION])
configuration[CONFIGURATION].init_app(app)


# Initializing the Flask Modules
db = SQLAlchemy(app) # Manage the communication with the database
migrate = Migrate(app, db) # Helps to migrate and upgrade the database
api = APIManager(app, flask_sqlalchemy_db=db) # Automatically create API for each database object

# Give access to low latency bi-directional communications between the clients and the server.
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

def register_blueprints(app):
    '''
    Register all available blueprints in the "controller" folder.
    :param app: the flask application
    :return: None
    '''
    from werkzeug.utils import find_modules, import_string

    for name in find_modules('controllers'):
        if name not in sys.modules:
            mod = importlib.import_module(name)

            for attr in dir(mod):
                #print(attr)
                if type(getattr(mod, attr)) == Blueprint:
                    app.register_blueprint(getattr(mod, attr))

# LoginManager handle login and logout
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'users_template.login'

@lm.user_loader
def load_user(id):
    '''
    Load and return data from the table by using user id.
    :param id: user id
    :return: User object
    '''
    from models.User import User
    return User.query.get(int(id))

@app.before_request
def before_app_request():
    '''
    This function runs before each request to the application
    :return:
    '''
    session.modified = True
    g.user = current_user

if __name__ == '__main__':

    {% if project.communication_protocols and project.get_mqtt_protocol() %}
    # MQTTManager is responsible for managing all communication with the MQTT Broker
    from MQTTManager import MQTTManager
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        mqttManager = MQTTManager()
        mqttManager.start()
    {% endif %}

    {% for socket in project.get_websockets() %}
    # {{socket.name}} manages web socket communication between client and server
    from sockets import {{socket.name}}
    socketio.on_namespace({{socket.name}}(app, "/{{socket.namespace}}"))
    {% endfor %}


    {% if project.database.type == 'postgre' %}
    def transform_points(obj):
        '''
        Recursively transform POINT objects inside a dict in dict objects
        :param obj: dict object
        :return: transformed dict
        '''
        if type(obj) is dict:
            for k, v in obj.items():
                obj[k] = transform_points(v)

            return obj

        if type(obj) is list:
            for i in range(len(obj)):
                obj[i] = transform_points(obj[i])

            return obj

        if isinstance(obj, WKBElement):
            return mapping(to_shape(obj))

        return obj


    def postprocessor_many(result=None, search_params=None, **kw):
        transform_points(result)


    def postprocessor_single(result=None, **kw):
        transform_points(result)
    {% endif %}

    {% for device in project.devices %}
    # Automatically generates an API based on {{device.name}} model
    from models import {{device.name}}
    api.create_api({{device.name}}, methods=['GET', 'POST', 'DELETE'], primary_key='key')

    {% for sensor in device.sensors %}
    # Automatically generates an API based on {{device.name}}{{sensor.name}} model
    from models import {{device.name}}{{sensor.name}}
    api.create_api({{device.name}}{{sensor.name}}, methods=['GET', 'POST', 'DELETE']
                    {% if project.database.type == 'postgre' %}
                    , postprocessors={
                       'GET_SINGLE': [postprocessor_single],
                       'GET_MANY': [postprocessor_many]
                   }
                    {% endif %}
                   )

    # Automatically generates an API based on {{device.name}}{{sensor.name}}Data model
    from models import {{device.name}}{{sensor.name}}Data
    api.create_api({{device.name}}{{sensor.name}}Data, methods=['GET', 'POST', 'DELETE']
                    {% if project.database.type == 'postgre' %}
                    ,exclude_columns=['position'],
                    postprocessors = {
                        'GET_SINGLE': [postprocessor_single],
                        'GET_MANY': [postprocessor_many]
                    }
                    {% endif %}
                  )

    {% endfor %}

    {% endfor %}

    # Register blueprints
    register_blueprints(app)

    # Run the application on the specified host and port {{project.app_port}}
    socketio.run(app, debug=True, host='0.0.0.0', port={{project.app_port}})

    {% if project.communication_protocols and project.get_mqtt_protocol() %}
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        mqttManager.stop()
    {% endif %}