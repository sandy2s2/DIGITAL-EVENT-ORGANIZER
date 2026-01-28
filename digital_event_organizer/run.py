"""
Digital Event Organizer - Main Application Entry Point
Run this file to start the Flask application
"""

from app import create_app

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode for development
    # Set debug=False for production
    app.run(
        host='0.0.0.0',  # Makes server accessible externally
        port=5000,        # Default Flask port
        debug=True        # Enable debug mode (auto-reload on code changes)
    )
