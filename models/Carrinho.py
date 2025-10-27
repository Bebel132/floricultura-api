from sqlalchemy import Numeric
from extensions import db

class CarrinhoModel(db.Model):
    __tablename__ = 'carrinhos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuarioId = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    preco = db.Column(Numeric(10, 2), nullable=True)

    def json(self):
        return {
            'id': self.id,
            'usuarioId': self.usuarioId,
            'preco': float(self.preco) if self.preco is not None else None
        }