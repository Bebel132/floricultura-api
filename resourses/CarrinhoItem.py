from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from extensions import db
from models.Carrinho import CarrinhoModel
from models.CarrinhoItem import CarrinhoItemModel
from models.Produtos import ProdutoModel


ns = Namespace('carrinhoItem', description='Operações relacionadas ao relacionamento Carrinho - Produto')

carrinhoItem_model = ns.model('CarrinhoItem', {
    'id': fields.Integer(readonly=True, description='O identificador único do item que está no carrinho'),
    'produtoId': fields.Integer(required=True, description='A chave estrangeira do produto'),
    'carrinhoId': fields.Integer(required=True, description='A chave estrangeira do carrinho'),
    'quantidadeProdutos': fields.Integer(required=True, description='A quantidade de produtos que tem no carrinho')
})

@ns.route('/<int:id>')
class CarrinhoItems(Resource):
    @jwt_required()
    def get(self, id):
        return [
            item.json() for item in CarrinhoItemModel.query.filter_by(carrinhoId=id).all()
        ]
    
    @ns.expect(ns.model('UpdateQuantidade', {'quantidadeProdutos': fields.Integer(required=True, description='A quantidade de produtos que tem no carrinho')}))
    @jwt_required()
    def put(self, id):
        item = CarrinhoItemModel.query.get_or_404(id)
        data = request.get_json()

        item.quantidadeProdutos = data.get('quantidadeProdutos', item.quantidadeProdutos)

        carrinho = CarrinhoModel.query.get(item.carrinhoId)
        produto = ProdutoModel.query.get(item.produtoId)

        carrinho.preco = produto.preco * item.quantidadeProdutos

        db.session.commit()
        return item.json(), 201
    
    @jwt_required()
    def delete(self, id):
        item = CarrinhoItemModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()

        return 204

@ns.route('/')
class CarrinhoItem(Resource):
    @ns.expect(carrinhoItem_model)
    @jwt_required()
    def post(self):
        data = request.get_json()

        novo_item = CarrinhoItemModel(
            produtoId=data['produtoId'],
            carrinhoId=data['carrinhoId'],
            quantidadeProdutos=data['quantidadeProdutos'],
        )

        db.session.add(novo_item)
        db.session.commit()

        carrinho = CarrinhoModel.query.get(data['carrinhoId'])
        produto = ProdutoModel.query.get(data['produtoId'])

        carrinho.preco = produto.preco * novo_item.quantidadeProdutos
        
        db.session.commit()
        return novo_item.json(), 201