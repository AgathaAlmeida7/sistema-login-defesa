import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa Flask
app = Flask(__name__)

# Configurações de segurança
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma_chave_muito_forte_e_aleatoria')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True       # Cookies só via HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True     # Não acessível via JS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # Proteção extra CSRF
app.config['REMEMBER_COOKIE_DURATION'] = 1800   # Expira 30 minutos
app.config['WTF_CSRF_TIME_LIMIT'] = None        # Duração do token CSRF (opcional)

# Inicializa extensões
db = SQLAlchemy(app)
csrf = CSRFProtect(app)  # Proteção CSRF
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Limiter configurado globalmente (por IP)
limiter = Limiter(
    key_func=get_remote_address,  # define função de key
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Importar rotas e models após inicializar extensões
from app import routes, models  # noqa: E402,F401

