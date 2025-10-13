from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager, limiter, csrf
from app.models import User
from app.forms import LoginForm, RegisterForm
import logging

# Configuração de logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

MAX_ATTEMPTS = 3
LOCK_MINUTES = 15  # Bloqueio por 15 minutos

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Login com limite de tentativas e proteção via Flask-Limiter
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per 15 minutes")  # Limite por IP
def login():
    form = LoginForm()
    if form.validate_on_submit():  # CSRF + validação de formulário
        email = form.username.data.strip().lower()
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Usuário não encontrado!", "error")
            logging.warning(f'Falha login: {email} - Usuário não encontrado - {datetime.utcnow()}')
            return redirect(url_for('login'))

        # Verifica bloqueio temporário
        if user.blocked_until and datetime.utcnow() < user.blocked_until:
            remaining = user.blocked_until - datetime.utcnow()
            flash(f"Conta bloqueada temporariamente. Tente novamente em {int(remaining.total_seconds()//60)+1} minutos.", "error")
            logging.warning(f'Falha login: {email} - Conta bloqueada - {datetime.utcnow()}')
            return redirect(url_for('login'))

        # Verifica limite de tentativas
        if user.login_attempts >= MAX_ATTEMPTS:
            user.blocked_until = datetime.utcnow() + timedelta(minutes=LOCK_MINUTES)
            db.session.commit()
            flash("Usuário bloqueado por muitas tentativas incorretas!", "error")
            logging.warning(f'Falha login: {email} - Bloqueado após {MAX_ATTEMPTS} tentativas - {datetime.utcnow()}')
            return redirect(url_for('login'))

        # Verifica senha
        if user.check_password(password):
            user.login_attempts = 0
            user.blocked_until = None
            db.session.commit()
            login_user(user, duration=timedelta(minutes=30))  # Expira sessão após 30 min
            flash("Login realizado com sucesso!", "success")
            logging.info(f'Sucesso login: {email} - {datetime.utcnow()}')
            return redirect(url_for('dashboard'))
        else:
            user.login_attempts += 1
            db.session.commit()
            flash(f"Senha incorreta! Tentativa {user.login_attempts}/{MAX_ATTEMPTS}", "error")
            logging.warning(f'Falha login: {email} - Senha incorreta - Tentativa {user.login_attempts} - {datetime.utcnow()}')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

# Registro de usuários
@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per 15 minutes")  # Limite por IP
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.username.data.strip().lower()
        password = form.password.data

        # Verifica se o usuário já existe
        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado.", "error")
            logging.warning(f'Tentativa registro: {email} - E-mail já cadastrado - {datetime.utcnow()}')
            return redirect(url_for('register'))

        # Cria novo usuário
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Cadastro realizado com sucesso. Faça login.", "success")
        logging.info(f'Cadastro realizado: {email} - {datetime.utcnow()}')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu da conta.", "success")
    logging.info(f'Logout: {current_user.email} - {datetime.utcnow()}')
    return redirect(url_for('login'))

