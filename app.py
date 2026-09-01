"""Entry point for running the AstraHaven Flask application locally."""

from AstraHaven import create_app

# Build the app once so the local server and tests can share the same config.
app = create_app()


if __name__ == "__main__":
    """Start the development server when this file is executed directly."""
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
