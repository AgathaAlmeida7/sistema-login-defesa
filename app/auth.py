#passos 

#ter uma pagina de registro(para criar usuarios);
#pagina de login (para acessar o sistema);
#começar a conectar o front(html) com back(flask);
#preparar a estrutura para autenticação e criptografia;

import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
