import socket
import sys
import time
import os
import ast

HOST = '127.0.0.1'          # IP do servidor
PORT = 9999                 #Porta do servidor
diretorio = 'TOPSECRET'

# Coloque a função de Upload aqui

def Upload(file, conn):
    # Abrir o arquivo em modo leitura
    with open(file, 'r') as f:
    # Ler uma linha do arquivo de cada vez
        for line in f:
    # Transmitir a linha para o servidor (converta a linha para bytes com enconde())
            conn.send(line.encode())
    # Após transmitir a última linha fechar o arquivo

#--------------------------------------------------------------------
# Incio do código principal

pydir = os.path.dirname(os.path.realpath(__file__))
print('Diretorio do script: ', pydir)
os.chdir(pydir)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
except:
    print('# erro de conexao')
    sys.exit()

# Verifica se o diretório já foi criado (resposta deve conter a lista de diretórios)

# PASSO1: Substitua COMANDO pelo comando de listar diretórios
s.send(bytes('os.listdir()\n', 'utf-8'))
time.sleep(2) #essa espera é para receber a resposta completa sem ter que criarum while
resposta = s.recv(2048).decode()

# Se não estiver, cria o diretório
if diretorio not in resposta:
    print('Diretorio nao encontrado')

# PASSO2: Substitua COMANDO pelo comando de criar diretório
    s.send(bytes('os.makedirs({})\n'.format(diretorio),'utf-8'))
    time.sleep(2)
    print(s.recv(2048).decode())
else:
    print('Conteudo do diretorio:')
    
    # INCLUA O CÓDIGO PARA MOSTRAR OS ARQUIVOS NA PASTA 
    # talvez você deva usar eval() ...
    s.send(bytes('os.listdir({})\n'.format(diretorio), 'utf-8'))
    time.sleep(2)
    resposta = s.recv(2048).decode()
    # print(type(resposta))
    resposta = ast.literal_eval(resposta)
    print(resposta)

# PASSO3: Inclua o código para verificar se o arquivo existe

print(os.getcwd())
print(os.listdir())

while True:

    arquivo = input('Digite o nome do arquivo para transferir: ')

    if not arquivo:
        print('<ENTER> encerra o programa')
        sys.exit()

    elif arquivo in resposta:
        print("Este arquivo ja existe no servidor!")

    elif not os.path.isfile(arquivo):
        print("Esse arquivo não existe no cliente")
    
    else:
        print("Ok!")
        break


#---------------------------------------------------------------------------------------------
# PASSO4: Inclua o código de UPLOAD AQUI 

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s2.bind(('', 9998))
    s2.listen(1)
except:
    print('# erro de bind')
    sys.exit()

# Envia ordem de upload aoservidor
s.send(bytes('upload({}\\{})\n'.format(diretorio,arquivo), 'utf-8'))

# Aguarda a conexão para criaro canal de dados
conn, addr = s2.accept()
print('Servidor {} fez a conexao'.format(addr))

# Chama a função que transfereo arquivo pelo canal de dados
Upload(arquivo, conn)
conn.close()
s2.close()

print('O arquivo foi transferido')
input('Digite <ENTER> para encerrar')