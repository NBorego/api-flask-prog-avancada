from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Produto

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    senha_hash = generate_password_hash(data['senha'])
    novo = Usuario(nome=data['nome'], email=data['email'], senha=senha_hash)
    db.session.add(novo)
    db.session.commit()
    return jsonify({"msg": "Usuário criado!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = Usuario.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.senha, data['senha']):
        return jsonify({"msg": "Login bem-sucedido!"})
    return jsonify({"msg": "Credenciais inválidas"}), 401

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios])

@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    user = Usuario.query.get_or_404(id)
    return jsonify({"id": user.id, "nome": user.nome, "email": user.email})

# ROTAS PRODUTOS
@app.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.json
    novo = Produto(nome=data['nome'], preco=data['preco'])
    db.session.add(novo)
    db.session.commit()
    return jsonify({"msg": "Produto criado!"})

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{"id": p.id, "nome": p.nome, "preco": p.preco} for p in produtos])

@app.route('/produtos/<int:id>', methods=['GET'])
def get_produto(id):
    p = Produto.query.get_or_404(id)
    return jsonify({"id": p.id, "nome": p.nome, "preco": p.preco})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
