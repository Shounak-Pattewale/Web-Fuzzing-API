# Import create_app
from app import create_app

# Create the Flask application instance by calling the create_app() function
app = create_app()

# If this script is run directly
if __name__ == "__main__":
    # Run the Flask app with debug mode enabled
    # Debug mode will auto-reload the server on code changes and show detailed error messages
    app.run(debug=True)
