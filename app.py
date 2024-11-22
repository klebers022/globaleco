from flask import Flask, request, jsonify
from flask_cors import CORS
from banco import (
    insere_usuario,
    recupera_usuario_por_email,
    recupera_veiculos_disponiveis,
    insere_agendamento,
    recupera_agendamentos_por_usuario,
    remover_agendamento,
)

app = Flask(__name__)

# Ativar o CORS para todas as rotas
CORS(app)

# Rota para cadastrar usuário
@app.route('/usuario', methods=['POST'])
def cadastrar_usuario():
    try:
        dados = request.json
        campos_obrigatorios = ["nome", "email", "senha", "cpf", "dt_nascimento", "estado", "numero_cnh"]
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                return jsonify({"status": "erro", "mensagem": f"Campo '{campo}' é obrigatório"}), 400

        insere_usuario(dados)
        return jsonify({"status": "sucesso", "mensagem": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": "Erro ao cadastrar usuário"}), 500


# Rota para login
@app.route('/login', methods=['POST'])
def login_usuario():
    try:
        dados = request.json
        email = dados.get("email")
        senha = dados.get("senha")

        if not email or not senha:
            return jsonify({"status": "erro", "mensagem": "Email e senha são obrigatórios"}), 400

        usuario = recupera_usuario_por_email(email)
        if usuario and usuario[3] == senha:
            return jsonify({
                "status": "sucesso",
                "usuario": {"id": usuario[0], "nome": usuario[1], "email": usuario[2]}
            }), 200
        else:
            return jsonify({"status": "erro", "mensagem": "Email ou senha inválidos"}), 401
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": "Erro ao realizar login"}), 500


# Rota para listar veículos disponíveis
@app.route('/veiculos/disponiveis', methods=['GET'])
def listar_veiculos_disponiveis():
    try:
        veiculos = recupera_veiculos_disponiveis()
        if not veiculos:
            return jsonify({"status": "sucesso", "mensagem": "Nenhum veículo disponível no momento"}), 200

        return jsonify({
            "status": "sucesso",
            "veiculos": [
                {"id": veiculo[0], "modelo": veiculo[1], "cor": veiculo[2], "placa": veiculo[3], "ponto": veiculo[4]}
                for veiculo in veiculos
            ]
        }), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": "Erro ao listar veículos"}), 500


# Rota para agendar veículo
@app.route('/agendamento', methods=['POST'])
def agendar_veiculo():
    try:
        dados = request.json
        id_usuario = dados.get("id_usuario")
        id_veiculo = dados.get("id_veiculo")

        if not id_usuario or not id_veiculo:
            return jsonify({"status": "erro", "mensagem": "Usuário e veículo são obrigatórios"}), 400

        agendamentos = recupera_agendamentos_por_usuario(id_usuario)
        if agendamentos:
            return jsonify({"status": "erro", "mensagem": "Usuário já possui um veículo agendado"}), 400

        insere_agendamento({"id_usuario": id_usuario, "id_veiculo": id_veiculo})
        return jsonify({"status": "sucesso", "mensagem": "Veículo agendado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": "Erro ao agendar veículo"}), 500


# Rota para devolver veículo
@app.route('/devolucao', methods=['DELETE'])
def devolver_veiculo():
    try:
        dados = request.json
        id_veiculo = dados.get("id_veiculo")
        id_usuario = dados.get("id_usuario")

        if not id_veiculo or not id_usuario:
            return jsonify({"status": "erro", "mensagem": "Usuário e veículo são obrigatórios"}), 400

        agendamentos = recupera_agendamentos_por_usuario(id_usuario)
        veiculo_agendado = next((a for a in agendamentos if a[0] == id_veiculo), None)

        if veiculo_agendado:
            remover_agendamento(id_veiculo)
            return jsonify({"status": "sucesso", "mensagem": "Veículo devolvido com sucesso!"}), 200
        else:
            return jsonify({"status": "erro", "mensagem": "Veículo não encontrado ou não pertence ao usuário"}), 400
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": "Erro ao devolver veículo"}), 500


# Endpoint raiz para verificar o status da API
@app.route('/', methods=['GET'])
def status():
    return jsonify({"status": "sucesso", "mensagem": "API está rodando"}), 200


# Tratamento global de erros
@app.errorhandler(500)
def erro_interno(e):
    return jsonify({"status": "erro", "mensagem": "Erro interno no servidor"}), 500


# Inicializar o servidor
if __name__ == '__main__':
    app.run(debug=True)
