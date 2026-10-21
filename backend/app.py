from flask import Flask
from flask_cors import CORS

from routes.auth import auth_bp
from routes.finance import finance_bp
from routes.groups import groups_bp
from routes.tools import tools_bp

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

app.register_blueprint(auth_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(groups_bp)
app.register_blueprint(tools_bp)


@app.get("/")
def home():
    return {"message": "Financial Manager API is running"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
