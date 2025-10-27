from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from extensions import db
from models.Carrinho import CarrinhoModel


ns = Namespace('carrinho', description='Operações relacionadas ao carrinho')

carrinho_model = ns.model('Carrinho', {
    'id': fields.Integer(readonly=True, description='O identificador único do carrinho'),
    'usuarioId': fields.Integer(required=True, description='A chave estrangeira do usuário'),
    'preco': fields.Float(required=True, description='O preço total dos itens no carrinho')
})

@ns.route('/<int:id>')
class Carrinho(Resource):
    @jwt_required()
    def get(self, id):
        carrinho = CarrinhoModel.query.filter_by(usuarioId=id).first_or_404()

        return carrinho.json()

    @jwt_required()
    def put(self, id):
        carrinho = CarrinhoModel.query.filter_by(usuarioId=id).first_or_404()
        data = request.get_json()

        carrinho.usuarioId = data.get('usuarioId', carrinho.usuarioId)
        carrinho.preco = data.get('preco', carrinho.preco)

        db.session.commit()
        
        return carrinho.json(), 201