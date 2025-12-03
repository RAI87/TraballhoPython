# Sistema de Reserva de Onibus

## COMO INICIAR/TERMINAR:
1. Certifique-se de ter Python 3 instalado
2. Execute no terminal: python main.py
3. Para sair: escolha a opcao 7 no menu

OPÇÕES OFERECIDAS:
1. Cadastrar linha: Adiciona nova rota de onibus
2. Consultar horarios por cidade: Busca linhas por cidade de origem ou destino
3. Consultar assentos disponiveis: Verifica lugares livres para uma viagem especifica
4. Fazer reserva: Reserva manual de assento
5. Ler reservas de arquivo: Processa reservas de um arquivo texto
6. Relatorios: Gera relatorios financeiros e de ocupacao
7. Sair: Encerra o sistema

PRINCIPAIS TELAS:
- Tela de menu principal com 7 opcoes numeradas
- Tela de cadastro com campos: origem, destino, horario, valor
- Tela de consulta com filtro por cidade
- Tela de assentos com lista numerada de 1 a 20
- Tela de relatorios com opcoes de visualizacao

FORMATOS DE ARQUIVO:
linhas.txt:
id;origem;destino;horário;valor

reservas_input.txt:
cidade,horário(hh:mm),data(dd/mm/aaaa),assenti

LIMITAÇÕES CONHECIDAS:
- Sistema trabalha apenas com datas dos proximos 30 dias
- Cada onibus tem capacidade fixa de 20 assentos
- Assentos impares sao janelas, pares sao corredor
- Nao e possivel reservar para onibus que ja partiram

OBSERVAÇÕES:
- Arquivos sao salvos automaticamente
- Reservas falhas sao registradas em reservas_falhas.txt
- Sistema verifica formatos de data e horario
- Validacao basica de entrada de dados
