from app import db, app
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)

    # Listar tabelas existentes
    tables = inspector.get_table_names()
    print("Tabelas no banco:")
    if tables:
        for table in tables:
            print(f"- {table}")
    else:
        print("Nenhuma tabela encontrada.")

    # Verificar e detalhar a tabela 'users'
    if 'users' in tables:
        print("\nColunas da tabela 'users':")
        for column in inspector.get_columns('users'):
            print(f"{column['name']} - {column['type']} - nullable: {column['nullable']} - default: {column['default']}")
    else:
        print("\nTabela 'users' não encontrada. Você precisará criar as tabelas com db.create_all() antes de usar o sistema.")
