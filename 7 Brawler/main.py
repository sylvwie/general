import pygame
from pygame import mixer

from fighter import Fighter

mixer.init()
pygame.init()

# window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# framerate
clock = pygame.time.Clock()
FPS = 70

# define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# load menu
menu_image = pygame.image.load("assets/menu/menu.jpg").convert()


def draw_menu():
	scaled_menu = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
	screen.blit(scaled_menu, (0, 0))


# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores [P1, P2]
round_over_time = 0
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# load background
bg_image = pygame.image.load("assets/images/background/background.jpeg").convert()

# load sprite sheets
warrior_sheet = pygame.image.load("assets/images/warrior/sprites/warrior.png").convert()
wizard_sheet = pygame.image.load("assets/images/wizard/sprites/wizard.png").convert()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 2, 8, 8, 3, 7]

# font
victory_font = pygame.font.Font("assets/fonts/Turok.ttf", 90)
count_font = pygame.font.Font("assets/fonts/Turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/Turok.ttf", 30)


def draw_text(text, font, text_col, x, y):  # func draw text
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_victory(text, font, text_col, x, y):
	img1 = font.render(text, True, text_col)
	screen.blit(img1, (x, y))


# func draw bg
def draw_bg():
	scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
	screen.blit(scaled_bg, (0, 0))


# function for drawing fighter health bars
def draw_health_bar(health, x, y):
	ratio = health / 100
	pygame.draw.rect(screen, RED, (x, y, 400, 30))
	pygame.draw.rect(screen, GREEN, (x, y, 400*ratio, 30))


# create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# game loop
menuOn = True
run = True
while run:

	clock.tick(FPS)

	# draw background
	if menuOn == False:
		draw_bg()

		# show player stats
		draw_health_bar(fighter_1.health, 20, 20)
		draw_health_bar(fighter_2.health, 580, 20)
		draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
		draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

		# update countdown
		if intro_count <= 0:
			# move fighters
			fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_2, round_over)
			fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_1, round_over)
		else:
			# display count timer
			draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
			# update countdown
			if (pygame.time.get_ticks() - last_count_update) >= 1000:
				intro_count -= 1
				last_count_update = pygame.time.get_ticks()

		# update fighters
		fighter_1.update()
		fighter_2.update()

		# draw fighters
		fighter_1.draw(screen)
		fighter_2.draw(screen)

		# check for player defeat
		if not round_over:
			if not fighter_1.alive:  # fighter_1.alive == false
				score[1] += 1
				round_over = True
				round_over_time = pygame.time.get_ticks()
			elif not fighter_2.alive:  # fighter_2.alive == false
				score[0] += 1
				round_over = True
				round_over_time = pygame.time.get_ticks()
				print("round is over")

		else:
			# display victory text
			draw_victory("Victory!", victory_font, RED, SCREEN_WIDTH - 650, SCREEN_HEIGHT - 500)
			if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
				round_over = False
				intro_count = 3
				fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
				fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

		pygame.display.update()

	# event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	# switch from menu to game
		if event.type == pygame.KEYDOWN:
			# checking if key "SPACE" was pressed
			if event.key == pygame.K_SPACE:
				menuOn = False

		if menuOn:  # menuOff == True
			draw_menu()
		pygame.display.update()

	# update display

# exit pygame
pygame.quit()

# by @sylvwie on GitHub for my first python exam :D
# "Street Fighter Style Fighting Game in Python using Pygame - Complete Tutorial" by @russs123
