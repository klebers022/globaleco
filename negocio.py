import datetime
from banco import (
    insere_usuario,
    recupera_usuario_por_email,
    insere_veiculo,
    recupera_veiculos_disponiveis,
    insere_ponto_aluguel,
    recupera_pontos,
    insere_agendamento,
    recupera_agendamentos_por_usuario,
    remover_agendamento,
)


usuario_logado = None


# Função para cadastro de usuários
def cadastrar_usuario():
    print("\n=== Cadastro de Usuário ===")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    cpf = input("CPF: ")
    dt_nascimento = input("Data de Nascimento (AAAA-MM-DD): ")
    estado = input("Estado: ")
    numero_cnh = input("Número da CNH: ")

    usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "cpf": cpf,
        "dt_nascimento": dt_nascimento,
        "estado": estado,
        "numero_cnh": numero_cnh,
    }
    insere_usuario(usuario)
    print("\nUsuário cadastrado com sucesso!")


# Função para login de usuários
def login_usuario():
    global usuario_logado
    print("\n=== Login ===")
    email = input("Email: ")
    senha = input("Senha: ")

    usuario = recupera_usuario_por_email(email)

    if usuario and usuario[3] == senha:  # Índice 3 é a senha no retorno
        usuario_logado = {
            "id": usuario[0],
            "nome": usuario[1],
            "email": usuario[2],
        }
        print(f"\nBem-vindo(a), {usuario_logado['nome']}!")
    else:
        print("\nEmail ou senha inválidos.")


# Função para verificar se o usuário está logado
def verificar_login():
    if not usuario_logado:
        print("\nVocê precisa estar logado para acessar esta funcionalidade.")
        return False
    return True


# Função para listar veículos disponíveis
def listar_veiculos_disponiveis():
    if not verificar_login():
        return

    print("\n=== Veículos Disponíveis para Agendamento ===")
    veiculos = recupera_veiculos_disponiveis()
    if not veiculos:
        print("Nenhum veículo disponível no momento.")
        return

    for veiculo in veiculos:
        print(f"[ID: {veiculo[0]}] {veiculo[1]} - {veiculo[2]} - {veiculo[3]} - {veiculo[4]}")


# Função para listar pontos de aluguel
def listar_pontos():
    if not verificar_login():
        return

    print("\n=== Pontos de Aluguel ===")
    pontos = recupera_pontos()
    for ponto in pontos:
        print(f"[ID: {ponto[0]}] {ponto[1]} - {ponto[2]}")


# Função para agendar veículo
def agendar_veiculo():
    if not verificar_login():
        return

    # Verificar se o usuário já tem um veículo agendado
    agendamentos = recupera_agendamentos_por_usuario(usuario_logado["id"])
    if agendamentos:
        print("\nVocê já possui um veículo agendado. Não é possível agendar outro.")
        return

    listar_veiculos_disponiveis()
    veiculo_id = int(input("\nDigite o ID do veículo que deseja agendar: "))

    veiculo = next((v for v in recupera_veiculos_disponiveis() if v[0] == veiculo_id), None)

    if veiculo:
        agendamento = {
            "id_usuario": usuario_logado["id"],
            "id_veiculo": veiculo_id,
        }
        insere_agendamento(agendamento)
        print(f"\nVeículo {veiculo[1]} agendado com sucesso.")
    else:
        print("\nVeículo não encontrado ou já está agendado.")


# Função para desbloquear veículo
def desbloquear_veiculo():
    if not verificar_login():
        return

    agendamentos = recupera_agendamentos_por_usuario(usuario_logado["id"])
    if not agendamentos:
        print("\nVocê não possui nenhum veículo agendado para desbloquear.")
        return

    print("\n=== Veículos Agendados ===")
    for agendamento in agendamentos:
        print(f"[ID: {agendamento[0]}] {agendamento[2]} - {agendamento[3]} - {agendamento[4]}")

    veiculo_id = int(input("\nDigite o ID do veículo que deseja desbloquear: "))
    veiculo_agendado = next((a for a in agendamentos if a[0] == veiculo_id), None)

    if veiculo_agendado:
        print(f"\nO veículo {veiculo_agendado[2]} foi desbloqueado com sucesso!")
    else:
        print("\nVocê não tem permissão para desbloquear este veículo.")


# Função para devolver veículo
def devolver_veiculo():
    if not verificar_login():
        return

    agendamentos = recupera_agendamentos_por_usuario(usuario_logado["id"])
    if not agendamentos:
        print("\nVocê não possui nenhum veículo agendado para devolver.")
        return

    print("\n=== Veículos Agendados ===")
    for agendamento in agendamentos:
        print(f"[ID: {agendamento[0]}] {agendamento[2]} - {agendamento[3]} - {agendamento[4]}")

    veiculo_id = int(input("\nDigite o ID do veículo que deseja devolver: "))
    veiculo_agendado = next((a for a in agendamentos if a[0] == veiculo_id), None)

    if veiculo_agendado:
        remover_agendamento(veiculo_id)
        print(f"\nO veículo {veiculo_agendado[2]} foi devolvido com sucesso e está disponível para novos agendamentos.")
    else:
        print("\nVocê não tem permissão para devolver este veículo.")


# Função para listar agendamentos do usuário logado
def listar_agendamentos():
    if not verificar_login():
        return

    print("\n=== Seus Agendamentos ===")
    agendamentos = recupera_agendamentos_por_usuario(usuario_logado["id"])
    if not agendamentos:
        print("Nenhum agendamento encontrado.")
        return

    for agendamento in agendamentos:
        print(f"[ID: {agendamento[0]}] {agendamento[2]} - {agendamento[3]} - {agendamento[4]} em {agendamento[1]}")


# Menu principal do sistema
def menu():
    while True:
        print("\n=== Sistema EcoRide ===")
        print("1. Cadastrar usuário")
        print("2. Fazer login")
        print("3. Listar veículos disponíveis")
        print("4. Listar pontos de aluguel")
        print("5. Agendar veículo")
        print("6. Desbloquear veículo")
        print("7. Devolver veículo")
        print("8. Listar seus agendamentos")
        print("9. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            login_usuario()
        elif opcao == "3":
            listar_veiculos_disponiveis()
        elif opcao == "4":
            listar_pontos()
        elif opcao == "5":
            agendar_veiculo()
        elif opcao == "6":
            desbloquear_veiculo()
        elif opcao == "7":
            devolver_veiculo()
        elif opcao == "8":
            listar_agendamentos()
        elif opcao == "9":
            print("\nSaindo do sistema... Até mais!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")


# Executa o sistema
if __name__ == "__main__":
    menu()
