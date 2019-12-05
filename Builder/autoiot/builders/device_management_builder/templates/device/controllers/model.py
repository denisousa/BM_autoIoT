from flask_login import login_required, login_user
from flask import Blueprint, redirect, url_for, g, render_template, request, flash
from forms.FormLogin import FormLogin

from sqlalchemy.orm.attributes import InstrumentedAttribute
from models.{{device.name}} import {{device.name}}

from main import db

{% set model_name = device.name %}
{% set template_name = str_converter(device.name).camel() + '_template' %}
{% set model_camel = str_converter(device.name).camel() %}

{{template_name}} = Blueprint("{{template_name}}", __name__, template_folder='templates')

{% if device.get_dashboard() %}
@{{template_name}}.route('/dashboard/{{model_camel}}/<int:id>')
def dashboard(id):
    '''
    Dashboard with information about list of devices.
    :param id: {{model_camel}} id
    :return: Render the HTML page
    '''
{% for line in device.get_dashboard().code.split('\n') %}
    {{line}}
{% endfor %}
{% endif %}


@{{template_name}}.route('/{{model_camel}}_list')
@login_required
def list():
    '''
    Returns information about the types of sensors.
    :return: Renders sensors list.
    '''
    models = {{model_name}}.query.all()

    list_of_attrs = []
    list_of_sensors = []
    for k, v in vars({{model_name}}).items():
        if (type(v) == InstrumentedAttribute):

            if('_sensor' in k):
                list_of_sensors.append(k)
            else:
                list_of_attrs.append(k)

    return render_template('{{model_camel}}_list.html',models=models, list_of_attrs=list_of_attrs, list_of_sensors=list_of_sensors)

@{{template_name}}.route('/delete/{{model_camel}}/<int:id>')
@login_required
def delete(id):
    '''
    Deletes a {{model_camel}} object from the database.
    :param id: {{model_camel}} object id.
    :return: Redirects to List Page.
    '''
    selected_object = {{model_name}}.query.filter_by(id=id).first()

    if (selected_object):
        db.session.delete(selected_object)
        db.session.commit()

        flash('{{model_name}} deleted successfully.', 'success')
        return redirect(url_for('{{template_name}}.list'))

    flash('Error deleting the {{model_name}}.', 'danger')
    return redirect(url_for('{{template_name}}.list'))