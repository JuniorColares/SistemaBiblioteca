import conexaobiblioteca as connect
import os

#COLOCAR O NOME DO BANCO DE DADOS E A SENHA NOS LOCAIS INDICADOS
conexao = connect.criar_conexao('localhost', 'NOME DB','root','SENHA')

if conexao.is_connected():
    cursor = conexao.cursor()

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    connect.menu_inicial()
    op = input('Opção: ')
    if op == '1':
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            connect.menu_livros()   
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
                os.system('cls' if os.name == 'nt' else 'clear')
                connect.consultar_pendencias(cursor)
                a = input('')
            elif op == '9':
                break
            else:
                print('Opção Inexistente!')
                a = input('')
    if op == '2':
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            connect.menu_associados() 
            op = input('Opção: ')
            if op == '1':
                os.system('cls' if os.name == 'nt' else 'clear')
                connect.cadatrar_associado(conexao, cursor)
                print('Cadastro realizado!')
                a = input('')            
            if op == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                connect.buscar_associado(cursor)
                a = input('')
            if op == '3':
                os.system('cls' if os.name == 'nt' else 'clear')
                connect.alterar_associado(conexao,cursor)
                a = input('')
            if op == '4':
                os.system('cls' if os.name == 'nt' else 'clear')
                connect.excluir_associado(conexao, cursor)
                a = input('')
            if op == '5':
                break
    if op == '3':
        pass

    if op == '4':
        break
    if op == '5':
        continue
    if op == '9':
        continue
    else:
        print('Comando inválido!')
        a = input('')
    
if conexao.is_connected():
    conexao.close()
    os.system('cls' if os.name == 'nt' else 'clear')
    print('SISTEMA FINALIZADO COM SUCESSO!')
    a = input('')
