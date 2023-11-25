import pygame
import sys
import random

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Space war')

# Carregar as imagens de fundo
fundo1 = pygame.image.load('space.png')
fundo2 = pygame.image.load('space2.png')
fundo_atual = fundo1  # Começa com o primeiro fundo

# Carregar a fonte para exibir a pontuação
fonte = pygame.font.Font(None, 36)

# Criar uma classe para representar o jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('ship.png')
        self.rect = self.image.get_rect()
        self.rect.center = (largura // 2, altura - 50)
        self.vida = 3  # Adiciona um contador de vidas
        self.velocidade_disparo = -10  # Velocidade do disparo

    def update(self):
        # Atualizar a posição do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidade_jogador
        if keys[pygame.K_RIGHT] and self.rect.right < largura:
            self.rect.x += velocidade_jogador
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= velocidade_jogador
        if keys[pygame.K_DOWN] and self.rect.bottom < altura:
            self.rect.y += velocidade_jogador

        # Verificar o disparo
        if keys[pygame.K_SPACE]:
            self.disparar()

    def disparar(self):
        novo_projetil = Projetil(self.rect.centerx, self.rect.top)
        todos_sprites.add(novo_projetil)
        projeteis.add(novo_projetil)

# Criar uma classe para representar os projéteis
class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # Atualizar a posição do projétil
        self.rect.y += jogador.velocidade_disparo
        if self.rect.bottom < 0:
            self.kill()  # Remover o projétil quando sair da tela

# Criar uma classe para representar os inimigos
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('ship2.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura - 50)
        self.rect.y = 0

    def update(self):
        # Atualizar a posição do inimigo
        self.rect.y += velocidade_inimigo

        # Verificar colisões com tiros do jogador
        colisoes_tiros_jogador = pygame.sprite.spritecollide(self, projeteis, True)
        for tiro_jogador in colisoes_tiros_jogador:
            aumentar_pontuacao()
            self.kill()  # Remover inimigo quando atingido por um tiro


# Criar uma classe para representar os tiros dos inimigos
class TiroInimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_tiro_inimigo = 5

    def update(self):
        self.rect.y += self.velocidade_tiro_inimigo
        if self.rect.top > altura:
            self.kill()


# Criar uma função para tratar a colisão entre o jogador e os tiros inimigos
def colisao_jogador_tiro_inimigo(jogador, tiros_inimigos):
    colisoes = pygame.sprite.spritecollide(jogador, tiros_inimigos, True)
    for colisao in colisoes:
        jogador.vida -= 1
        if jogador.vida <= 0:
            fim_de_jogo()

def aumentar_pontuacao():
    global pontuacao, fundo_atual
    pontuacao += 1
    print(f'Pontuação: {pontuacao}')

    # Mudar o cenário após 100 inimigos mortos
    if pontuacao % 100 == 0:
        if fundo_atual == fundo1:
            fundo_atual = fundo2
        else:
            fundo_atual = fundo1

    # Verificar se a pontuação atingiu 1000 pontos
    if pontuacao >= 1000:
        fim_de_jogo()


def fim_de_jogo():
    global pontuacao, fundo_atual, rodando

    print("Fim de Jogo!")
    print(f"Sua pontuação final: {pontuacao}")

    # Exibir opções de continuar o jogo ou sair
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_c:
                    reiniciar_jogo()
                    return  # Adicione isso para sair do loop quando o jogo for reiniciado
                elif evento.key == pygame.K_s:
                    pygame.quit()
                    sys.exit()

        # Desenhar a tela de fim de jogo
        tela.fill((0, 0, 0))
        texto_fim_de_jogo = fonte.render("Fim de Jogo", True, (255, 255, 255))
        texto_pontuacao_final = fonte.render(f"Sua pontuação final: {pontuacao}", True, (255, 255, 255))
        texto_opcoes = fonte.render("Pressione 'C' para continuar ou 'S' para sair", True, (255, 255, 255))

        tela.blit(texto_fim_de_jogo, (largura // 2 - texto_fim_de_jogo.get_width() // 2, altura // 2 - 50))
        tela.blit(texto_pontuacao_final, (largura // 2 - texto_pontuacao_final.get_width() // 2, altura // 2))
        tela.blit(texto_opcoes, (largura // 2 - texto_opcoes.get_width() // 2, altura // 2 + 50))

        pygame.display.flip()

        clock.tick(60)



def reiniciar_jogo():
    global pontuacao, fundo_atual
    pontuacao = 0
    fundo_atual = fundo1

    todos_sprites.empty()
    inimigos.empty()
    projeteis.empty()
    tiros_inimigos.empty()

    jogador.vida = 3
    jogador.rect.center = (largura // 2, altura - 50)
    todos_sprites.add(jogador)

# Criar grupos de sprites
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
projeteis = pygame.sprite.Group()
tiros_inimigos = pygame.sprite.Group()

velocidade_jogador = 5
velocidade_inimigo = 3

jogador = Jogador()
todos_sprites.add(jogador)

pontuacao = 0

rodando = True
clock = pygame.time.Clock()
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False


    todos_sprites.update()

    # Verificar colisões entre projéteis e inimigos
    colisoes_tiros_jogador = pygame.sprite.groupcollide(projeteis, inimigos, True, True)
    for tiro_jogador in colisoes_tiros_jogador:
        aumentar_pontuacao()

    # Atualizar a posição dos tiros dos inimigos
    for inimigo in inimigos:
        if random.randint(0, 100) < 5:
            novo_tiro_inimigo = TiroInimigo(inimigo.rect.centerx, inimigo.rect.bottom)
            todos_sprites.add(novo_tiro_inimigo)
            tiros_inimigos.add(novo_tiro_inimigo)

    colisoes_jogador_tiro_inimigo = pygame.sprite.spritecollide(jogador, tiros_inimigos, True)
    for tiro_inimigo in colisoes_jogador_tiro_inimigo:
        jogador.vida -= 1
        if jogador.vida <= 0:
            fim_de_jogo()

    # Criar inimigos aleatórios
    if random.randint(0, 100) < 5:
        novo_inimigo = Inimigo()
        todos_sprites.add(novo_inimigo)
        inimigos.add(novo_inimigo)

    # Desenhar o fundo
    tela.blit(fundo_atual, (0, 0))

    # Desenhar os sprites
    todos_sprites.draw(tela)

    # Exibir a pontuação na tela
    texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
    tela.blit(texto_pontuacao, (10, 10))

    # Exibir o número de vidas do jogador
    texto_vida = fonte.render(f'Vidas: {jogador.vida}', True, (255, 255, 255))
    tela.blit(texto_vida, (largura - 120, 10))

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
sys.exit()
