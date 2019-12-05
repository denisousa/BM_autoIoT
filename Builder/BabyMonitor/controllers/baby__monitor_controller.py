from flask_login import login_required, login_user
from flask import Blueprint, redirect, url_for, g, render_template, request, flash
from forms.FormLogin import FormLogin

from sqlalchemy.orm.attributes import InstrumentedAttribute
from models.Baby_Monitor import Baby_Monitor

from main import db


baby__monitor_template = Blueprint("baby__monitor_template", __name__, template_folder='templates')

@baby__monitor_template.route('/dashboard/baby__monitor/<int:id>')
def dashboard(id):
    '''
    Dashboard with information about list of devices.
    :param id: baby__monitor id
    :return: Render the HTML page
    '''
    
    baby__monitor = Baby_Monitor.query.filter_by(id=id).first()
    list_of_attrs = []
    list_of_sensors = []
    for k, v in vars(Baby_Monitor).items():
        if (type(v) == InstrumentedAttribute):
            if('_sensor' in k):
                list_of_sensors.append(k)
            else:
                list_of_attrs.append(k)        
    return render_template('dashboard_baby__monitor.html', baby__monitor=baby__monitor, list_of_attrs = list_of_attrs, list_of_sensors = list_of_sensors)        
    


@baby__monitor_template.route('/baby__monitor_list')
@login_required
def list():
    '''
    Returns information about the types of sensors.
    :return: Renders sensors list.
    '''
    models = Baby_Monitor.query.all()

    list_of_attrs = []
    list_of_sensors = []
    for k, v in vars(Baby_Monitor).items():
        if (type(v) == InstrumentedAttribute):

            if('_sensor' in k):
                list_of_sensors.append(k)
            else:
                list_of_attrs.append(k)

    return render_template('baby__monitor_list.html',models=models, list_of_attrs=list_of_attrs, list_of_sensors=list_of_sensors)

@baby__monitor_template.route('/delete/baby__monitor/<int:id>')
@login_required
def delete(id):
    '''
    Deletes a baby__monitor object from the database.
    :param id: baby__monitor object id.
    :return: Redirects to List Page.
    '''
    selected_object = Baby_Monitor.query.filter_by(id=id).first()

    if (selected_object):
        db.session.delete(selected_object)
        db.session.commit()

        flash('Baby_Monitor deleted successfully.', 'success')
        return redirect(url_for('baby__monitor_template.list'))

    flash('Error deleting the Baby_Monitor.', 'danger')
    return redirect(url_for('baby__monitor_template.list'))