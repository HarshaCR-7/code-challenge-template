from app import create_app, db

def initialize(app):
    """
    Initializes the database and starts the Flask app in debug mode.
    """
    with app.app_context():
        db.create_all()  # Creates all the database tables from models
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    app = create_app()  # Create the Flask app instance
    # Initialize the database and then start the app
    initialize(app)