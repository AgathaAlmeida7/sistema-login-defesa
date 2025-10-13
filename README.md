# Sistema Login Defesa 🔒

## Descrição
O **Sistema Login Defesa** é um sistema de autenticação seguro, desenvolvido em Flask, com funcionalidades de **login e cadastro de usuários**. O objetivo é fornecer **uma aplicação de login protegida**, utilizando técnicas de validação, hashing de senhas e proteção contra ataques comuns, como CSRF e brute force.

---

## Funcionalidades
- Cadastro de usuário com validação de e-mail e senha segura.
- Login com verificação de senha e bloqueio após múltiplas tentativas.
- Proteção CSRF em formulários.
- Hash seguro das senhas com `generate_password_hash`.
- Limite de requisições por IP para proteção contra ataques de força bruta.
- Sistema de mensagens flash para feedback do usuário.
- Sessões de usuário com expiração automática.
- Estrutura de templates para login, registro e dashboard.

---

## Tecnologias Utilizadas

**Backend:** Flask (Python)  
**Banco de dados:** SQLite (local, leve e simples para testes)  
**Segurança:**
- Flask-WTF para proteção CSRF
- Werkzeug Security (`generate_password_hash` e `check_password_hash`) para senhas
- Flask-Limiter para limitar tentativas de login
- Configurações de cookies seguros (HttpOnly, SameSite, Secure)  

**Front-end:** HTML, CSS, JS (templates Jinja2)  
**Controle de versão:** Git + GitHub  

---

## Estrutura do Projeto
app/
│
├─ templates/
│ ├─ login.html
│ ├─ register.html
│ └─ dashboard.html
├─ static/
│ ├─ css/
│ └─ js/
├─ init.py
├─ routes.py
├─ forms.py
├─ models.py
└─ run.py

## como rodar o projeto
1. Clone o repositório:  
```bash
git clone https://github.com/AgathaAlmeida7/sistema-login-defesa.git
2.Entre na pasta do projeto:
cd sistema-login-defesa

3.crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

4.Instale as dependencias
pip install -r requirements.txt

5.Rode o projeto
python run.py

6.Abra o navegador
http://127.0.0.1:5000

## Objetivo do projeto
O projeto serve como base para um sistema de login seguro, com boas práticas de autenticação, proteção de dados do usuário e monitoramento de tentativas de login.

## Contato
Desenvolvido por Agatha Almeida.






