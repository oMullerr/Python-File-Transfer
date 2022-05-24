import socket
import sys
import time
import os

HOST = '127.0.0.1'          # IP do servidor
PORT = 9999                 #Porta do servidor

# Coloque a função de Download aqui

def Download(path, conn):
    # AQUI 5: Obtenha o nome do arquivo a partir do path
    file = os.path.basename(path)
    # Abrir o arquivo em modo escrita
    f = open(file, 'wb')
    while True:
    # Receber os dados da conexão em blocos de 1000 bytes
        data = conn.recv(1000)
        print("data: ", len(data))
        if len(data) == 0 or data is None:
            break
        else:
            # Escrever os dados no arquivo
            f.write(data)
    # Quando o servidor encerrar a conexão, fechar o arquivo
    f.close()
    return None

def selPastaLocal():

    # AQUI 1: Lista o diretorio atual e seu conteudo
    print('Diretorio atual:', os.getcwd())
    print('Conteudo da pasta:', os.listdir())
    # Cria uma pasta para receber os arquivos de download (opcional)
    dir = input('Escolha a pasta de Download ou <ENTER> para manter a atual: ')
    if len(dir) > 0:
        try:
            # AQUI 2: cria e seta o novo diretório
            # print('Esqueci o AQUI 2')
            if not os.path.isdir(dir):
                os.makedirs(dir)
            os.chdir(dir)
            print('Pasta Download:', os.getcwd())
        except:
            print('Pasta Download:', os.getcwd())
  
def arquivoRemoto(s):
    # Lista o diretorio no servidor remoto
    s.send(bytes('os.listdir()\n', 'utf-8'))
    time.sleep(2) #essa espera é para receber a resposta completa sem ter que criarum while
    resposta = s.recv(2048).decode()
    print('Conteudo remoto: ', resposta)

    # Seleciona um subdiretório
    dir = input('Digite a pasta de Upload (Remota) ou <ENTER> para manter a mesma: ')
    
    if len(dir) > 0:
        if dir not in eval(resposta):
            print('Esse diretorio não pode ser selecionado')
        else:
            # AQUI 3: Envia o comando para o servidor listar o diretorio selecionado
            # print('Esqueci o AQUI 3') 
            s.send(f'os.listdir({dir})\n'.encode())
            time.sleep(2) 
            resposta = s.recv(2048).decode()
            print('Conteudo remoto: ', resposta)

    # Selecione o arquivo para download
    file = input('selecione o arquivo para download: ')
    if file not in eval(resposta):
        print('esse arquivo nao existe')
        # selecionar o primeiro arquivo
        file = eval(resposta)[0]

    # AQUI 4: Retorna o caminho para um arquivo da lista 
    # print('Esqueci o AQUI 4')
    return os.path.join(dir, file)
   # return None

#--------------------------------------------------------------------
# Incio do código principal
pydir=  os.path.dirname(os.path.realpath(__file__))
print('Diretorio do script: ', pydir)
os.chdir(pydir)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
except:
    print('# erro de conexao')
    sys.exit()

print('selecao da pasta local ...')
selPastaLocal()

print('selecao do arquivo remoto ...')
remoto = arquivoRemoto(s)

if not remoto:
    print('O arquivo remoto não foi selecionado. Bye!!!')
    sys.exit()

print(remoto)

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s2.bind(('', 9998))
    s2.listen(1)
except:
    print('# erro de bind')
    sys.exit()

# Envia ordem de download ao servidor
s.send('download({})\n'.format(remoto).encode())

# Aguarda a conexão para criaro canal de dados
conn, addr = s2.accept()
print('Servidor {} fez a conexao'.format(addr))

# Chamada para rotina de download
Download(remoto, conn)
conn.close()
s2.close()

print('O arquivo foi transferido')
input('Digite <ENTER> para encerrar')

s.close()