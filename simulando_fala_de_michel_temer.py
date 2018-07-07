import nltk
from nltk import sent_tokenize, word_tokenize
from nltk import trigrams
from collections import defaultdict
import random

def criar_fala_de_temer(model):
    text = [None, None]
    sentence_finished = False
    prob = 1.0
    while not sentence_finished:
        r = random.random()
        accumulator = .0
     
        for word in model[tuple(text[-2:])].keys():
            accumulator += model[tuple(text[-2:])][word]
            if accumulator >= r:
                if model[tuple(text[-2:])][word] != 0.0:
                    prob *= model[tuple(text[-2:])][word]
                text.append(word)
                break
     
        if text[-2:] == [None, None]:
            sentence_finished = True

    return ' '.join([t for t in text if t]) 

def main():
    discursos = open('texto_discursos.txt', 'r').readlines()
    lista_sentencas  = [sent_tokenize(discurso) for discurso in discursos]
    todas_sentencas = []
    for lista in lista_sentencas:
        todas_sentencas += lista
    sentencas_com_palavras_tokenizadas = [word_tokenize(sentenca) for sentenca in todas_sentencas]

    model = defaultdict(lambda: defaultdict(lambda: 0))

    # contando os trigramas
    for sentence in sentencas_com_palavras_tokenizadas:
        for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
            model[(w1, w2)][w3] += 1

    # estimativa das probabilidade
    # dos trigramas usando 
    # a máxima verossimilhança
    for w1_w2 in model:
        total_count = float(sum(model[w1_w2].values()))
        for w3 in model[w1_w2]:
            if total_count > 0:
                model[w1_w2][w3] /= total_count
            else:
                 model[w1_w2][w3] = 0.0

    fala = criar_fala_de_temer(model)
    print(fala)

if __name__=='__main__':
    main()
