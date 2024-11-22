import oracledb

def get_conexao():
    return oracledb.connect(user="rm557887", password="210106", dsn="oracle.fiap.com.br/orcl")


# Funções de usuário
def insere_usuario(usuario: dict):
    sql = """
    INSERT INTO tbj_usuario (nome, email, senha, cpf, dt_nascimento, estado, numero_cnh)
    VALUES (:nome, :email, :senha, :cpf, TO_DATE(:dt_nascimento, 'YYYY-MM-DD'), :estado, :numero_cnh)
    """
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, usuario)
        con.commit()


def recupera_usuario_por_email(email: str):
    sql = "SELECT id, nome, email, senha, cpf, dt_nascimento, estado, numero_cnh FROM tbj_usuario WHERE email = :email"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"email": email})
            return cur.fetchone()


# Funções de veículo
def insere_veiculo(veiculo: dict):
    sql = """
    INSERT INTO tbj_veiculo (modelo, cor, placa, ponto)
    VALUES (:modelo, :cor, :placa, :ponto)
    """
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, veiculo)
        con.commit()


def recupera_veiculos_disponiveis():
    sql = """
    SELECT v.id, v.modelo, v.cor, v.placa, v.ponto
    FROM tbj_veiculo v
    WHERE NOT EXISTS (
        SELECT 1 FROM tbj_agendamento a WHERE a.id_veiculo = v.id
    )
    """
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


# Funções de pontos de aluguel
def insere_ponto_aluguel(ponto: dict):
    sql = """
    INSERT INTO tbj_ponto_aluguel (nome, endereco)
    VALUES (:nome, :endereco)
    """
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, ponto)
        con.commit()


def recupera_pontos():
    sql = "SELECT id, nome, endereco FROM tbj_ponto_aluguel"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


# Funções de agendamento
def insere_agendamento(agendamento: dict):
    sql = """
    INSERT INTO tbj_agendamento (id_usuario, id_veiculo, data_agendamento)
    VALUES (:id_usuario, :id_veiculo, SYSTIMESTAMP)
    """
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, agendamento)
        con.commit()


def recupera_agendamentos_por_usuario(id_usuario: int):
    sql = """
    SELECT a.id, a.data_agendamento, v.modelo, v.cor, v.placa
    FROM tbj_agendamento a
    JOIN tbj_veiculo v ON a.id_veiculo = v.id
    WHERE a.id_usuario = :id_usuario
    """
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"id_usuario": id_usuario})
            return cur.fetchall()


def remover_agendamento(id_veiculo: int):
    sql = "DELETE FROM tbj_agendamento WHERE id_veiculo = :id_veiculo"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"id_veiculo": id_veiculo})
        con.commit()
