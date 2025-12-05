import datetime
import os

# ========== ESTRUTURAS DE DADOS ==========
linhas = {}
reservas = []
datas_futuras = []

# ========== FUNCOES AUXILIARES ==========
def carregar_datas():
    hoje = datetime.date.today()
    datas_futuras.clear()
    for i in range(30):
        data = hoje + datetime.timedelta(days=i)
        datas_futuras.append(data.strftime("%d/%m/%Y"))

def carregar_linhas():
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
    with open("linhas.txt", "w", encoding="utf-8") as f:
        for id_linha, dados in linhas.items():
            f.write(f"{id_linha};{dados['origem']};{dados['destino']};{dados['horario']};{dados['valor']}\n")

def salvar_reserva_falha(motivo, dados):
    with open("reservas_falhas.txt", "a", encoding="utf-8") as f:
        f.write(f"{dados}; Motivo: {motivo}\n")

# ========== FUNCOES DE RELATORIO ==========
def gerar_relatorio_arrecadacao():
    """Relatorio 1: Total arrecadado no mes atual por linha"""
    hoje = datetime.date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    print("\n" + "="*60)
    print("RELATORIO DE ARRECADACAO - MES ATUAL")
    print("="*60)
    
    totais_por_linha = {}
    
    # Calcula totais
    for reserva in reservas:
        try:
            # Converte data da reserva de string para objeto date
            data_reserva = datetime.datetime.strptime(reserva["data"], "%d/%m/%Y").date()
            
            # Verifica se a reserva e do mes atual
            if data_reserva.month == mes_atual and data_reserva.year == ano_atual:
                linha_id = reserva["linha"]
                valor = reserva["valor"]
                
                if linha_id not in totais_por_linha:
                    totais_por_linha[linha_id] = 0
                totais_por_linha[linha_id] += valor
        except ValueError:
            continue
    
    # Exibe resultados
    if not totais_por_linha:
        print("Nenhuma venda registrada no mes atual.")
        return
    
    total_geral = 0
    print("\n{:^10} {:^20} {:^15} {:^10}".format("ID", "ORIGEM -> DESTINO", "HORARIO", "TOTAL"))
    print("-"*60)
    
    for linha_id, total in sorted(totais_por_linha.items()):
        if linha_id in linhas:
            dados = linhas[linha_id]
            rota = f"{dados['origem']} -> {dados['destino']}"
            print(f"{linha_id:^10} {rota:^20} {dados['horario']:^15} R$ {total:>7.2f}")
            total_geral += total
    
    print("-"*60)
    print(f"{'TOTAL GERAL':^45} R$ {total_geral:>7.2f}")
    
    # Pergunta se quer salvar em arquivo
    salvar = input("\nDeseja salvar este relatorio em arquivo? (s/n): ")
    if salvar.lower() == 's':
        nome_arquivo = f"relatorio_arrecadacao_{mes_atual:02d}_{ano_atual}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("="*60 + "\n")
            f.write("RELATORIO DE ARRECADACAO - MES ATUAL\n")
            f.write("="*60 + "\n\n")
            f.write(f"{'ID':^10} {'ORIGEM -> DESTINO':^20} {'HORARIO':^15} {'TOTAL':^10}\n")
            f.write("-"*60 + "\n")
            
            for linha_id, total in sorted(totais_por_linha.items()):
                if linha_id in linhas:
                    dados = linhas[linha_id]
                    rota = f"{dados['origem']} -> {dados['destino']}"
                    f.write(f"{linha_id:^10} {rota:^20} {dados['horario']:^15} R$ {total:>7.2f}\n")
            
            f.write("-"*60 + "\n")
            f.write(f"{'TOTAL GERAL':^45} R$ {total_geral:>7.2f}\n")
        
        print(f"Relatorio salvo em: {nome_arquivo}")

