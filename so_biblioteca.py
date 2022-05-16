import conexaobiblioteca as connect
import os

#COLOCAR O NOME DO BANCO DE DADOS E A SENHA NOS LOCAIS INDICADOS
conexao = connect.criar_conexao('localhost', 'NOME DO DATABASE','root','SENHA DE ACESSO')

if conexao.is_connected():
    cursor = conexao.cursor()

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
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
    print("| (8) Encerrar sistema                              |")
    print("|                                                   |")
    print("|                                                   |")
    print("|                                                   |")
    print("-----------------------------------------------------")    
    op = input('Oprção: ')

    if op == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        connect.cadastrar_livro(conexao, cursor)
        a = input('')
    elif op == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        connect.listar_livros(cursor)
        a = input('')
    elif op == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        connect.pesquisar_livro(cursor)
        a = input('')
    elif op == '4':
        os.system('cls' if os.name == 'nt' else 'clear')
        connect.alugar_livro(conexao, cursor)
        a = input('')
    elif op == '5':
        os.system('cls' if os.name == 'nt' else 'clear')
        connect.devolver_livro(conexao, cursor)
        a = input('')
    elif op == '6':
        os.system('cls' if os.name == 'nt' else 'clear')
        connect.alterar_livro(conexao, cursor)
        a = input('')
    elif op == '7':
        os.system('cls' if os.name == 'nt' else 'clear')
        connect.excluir_livro(conexao, cursor)
        a = input('')
    elif op == '8':
        break
    else:
        print('Opção Inexistente!')
        a = input('')

if conexao.is_connected():
    conexao.close()
    os.system('cls' if os.name == 'nt' else 'clear')
    print('SISTEMA FINALIZADO COM SUCESSO!')
    a = input('')