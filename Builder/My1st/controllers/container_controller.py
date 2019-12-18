from flask_login import login_required, login_user
from flask import Blueprint, redirect, url_for, g, render_template, request, flash
from forms.FormLogin import FormLogin

from sqlalchemy.orm.attributes import InstrumentedAttribute
from models.Container import Container

from main import db


container_template = Blueprint("container_template", __name__, template_folder='templates')

@container_template.route('/dashboard/container/<int:id>')
def dashboard(id):
    '''
    Dashboard with information about list of devices.
    :param id: container id
    :return: Render the HTML page
    '''
    
    container = Container.query.filter_by(id=id).first()
    list_of_attrs = []
    list_of_sensors = []
    for k, v in vars(Container).items():
        if (type(v) == InstrumentedAttribute):
            if('_sensor' in k):
                list_of_sensors.append(k)
            else:
                list_of_attrs.append(k)        
    return render_template('dashboard_container.html', container=container, list_of_attrs = list_of_attrs, list_of_sensors = list_of_sensors)        
    


@container_template.route('/container_list')
@login_required
def list():
    '''
    Returns information about the types of sensors.
    :return: Renders sensors list.
    '''
    models = Container.query.all()

    list_of_attrs = []
    list_of_sensors = []
    for k, v in vars(Container).items():
        if (type(v) == InstrumentedAttribute):

            if('_sensor' in k):
                list_of_sensors.append(k)
            else:
                list_of_attrs.append(k)

    return render_template('container_list.html',models=models, list_of_attrs=list_of_attrs, list_of_sensors=list_of_sensors)

@container_template.route('/delete/container/<int:id>')
@login_required
def delete(id):
    '''
    Deletes a container object from the database.
    :param id: container object id.
    :return: Redirects to List Page.
    '''
    selected_object = Container.query.filter_by(id=id).first()

    if (selected_object):
        db.session.delete(selected_object)
        db.session.commit()

        flash('Container deleted successfully.', 'success')
        return redirect(url_for('container_template.list'))

    flash('Error deleting the Container.', 'danger')
    return redirect(url_for('container_template.list'))