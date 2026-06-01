import oracledb
#conexão oracle
connection = oracledb.connect(
    user = "",
    password='',
    dsn="BD-ACD/XE"
)
print("Conectado ao banco de dados")
#Se for testar modificar os dados acima
connection.commit()
#
#A coluna descrição provavelmente ta com o nome errado aqui, ver no bd e alterar aqui ou lá
#

repetir = 1
#função update
#checar se realmente precisa ter um argumento ali
#CRIAR um loop dentro da função para alterar os dados quantas vezes quiser
def update(idupdate):
    oque =int(input("O que deseja alterar?\n1 - Nome\n2 - Descrição\n3 - Custo do produto\n4 - Custo fixo\n5 - Comissão de vendas\n6 - Imposto sobre vendas \n7 - Margem de lucro\nSelecione uma opção: "))
    if (oque == 1):
        novo = input("Insira o novo nome: ")
        cursor = connection.cursor()
        cursor.execute("UPDATE produtos_pi SET NOME = :novo WHERE CODIGO=:qual", [novo,idupdate])
        cursor.close

    elif oque == 2:
        novo = input("Insira a nova descrição: ")
        novo = trans(1,novo)
        cursor = connection.cursor()
        cursor.execute("UPDATE produtos_pi SET DESCRICAO = :novo WHERE CODIGO=:qual", [novo,idupdate])
        cursor.close

    elif oque == 3:
        novo=float(input("Insira o novo custo do produto"))
        cursor = connection.cursor()
        cursor.execute("UPDATE produtos_pi SET CP = :novo WHERE CODIGO=:qual", [novo,idupdate])
        cursor.close

    elif oque == 4:
        novo=float(input("Insira o novo custo fixo"))
        cursor = connection.cursor()
        cursor.execute("UPDATE produtos_pi SET CF = :novo WHERE CODIGO=:qual", [novo,idupdate])
        cursor.close
    
    elif oque == 5:
        novo=float(input("Insira a nova comissão de vendas"))
        cursor = connection.cursor()
        cursor.execute("UPDATE produtos_pi SET CV = :novo WHERE CODIGO=:qual", [novo,idupdate])
        cursor.close
    elif oque == 6:
        novo=float(input("Insira o novo imposto sobre vendas"))
        cursor = connection.cursor()
        cursor.execute("UPDATE produtos_pi SET IV = :novo WHERE CODIGO=:qual", [novo,idupdate])
        cursor.close
    elif oque == 7:
        novo=float(input("Insira a nova margem de lucro"))
        cursor = connection.cursor()
        cursor.execute("UPDATE produtos_pi SET ML = :novo CODIGO ID=:qual", [novo,idupdate])
        cursor.close
    return(idupdate)
def trans(qual,palavra):
    m1 = []
    m2 = []
    criptografada = []
    letras = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I', 10:'J', 11:'K', 12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z', 27:' '}
    palavra = palavra.upper()
    for n in range (len(palavra)):
        x = palavra[n]
        if (n%2 == 0):
            m1.append(x)
        else:
            m2.append(x)
    if len(palavra)%2 != 0:
        m2.append(" ")
    for n in range (len(m1)):
        m = n
        for indice,letra in letras.items():
            if (m1[n] == letra):
                m1[n] = indice
            if (m2[m] == letra):
                m2[m] = indice
    if qual == 0:
        #Matriz inversa pré definida com cálculos no scilab, utilizando o inverso da determinante da matriz chave em um Z27 (quantia de entradas na indexação (dicionário letras))
        m3 = [22, -33]
        m4 = [-11, 44]
    if qual == 1:
        m3 = [4,3]
        m4 = [1,2]
    for n in range (len(m1)):
        x = (m3[0]*m1[n]) + (m3[1]*m2[n])
        if  (x==0) or (x<0) or (x >27):
            x = x%27
            criptografada.append(x)
        else:
            criptografada.append(x)
        x = (m4[0]*m1[n]) + (m4[1]*m2[n])
        if (x==0) or (x<0) or (x >27):
            x = x%27
            criptografada.append(x)
        else:
            criptografada.append(x)
    for n in range (len(criptografada)):
        x = criptografada[n]
        for indice,letra in letras.items():
            if x == indice:
                criptografada[n] = letra
        if qual == 0:
            if criptografada[n] == 0:
                criptografada[n] = ' '
    palavraC = ''.join(criptografada)
    return(palavraC)
