from extensions import db

class UsuarioModel(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    apelido = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senhaHash = db.Column(db.String(128), nullable=False)

    carrinho = db.relationship('CarrinhoModel', backref='usuario', lazy=True, cascade="all, delete-orphan")

    def json(self):
        return {
            'id': self.id,
            'apelido': self.apelido,
            'email': self.email
        }