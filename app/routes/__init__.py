from app.routes.auth import auth_bp

def registerBlueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')