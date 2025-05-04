from flask import Blueprint, render_template

view = Blueprint('view', __name__)

@view.route('/template', methods=['GET'])
def show_base_template():
    return render_template('base.html')