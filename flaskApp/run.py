"""This allows Gunicorn to serve the app in production"""

import create_app

app = create_app()