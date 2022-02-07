import sqlite3
class Banco():
    def __init__(self,nome):
        self._nome = nome


    def interface(self):
        self.opcoes()


    @staticmethod
    def titulo(palavra,l = 42):
        print('-' * l)
        print(palavra.center(42))
        print('-' * l)


    def opcoes(self):
        cont = 1
        listaop = ['Criar conta','Entrar na conta', 'Lista de contas', 'Sair']
        while True:
            self.titulo(self._nome)
            for c in listaop:
                print(f'[{cont}]\033[34m{c}\033[m')
                cont += 1
                if cont > 4: cont = 1

            op = int(input('Escolha sua opção: '))
            if op == 1:
                self.titulo('Crie sua conta')
                nome = str(input('Seu nome: '))
                conta = int(input('Numero para sua conta: '))
                saldo = float(input('Saldo desejado: '))
                self.criarconta(nome,conta,saldo)
            elif op == 2:
                while True:
                    self.titulo('Login')
                    self.entrar()
            elif op == 3:
                self.titulo('Lista de clientes')
                self.listaconta()
            elif op == 4:
                exit()
            else:
                print('\033[31mOpção invalida!\033[m')

    def criarconta(self,nome,conta,saldo=0):
        nome = nome
        conta = conta
        saldo = saldo
        try:
            conexao = sqlite3.connect('bancodados.db')
            cursor = conexao.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTs clientes ('
                           'nome TEXT,'
                           'conta INTEGER,'
                           'saldo INTEGER'
                           ') ')
            cursor.execute('INSERT INTO clientes (nome,conta,saldo) VALUES (?,?,?)',(nome,conta,saldo))
            conexao.commit()

            cursor.close()
            conexao.close()
        except sqlite3.Error as erro:
            print(f'Erro ao criar a conta: {erro}')




    def entrar(self):
        cont = 1
        nome = str(input('Digite seu nome: '))
        conta = int(input('Digite o numero da sua conta: '))
        conexao = sqlite3.connect('bancodados.db')
        cursor = conexao.cursor()
        cursor.execute(f'SELECT conta FROM clientes WHERE nome = "{nome}"')
        verificar = cursor.fetchall()
        try:
            if conta == verificar[0][0]:
                print('\033[44mLogin bem sucedido!\033[m')
                cursor.execute(f'SELECT saldo FROM clientes WHERE nome = "{nome}"')
                saldo_db = cursor.fetchall()[0][0]
                self.titulo(f'Sua conta, {nome}')
                listaop = ['Deposito', 'Saque', 'Voltar']
                print(f'{nome}, seu saldo em conta é \033[32:40mR${saldo_db}\033[m')
                while True:
                    for c in listaop:
                        print(f'[{cont}]\033[34m{c}\033[m')
                        cont += 1
                        if cont > 3: cont = 1
                    opcao = int(input('Qual opção deseja? '))
                    if opcao == 1:
                        self.depositar(saldo_db,nome)
                    elif opcao == 2:
                        self.sacar(saldo_db,nome)
                    elif opcao == 3:
                        exit()
                    else:
                        print('Opção invalida!')
        except:
            print(f'\033[31mNome ou conta incorretas!\033[m')




        cursor.close()
        conexao.close()



    def listaconta(self):
        conexao = sqlite3.connect('bancodados.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM clientes')
        print('Cliente | Conta | Saldo')
        for linha in cursor.fetchall():
            nome,conta,saldo = linha
            print(f'\033[7:40m{nome:<8}\033[m   {conta:<-5}   {saldo}')

        cursor.close()
        conexao.close()


    def depositar(self,saldo,nome):
        depo = float(input('Quanto deseja depositar? '))
        deposito = depo + saldo
        deposito = str(deposito)
        conexao = sqlite3.connect('bancodados.db')
        cursor = conexao.cursor()
        cursor.execute(f'UPDATE clientes SET saldo = "{deposito}" WHERE nome = "{nome}"')
        conexao.commit()
        print(f'\033[32mDeposito de {depo} bem sucedido! Agora você possui {deposito} em conta\033[m')

        cursor.close()
        conexao.close()

    def sacar(self,saldo,nome):
        depo = float(input('Quanto deseja Sacar? '))
        saque = saldo - depo
        conexao = sqlite3.connect('bancodados.db')
        cursor = conexao.cursor()
        cursor.execute(f'UPDATE clientes SET saldo = "{saque}" WHERE nome = "{nome}"')
        conexao.commit()
        print(f'\033[32mSaque de {depo} bem sucedido! Agora você possui {saque} em conta\033[m')


        cursor.close()
        conexao.close()





