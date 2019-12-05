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

    devices.append(( "Baby_Monitor", "iot_default_device.png", "An IoT device monitors the breathing, sound and wether the baby is sleeping or not.", "baby__monitor" ))
    devices.append(( "Smart_Light", "iot_default_device.png", "An IoT device turn on sensing presence of people, and turn off otherwise. It also can be configured to turn on/off during a period of time.", "smart__light" ))

    return render_template('home.html', devices=devices)