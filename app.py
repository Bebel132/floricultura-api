from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api
from extensions import db
from flask_jwt_extended import JWTManager
from resourses.Produtos import ns as ns_produtos
from resourses.Auth import ns as ns_auth
from resourses.CarrinhoItem import ns as ns_carrinhoItem
from resourses.Carrinho import ns as ns_carrinho


app = Flask(__name__)


CORS(
    app,
    resources={r"/*": {"origins": ["https://bebel132.github.io"]}},
    # supports_credentials=True,  # só se você usa cookies/sessions; veja nota abaixo
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type", "Authorization"]
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "supersegredolalalala"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)


db.init_app(app)
migrate = Migrate(app, db)

authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}

api = Api(
    app, 
    doc='/docs',
    authorizations=authorizations, 
    security="Bearer Auth"
)

api.title = "Floricultura API"
jwt = JWTManager(app)

api.add_namespace(ns_produtos)
api.add_namespace(ns_auth)
api.add_namespace(ns_carrinhoItem)
api.add_namespace(ns_carrinho)

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug=True)