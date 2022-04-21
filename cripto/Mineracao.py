from hashlib import sha256
import time

zeros = 7

def hash(texto):
    return sha256(texto.encode('ascii')).hexdigest()

def minerar(numBloco, transacoes, hashAnt, zeros):
    qtdZeros = '0' * zeros
    naoAchei = True
    nonce = 0

    while naoAchei:
        hashBloco = str(numBloco) + transacoes + hashAnt + str(nonce)
        hashAtual = hash(hashBloco)
        nonce += 1

        if hashAtual.startswith(qtdZeros):
            naoAchei = False
            print(f'Nonce encontrado: {nonce}')
            return hashAtual


transacoes = '''
Fabricio-Joao-100
Antonio-Flavio-20
Pedro-Marina-47
'''

if __name__ == '__main__':
    inicio = time.time()
    print('Início da mineração')
    hashAtual = minerar(732893, transacoes, '00000000000000000004743a01574b81366a690037542a34fb5cedbced5cc005', zeros)
    total = str((time.time() - inicio))
    print(f'Fim da mineração. Tempo de processamento: {total}')
    print(hashAtual)


