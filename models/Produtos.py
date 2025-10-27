import base64

from sqlalchemy import Numeric
from extensions import db

class ProdutoModel(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    preco = db.Column(Numeric(10, 2), nullable=False)
    imagem = db.Column(db.LargeBinary, nullable=True)

    def json(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'preco': float(self.preco) if self.preco is not None else None,
            'imagem': base64.b64encode(self.imagem).decode('utf-8') if self.imagem else None
        }