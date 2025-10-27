from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from extensions import db
from models.Carrinho import CarrinhoModel
from models.Usuario import UsuarioModel

ns = Namespace("auth", description="Operações de autenticação")

# Modelos para Swagger
cadastro_model = ns.model("Register", {
    "apelido": fields.String(required=True, description="Nome de usuário"),
    "email": fields.String(required=True, description="E-mail"),
    "senha": fields.String(required=True, description="Senha"),
})

login_model = ns.model("Login", {
    "email": fields.String(required=True, description="E-mail"),
    "senha": fields.String(required=True, description="Senha"),
})


@ns.route("/cadastro")
class Cadastro(Resource):
    @ns.expect(cadastro_model)
    def post(self):
        dados = request.get_json()
        apelido = dados.get("apelido")
        email = dados.get("email")
        senha = dados.get("senha")

        if UsuarioModel.query.filter((UsuarioModel.apelido == apelido) | (UsuarioModel.email == email)).first():
            return {"message": "Usuário ou email já cadastrados"}, 400

        usuario = UsuarioModel(
            apelido=apelido,
            email=email,
            senhaHash=generate_password_hash(senha)
        )
        
        db.session.add(usuario)
        db.session.commit()

        carrinho = CarrinhoModel(
            usuarioId=usuario.id
        )

        db.session.add(carrinho)
        db.session.commit()

        return usuario.json(), 201


@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        dados = request.get_json()
        email = dados.get("email")
        senha = dados.get("senha")

        user = UsuarioModel.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.senhaHash, senha):
            return {"message": "Credenciais inválidas"}, 401

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.json()
        }, 200


@ns.route("/refresh")
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {"access_token": new_access_token}, 200

@ns.route("/eu")
class UserProfile(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = UsuarioModel.query.get(current_user_id)
        if not user:
            return {"message": "Usuário não encontrado"}, 404
        return user.json(), 200