from flask import Flask

def create_app():
    app = Flask(__name__, 
                template_folder='../../templates',
                static_folder='../../static')
    
    # Configuration de l'application
    app.config['SECRET_KEY'] = 'votre_clé_secrète_ici'
    
    # Importer les routes
    from src.webapp.routes import main_bp
    
    # Enregistrer les blueprints
    app.register_blueprint(main_bp)
    
    return app