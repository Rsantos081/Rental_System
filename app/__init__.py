import os 
from dotenv import load_dotenv
from flask import Flask
from app.extensions import db, login_manager

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = (f'mysql+pymysql://{os.getenv('DB_USER')}:'
    f'{os.getenv('DB_PASSWORD')}@'
    f'{os.getenv('DB_HOST')}:'
    f'{os.getenv('DB_PORT')}/'
    f'{os.getenv('DB_NAME')}'
)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    from app.src import marcas_bp
    from app.src import inventario_bp
    from app.src import cliente_bp
    from app.src import pagamentos_bp
    
    app.register_blueprint(marcas_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(pagamentos_bp)
    
    db.init_app(app)
    login_manager.init_app(app)
    return app