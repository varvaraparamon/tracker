from app import create_app
from models import db, User, Team, Case, Participant
import click

app = create_app()

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        click.echo("DB initialized")

@app.cli.command("create-user")
@click.argument("login")
@click.argument("password")
def create_user(login, password):
    with app.app_context():
        u = User(login=login)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        click.echo(f"User {login} created")

@app.cli.command("demo-data")
def demo_data():
    with app.app_context():
        # Teams
        t1 = Team(name="Команда A")
        t2 = Team(name="Команда B")
        db.session.add_all([t1, t2]); db.session.flush()

        # Cases bound to teams
        c1 = Case(title="Кейс A1", team_id=t1.id)
        c2 = Case(title="Кейс A2", team_id=t1.id)
        c3 = Case(title="Кейс B1", team_id=t2.id)
        db.session.add_all([c1, c2, c3]); db.session.flush()

        # Participants bound to teams
        p1 = Participant(full_name="Иванов Иван", team_id=t1.id)
        p2 = Participant(full_name="Петров Петр", team_id=t1.id)
        p3 = Participant(full_name="Сидорова Анна", team_id=t2.id)
        db.session.add_all([p1, p2, p3])

        db.session.commit()
        click.echo("Demo data inserted")
