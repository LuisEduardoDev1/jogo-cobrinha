import pygame
from pygame.locals import *
import random
import math

TAMANHO_JANELA = (600, 600)
TAMANHO_PIXEL = 10


CORES = [
    (0, 0, 255),    # Azul
    (0, 255, 0),    # Verde
    (255, 0, 0),    # Vermelho
    (255, 255, 255),    # Branco
    (255, 255, 0),    # Amarelo
    (255, 0, 255),    # Roxo
    (128, 128, 128),    # Cinza
    (139, 69, 19),    # Marrom
    (255, 165, 0),    # Laranja
    (255, 253, 208)    # Creme
]


def comer(pos1, pos2):
    return pos1 == pos2


def fora_dos_limites(pos):
    if 0 <= pos[0] < TAMANHO_JANELA[0] and 0 <= pos[1] < TAMANHO_JANELA[1]:
        return False
    else:
        return True


def posicao_aleatoria():
    x = random.randint(0, TAMANHO_JANELA[0] - TAMANHO_PIXEL)
    y = random.randint(0, TAMANHO_JANELA[1] - TAMANHO_PIXEL)
    return x // TAMANHO_PIXEL * TAMANHO_PIXEL, y // TAMANHO_PIXEL * TAMANHO_PIXEL


def reiniciar_jogo():
    global segmentos_cobra, direcao_cobra, maca, score, level
    segmentos_cobra = [{'pos': (250, 50), 'cor': random.choice(CORES)}]
    direcao_cobra = K_LEFT
    maca = {'pos': posicao_aleatoria(), 'cor': random.choice(CORES)}
    score = 0
    level = 1


pygame.init()
tela = pygame.display.set_mode(TAMANHO_JANELA)
pygame.display.set_caption('Jogo da Cobrinha')

segmentos_cobra = [{'pos': (250, 50), 'cor': random.choice(CORES)}]
direcao_cobra = K_LEFT

maca = {'pos': posicao_aleatoria(), 'cor': random.choice(CORES)}

score = 0
level = 1

botao_play = pygame.Rect(250, 250, 100, 50)
botao_play_hover = False

jogando = False

while True:
    velocidade = math.pow(2, level - 1) * 10

    pygame.time.Clock().tick(velocidade + 5)

    tela.fill((0, 0, 0))
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            quit()
        elif evento.type == MOUSEBUTTONDOWN:
            if evento.button == 1 and botao_play.collidepoint(evento.pos) and not jogando:
                jogando = True
                reiniciar_jogo()
        elif evento.type == KEYDOWN:
            if evento.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT] and jogando:
                direcao_cobra = evento.key

    if jogando:
        pygame.draw.rect(tela, maca['cor'], (maca['pos'][0], maca['pos'][1], TAMANHO_PIXEL, TAMANHO_PIXEL))

        for segmento in segmentos_cobra:
            pygame.draw.rect(tela, segmento['cor'], (segmento['pos'][0], segmento['pos'][1], TAMANHO_PIXEL, TAMANHO_PIXEL))

        if comer(maca['pos'], segmentos_cobra[0]['pos']):
            if maca['cor'] == segmentos_cobra[0]['cor']:
                segmentos_cobra.pop(0)
                score -= 1
            else:
                score += 1
                novo_segmento = {'pos': segmentos_cobra[-1]['pos'], 'cor': maca['cor']}
                segmentos_cobra.append(novo_segmento)

            if score % 10 == 0 and score != 0:
                level += 1

            maca = {'pos': posicao_aleatoria(), 'cor': random.choice(CORES)}

        for i in range(len(segmentos_cobra) - 1, 0, -1):
            segmentos_cobra[i]['pos'] = segmentos_cobra[i - 1]['pos']

        if direcao_cobra == K_UP:
            segmentos_cobra[0]['pos'] = (segmentos_cobra[0]['pos'][0], segmentos_cobra[0]['pos'][1] - TAMANHO_PIXEL)
        elif direcao_cobra == K_DOWN:
            segmentos_cobra[0]['pos'] = (segmentos_cobra[0]['pos'][0], segmentos_cobra[0]['pos'][1] + TAMANHO_PIXEL)
        elif direcao_cobra == K_LEFT:
            segmentos_cobra[0]['pos'] = (segmentos_cobra[0]['pos'][0] - TAMANHO_PIXEL, segmentos_cobra[0]['pos'][1])
        elif direcao_cobra == K_RIGHT:
            segmentos_cobra[0]['pos'] = (segmentos_cobra[0]['pos'][0] + TAMANHO_PIXEL, segmentos_cobra[0]['pos'][1])

        if fora_dos_limites(segmentos_cobra[0]['pos']):
            reiniciar_jogo()

        for segmento in segmentos_cobra[1:]:
            if comer(segmentos_cobra[0]['pos'], segmento['pos']):
                reiniciar_jogo()
                break

        fonte = pygame.font.Font(None, 36)
        texto_score = fonte.render("Score: " + str(score), True, (255, 255, 255))
        texto_level = fonte.render("Level: " + str(level), True, (255, 255, 255))
        tela.blit(texto_score, (10, 10))
        tela.blit(texto_level, (10, 50))
    else:
        if botao_play.collidepoint(pygame.mouse.get_pos()):
            botao_play_hover = True
        else:
            botao_play_hover = False

        pygame.draw.rect(tela, (0, 255, 0) if botao_play_hover else (0, 200, 0), botao_play)
        fonte = pygame.font.Font(None, 24)
        superficie_texto = fonte.render("Play", True, (255, 255, 255))
        texto = superficie_texto.get_rect(center=botao_play.center)
        tela.blit(superficie_texto, texto)

    pygame.display.update()
