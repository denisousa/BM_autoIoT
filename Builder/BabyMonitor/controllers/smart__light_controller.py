from flask_login import login_required, login_user
from flask import Blueprint, redirect, url_for, g, render_template, request, flash
from forms.FormLogin import FormLogin

from sqlalchemy.orm.attributes import InstrumentedAttribute
from models.Smart_Light import Smart_Light

from main import db


smart__light_template = Blueprint("smart__light_template", __name__, template_folder='templates')

@smart__light_template.route('/dashboard/smart__light/<int:id>')
def dashboard(id):
    '''
    Dashboard with information about list of devices.
    :param id: smart__light id
    :return: Render the HTML page
    '''
    
    smart__light = Smart_Light.query.filter_by(id=id).first()
    list_of_attrs = []
    list_of_sensors = []
    for k, v in vars(Smart_Light).items():
        if (type(v) == InstrumentedAttribute):
            if('_sensor' in k):
                list_of_sensors.append(k)
            else:
                list_of_attrs.append(k)        
    return render_template('dashboard_smart__light.html', smart__light=smart__light, list_of_attrs = list_of_attrs, list_of_sensors = list_of_sensors)        
    


@smart__light_template.route('/smart__light_list')
@login_required
def list():
    '''
    Returns information about the types of sensors.
    :return: Renders sensors list.
    '''
    models = Smart_Light.query.all()

    list_of_attrs = []
    list_of_sensors = []
    for k, v in vars(Smart_Light).items():
        if (type(v) == InstrumentedAttribute):

            if('_sensor' in k):
                list_of_sensors.append(k)
            else:
                list_of_attrs.append(k)

    return render_template('smart__light_list.html',models=models, list_of_attrs=list_of_attrs, list_of_sensors=list_of_sensors)

@smart__light_template.route('/delete/smart__light/<int:id>')
@login_required
def delete(id):
    '''
    Deletes a smart__light object from the database.
    :param id: smart__light object id.
    :return: Redirects to List Page.
    '''
    selected_object = Smart_Light.query.filter_by(id=id).first()

    if (selected_object):
        db.session.delete(selected_object)
        db.session.commit()

        flash('Smart_Light deleted successfully.', 'success')
        return redirect(url_for('smart__light_template.list'))

    flash('Error deleting the Smart_Light.', 'danger')
    return redirect(url_for('smart__light_template.list'))