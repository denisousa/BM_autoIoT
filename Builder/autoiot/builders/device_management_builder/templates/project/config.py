import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Application Name
PRODUCT_NAME = 'AutoIoT.{}'.format('{{project.title}}')

class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'asdf1234' # HINT: Choose a better SECRET_KEY

    STATIC_FOLDER = 'static' # Static folder path

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    {% if project.get_mqtt_protocol() %}
    #MQTT Broker Configuration
    MQTT_BROKER_URL = '{{project.get_mqtt_protocol().hostname}}'
    MQTT_BROKER_PORT = {{project.get_mqtt_protocol().port}}
    MQTT_USERNAME = '{{project.get_mqtt_protocol().username}}'
    MQTT_PASSWORD = '{{project.get_mqtt_protocol().password}}'
    {% endif %}

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

    {% if project.database %}
    # Database Configuration
    
    {% if project.database.type == 'postgre' %}
    
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{username}:{password}@{hostname}/{databasename}".format(
        username="{{project.database.username}}",
        password="{{project.database.password}}",
        {% if 'docker' in config and config['docker'] == True %}
        hostname = "postgis:5432",
        {% else %}
        hostname="{{project.database.hostname}}:{{project.database.port}}",
        {% endif %}
        databasename="{{project.database.database_name}}",
    )
    
    {% else %}
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    {% endif %}

    # Advanced Database Configuration
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository') # Directory to help migrate database schema
    {% endif %}

configuration = {
    'development': DevelopmentConfig
}