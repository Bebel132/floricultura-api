from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from extensions import db
from models.Produtos import ProdutoModel


ns = Namespace('produtos', description='Operações relacionadas a produtos')

upload_parser = ns.parser()
upload_parser.add_argument(
    'file',
    type='file',
    location='files',
    required=True
)

produto_model = ns.model('Produto', {
    'id': fields.Integer(readonly=True, description='O identificador único do produto'),
    'titulo': fields.String(required=True, description='O título do produto'),
    'descricao': fields.String(required=True, description='A descrição do produto'),
    'categoria': fields.String(required=True, description='A categoria do produto'),
    'preco': fields.Float(required=True, description='O preço do produto')
})

@ns.route('/')
class Produtos(Resource):
    def get(self):
        return [
            produto.json() for produto in ProdutoModel.query.all()
        ]
    
    @ns.expect(produto_model)
    @jwt_required()
    def post(self):
        data = request.get_json()

        novo_produto = ProdutoModel(
            titulo=data['titulo'],
            descricao=data['descricao'],
            categoria=data['categoria'],
            preco=data['preco'],
        )

        db.session.add(novo_produto)
        db.session.commit()
        return novo_produto.json(), 201
    
    
@ns.route('/<int:id>/upload')
class ImagemUpload(Resource):
    @ns.expect(upload_parser)
    @jwt_required()
    def post(self, id):
        produto = ProdutoModel.query.get_or_404(id)

        arquivo = request.files['file']

        file_bytes = arquivo.read()
        produto.imagem = file_bytes

        db.session.commit()

        return '', 200


@ns.route('/<int:id>')
class Produto(Resource):
    @jwt_required()
    def delete(self, id):
        produto = ProdutoModel.query.get_or_404(id)

        db.session.delete(produto)
        db.session.commit()

        return '', 204
    
    @ns.expect(produto_model)
    @jwt_required()
    def put(self, id):
        produto = ProdutoModel.query.get_or_404(id)
        data = request.get_json()

        produto.titulo = data['titulo']
        produto.descricao = data['descricao']
        produto.categoria = data['categoria']
        produto.preco = data['preco']

        db.session.commit()

        return produto.json(), 200
