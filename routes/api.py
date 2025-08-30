from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import Team, Case, Participant, db

api_bp = Blueprint("api", __name__)

@api_bp.get("/cases")
@login_required
def cases_by_team():
    team_id = request.args.get("team_id", type=int)
    if not team_id:
        return jsonify([])
    cases = Case.query.filter_by(team_id=team_id).order_by(Case.title).all()
    return jsonify([{"id": c.id, "title": c.title, "team_id": c.team_id} for c in cases])

@api_bp.get("/participants")
@login_required
def participants_by_team():
    team_id = request.args.get("team_id", type=int)
    if not team_id:
        return jsonify([])
    participants = Participant.query.filter_by(team_id=team_id).order_by(Participant.full_name).all()
    return jsonify([{"id": p.id, "full_name": p.full_name, "team_id": p.team_id} for p in participants])

@api_bp.get("/team-for-case")
@login_required
def team_for_case():
    case_id = request.args.get("case_id", type=int)
    if not case_id:
        return jsonify({})
    case = db.session.get(Case, case_id)
    if not case:
        return jsonify({})
    team = db.session.get(Team, case.team_id)
    return jsonify({"team_id": team.id, "team_name": team.name}) if team else jsonify({})
