from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from werkzeug.exceptions import BadRequest

from todo_list_api import db, WAITING_TASK, IN_PROGRESS_TASK, DONE_TASK
from todo_list_api.tasks.models import Task

tasks = Blueprint('tasks', __name__)


@tasks.route('/')
@tasks.route('/tasks')
def active_tasks():
    all_tasks = Task.query.filter_by(is_active=True).all()
    return jsonify(
        status=200,
        data=[task.to_dict() for task in all_tasks]
    )


@tasks.route('/tasks/done')
def finished_tasks():
    finished_tasks = Task.query.filter_by(status=DONE_TASK).all()
    return jsonify(
        status=200,
        data=[task.to_dict() for task in finished_tasks]
    )


@tasks.route('tasks/pending')
def pending_tasks():
    pending_tasks = Task.query.filter(
        or_(
            Task.status == WAITING_TASK,
            Task.status == IN_PROGRESS_TASK
        )
    ).all()
    return jsonify(
        status=200,
        data=[task.to_dict() for task in pending_tasks]
    )


@tasks.route('/tasks', methods=['POST'])
def create_new_task():
    try:
        request_body = request.get_json()
    except BadRequest:
        return 'Something went wrong with request', 400
    if not request_body.get('title'):
        return 'You should give a title to a task', 400
    title = request_body.get('title')
    status = request_body.get('status') or 0
    description = request_body.get('description')
    new_task = Task(title=title, status=status, description=description)
    db.session.add(new_task)
    db.session.commit()
    return 'Task successfully created', 201
