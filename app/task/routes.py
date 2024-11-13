from datetime import datetime, timedelta

from . import blueprint
from ..auth.helpers import auth_protected, generate_uuid_integer, extract_token_data
from ..models.task import Task
from ..models import db

from flask import request, jsonify
from sqlalchemy import or_


@blueprint.route("/<id>", methods=["GET", "PUT"])
@auth_protected
def get_task_by_id(id):
    if request.method == "GET":
        task = Task.query.filter_by(id=id).first()
        if not task:
            return jsonify({"message": "task not found"}), 404
        return jsonify(task.to_dict()), 200
    if request.method == "PUT":
        task = Task.query.filter_by(id=id).first()
        if not task:
            return "Task not found", 404
        try:
            task.update(request.get_json())

            return jsonify(task.to_dict()), 200
        except Exception as e:
            return f"An issue occured when updating task: {e}", 500


@blueprint.route("", methods=["POST", "GET"])
@auth_protected
def modify_task():
    id, _ = extract_token_data()
    if request.method == "POST":
        body = request.get_json()
        if "title" not in body:
            return jsonify({"message": "Missing title"}), 400
        task = Task(
            id=generate_uuid_integer(),
            title=body["title"],
            description=body.get("description", ""),
            due_date=body.get("due_date", datetime.utcnow() + timedelta(days=30)),
            priority=body.get("priority", ""),
            status=body.get("status", ""),
            created_by=id,
            assigned_to=body.get("assigned_to", None),
            reviewed_by=body.get("reviewed_by", None),
            tags=body.get("tags", "[]"),
            completed=False,
            updated_at=datetime.utcnow(),
        )
        try:
            db.session.add(task)
            db.session.commit()
            return jsonify({"message": "Task successfully created"}), 200
        except Exception as e:
            db.session.rollback()
            return (
                jsonify(
                    {
                        "message": "An error occurred while registering the user",
                        "error": str(e),
                    }
                ),
                500,
            )

    if request.method == "GET":
        tasks = Task.query.filter(
            or_(
                Task.created_by == id,
                Task.assigned_to == id,
                Task.reviewed_by == id,
            )
        ).all()
        tasks = [task.to_dict() for task in tasks]
        return jsonify(tasks)
