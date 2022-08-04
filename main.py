import pygame
import os

pygame.font.init()
pygame.mixer.init()


WIDTH = 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("YOOOOOOOOOOO")
PINK = (189, 115, 183)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
BLUE = (135, 224, 236)
BAR_WIDTH = 10
# // for int division because Rect cant take float only int
MIDDLE_BAR = pygame.Rect(WIDTH//2 - BAR_WIDTH//2, 0, BAR_WIDTH, HEIGHT)


BEAM_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Hit-moan.mp3'))
BEAM_BLAST_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'beam-blast.mp3'))
WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'win-sound.mp3'))
print(BEAM_HIT_SOUND.get_volume())
BEAM_BLAST_SOUND.set_volume(.35)
print(BEAM_BLAST_SOUND.get_volume())
print(WIN_SOUND.get_volume())

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#controls the while loop to only run 60 times a second
FPS = 60
#vel is used for how much the player moves each key press
VEL = 5
#how fast beams shoot
BEAM_VEL = 10
B_WIDTH = 10
B_HEIGHT = 5
MAX_BEAMS = 3

NARUTO_HIT = pygame.USEREVENT + 1
SASUKE_HIT = pygame.USEREVENT + 2

#######################image stuff##############################
#load in images
NARUTO = pygame.image.load(os.path.join('Assets', 'naruto.png'))
SASUKE = pygame.image.load(os.path.join('Assets', 'sasuke.png'))
B_GROUND = pygame.image.load(os.path.join('Assets', 'cherrybaby.png'))
#resize to whatever
PLAYER_WIDTH = 55
PLAYER_HEIGHT = 40
NARUTO = pygame.transform.scale(NARUTO, (PLAYER_WIDTH, PLAYER_HEIGHT))
SASUKE = pygame.transform.scale(SASUKE, (PLAYER_WIDTH, PLAYER_HEIGHT))
B_GROUND = pygame.transform.scale(B_GROUND, (WIDTH, HEIGHT))
#rotate if desired -- ..rotate(image, degree_to_be_rotated)
#NARUTO = pygame.transform.rotate(NARUTO, 90)
#SASUKE = pygame.transform.rotate(SASUKE, 270)
################################################################



def draw_window(naruto, sasuke, naruto_beams, sasuke_beams, naruto_health, sasuke_health):
    #set background color for solid background
    #WIN.fill(PINK)
    #set background with image
    WIN.blit(B_GROUND, (0,0))
    pygame.draw.rect(WIN, BLUE, MIDDLE_BAR)

    naruto_health_text = HEALTH_FONT.render("Health: " + str(naruto_health), 1, RED)
    sasuke_health_text = HEALTH_FONT.render("Health: " + str(sasuke_health), 1, RED)
    # 10 chosen for padding
    WIN.blit(naruto_health_text, (10, 10))
    WIN.blit(sasuke_health_text, (WIDTH - sasuke_health_text.get_width() - 10,10))

    WIN.blit(NARUTO, (naruto.x, naruto.y))
    WIN.blit(SASUKE, (sasuke.x, sasuke.y))

    for beam in naruto_beams:
        pygame.draw.rect(WIN, YELLOW, beam)
    for beam in sasuke_beams:
        pygame.draw.rect(WIN, RED, beam)

    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLUE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2
        , HEIGHT//2 - draw_text.get_height()//2 ) )
    pygame.display.update()
    WIN_SOUND.play()
    pygame.time.delay(5000)


########################### Handle movement function###################
#checks if key is pressed and makes sure its within bounds
def naruto_handle_move(keys_pressed, naruto):
    #IMPORTANT: when using elif instead of multi ifs it only allowd
        #   one direction at a time and no diagonals. Multi ifs allows for 
        #   diagonals.
    if keys_pressed[pygame.K_a] and naruto.x - VEL > 0: #LEFT
        naruto.x -= VEL
    if keys_pressed[pygame.K_d] and naruto.x + VEL + naruto.width < MIDDLE_BAR.x: #RIGHT
        naruto.x += VEL
    if keys_pressed[pygame.K_w] and naruto.y - VEL > 0: #UP
        naruto.y -= VEL
    if keys_pressed[pygame.K_s] and naruto.y + VEL + naruto.height < HEIGHT: #DOWN
        naruto.y += VEL

def sasuke_handle_move(keys_pressed, sasuke):
    if keys_pressed[pygame.K_LEFT] and sasuke.x - VEL > MIDDLE_BAR.x + MIDDLE_BAR.width: #LEFT
        sasuke.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and sasuke.x + VEL + sasuke.width < WIDTH: #RIGHT
        sasuke.x += VEL
    if keys_pressed[pygame.K_UP] and sasuke.y - VEL > 0: #UP
        sasuke.y -= VEL
    if keys_pressed[pygame.K_DOWN] and sasuke.y + VEL + sasuke.height < HEIGHT: #DOWN
        sasuke.y += VEL

def handle_beams(naruto_beams, sasuke_beams, naruto, sasuke):
    for beam in naruto_beams:
        beam.x += BEAM_VEL
        #check if narutos beams hit sasuke
        if sasuke.colliderect(beam):
            pygame.event.post(pygame.event.Event(SASUKE_HIT))
            naruto_beams.remove(beam)
       
        #check if beams go off screen
        elif beam.x > WIDTH:
            naruto_beams.remove(beam)


    for beam in sasuke_beams:
        beam.x -= BEAM_VEL
        #check if sasuke beams hit naruto
        if naruto.colliderect(beam):
            pygame.event.post(pygame.event.Event(NARUTO_HIT))
            sasuke_beams.remove(beam)
        
        #check if beams go off screen
        elif beam.x < 0:
            sasuke_beams.remove(beam)


def main():

    naruto = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    sasuke = pygame.Rect(700, 300, PLAYER_WIDTH, PLAYER_HEIGHT)

    naruto_beams = []
    sasuke_beams = []

    naruto_health = 10
    sasuke_health = 10


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(naruto_beams) < MAX_BEAMS:
                    #for plyer on left- this makes it be on right side in middle
                    # // is used for int division since Rect cant take float
                    n_beam = pygame.Rect(naruto.x + naruto.width, naruto.y + naruto.height//2
                        , B_WIDTH, B_HEIGHT)
                    naruto_beams.append(n_beam)
                    BEAM_BLAST_SOUND.play()
                if event.key == pygame.K_RCTRL and len(sasuke_beams) < MAX_BEAMS:
                    s_beam = pygame.Rect(sasuke.x, sasuke.y + sasuke.height//2
                        , B_WIDTH, B_HEIGHT)
                    sasuke_beams.append(s_beam)
                    BEAM_BLAST_SOUND.play()

            if event.type == NARUTO_HIT:
                BEAM_HIT_SOUND.play()
                naruto_health -= 1

            if event.type == SASUKE_HIT:
                BEAM_HIT_SOUND.play()
                sasuke_health -= 1
        
        winner_text = ""
        if naruto_health <= 0:
            winner_text = "Sasuke Wins"
        if sasuke_health <= 0:
            winner_text = "Naruto Wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

        
        #keeps track of all keys pressed
        keys_pressed = pygame.key.get_pressed()
        naruto_handle_move(keys_pressed, naruto)
        sasuke_handle_move(keys_pressed, sasuke)

        handle_beams(naruto_beams, sasuke_beams, naruto, sasuke)


        draw_window(naruto, sasuke, naruto_beams, sasuke_beams
            , naruto_health, sasuke_health)
        
    
    #restarts game
    main()



if __name__ == "__main__":
    main()
