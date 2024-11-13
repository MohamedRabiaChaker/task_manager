from datetime import datetime, timedelta

from . import blueprint
from ..auth.helpers import auth_protected, generate_uuid_integer, extract_token_data
from ..models.task import Task
from ..models import db

from flask import request, jsonify


@blueprint.route("/<id>", methods=["GET"])
@auth_protected
def get_task_by_id(id):
    task = Task.query.filter_by(id=id).first()
    if not task:
        return jsonify({"message": "task not found"}), 404
    return jsonify(task.to_dict()), 200


@blueprint.route("", methods=["POST", "PUT"])
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
