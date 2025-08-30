from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Team, Case, Participant, IndividualEvaluation, Block

indiv_eval_bp = Blueprint("indiv_eval", __name__, template_folder="../templates")

@indiv_eval_bp.route("/", methods=["GET"])
@login_required
def form():
    teams = Team.query.order_by(Team.name).all()
    cases = Case.query.order_by(Case.title).all()
    participants = Participant.query.order_by(Participant.full_name).all()
    blocks = Block.query.order_by(Block.name).all()
    return render_template(
        "indiv_eval.html",
        teams=teams,
        cases=cases,
        participants=participants,
        blocks=blocks
    )

@indiv_eval_bp.route("/save", methods=["POST"])
@login_required
def save():
    block_id = request.form.get("block_id", type=int)
    team_id = request.form.get("team_id", type=int)
    case_id = request.form.get("case_id", type=int)
    participant_id = request.form.get("participant_id", type=int)
    score = request.form.get("score", type=float)
    comment = request.form.get("comment")

    # # Проверки связей
    # ok = True
    # case = db.session.get(Case, case_id) if case_id else None
    # if not case or case.team_id != team_id:
    #     ok = False
    # participant = db.session.get(Participant, participant_id) if participant_id else None
    # if not participant or participant.team_id != team_id:
    #     ok = False

    # if not ok:
    #     flash("Неверная связка команда/кейс/участник", "error")
    #     return redirect(url_for("indiv_eval.form"))

    ie = IndividualEvaluation(
        block_id=block_id, team_id=team_id, case_id=case_id,
        participant_id=participant_id, score=score, comment=comment
    )
    db.session.add(ie)
    db.session.commit()
    flash("Индивидуальная оценка сохранена", "success")
    return redirect(url_for("indiv_eval.form"))
