from flask import Flask
from routes.alerts import alerts_bp

app = Flask(__name__)

# Register routes
app.register_blueprint(alerts_bp)

if __name__ == "__main__":
    app.run(debug=True)