def gerar_relatorio_ocupacao():
    """Relatorio 2: Ocupacao percentual media por dia da semana"""
    print("\n" + "="*60)
    print("RELATORIO DE OCUPACAO MEDIA POR DIA DA SEMANA")
    print("="*60)
    
    # Dicionario para armazenar dados por dia da semana
    dias_semana = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
    ocupacao_dias = {dia: {"total_assentos": 0, "assentos_ocupados": 0} for dia in dias_semana}
    
    # Coleta dados das reservas
    for reserva in reservas:
        try:
            # Converte data da reserva
            data_reserva = datetime.datetime.strptime(reserva["data"], "%d/%m/%Y")
            
            # Obtem dia da semana (0=Segunda, 6=Domingo)
            dia_num = data_reserva.weekday()  # Python: 0=Segunda, 6=Domingo
            dia_semana = dias_semana[dia_num]
            
            # Atualiza contadores
            ocupacao_dias[dia_semana]["assentos_ocupados"] += 1
            ocupacao_dias[dia_semana]["total_assentos"] += 20  # Cada onibus tem 20 assentos
            
        except ValueError:
            continue
    
    # Calcula porcentagens
    print("\n{:^15} {:^20} {:^20} {:^15}".format("DIA", "ASSENTOS OCUPADOS", "TOTAL ASSENTOS", "OCUPACAO"))
    print("-"*75)
    
    for dia in dias_semana:
        dados = ocupacao_dias[dia]
        total = dados["total_assentos"]
        ocupados = dados["assentos_ocupados"]
        
        if total > 0:
            porcentagem = (ocupados / total) * 100
        else:
            porcentagem = 0.0
        
        print(f"{dia:^15} {ocupados:^20} {total:^20} {porcentagem:>6.1f}%")
    
    # Calcula media geral
    total_geral = sum(d["total_assentos"] for d in ocupacao_dias.values())
    ocupados_geral = sum(d["assentos_ocupados"] for d in ocupacao_dias.values())
    
    if total_geral > 0:
        media_geral = (ocupados_geral / total_geral) * 100
    else:
        media_geral = 0.0
    
    print("-"*75)
    print(f"{'MEDIA GERAL':^15} {ocupados_geral:^20} {total_geral:^20} {media_geral:>6.1f}%")
    
    # Pergunta se quer salvar em arquivo
    salvar = input("\nDeseja salvar este relatorio em arquivo? (s/n): ")
    if salvar.lower() == 's':
        nome_arquivo = "relatorio_ocupacao_semanal.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("="*60 + "\n")
            f.write("RELATORIO DE OCUPACAO MEDIA POR DIA DA SEMANA\n")
            f.write("="*60 + "\n\n")
            f.write(f"{'DIA':^15} {'ASSENTOS OCUPADOS':^20} {'TOTAL ASSENTOS':^20} {'OCUPACAO':^15}\n")
            f.write("-"*75 + "\n")
            
            for dia in dias_semana:
                dados = ocupacao_dias[dia]
                total = dados["total_assentos"]
                ocupados = dados["assentos_ocupados"]
                
                if total > 0:
                    porcentagem = (ocupados / total) * 100
                else:
                    porcentagem = 0.0
                
                f.write(f"{dia:^15} {ocupados:^20} {total:^20} {porcentagem:>6.1f}%\n")
            
            f.write("-"*75 + "\n")
            f.write(f"{'MEDIA GERAL':^15} {ocupados_geral:^20} {total_geral:^20} {media_geral:>6.1f}%\n")
        
        print(f"Relatorio salvo em: {nome_arquivo}")

def relatorios():
    """Menu de relatorios"""
    print("\n--- RELATORIOS ---")
    print("1. Total arrecadado no mes atual por linha")
    print("2. Ocupacao percentual media por dia da semana")
    print("3. Voltar ao menu principal")
    
    op = input("\nEscolha uma opcao: ")
    
    if op == "1":
        gerar_relatorio_arrecadacao()
    elif op == "2":
        gerar_relatorio_ocupacao()
    elif op == "3":
        return
    else:
        print("Opcao invalida. Voltando ao menu principal.")

# ========== FUNCOES PRINCIPAIS ==========
def menu():
    print("\n" + "="*50)
    print("SISTEMA DE RESERVA DE ONIBUS")
    print("="*50)
    print("1. Cadastrar linha")
    print("2. Consultar horarios por cidade")
    print("3. Consultar assentos disponiveis")
    print("4. Fazer reserva")
    print("5. Ler reservas de arquivo")
    print("6. Relatorios")
    print("7. Sair")
    return input("Escolha uma opcao: ")

def cadastrar_linha():
    print("\n--- CADASTRO DE LINHA ---")
    origem = input("Cidade de origem: ")
    destino = input("Cidade de destino: ")
    horario = input("Horario (HH:MM): ")
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
    cidade = input("Digite a cidade (origem ou destino): ")
    print(f"\nHorarios disponiveis para {cidade}:")
    encontrou = False
    for id_linha, dados in linhas.items():
        if dados["origem"] == cidade or dados["destino"] == cidade:
            print(f"ID {id_linha}: {dados['origem']} -> {dados['destino']} as {dados['horario']}")
            encontrou = True
    if not encontrou:
        print("Nenhum horario encontrado.")

def consultar_assentos():
    cidade_destino = input("Cidade de destino: ")
    horario = input("Horario (HH:MM): ")
    data = input("Data (DD/MM/AAAA): ")
    
    for id_linha, dados in linhas.items():
        if dados["destino"] == cidade_destino and dados["horario"] == horario:
            if data in dados["assentos"]:
                assentos = dados["assentos"][data]
                print(f"Assentos disponiveis ({len(assentos)}): {assentos}")
                reservar = input("Deseja reservar um assento? (s/n): ")
                if reservar.lower() == "s":
                    fazer_reserva(id_linha, data)
                return
            else:
                print("Data fora do periodo permitido (30 dias).")
                return
    print("Viagem nao encontrada.")

def fazer_reserva(id_linha, data):
    try:
        assento = int(input("Numero do assento: "))
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
            print("Assento ja ocupado.")
            salvar_reserva_falha("Assento ocupado", f"Linha {id_linha}, Data {data}, Assento {assento}")
    except ValueError:
        print("Assento invalido.")

def ler_reservas_arquivo():
    arquivo = input("Nome do arquivo (ex: reservas.txt): ")
    if not os.path.exists(arquivo):
        print("Arquivo nao encontrado.")
        return
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split(",")
            if len(partes) == 4:
                cidade, horario, data, assento = partes
                assento = int(assento.strip())
                print(f"Processando: {cidade}, {horario}, {data}, Assento {assento}")
    print("Leitura concluida.")

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
            horario = input("Horario: ")
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
            print("Opcao invalida.")

if __name__ == "__main__":
    main()