from sqlite3 import connect
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
    print("| (8) Consultar alugueis                            |")
    print("| (9) Voltar para o menu principal                  |")
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
    cursor.execute(f"INSERT INTO Livros (titulo_livro, autor_livro, editora_livro, ano_edicao, disponibilidade_livro) VALUES ('{titulo}', '{autor}', '{editora}', {ano}, '{disponibilidade}')")
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
    cursor.execute(f"SELECT * FROM livros WHERE titulo_livro LIKE '%{pesquisa}%'")
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
    cursor.execute(f'SELECT disponibilidade_livro FROM livros WHERE id_livro = {aluguel}')
    disp = cursor.fetchone()
    associado = int(input('Código do associado: '))
    cursor.execute(f'SELECT n_livros_alugados FROM associados where id_associado = {associado}')
    qtd = cursor.fetchone()
    qtd = int(qtd[0])
    
    if qtd < 3:
        if disp[0] == 'DISPONÍVEL':
            cursor.execute(f'UPDATE livros SET disponibilidade_livro = "ALUGADO" WHERE id_livro = {aluguel}')
            conexao.commit()
            cursor.execute(f'UPDATE associados SET n_livros_alugados = {qtd+1} WHERE id_associado = {associado}')
            conexao.commit()
            if qtd + 1 == 3:
                cursor.execute(f'UPDATE associados SET pendencia_associado = "SIM" WHERE id_associado = {associado}')
                conexao.commit()
            cursor.execute(f'SELECT titulo_livro FROM livros WHERE id_livro = {aluguel}')
            titulo = cursor.fetchone()
            cursor.execute(f'SELECT nome_associado FROM associados WHERE id_associado = {associado}')
            nome = cursor.fetchone()
            cursor.execute(f'insert into alugueis (nome_associado, titulo_livro, data_aluguel, data_limite, data_devolucao, multa) values ("{nome[0]}", "{titulo[0]}", curdate(), date_add(now(), interval 7 day), null, 0)')
            conexao.commit()
            cursor.execute(f'insert into arquivo (nome_associado, titulo_livro, data_aluguel, data_limite) values ("{nome[0]}", "{titulo[0]}", curdate(), date_add(now(), interval 7 day))')
            conexao.commit()
            print('Livro alugado com sucesso!')
        else:
            print('Livro indisponíel!')
    else:
        print('O associado possui pendência na biblioteca!')
    
def consultar_pendencias(cursor):
    cursor.execute('select * from alugueis')
    alugueis = cursor.fetchall()
    for i in alugueis:
        print(f'\nCod aluguel: {i[0]}')
        print(f'Associado: {i[1]}')
        print(f'Título: {i[2]}')
        print(f'Data do aluguel: {i[3]}')
        print(f'Data limite: {i[4]}')
        print(f'Data de devolução: {i[5]}')
        if i[5] is None:
            print("Status: Alugado")
        else:
            print('Status: Devolvido')    
    
    
def devolver_livro(conexao, cursor):    
    aluguel = int(input('Digite o código do livro que deseja devolver: '))
    cursor.execute(f'SELECT disponibilidade_livro FROM livros WHERE id_livro = {aluguel}')
    disp = cursor.fetchone()
    associado = int(input('Código do associado: '))
    cursor.execute(f'SELECT n_livros_alugados FROM associados where id_associado = {associado}')
    qtd = cursor.fetchone()
    qtd = int(qtd[0])
    if qtd > 0:
        if disp[0] == 'ALUGADO':
            cursor.execute(f'UPDATE livros SET disponibilidade_livro = "DISPONÍVEL" WHERE id_livro = {aluguel}')
            conexao.commit()
            cursor.execute(f'UPDATE associados SET n_livros_alugados = {qtd - 1} WHERE id_associado = {associado}')
            conexao.commit()
            if qtd != 3:
                cursor.execute(f'UPDATE associados SET pendencia_associado = "NÃO" where id_associado = {associado}')
                conexao.commit()
            cursor.execute(f'SELECT titulo_livro FROM livros WHERE id_livro = {aluguel}')
            titulo = cursor.fetchone()
            cursor.execute(f'UPDATE alugueis set data_devolucao = curdate() where titulo_livro = "{titulo[0]}"')
            conexao.commit()
            #FAZER O CALCULO DOS JUROS SE HOUVEREM
            cursor.execute(f'delete from alugueis where titulo_livro = "{titulo[0]}"')
            conexao.commit()
            print('Livro devolvido com sucesso!')
        else:
            print('Livro não alugado!')
    else:
        print('O associado não possui pendência na biblioteca!')

def alterar_livro(conexao, cursor):
    query = input('Qual valor deseja alterar? (t)Título (a)Autor (e)Editora (an)Ano ')
    if query.lower() == 't':
        cod = int(input('Informe o código do livro que deseja alterar o título: '))
        titulo = input('Informe o novo título: ')
        titulo = titulo.replace("'",'')
        cursor.execute(f'UPDATE livros SET titulo_livro = "{titulo}" WHERE id_livro = {cod}')
    elif query.lower() == 'a':
        cod = int(input('Informe o código do livro que deseja alterar o autor: '))
        autor = input('Informe o nome do autor: ')
        cursor.execute(f'UPDATE livros SET autor_livro = "{autor}" WHERE id_livro = {cod}')
    elif query.lower() == 'e':
        cod = int(input('Informe o código do livro que deseja alterar a editora: '))
        editora = input('Informe a nova editora: ')
        cursor.execute(f'UPDATE livros SET editora_livro = "{editora}" WHERE id_livro = {cod}')
    elif query.lower() == 'an':
        cod = int(input('Informe o código do livro que deseja alterar o ano: '))
        ano = int(input('Informe o novo ano: '))
        cursor.execute(f'UPDATE livros SET ano_edicao = {ano} WHERE id_livro = {cod}')
    else:
        print('Comando inválido!')
    conexao.commit()
    print('Alteração realizada')

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
    cursor.execute(f'insert into associados (nome_associado, cpf_associado, data_cadastro, n_livros_alugados, pendencia_associado) values ("{nome}", "{cpf}", curdate(), 0, "NÃO")')
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
            print(f'Livros alugados: {i[4]}')
            print(f'Pendência: {i[5]}')
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
