from flask_login import login_required, login_user
from flask import Blueprint, redirect, url_for, g, render_template, request, flash
from forms.FormLogin import FormLogin

from models.User import User

base_template = Blueprint('base_template', __name__, template_folder='templates')

@base_template.route('/')
def landing_page():
    '''
    Default/Index page redirects to the login page.
    :return: User Login Page redirect
    '''
    return redirect(url_for('users_template.login'))

@base_template.route('/home')
def home():
    '''
    Return a page that shows all the devices in the project.
    :return: Device Information Page.
    '''
    devices = []

    {% for device in project.devices %}
    devices.append(( "{{device.name}}", "iot_default_device.png", "{{device.description}}", "{{str_converter(device.name).camel()}}" ))
    {% endfor %}

    return render_template('home.html', devices=devices)