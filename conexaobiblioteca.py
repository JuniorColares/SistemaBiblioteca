import mysql.connector

def criar_conexao(host, database, user, password):
    conexao = mysql.connector.connect(host = host,
        database = database,
        user = user,
        password = password)
    return conexao


# FUNÇÕES COM OS MENUS:

def menu_inicial():
    print("-----------------------------------------------------")
    print("|              Escolha a opção desejada             |")
    print("|                                                   |")
    print("|                                                   |")
    print("| (1) Menu Livros                                   |")
    print("| (2) Menu Associados                               |")
    print("| (3) Realizar Locação de livro                     |")
    print("| (4) Encerrar sistema                              |")
    print("|                                                   |")
    print("|                                                   |")
    print("-----------------------------------------------------") 

def menu_livros():
    print("-----------------------------------------------------")
    print("|              Escolha a opção desejada             |")
    print("|                                                   |")
    print("|                                                   |")
    print("|                                                   |")
    print("| (1) Cadastrar Livro                               |")
    print("| (2) Consultar livros cadastrados                  |")
    print("| (3) Consultar livro pelo título                   |")
    print("| (4) Alugar livro                                  |")
    print("| (5) Devolver livro                                |")
    print("| (6) Alterar cadastro de livro                     |")
    print("| (7) Excluir livro                                 |")
    print("| (8) Voltar para o menu principal                  |")
    print("|                                                   |")
    print("|                                                   |")
    print("|                                                   |")
    print("-----------------------------------------------------") 

def menu_associados():
    print("-----------------------------------------------------")
    print("|              Escolha a opção desejada             |")
    print("|                                                   |")
    print("|                                                   |")
    print("| (1) Cadastrar Associado                           |")
    print("| (2) Buscar Associado                              |")
    print("| (3) Alterar Associado                             |")
    print("| (4) Excluir Associado                             |")
    print("| (5) Voltar para o menu principal                  |")
    print("|                                                   |")
    print("|                                                   |")
    print("-----------------------------------------------------")


#FUNÇÕES PARA O MENU LIVROS:

def cadastrar_livro(conexao, cursor):
    titulo = input('Título: ')
    titulo = titulo.replace("'",'')
    autor = input('Autor: ')
    editora = input('Editora: ')
    ano = int(input('Ano: '))
    disponibilidade = 'DISPONÍVEL'
    cursor.execute(f"INSERT INTO Livros (titulo, autor, editora, ano, disponibilidade) VALUES ('{titulo}', '{autor}', '{editora}', {ano}, '{disponibilidade}')")
    conexao.commit()
    print('Livro cadastrado com sucesso!')

def listar_livros(cursor):
    cursor.execute('SELECT * FROM Livros')
    livros = cursor.fetchall()
    for i in livros:
        print(f'\nCod: {i[0]:03.0f}')
        print('Titulo: ',i[1])
        print('Autor: ',i[2])
        print('Editora: ',i[3])
        print('Ano: ',i[4])
        print('Disponibilidade: ',i[5])

def pesquisar_livro(cursor):
    pesquisa = input('Pesquisa: ')
    pesquisa = pesquisa.replace("'",'')
    cursor.execute(f"SELECT * FROM livros WHERE titulo LIKE '%{pesquisa}%'")
    livros = cursor.fetchall()
    for i in livros:
        print(f'\nCod: {i[0]:03.0f}')
        print('Titulo: ',i[1])
        print('Autor: ',i[2])
        print('Editora: ',i[3])
        print('Ano: ',i[4])
        print('Disponibilidade: ',i[5])

def alugar_livro(conexao, cursor):
    aluguel = int(input('Digite o código do livro que deseja alugar: '))
    cursor.execute(f'SELECT disponibilidade FROM livros WHERE id_livro = {aluguel}')
    disp = cursor.fetchone()
    if disp[0] == 'DISPONÍVEL' or disp[0] == 'DISPONIVEL':
        cursor.execute(f'UPDATE livros SET disponibilidade = "ALUGADO" WHERE id_livro = {aluguel}')
        conexao.commit()
        print('Livro alugado com sucesso!')
    else:
        print('Livro indisponíel!')
    
