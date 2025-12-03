import datetime
import os

# ========== ESTRUTURAS DE DADOS ==========
# Dicionário para armazenar linhas: {id_linha: dados}
linhas = {}
# Matriz de reservas: lista de dicionários de reservas
reservas = []
# Lista de datas futuras (próximos 30 dias)
datas_futuras = []

# ========== FUNÇÕES AUXILIARES ==========
def carregar_datas():
    """Gera lista de datas dos próximos 30 dias."""
    hoje = datetime.date.today()
    datas_futuras.clear()
    for i in range(30):
        data = hoje + datetime.timedelta(days=i)
        datas_futuras.append(data.strftime("%d/%m/%Y"))

def carregar_linhas():
    """Carrega linhas do arquivo linhas.txt para o dicionário."""
    if not os.path.exists("linhas.txt"):
        return
    with open("linhas.txt", "r", encoding="utf-8") as f:
        for linha in f:
            dados = linha.strip().split(";")
            if len(dados) == 5:
                id_linha, origem, destino, horario, valor = dados
                linhas[int(id_linha)] = {
                    "origem": origem,
                    "destino": destino,
                    "horario": horario,
                    "valor": float(valor),
                    "assentos": {data: list(range(1, 21)) for data in datas_futuras}
                }

def salvar_linhas():
    """Salva linhas no arquivo linhas.txt."""
    with open("linhas.txt", "w", encoding="utf-8") as f:
        for id_linha, dados in linhas.items():
            f.write(f"{id_linha};{dados['origem']};{dados['destino']};{dados['horario']};{dados['valor']}\n")

def salvar_reserva_falha(motivo, dados):
    """Salva reservas que falharam em arquivo."""
    with open("reservas_falhas.txt", "a", encoding="utf-8") as f:
        f.write(f"{dados}; Motivo: {motivo}\n")

# ========== FUNÇÕES PRINCIPAIS ==========
def menu():
    """Exibe menu principal."""
    print("\n" + "="*50)
    print("SISTEMA DE RESERVA DE ÔNIBUS")
    print("="*50)
    print("1. Cadastrar linha")
    print("2. Consultar horários por cidade")
    print("3. Consultar assentos disponíveis")
    print("4. Fazer reserva")
    print("5. Ler reservas de arquivo")
    print("6. Relatórios")
    print("7. Sair")
    return input("Escolha uma opção: ")

def cadastrar_linha():
    """Cadastra uma nova linha."""
    print("\n--- CADASTRO DE LINHA ---")
    origem = input("Cidade de origem: ")
    destino = input("Cidade de destino: ")
    horario = input("Horário (HH:MM): ")
    valor = float(input("Valor da passagem: "))
    novo_id = max(linhas.keys()) + 1 if linhas else 1
    linhas[novo_id] = {
        "origem": origem,
        "destino": destino,
        "horario": horario,
        "valor": valor,
        "assentos": {data: list(range(1, 21)) for data in datas_futuras}
    }
    salvar_linhas()
    print(f"Linha {novo_id} cadastrada com sucesso!")

def consultar_horarios():
    """Consulta horários por cidade de origem ou destino."""
    cidade = input("Digite a cidade (origem ou destino): ")
    print(f"\nHorários disponíveis para {cidade}:")
    encontrou = False
    for id_linha, dados in linhas.items():
        if dados["origem"] == cidade or dados["destino"] == cidade:
            print(f"ID {id_linha}: {dados['origem']} -> {dados['destino']} às {dados['horario']}")
            encontrou = True
    if not encontrou:
        print("Nenhum horário encontrado.")

def consultar_assentos():
    """Consulta assentos disponíveis para uma viagem."""
    cidade_destino = input("Cidade de destino: ")
    horario = input("Horário (HH:MM): ")
    data = input("Data (DD/MM/AAAA): ")
    
    for id_linha, dados in linhas.items():
        if dados["destino"] == cidade_destino and dados["horario"] == horario:
            if data in dados["assentos"]:
                assentos = dados["assentos"][data]
                print(f"Assentos disponíveis ({len(assentos)}): {assentos}")
                reservar = input("Deseja reservar um assento? (s/n): ")
                if reservar.lower() == "s":
                    fazer_reserva(id_linha, data)
                return
            else:
                print("Data fora do período permitido (30 dias).")
                return
    print("Viagem não encontrada.")

def fazer_reserva(id_linha, data):
    """Faz uma reserva manual."""
    try:
        assento = int(input("Número do assento: "))
        dados = linhas[id_linha]
        if assento in dados["assentos"][data]:
            dados["assentos"][data].remove(assento)
            reservas.append({
                "linha": id_linha,
                "data": data,
                "assento": assento,
                "valor": dados["valor"]
            })
            salvar_linhas()
            print("Reserva confirmada!")
        else:
            print("Assento já ocupado.")
            salvar_reserva_falha("Assento ocupado", f"Linha {id_linha}, Data {data}, Assento {assento}")
    except ValueError:
        print("Assento inválido.")

def ler_reservas_arquivo():
    """Lê reservas de um arquivo."""
    arquivo = input("Nome do arquivo (ex: reservas.txt): ")
    if not os.path.exists(arquivo):
        print("Arquivo não encontrado.")
        return
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split(",")
            if len(partes) == 4:
                cidade, horario, data, assento = partes
                assento = int(assento.strip())
                # (Aqui implementaria a lógica de validação e reserva)
                print(f"Processando: {cidade}, {horario}, {data}, Assento {assento}")
    print("Leitura concluída.")

def relatorios():
    """Exibe relatórios."""
    print("\n--- RELATÓRIOS ---")
    print("1. Total arrecadado no mês atual por linha")
    print("2. Ocupação média por dia da semana")
    op = input("Escolha: ")
    if op == "1":
        print("(Implementação do relatório de arrecadação)")
    elif op == "2":
        print("(Implementação da matriz de ocupação)")
    else:
        print("Opção inválida.")

# ========== PROGRAMA PRINCIPAL ==========
def main():
    carregar_datas()
    carregar_linhas()
    while True:
        opcao = menu()
        if opcao == "1":
            cadastrar_linha()
        elif opcao == "2":
            consultar_horarios()
        elif opcao == "3":
            consultar_assentos()
        elif opcao == "4":
            cidade = input("Cidade de destino: ")
            horario = input("Horário: ")
            data = input("Data: ")
            for id_linha, dados in linhas.items():
                if dados["destino"] == cidade and dados["horario"] == horario:
                    fazer_reserva(id_linha, data)
                    break
        elif opcao == "5":
            ler_reservas_arquivo()
        elif opcao == "6":
            relatorios()
        elif opcao == "7":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()