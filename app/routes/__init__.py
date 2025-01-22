from app.routes.auth import auth_bp
from app.routes.event import event_bp
from app.routes.find import find_bp

def registerBlueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(event_bp, url_prefix='/event')
    app.register_blueprint(find_bp, url_prefix='/find')