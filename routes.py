# routes.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Camper, Activity, Signup

bp = Blueprint('api', __name__)

# -------------------- Utility --------------------
def validation_error_response(messages):
    return jsonify({"errors": messages}), 400

# -------------------- CAMPERS --------------------
@bp.get('/campers')
def list_campers():
    campers = Camper.query.all()
    return jsonify([c.to_dict() for c in campers]), 200

@bp.get('/campers/<int:id>')
def get_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    return jsonify(camper.to_dict(include_signups=True)), 200

@bp.post('/campers')
def create_camper():
    payload = request.get_json() or {}
    name = payload.get('name')
    age = payload.get('age')

    try:
        camper = Camper(name=name, age=age)
        db.session.add(camper)
        db.session.commit()
        return jsonify(camper.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return validation_error_response([str(e)])

@bp.patch('/campers/<int:id>')
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404

    payload = request.get_json() or {}
    name = payload.get('name', camper.name)
    age = payload.get('age', camper.age)

    try:
        camper.name = name
        camper.age = age
        db.session.commit()
        return jsonify(camper.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return validation_error_response([str(e)])

# -------------------- ACTIVITIES --------------------
@bp.get('/activities')
def list_activities():
    activities = Activity.query.all()
    return jsonify([a.to_dict() for a in activities]), 200

@bp.get('/activities/<int:id>')
def get_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404
    return jsonify(activity.to_dict()), 200

@bp.post('/activities')
def create_activity():
    payload = request.get_json() or {}
    name = payload.get('name')
    difficulty = payload.get('difficulty')

    try:
        activity = Activity(name=name, difficulty=difficulty)
        db.session.add(activity)
        db.session.commit()
        return jsonify(activity.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return validation_error_response([str(e)])

# -------------------- SIGNUPS --------------------
@bp.get('/signups')
def list_signups():
    signups = Signup.query.all()
    return jsonify([s.to_dict(include_nested_activity=True) for s in signups]), 200

@bp.post('/signups')
def create_signup():
    payload = request.get_json() or {}
    camper_id = payload.get('camper_id')
    activity_id = payload.get('activity_id')
    time = payload.get('time')

    try:
        signup = Signup(camper_id=camper_id, activity_id=activity_id, time=time)
        db.session.add(signup)
        db.session.commit()
        return jsonify(signup.to_dict(include_nested_activity=True)), 201
    except Exception as e:
        db.session.rollback()
        return validation_error_response([str(e)])
