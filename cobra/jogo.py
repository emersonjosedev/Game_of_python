import pygame
from pygame.locals import *
from random import randint
from datetime import date
import os.path #modulo para verificar se arquivo existe no modulo de salvar arquivo

pygame.init()

pygame.mixer.music.set_volume(0.2)
musica_de_fundo = pygame.mixer.music.load('audio\Eggy_Toast_-_Enemies_of_the_People.mp3')
pygame.mixer.music.play(-1)

barulho_morte = pygame.mixer.Sound('audio/ta-snes_bowser_laugh.wav')
barulho_colisao = pygame.mixer.Sound('audio\smw_vine.wav')
background = pygame.image.load('fundos\cenario2.png')
bg_gameover = pygame.image.load('fundos\gameover.png')
musica_fim = pygame.mixer.Sound('audio/Game Over -  Kof 2002(MP3_160K)(3)(2)(2).wav')


#cores utilizadas

preto = (0,0,0)
branco = (255,255,255)
verde = (0, 255, 0)
azul = (0, 0, 255)
vermelho = (255, 0, 0)
rosa = (255, 0, 255)

#cria arquivo ou abre, adiciona os dados
def salvararquivo(usuario, score):
    arquivoexiste = os.path.exists('scoresalvar.txt')
    data_atual = date.today()
    data_em_texto = data_atual.strftime('%d/%m/%Y')
    if arquivoexiste == True:
        f = open("scoresalvar.txt", 'a')
        f.write(f"\n{data_em_texto}, {usuario}, {score}")
        f.close()
    else:
        f = open("scoresalvar.txt", 'w')
        f.write(f"{data_em_texto}, {usuario}, {score}")
        f.close()
    return print("Seu Score foi Salvo")

#função para ler arquivo e definir o score máximo
# verifica se o arquivo existe, se não, define scoremax = 0
def highscore():
    arquivoexiste = os.path.exists('scoresalvar.txt')
    if arquivoexiste == True:
        arquivo = open("scoresalvar.txt", 'r')

        lista = []

        for item in arquivo:
            item = item.replace("\n", "")
            item = item.split(',')
            lista.append(item)
        scoremax = 0
        for item in lista:
            if int(item[2]) > scoremax:
                scoremax = int(item[2])
    else:
        scoremax = 0
    return scoremax

def on_grid_random(m,n):
    x = randint(m,n)
    return x//10*10

class tela_pos:
    def __init__(self,largura=640,altura=480):
        self.largura = largura
        self.altura = altura

class cobra_pos(tela_pos):
    def __init__(self,largura,altura):
        super().__init__(largura,altura)

tamanho_tela = tela_pos()

largura = tamanho_tela.largura
altura = tamanho_tela.altura

tamanho_cobra = cobra_pos(largura,altura)

x_cobra = int(tamanho_cobra.largura / 2)
y_cobra = int(tamanho_cobra.altura / 2)

velocidade = 10
x_controle = velocidade
y_controle = 0

x_maca = on_grid_random(40, 600)
y_maca = on_grid_random(50, 430)


pontos = 0
maxpontos = highscore()
fonte = pygame.font.SysFont('arial', 30, bold=True, italic=True)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Game of Python')
relogio = pygame.time.Clock()
lista_cobra = []
comprimento_inicial = 5
morreu = False

maca_image = pygame.image.load('sprites/red-apple-removebg-preview (1).png')

