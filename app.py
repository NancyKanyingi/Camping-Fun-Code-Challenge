from flask import Flask, jsonify
from .extensions import db, migrate
import os

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:123@localhost:5432/access_camp'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so SQLAlchemy knows them
    from .models import Camper, Activity, Signup  # noqa: E402

    # Register routes (make sure routes.py exists in the same folder)
    from .routes import bp as api_bp  # noqa: E402
    app.register_blueprint(api_bp)

    # Simple root endpoint
    @app.get('/')
    def index():
        return jsonify({"message": "Welcome to the Access Camp API up. Endpoints: /campers, /activities, /signups"})

    return app


if __name__ == '__main__':
    app = create_app()

    # Import models again to ensure tables are created

    # Create all tables in the database (no CLI needed)
    with app.app_context():
        db.create_all()

    # Run the server
    app.run(host='0.0.0.0', port=5555, debug=True)
