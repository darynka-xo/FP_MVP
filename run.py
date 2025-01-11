from datetime import timedelta
from app import create_app
from flask_session import Session

app = create_app()

# Explicit session config
app.config.update(
    SESSION_COOKIE_SAMESITE="None",  # Required for cross-origin
    SESSION_COOKIE_SECURE=False,    # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
    SESSION_REFRESH_EACH_REQUEST=True,
    SESSION_TYPE='filesystem'
)

# Initialize Session
Session(app)

if __name__ == '__main__':
    app.run(debug=True)