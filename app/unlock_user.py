# unlock_user.py
from app import app, db
from app.models import User

with app.app_context():
    email = input("Email para desbloquear: ").strip().lower()
    user = User.query.filter_by(email=email).first()
    if not user:
        print("Usuário não encontrado.")
    else:
        user.login_attempts = 0
        user.blocked_until = None
        db.session.commit()
        print("Usuário desbloqueado:", email)