def aumenta_cobra(lista_cobra):
    for tile in range(len(lista_cobra)):
        if (tile == 0 and len(lista_cobra) > 1):  # Rabo
            snake_tail = pygame.image.load('sprites/tail_up.png')
            if(lista_cobra[tile][0] > lista_cobra[tile+1][0] and lista_cobra[tile][1] == lista_cobra[tile+1][1]):
                snake_tail = pygame.image.load('sprites/tail_right.png')
            if(lista_cobra[tile][0] < lista_cobra[tile+1][0] and lista_cobra[tile][1] == lista_cobra[tile+1][1]):
                snake_tail = pygame.image.load('sprites/tail_left.png')
            if(lista_cobra[tile][0] == lista_cobra[tile+1][0] and lista_cobra[tile][1] > lista_cobra[tile+1][1]):
                snake_tail = pygame.image.load('sprites/tail_down.png')
            if(lista_cobra[tile][0] == lista_cobra[tile+1][0] and lista_cobra[tile][1] < lista_cobra[tile+1][1]):
                snake_tail = pygame.image.load('sprites/tail_up.png')
            tela.blit(snake_tail, (lista_cobra[tile][0], lista_cobra[tile][1]))
        elif (lista_cobra[tile] == lista_cobra[-1] and len(lista_cobra) > 1):  # Cabeca
            snake_head = pygame.image.load('sprites/head_up1.gif')
            if(lista_cobra[tile][0] > lista_cobra[tile-1][0] and lista_cobra[tile][1] == lista_cobra[tile-1][1]):
                snake_head = pygame.image.load('sprites/head_right.png')
            if(lista_cobra[tile][0] < lista_cobra[tile-1][0] and lista_cobra[tile][1] == lista_cobra[tile-1][1]):
                snake_head = pygame.image.load('sprites/head_left.png')
            if(lista_cobra[tile][0] == lista_cobra[tile-1][0] and lista_cobra[tile][1] > lista_cobra[tile-1][1]):
                snake_head = pygame.image.load('sprites/head_down.png')
            if(lista_cobra[tile][0] == lista_cobra[tile-1][0] and lista_cobra[tile][1] < lista_cobra[tile-1][1]):
                snake_head = pygame.image.load('sprites/head_up.gif')
            tela.blit(snake_head, (lista_cobra[tile][0], lista_cobra[tile][1]))
        elif(len(lista_cobra) > 1):  # Corpo
            snake_body = pygame.image.load('sprites/body_horizontal.png')
            if(lista_cobra[tile][0] > lista_cobra[tile-1][0] and lista_cobra[tile][1] < lista_cobra[tile+1][1]) or (lista_cobra[tile][1] < lista_cobra[tile-1][1] and lista_cobra[tile][0] > lista_cobra[tile+1][0]):
                snake_body = pygame.image.load('sprites/body_bottomleft.png')
            elif(lista_cobra[tile][0] < lista_cobra[tile-1][0] and lista_cobra[tile][1] > lista_cobra[tile+1][1]) or (lista_cobra[tile][1] > lista_cobra[tile-1][1] and lista_cobra[tile][0] < lista_cobra[tile+1][0]):
                snake_body = pygame.image.load('sprites/body_topright.png')
            elif(lista_cobra[tile][0] < lista_cobra[tile-1][0] and lista_cobra[tile][1] < lista_cobra[tile+1][1]) or (lista_cobra[tile][1] < lista_cobra[tile-1][1] and lista_cobra[tile][0] < lista_cobra[tile+1][0]):
                snake_body = pygame.image.load('sprites/body_bottomright.png')
            elif(lista_cobra[tile][0] > lista_cobra[tile-1][0] and lista_cobra[tile][1] > lista_cobra[tile+1][1]) or (lista_cobra[tile][1] > lista_cobra[tile-1][1] and lista_cobra[tile][0] > lista_cobra[tile+1][0]):
                snake_body = pygame.image.load('sprites/body_topleft.png')
            elif(lista_cobra[tile][0] == lista_cobra[tile-1][0]):
                snake_body = pygame.image.load('sprites/body_vertical.png')
            elif(lista_cobra[tile][1] == lista_cobra[tile-1][1]):
                snake_body = pygame.image.load('sprites/body_horizontal.png')
            tela.blit(snake_body, (lista_cobra[tile][0], lista_cobra[tile][1]))

def reiniciar_jogo():
    global pontos,maxpontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeca, x_maca, y_maca, morreu
    pontos = 0
    maxpontos = highscore()
    comprimento_inicial = 5
    x_cobra = int(largura / 2)
    y_cobra = int(altura / 2)
    lista_cobra = []
    lista_cabeca = []
    x_maca = on_grid_random(40, 600)
    y_maca = on_grid_random(50, 430)
    morreu = False
    pygame.mixer.stop()
    pygame.mixer.music.play()

while True:
    relogio.tick(20)
    #tela.fill(branco)
    tela.blit(background, (0,0))

    mensagem = f'score: {pontos}'

    texto_formatado = fonte.render(mensagem, True, preto)

    mensagem2 = f'Highscore: {maxpontos}'
    texto_formatado2 = fonte.render(mensagem2, True, vermelho)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    y_controle = -velocidade
                    x_controle = 0
            if event.key == K_s:
                if y_controle == -velocidade:
                    pass
                else:
                    y_controle = velocidade
                    x_controle = 0

    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle

    cobra = pygame.draw.rect(tela, vermelho, (x_cobra+10, y_cobra+10, 20, 20),1)

    maca = tela.blit(maca_image,(x_maca, y_maca))

    pygame.draw.line(tela, preto, (636, 0), (636, 480), 7)
    pygame.draw.line(tela, preto, (0, 478), (640, 478), 7)
    pygame.draw.line(tela, preto, (0, 2), (640, 2), 7)
    pygame.draw.line(tela, preto, (2, 0), (2, 475), 7)

    if cobra.colliderect(maca):
        x_maca = on_grid_random(40, 600)
        y_maca = on_grid_random(50, 430)
        pontos += 1
        barulho_colisao.play()
        comprimento_inicial += 1

    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)

    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1:
        salvararquivo("computador", pontos)
        pygame.mixer_music.stop()
        musica_fim.play()

        fonte2 = pygame.font.SysFont('arial', 20, True, True)
        mensagem = 'Pressione 1 para jogar novamente ou 2 para sair '
        texto_formatado = fonte2.render(mensagem, True, branco)
        ret_texto = texto_formatado.get_rect()

        morreu = True
        while morreu:
            #tela.fill(branco)
            tela.blit(bg_gameover, (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_2:
                        print('Obrigado por jogar')
                        pygame.quit()
                        exit()
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        reiniciar_jogo()

            ret_texto.center = (largura // 2, altura // 2)
            tela.blit(texto_formatado, ret_texto)

            pygame.display.update()

    if x_cobra > largura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largura
    if y_cobra < 0:
        y_cobra = altura
    if y_cobra > altura:
        y_cobra = 0

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    tela.blit(texto_formatado, (450, 40))
    tela.blit(texto_formatado2, (50, 40))

    pygame.display.update()