def devolver_livro(conexao, cursor):    
    devolucao = int(input('Digite o código do livro que deseja devolver: '))
    cursor.execute(f'SELECT disponibilidade FROM livros WHERE id_livro = {devolucao}')
    disp = cursor.fetchone()
    if disp[0] == 'ALUGADO':
        cursor.execute(f'UPDATE livros SET disponibilidade = "DISPONÍVEL" WHERE id_livro = {devolucao}')
        conexao.commit()
        print('Livro devolvido com sucesso!')
    else:
        print('Livro já se encontra na biblioteca!')

def alterar_livro(conexao, cursor):
    query = input('Qual valor deseja alterar? (t)Título (a)Autor (e)Editora (an)Ano ')
    if query.lower() == 't':
        cod = int(input('Informe o código do livro que deseja alterar o título: '))
        titulo = input('Informe o novo título: ')
        titulo = titulo.replace("'",'')
        cursor.execute(f'UPDATE livros SET titulo = "{titulo}" WHERE id_livro = {cod}')
        print('Alteração realizada')
    elif query.lower() == 'a':
        cod = int(input('Informe o código do livro que deseja alterar o autor: '))
        autor = input('Informe o nome do autor: ')
        cursor.execute(f'UPDATE livros SET autor = "{autor}" WHERE id_livro = {cod}')
    elif query.lower() == 'e':
        cod = int(input('Informe o código do livro que deseja alterar a editora: '))
        editora = input('Informe a nova editora: ')
        cursor.execute(f'UPDATE livros SET editora = "{editora}" WHERE id_livro = {cod}')
    elif query.lower() == 'an':
        cod = int(input('Informe o código do livro que deseja alterar o ano: '))
        ano = int(input('Informe o novo ano: '))
        cursor.execute(f'UPDATE livros SET ano = {ano} WHERE id_livro = {cod}')
    else:
        print('Comando inválido!')
    conexao.commit()

def excluir_livro(conexao, cursor):
    cod = int(input('Infome o código do livro que deseja excluir do sistema: '))
    cursor.execute(f'SELECT * FROM livros WHERE id_livro = {cod}')
    livro = cursor.fetchone()
    if livro != None:
        conf = input(f'Tem certeza que deseja excluir o livro {livro[1]} de {livro[2]}? (s/n) ')
        if conf == 's':
            cursor.execute(f'DELETE FROM livros WHERE id_livro = {cod}')
            conexao.commit()
            print('Livro excluído')
    else:
        print('Código inexistente!')


#FUNÇÕES PARA MENU ASSOCIADOS: 

def cadatrar_associado(conexao, cursor):
    nome = input('Nome: ')
    nome = nome.replace("'",'')
    cpf = input('CPF: ')
    cpf = cpf.replace('.','')
    cpf = cpf.replace('-','')
    cursor.execute(f'insert into associados (nome_associado, cpf, qtd_alugueis_feitos, pendencia) values ("{nome}", "{cpf}", 0, "NÃO")')
    conexao.commit()

def buscar_associado(cursor):
    query = input('Busca: ')
    query = query.replace("'",'')
    cursor.execute(f'select * from associados where nome_associado like "%{query}%"')
    associados = cursor.fetchall()
    if associados != []:
        for i in associados:
            print(f'\nCod: {i[0]:03.0f}')
            print(f'Nome: {i[1]}')
            print(f'Pendência: {i[4]}')
    else:
        print('Nenhum usuário encontrado!')
    
def alterar_associado(conexao, cursor):
    cod = int(input('Informe o código do associado que deseja alterar: '))
    nome = input('Informe para qual nome deseja alterar: ')
    cursor.execute(f'update associados set nome_associado = "{nome}" where id_associado = {cod}')
    conexao.commit()
    print('Alteração realizada!')

def excluir_associado(conexao, cursor):
    cod = int(input('Informe o código do associado que deseja excluir: '))
    cursor.execute(f'select * from associados where id_associado = {cod}')
    associado = cursor.fetchone()
    if associado != None:
        conf = input(f'Tem certeza que deseja excluir o cadastro de {associado[1]}? (s/n) ')
        if conf == 'n':
            print('Exclusão cancelada!')
        elif conf == 's':
            cursor.execute(f'delete from associados where id_associado = {cod}')
            conexao.commit()
            print('Associado excluído!')
        else:
            print('Comando inválido')
    else:
        print('Nenhum usuário encontrado!')
