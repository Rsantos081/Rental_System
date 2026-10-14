import os 
from dotenv import load_dotenv
from flask import Flask
from app.extensions import db, login_manager
from flasgger import Swagger

load_dotenv()

def create_app():
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # TRACK_MODIFICATIONS serve para desativar o envio de alertas e economia de memoria e desempenho da CPU, boas praticas da biblioteca
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    app.config['SWAGGER'] = {
    'title': 'Rental System API',
    'uiversion': 3,
    'openapi': '3.0.3', # Versão Atualizado do Swagger para o Flasger
 } 
    swagger = Swagger(app, template_file=os.path.join(base_dir, 'swagger.yaml'))

    
    from app.src import marcas_bp
    from app.src import inventario_bp
    from app.src import cliente_bp
    from app.src import pagamentos_bp
    from app.src import locacao_bp
    from app.src import routes
    from app.auth import auth_bp
    
    app.register_blueprint(marcas_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(pagamentos_bp)
    app.register_blueprint(locacao_bp)
    app.register_blueprint(auth_bp)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        db.create_all()
        
    return app