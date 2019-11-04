import pygame as pg
import random 
import math
from pygame import mixer

#initialize pygame
pg.init()

#create screen
screen = pg.display.set_mode((800,500))

#title and icon
pg.display.set_caption("Space Adventure")
icon = pg.image.load('ufo.png')
pg.display.set_icon(icon)

# add background
bgimg = pg.image.load("bgimg.jpg")

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#player
playerImg = pg.image.load("rocket.png")
playerX = 370
playerY = 400
playerX_chnge = 0

#monster
monsterImg = []
monsterX = []
monsterY = []
monsterX_chnge = []
monsterY_chnge = []
num_monster = 5

for i in range(num_monster):
	monsterImg.append(pg.image.load("monster.png"))
	monsterX.append(random.randint(0, 735))
	monsterY.append(random.randint(0, 50))
	monsterX_chnge.append(2)
	monsterY_chnge.append(40)

#bullet
bulletImg = pg.image.load("bullet.png")
bulletX = 0
bulletY = 400
bulletY_chnge = 7
bullet_state = "ready"

#score

score = 0
font = pg.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

def show_score(x,y):
	display = font.render("Score : "+ str(score), True, (255,255,255))
	screen.blit(display, (x,y))

def monster(x,y,i):
	screen.blit(monsterImg[i], (x, y))   #drawing

def player(x,y):
	screen.blit(playerImg, (x, y))   #drawing

def bullet_fire(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x+16, y+20))   #drawing

def isCollision(x1, y1, x2, y2):
	dist = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))
	if dist < 28:
		return True
	else:
		return False

end_font = pg.font.Font('freesansbold.ttf',64)

def the_end():
	end_text = end_font.render("The End", True, (255,255,255))
	screen.blit(end_text, (260,220))
	dead_sound = mixer.Sound("dead.wav")
	dead_sound.play()

#game loop
run = True
while run:
	#screen bg color
	screen.fill((0,0,0))
	# backgroung image
	screen.blit(bgimg, (0, 0))

	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False

		if event.type == pg.KEYDOWN:
			if event.key == pg.K_LEFT or event.key == ord('a'):
				playerX_chnge = -3
			if event.key == pg.K_RIGHT or event.key == ord('d'):
				playerX_chnge = 3
			if event.key == pg.K_SPACE:
				bullet_sound = mixer.Sound("laser.wav")
				bullet_sound.play()
				bulletX = playerX
				bullet_fire(bulletX, bulletY)

		if event.type == pg.KEYUP:
			if event.key == pg.K_LEFT or event.key == pg.K_RIGHT or event.key == ord('a') or event.key == ord('d'):
				playerX_chnge = 0


	#bullet move
	if bulletY <= 0:
		bulletY = 400
		bullet_state = "ready"

	if bullet_state is "fire":
		bullet_fire(bulletX, bulletY)
		bulletY -= bulletY_chnge
		
	playerX += playerX_chnge

	if playerX <=0:
		playerX = 0
	if playerX >= 736:
		playerX = 736

	#monster moves
	for i in range(num_monster):

		#the end
		if monsterY[i] > 400:
			for j in range(num_monster):
				monsterY[j] = 2000
			the_end()
			break

		if monsterX[i] <=0:
			monsterX_chnge[i] = 2
			monsterY[i] += monsterY_chnge[i]

		if monsterX[i] >= 736:
			monsterX_chnge[i] = -2
			monsterY[i] += monsterY_chnge[i]

		monsterX[i] += monsterX_chnge[i]

		#add collision
		collision = isCollision(monsterX[i], monsterY[i], bulletX, bulletY)
		if collision:
			blast_sound = mixer.Sound("explosion.wav")
			blast_sound.play()
			bulletY = 400
			bullet_state = "ready"
			score += 1
			monsterX[i] = random.randint(0, 735)
			monsterY[i] = random.randint(0, 50)


		monster(monsterX[i], monsterY[i], i)


	player(playerX, playerY)

	show_score(textX, textY)

	pg.display.update()