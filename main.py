import pygame
import random

pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego")
background_img = pygame.image.load("img/background.png")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Jugador
player_img = pygame.image.load("img/player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
player_inver=pygame.transform.flip(player_img, True, False)
player_size = 50
player_pos = [SCREEN_WIDTH / 2, SCREEN_HEIGHT - 2 * player_size]

# Enemigos
enemy_img = pygame.image.load("img/Spiked Ball.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
enemy_size = 50
enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

# Explosion
exp_img = pygame.image.load("img/explosion.png")
exp_img = pygame.transform.scale(exp_img, (32,16))
exp_pos = [0, 0]
exp_duration = 15  # Duración de la explosión en frames
exp_counter = 0

# Velocidad y puntaje
SPEED = 10
SCORE = 0

clock = pygame.time.Clock()

# Funciones
def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, SCREEN_WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < SCREEN_HEIGHT - 100:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
            exp_pos[0] = enemy_pos[0]
            exp_pos[1] = enemy_pos[1] + 30
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size-15)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size-15)):
            return True
    return False

# Game Loop
running = True
pause = False
right = True
collision = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_LEFT:
                x -= player_size
                right = False
            elif event.key == pygame.K_RIGHT:
                x += player_size
                right = True
            player_pos = [x, y]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = not pause

    if not pause and not collision:
        screen.blit(background_img, (0, -185))

        # Actualizar posición de los enemigos
        drop_enemies(enemy_list)
        SCORE = update_enemy_positions(enemy_list, SCORE)

        # Dibujar enemigos
        for enemy_pos in enemy_list:
            screen.blit(enemy_img, (enemy_pos[0], enemy_pos[1]))
    
        # Dibujar jugador
        if right:
            screen.blit(player_img, (player_pos[0], player_pos[1]))
        else:
            screen.blit(player_inver, (player_pos[0], player_pos[1]))
            
        # Dibujar explosion 
        if exp_counter < exp_duration and exp_pos != [0, 0]:
            screen.blit(exp_img, (exp_pos[0], exp_pos[1]))
            exp_counter += 1
        else:
            exp_pos = [0, 0]
            exp_counter = 0

        # Mostrar puntuación
        font = pygame.font.SysFont(None, 25)
        score_text = font.render("Score: " + str(SCORE), True, BLACK)
        screen.blit(score_text, [0, 0])
        
        # Detectar colisión
        if collision_check(enemy_list, player_pos):
            collision = True

        pygame.display.update()
        
    # Pausa
    elif pause and not collision:
        font = pygame.font.SysFont(None, 50)
        pause_text = font.render("Juego Pausado", True, WHITE)
        screen.blit(pause_text, [SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25])

        pygame.display.update()
    
    # Juego terminado
    else:
        font = pygame.font.SysFont(None, 50)
        font_c = pygame.font.SysFont(None, 30)
        end_text = font.render("Game Over", True, WHITE)
        end_text_c = font_c.render("Cierra la ventana para salir", True, WHITE)
        screen.blit(end_text, [SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25])
        screen.blit(end_text_c, [SCREEN_WIDTH // 2 - 135, SCREEN_HEIGHT // 2 + 15])
        
        pygame.display.update()

    clock.tick(30)

pygame.quit()