while (repetir == 1):
    print("Escolha uma opção:\n1: Inserir produto\n2: cálculo de preço de algum produto\n3:Modificar produto\n4:Apagar produto\n5:Visualizar Produtos\n6:Visualizar Preços\n7:Sair do sistema")
    op = int(input(" "))
    while (not 1<op<7):
        print("Insira uma opção válida")
        op = int(input (" "))
    if (op==1):
        NO = input("Insira o nome do produto: ")
        DESCRI = input("Insira a descrição do produto: ")
        DESCRI = trans(1,DESCRI)
        ID = int(input("Insira o ID do produto: "))
        CP = input("Insira o custo base do produto:")
        print("Insira os próximos dados em %")
        CF = float(input("Insira o custo fixo: "))
        CV = float(input("Insira a comissão de vendas: "))
        IV = float(input("Insira os impostos sobre venda: "))
        print("Alta >20%\nMédia >=10% até 20%\nBaixa >0% até 10%\nEqulíbrio = 0\nPrejuízo <0%")
        ML = float(input("Insira a margem de lucro desejada: "))
        #precisa fazer uma função pra criptografia
        cursor = connection.cursor()
        cursor.execute("INSERT INTO produtos_pi VALUES (:id, :nome, :descri, :cp, :cf, :cv, :iv, :ml)", [ID, NO, DESCRI, CP, CF, CV, IV, ML])
        connection.commit()
        cursor.close

 

    if (op==2):
        NO = input("Insira o nome do produto: ")
        DESCRI = input("Insira a descrição do produto: ")
        DESCRI = trans(1,DESCRI)
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
        #
        #contas da margem de lucro pra printar
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

    if (op == 3): #update
        idupdate = int(input("Insira o ID do produto que deseja alterar: "))
        update(idupdate)
        cursor = connection.cursor()
        print('Novos dados do produto:')
        print(cursor.execute("SELECT * FROM produtos_pi WHERE CODIGO=:idupdate", [idupdate]))
        connection.commit()
        cursor.close


    if (op == 4):
        apagar = int(input("Insira o ID do produto que deseja apagar: "))
        cursor = connection.cursor()
        cursor.execute("DELETE FROM produtos_pi WHERE CODIGO=:apagar", [apagar])
        connection.commit()
        cursor.close

    if (op == 5):
        cursor = connection.cursor()
        for qual in cursor.execute("SELECT * FROM produtos_pi"):
            ID = qual[0]
            NO = qual[1]
            DESCRI = qual[2]
            DESCRI = trans(0,DESCRI)
            CP = qual[3]
            CF = qual[4]
            CV = qual[5]
            IV = qual[6]
            ML = qual[7]

            PV = (CP/(1-((CF+CV+IV+ML)/100)))
            RB = PV-CP
            CF = (CF/100)*PV
            CV = (CV/100)*PV
            IV = (IV/100)*PV
            OC = CF+CV+IV
            RB = PV-CP
            RA = RB-OC
            print (ID, NO, DESCRI, CP, CF, CV, IV, ML, PV, RB, CF, IV, OC, RB, RA)


    if (op == 6):
        cursor = connection.cursor()
        for qual in cursor.execute("SELECT * FROM produtos_pi"):
            ID = qual[0]
            NO = qual[1]
            DESCRI = qual[2]
            DESCRI = trans(0,DESCRI)
            CP = qual[3]
            CF = qual[4]
            CV = qual[5]
            IV = qual[6]
            ML = qual[7]

            PV = (CP/(1-((CF+CV+IV+ML)/100)))
            RB = PV-CP
            CF = (CF/100)*PV
            CV = (CV/100)*PV
            IV = (IV/100)*PV
            OC = CF+CV+IV
            RB = PV-CP
            RA = RB-OC
            print(NO)
            print(f"Os preços do produto de ID {ID}, {NO} - {DESCRI} são:")
            print(f"                            Valor      %")
            print(f"Preço de venda             {PV:.2f}    {(PV/PV)*100:.2f}%")
            print(f"Custo de aquisição         {CP:.2f}    {(CP/PV)*100:.2f}%")
            print(f"Receita bruta              {RB:.2f}    {(RB/PV)*100:.2f}%")
            print(f"Custo fixo                 {CF:.2f}    {(CF/PV)*100:.2f}%")
            print(f"Comissão de vendas         {CV:.2f}     {(CV/PV)*100:.2f}%")
            print(f"Impostos                   {IV:.2f}    {(IV/PV)*100:.2f}%")
            print(f"Outros custos (CF+CV+IV)   {OC:.2f}    {(OC/PV)*100:.2f}%")
            print(f"Rentabilidade              {RA:.2f}     {(RA/PV)*100 :.2f}%")
            if (ML>20):
                print(f"Margem de lucro ({ML:.2f}%) Alta\n")
            if (10<=ML<=20):
                print (f"Margem de lucro ({ML:.2f}%) Média\n")
            if (0<ML<10):
                print (f"Margem de lucro ({ML:.2f}%) Baixa\n")
            if (ML == 0):
                print (f"Margem de lucro ({ML:.2f}%) em equilíbrio\n")
            if (ML<0):
                print (f"Margem de lucro ({ML:.2f}%) prejuízo\n")

    if (op == 7):
        repetir = 0
