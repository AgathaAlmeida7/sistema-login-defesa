# create_user.py
import getpass
from app import app, db
from app.models import User

with app.app_context():
    email = input("Email (ex: teste@ex.com): ").strip().lower()
    if User.query.filter_by(email=email).first():
        print("Usuário já existe.")
    else:
        pw = getpass.getpass("Senha: ")
        user = User(email=email)
        user.set_password(pw)
        db.session.add(user)
        db.session.commit()
        print("Usuário criado:", email)
