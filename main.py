import pygame 
import time 
import random 
import os

pygame.font.init()
pygame.mixer.init()

HIT_SOUND = pygame.mixer.Sound("hit.wav")

pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.set_volume(0.5)

WIDTH, HEIGHT = 800,600
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 120
PLAYER_VELOCITY = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3



WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Wizard Dash")
FONT = pygame.font.SysFont("comicsans",40)

FRAMES = []
for i in range(0,24):
    img = pygame.image.load(f"frames/frame_{i}.png").convert_alpha()
    FRAMES.append(img)

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH,HEIGHT))

def draw(player, elapsed_time, stars):
    WIN.blit(BG,(0,0))
    time_text = FONT.render(f"TIME: {round(elapsed_time)}s", 1, "lightyellow")
    WIN.blit(time_text, (10,10))
    

    # Animate the player
    frame_index = int((pygame.time.get_ticks() / 100) % len(FRAMES))
    frame = pygame.transform.scale(FRAMES[frame_index], (PLAYER_WIDTH, PLAYER_HEIGHT))
    WIN.blit(frame, (player.x, player.y))
    

    for star in stars:
        pygame.draw.rect(WIN,"gold",star)
    pygame.display.update()


def main():
    run = True
    pygame.mixer.music.play(-1)

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars =[]
    hit = False


    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, - STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(150, star_add_increment-50)
            star_count = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >=0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                HIT_SOUND.play()
                hit = True
                break
        if hit:
            lost_text = FONT.render("You Lost!",1,"crimson")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
        draw(player, elapsed_time, stars)

    
    pygame.quit()
   

if __name__ == "__main__":
    main()
    
            