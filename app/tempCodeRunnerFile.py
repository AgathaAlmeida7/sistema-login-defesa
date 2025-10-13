from flask import Flask

app = Flask(__name__)

# importar as rotas para que Flask as conheça
from app import routes

if __name__ == "__main__":
    app.run(debug=True)