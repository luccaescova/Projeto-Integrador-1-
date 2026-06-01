print("Escolha uma opção:\n1: cadastro de produto    2: cálculo de preço")
op = int(input(" "))
if (op==1):
    NO = input("Insira o nome do produto: ")
    ID = input("Insira o ID do produto: ")

if (op==2):
    NO = input("Insira o nome do produto: ")
    ID = input("Insira o ID do produto: ")
    CP = float(input("Insira o custo do produto: "))
    print("Insira os próximos dados em %")
    CF = float(input("Insira o custo fixo: "))
    CV = float(input("Insira a comissão de vendas: "))
    IV = float(input("Insira os impostos sobre venda: "))
    print("Alta >20%\nMédia >=10% até 20%\nBaixa >0% até 10%\nEqulíbrio = 0\nPrejuízo <0%")
    ML = float(input("Insira a margem de lucro desejada: "))
    #valores serão transformados em % na conta seguinte para calcular o preço de venda
    PV = (CP/(1-((CF+CV+IV+ML)/100)))
    #serão calculados os valores em %, baseado no preço de venda, de cada custo seguinte
    CF = (CF/100)*PV
    CV = (CV/100)*PV
    IV = (IV/100)*PV
    #serão definidas as seguintes variáveis com os valores definidos sendo baseados em PV
    OC = CF+CV+IV
    RB = PV-CP
    RA = RB-OC
    #Abaixo: Valor = custo de cada item. % = quanto % cada custo representa do PV
    print(f"As informações do produto {NO} de ID {ID} são:")
    print(f"Descrição                  Valor      %")
    print(f"Preço de venda             {PV:.2f}    {(PV/PV)*100:.2f}%")
    print(f"Custo de aquisição         {CP:.2f}    {(CP/PV)*100:.2f}%")
    print(f"Receita bruta              {RB:.2f}    {(RB/PV)*100:.2f}%")
    print(f"Custo fixo                 {CF:.2f}    {(CF/PV)*100:.2f}%")
    print(f"Comissão de vendas         {CV:.2f}     {(CV/PV)*100:.2f}%")
    print(f"Impostos                   {IV:.2f}    {(IV/PV)*100:.2f}%")
    print(f"Outros custos (CF+CV+IV)   {OC:.2f}    {(OC/PV)*100:.2f}%")
    print(f"Rentabilidade              {RA:.2f}     {(RA/PV)*100 :.2f}%")
if (ML>20):
    print(f"Margem de lucro ({ML}%) Alta")
if (10<=ML<=20):
    print (f"Margem de lucro ({ML}%) Média")
if (0<ML<10):
    print (f"Margem de lucro ({ML}%) Baixa")
if (ML == 0):
    print (f"Margem de lucro ({ML}%) em equilíbrio")
if (ML<0):
    print (f"Margem de lucro ({ML}%) prejuízo")
