import re

def le_assinatura():
    '''A funcao le os valores dos tracos linguisticos do modelo e devolve uma assinatura a ser comparada com os textos fornecidos'''
    print("Bem-vindo ao detector automático de COH-PIAH.")
    print("Informe a assinatura típica de um aluno infectado:")

    wal = float(input("Entre o tamanho médio de palavra:"))
    ttr = float(input("Entre a relação Type-Token:"))
    hlr = float(input("Entre a Razão Hapax Legomana:"))
    sal = float(input("Entre o tamanho médio de sentença:"))
    sac = float(input("Entre a complexidade média da sentença:"))
    pal = float(input("Entre o tamanho medio de frase:"))

    return [wal, ttr, hlr, sal, sac, pal]

def le_textos():
    '''A funcao le todos os textos a serem comparados e devolve uma lista contendo cada texto como um elemento'''
    i = 1
    textos = []
    texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")
    while texto:
        textos.append(texto)
        i += 1
        texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")

    return textos

def separa_sentencas(texto):    #  parametro 1 wal
    '''A funcao recebe um texto e devolve uma lista das sentencas dentro do texto'''
    sentencas = re.split(r'[.!?]+', texto)
    if sentencas[-1] == '':
        del sentencas[-1]
    return sentencas

def separa_frases(sentenca):    #  parametro 1 wal
    '''A funcao recebe uma sentenca e devolve uma lista das frases dentro da sentenca'''
    return re.split(r'[,:;]+', sentenca)

def separa_palavras(frase):    #  parametro 1 wal
    '''A funcao recebe uma frase e devolve uma lista das palavras dentro da frase'''
    return frase.split()

def n_palavras_unicas(lista_palavras):      #  parametro 3 hlr
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras que aparecem uma unica vez'''
    freq = dict()
    unicas = 0
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            if freq[p] == 1:
                unicas -= 1
            freq[p] += 1
        else:
            freq[p] = 1
            unicas += 1

    return unicas

def n_palavras_diferentes(lista_palavras):      #  parametro 2 ttr
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras diferentes utilizadas'''
    freq = dict()
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1

    return len(freq)

def compara_assinatura(as_a, as_b):
    '''Essa funcao recebe duas assinaturas de texto e deve devolver o grau de similaridade nas assinaturas.'''
    somatorio = 0
    for tracos in range(6):
        somatorio += abs(as_a[tracos] - as_b[tracos])
    similaridade = somatorio/6
    return similaridade

def calcula_assinatura(texto):
    '''Essa função recebe um texto e deve devolver a assinatura do texto.'''
    sentencas = separa_sentencas(texto)     #  lista das sentenças dentro do texto
    frases = []
    palavras = []
    for sentenca in sentencas:              #  preciso criar uma lista com todas as frases (concatenar frases de cada sentença)
        frases += separa_frases(sentenca)   #  frases: É uma lista com todas as frases do texto
    for frase in frases:
        palavras += separa_palavras(frase)  #  palavras: É uma lista com todas as palavras do texto
    qtd_palavras = len(palavras)
    qtd_frases = len(frases)
    qtd_sentencas = len(sentencas)
    
    wal = calcula_wal(palavras, qtd_palavras)
    ttr = calcula_ttr(palavras, qtd_palavras)
    hlr = calcula_hlr(palavras, qtd_palavras)
    sal = calcula_sal(sentencas, qtd_sentencas)
    sac = qtd_frases/qtd_sentencas
    pal = calcula_pal(frases, qtd_frases)
    return [wal, ttr, hlr, sal, sac, pal]   #  assinatura de um texto fornecido

def avalia_textos(textos, ass_cp):
    '''IMPLEMENTAR Essa função recebe uma lista de textos e uma assinatura ass_cp e deve devolver o numero (1 a n) do texto com maior probabilidade de ter sido infectado por COH-PIAH.'''
    menor_grau = compara_assinatura(calcula_assinatura(textos[0]), ass_cp)
    n_menor_grau = 0
    for texto in range(len(textos)):
        ass_texto = calcula_assinatura(textos[texto])
        if compara_assinatura(ass_texto, ass_cp) < menor_grau:
            menor_grau = compara_assinatura(ass_texto, ass_cp)
            n_menor_grau = texto
    n_menor_grau += 1
    return n_menor_grau

def calcula_wal(palavras, qtd_palavras):
    '''Essa função recebe uma lista de palavras e sua extensão e devolve o tamanho médio da palavra. parametro = 1'''
    tamanho_total_palavras = 0
    for palavra in palavras:
        tamanho_total_palavras += len(palavra)
    wal = tamanho_total_palavras/qtd_palavras
    return wal

def calcula_ttr(palavras, qtd_palavras):
    '''Essa função recebe uma lista de palavras e sua extensão e devolve a Relação Type-Token'''
    palavras_diferentes = n_palavras_diferentes(palavras)
    ttr = palavras_diferentes/qtd_palavras
    return ttr

def calcula_hlr(palavras, qtd_palavras):
    '''Essa função recebe uma lista de palavras e sua extensão e devolve a Razão Hapax Legomana'''
    palavras_unicas = n_palavras_unicas(palavras)
    hlr = palavras_unicas/qtd_palavras
    return hlr

def calcula_sal(sentencas, qtd_sentencas):
    '''Essa função recebe uma lista de sentenças e sua extensão e devolve o tamanho médio de sentença'''
    caracteres_totais_sentenca = 0
    for sentenca in sentencas:
        caracteres_totais_sentenca += len(sentenca)
    sal = caracteres_totais_sentenca/qtd_sentencas
    return sal

def calcula_pal(frases, qtd_frases):
    caracteres_totais_frase = 0
    for frase in frases:
        caracteres_totais_frase += len(frase)
    pal = caracteres_totais_frase/qtd_frases
    return pal

def main():
    ass_cp = le_assinatura()
    textos = le_textos()
    autor = avalia_textos(textos, ass_cp)
    print ("O autor do texto {} está infectado com COH-PIAH".format(autor))
    
main()
