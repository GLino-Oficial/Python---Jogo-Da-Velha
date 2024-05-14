import pygame
import sys
import random

# Inicializando o Pygame
pygame.init()

# Definindo as constantes
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
# Cores
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (128, 0, 128)  # Roxo
CROSS_COLOR = (255, 0, 0)  # Vermelho
TEXT_COLOR = (255, 255, 255)
TRANSPARENT_BLACK = (0, 0, 0, 128)

# Configurando a janela do jogo
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Velha")
win.fill(BG_COLOR)

# Tabuleiro
board = [[None]*BOARD_COLS for _ in range(BOARD_ROWS)]

# Fonte
font = pygame.font.SysFont(None, 50)

# Funções
def desenhar_linhas():
    # Linhas horizontais
    pygame.draw.line(win, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(win, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Linhas verticais
    pygame.draw.line(win, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(win, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def desenhar_figuras():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(win, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                pygame.draw.line(win, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(win, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def marca_casa(row, col, player):
    board[row][col] = player

def casa_disponivel(row, col):
    return board[row][col] is None

def tabuleiro_cheio():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_vitoria(player):
    # Verifica vitória nas linhas
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # Verifica vitória nas colunas
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    # Verifica vitória nas diagonais
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def reiniciar_jogo():
    win.fill(BG_COLOR)
    desenhar_linhas()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

def desenhar_jogo():
    desenhar_linhas()
    desenhar_figuras()
    pygame.display.update()

def fazer_jogada_maquina():
    # Implementação de uma IA simples que faz jogadas aleatórias
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if casa_disponivel(row, col):
            marca_casa(row, col, "X")
            break

def exibir_mensagem(mensagem):
    text_surface = font.render(mensagem, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    pygame.draw.rect(win, TRANSPARENT_BLACK, (WIDTH/4, HEIGHT/4, WIDTH/2, HEIGHT/2))
    win.blit(text_surface, text_rect)
    pygame.display.update()

# Variáveis
game_over = False

# Desenha o tabuleiro ao iniciar o jogo
desenhar_jogo()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] # x
            mouseY = event.pos[1] # y
            
            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            
            if casa_disponivel(clicked_row, clicked_col):
                marca_casa(clicked_row, clicked_col, "O")
                desenhar_jogo()
                if check_vitoria("O"):
                    exibir_mensagem("Você ganhou!")
                    game_over = True
                elif tabuleiro_cheio():
                    exibir_mensagem("Empate!")
                    game_over = True
                else:
                    fazer_jogada_maquina()
                    desenhar_jogo()
                    if check_vitoria("X"):
                        exibir_mensagem("Você perdeu!")
                        game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reiniciar_jogo()
                game_over = False
                desenhar_jogo()
    
    # Atualiza a janela
    pygame.display.update()
