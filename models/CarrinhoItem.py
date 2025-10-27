from extensions import db

class CarrinhoItemModel(db.Model):
    __tablename__ = 'carrinhoItem'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produtoId = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False)
    carrinhoId = db.Column(db.Integer, db.ForeignKey('carrinhos.id', ondelete='CASCADE'), nullable=False)
    quantidadeProdutos = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'produtoId': self.produtoId,
            'carrinhoId': self.carrinhoId,
            'quantidadeProdutos': self.quantidadeProdutos
        }