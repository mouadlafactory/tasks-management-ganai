from flask import Blueprint
from controllers.tasks_controllers import (get_all_tasks,
create_task, get_task, update_task, 
delete_task)
from middlewares.auth_middlewares import auth_required, admin_required

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
@auth_required
@admin_required
def tasks():
    return get_all_tasks()

@tasks_bp.route('/', methods=['POST'])
@auth_required
def create_task_route():
    return create_task()

@tasks_bp.route('/<string:task_id>', methods=['GET'])
@auth_required
def get_task_route(task_id):
    return get_task(task_id)

@tasks_bp.route('/<string:task_id>', methods=['PUT'])
@auth_required
def update_task_route(task_id):
    return update_task(task_id)

@tasks_bp.route('/<string:task_id>', methods=['DELETE'])
@auth_required
def delete_task_route(task_id):
    return delete_task(task_id)
