from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Team, Case, TeamEvaluation, Block

team_eval_bp = Blueprint("team_eval", __name__, template_folder="../templates")

@team_eval_bp.route("/", methods=["GET"])
@login_required
def form():
    teams = Team.query.order_by(Team.name).all()
    cases = Case.query.order_by(Case.title).all()
    blocks = Block.query.order_by(Block.name).all()
    return render_template(
        "team_eval.html",
        teams=teams,
        cases=cases,
        blocks=blocks
    )

@team_eval_bp.route("/save", methods=["POST"])
@login_required
def save():
    block_id = request.form.get("block_id", type=int)
    team_id = request.form.get("team_id", type=int)
    case_id = request.form.get("case_id", type=int)
    points = request.form.get("points", type=float)

    # # Безопасность: проверяем, что кейс принадлежит команде
    # if case_id and team_id:
    #     case = db.session.get(Case, case_id)
    #     if not case or case.team_id != team_id:
    #         flash("Кейс не принадлежит выбранной команде", "error")
    #         return redirect(url_for("team_eval.form"))

    te = TeamEvaluation(block_id=block_id, team_id=team_id, case_id=case_id, points=points)
    db.session.add(te)
    db.session.commit()
    flash("Командная оценка сохранена", "success")
    return redirect(url_for("team_eval.form"))
