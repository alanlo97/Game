
import pygame, random, sys

from pygame.event import wait

ancho_ventana = 1200
alto_ventana = 700

BLACK = (0, 0, 0)
COLOR= (255,0,255)

pygame.init()
pygame.mixer.init()

background = pygame.image.load("images\cyberpunk-street-files\cyberpunk-street.png")
background2 = pygame.image.load("images\cyberpunk-street-files\cyberpunk-street2.png")

pos_background = 0
pos_background2 = 1200

speed_background = 5

screen = pygame.display.set_mode((ancho_ventana, alto_ventana))

pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.sheet = pygame.image.load('images\Arcane archer\spritesheet1.png')
		self.sheet_back = pygame.image.load('images\Arcane archer\spritesheet1back.png')
		self.sheet.set_clip(pygame.Rect(0, 101, 105, 101))
		self.sheet_back.set_clip(pygame.Rect(0, 101, 105, 101))
		self.image = self.sheet.subsurface(self.sheet.get_clip())
		self.rect = self.image.get_rect()
		self.rect.topleft = (ancho_ventana/2, alto_ventana * 3/4)
		self.frame = 0
		self.frame_arrow = 0
		self.frame_dead = 0
		self.frame_back = 0
		self.frame_wait = 0
		self.player_states = { 0: (735, 0, 105, 101), 1: (0, 0, 105, 101), 2: (105, 0, 105, 101), 3: (210, 0, 105, 101), 4: (315, 0, 105, 101), 5: (420, 0, 105, 101), 6: (525, 0, 105, 101), 7: (630, 0, 105, 101) }
		self.player_states_back = { 0: (0, 101, 105, 101), 1: (0, 0, 105, 101), 2: (105, 0, 105, 101), 3: (210, 0, 105, 101), 4: (315, 0, 105, 101), 5: (420, 0, 105, 101), 6: (525, 0, 105, 101), 7: (630, 0, 105, 101), 8: (735, 0, 105, 101) }
		self.shoot_states = { 0: (630, 303, 105, 101), 1: (0, 303, 105, 101), 2:(105, 303, 105, 101), 3: (210, 303, 105, 101), 4: (315, 303, 105, 101), 5: (420, 303, 105, 101), 6: (525, 303, 105, 101) }
		self.dead_states = { 0: (630, 101, 105, 101), 1: (0, 101, 105, 101), 2:(105, 101, 105, 101), 3: (210, 101, 105, 101), 4: (315, 101, 105, 101), 5: (420, 101, 105, 101), 6: (525, 101, 105, 101) }
		self.wait_states = {0: (315, 505, 105, 101), 1: (0, 505, 105, 101), 2:(105, 505, 105, 101), 3: (210, 505, 105, 101) }
		self.speed_x = 6
		self.speed_y = 6
		self.shooting = False
		self.move_right = False
		self.move_left = False
		self.dead = False
		self.wait = True

	def get_frame(self, frame_set):
		self.frame += 1
		if self.frame > (len(frame_set) - 1):
			self.frame = 0
		return frame_set[self.frame]

	def get_frame_arrow(self, frame_set):
		self.frame_arrow += 1
		if self.frame_arrow > (len(frame_set) - 1):
			self.frame_arrow = 0
			self.shooting = False
		return frame_set[self.frame_arrow]

	def get_frame_dead(self, frame_set):
		self.frame_dead += 1
		if self.frame_dead > (len(frame_set) - 1):
			self.frame_dead = 6
			self.dead = False
		return frame_set[self.frame_dead]

	def get_frame_wait(self, frame_set):
		self.frame_wait += 1
		if self.frame_wait > (len(frame_set) - 1):
			self.frame_wait = 0
		return frame_set[self.frame_wait]

# ------------------------------------------------------------------------------------
#JUNTE LOS 3 CLIPS EN UNO SOLO, EL DE PARA CAMINAR PARA ATRAS NO SE PUEDE PORQUE USA OTRO .JPG
# ------------------------------------------------------------------------------------

	def clip(self, clipped_rect):
		if type(clipped_rect) is dict:
			if not self.shooting and not self.dead:
				self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
			elif self.shooting and not self.dead:
				self.sheet.set_clip(pygame.Rect(self.get_frame_arrow(clipped_rect)))
			else:
				self.sheet.set_clip(pygame.Rect(self.get_frame_dead(clipped_rect)))
		else:
			self.sheet.set_clip(pygame.Rect(clipped_rect))
		return clipped_rect

# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

	def get_frame_back(self, frame_set):
		self.frame_back += 1
		if self.frame_back > (len(frame_set) - 1):
			self.frame_back = 1
		return frame_set[self.frame_back]

	def clip_back(self, clipped_rect):
		if type(clipped_rect) is dict:
			self.sheet_back.set_clip(pygame.Rect(self.get_frame_back(clipped_rect)))
		else:
			self.sheet_back.set_clip(pygame.Rect(clipped_rect))
		return clipped_rect

	def update(self, spawn_enemys):
		self.speed_x = 0
		self.speed_y = 0
		self.move_left = False
		self.move_right = False

		keystate = pygame.key.get_pressed()

		self.wait = True

		if not keystate[pygame.K_LEFT]:
			if keystate[pygame.K_RIGHT]:
				self.move_right = True
				self.wait = False
				if spawn_enemys:
					self.speed_x = 6
				self.clip(self.player_states)

			self.rect.x += self.speed_x

			if self.rect.right > ancho_ventana:
				self.rect.right = ancho_ventana
			if self.rect.left < 0:
				self.rect.left = 0

			if keystate[pygame.K_UP] and keystate[pygame.K_RIGHT]:
				self.wait = False
				self.speed_y = -6
			elif keystate[pygame.K_UP]:
				self.wait = False
				self.speed_y = -6
				self.clip(self.player_states)

			if keystate[pygame.K_DOWN] and keystate[pygame.K_RIGHT]:
				self.wait = False
				self.speed_y = 6
			elif keystate[pygame.K_DOWN]:
				self.wait = False
				self.speed_y = 6
				self.clip(self.player_states)

			self.rect.y += self.speed_y

			if self.rect.bottom > alto_ventana:
				self.rect.bottom = alto_ventana
			if self.rect.top < 450:
				self.rect.top = 450

			self.image = self.sheet.subsurface(self.sheet.get_clip())

		if keystate[pygame.K_LEFT]:

			self.speed_x = -6
			self.move_left = True
			self.wait = False
			self.clip_back(self.player_states_back)

			self.rect.x += self.speed_x

			if self.rect.left < 0:
				self.rect.left = 0

			if keystate[pygame.K_UP]:
				self.wait = False
				self.speed_y = -6
				self.clip(self.player_states_back)
			if keystate[pygame.K_DOWN]:
				self.wait = False
				self.speed_y = 6
				self.clip(self.player_states_back)

			self.rect.y += self.speed_y

			if self.rect.bottom > alto_ventana:
				self.rect.bottom = alto_ventana
			if self.rect.top < 450:
				self.rect.top = 450

			self.image = self.sheet_back.subsurface(self.sheet_back.get_clip())

		if self.wait:
			self.clip(self.wait_states)
			self.image = self.sheet.subsurface(self.sheet.get_clip())

		

	def shoot_move(self):

		self.clip(self.shoot_states)
		self.image = self.sheet.subsurface(self.sheet.get_clip())

	def dead_move(self):

		self.clip(self.dead_states)
		self.image = self.sheet.subsurface(self.sheet.get_clip())


class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.sheet = pygame.image.load("images\Skeleton enemy\Skeleton enemy1.png")
		self.sheet.set_clip(pygame.Rect(0, 0, 105, 101))
		self.image = self.sheet.subsurface(self.sheet.get_clip())
		self.rect = self.image.get_rect()
		self.rect.topleft = (ancho_ventana - 105, random.randint(450, 600))
		self.frame = 0
		self.dead_frame = 0
		self.attack_frame = 0
		self.enemy_states = {0: (100, 202, 100, 101), 1: (1200, 202, 100, 101), 2: (1100, 202, 100, 101), 3: (1000, 202, 100, 101), 4: (900, 202, 100, 101), 5: (800, 202, 100, 101), 6: (700, 202, 100, 101), 7: (600, 202, 100, 101), 8: (500, 202, 100, 101), 9: (400, 202, 100, 101), 10: (300, 202, 100, 101), 11: (200, 202, 100, 101)}
		self.enemy_dead = { 0: (0, 101, 100, 101), 1: (1200, 101, 100, 101), 2: (1100, 101, 100, 101), 3: (1000, 101, 100, 101), 4: (900, 101, 100, 101), 5: (800, 101, 100, 101), 6: (700, 101, 100, 101), 7: (600, 101, 100, 101), 8: (500, 101, 100, 101), 9: (400, 101, 100, 101), 10: (300, 101, 100, 101), 11: (200, 101, 100, 101), 12: (100, 101, 100, 101)}
		self.enemy_attack = { 0: (0, 0, 100, 101), 1: (1200, 0, 100, 101), 2: (1100, 0, 100, 101), 3: (1000, 0, 100, 101), 4: (900, 0, 100, 101), 5: (800, 0, 100, 101), 6: (700, 0, 100, 101), 7: (600, 0, 100, 101), 8: (500, 0, 100, 101), 9: (400, 0, 100, 101), 10: (300, 0, 100, 101), 11: (200, 0, 100, 101), 12: (100, 0, 100, 101)}
		self.speed_x = -15
		self.speed_y = 0
		self.dead = False
		self.attack = False
		self.enemy_wins = False

	def get_frame(self, frame_set):
		self.frame += 1
		if self.frame > (len(frame_set) - 1):
			self.frame = 0
		return frame_set[self.frame]

	def clip(self, clipped_rect):
		if type(clipped_rect) is dict:
			if not self.dead and not self.attack:
				self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
			elif self.dead and not self.attack:
				self.sheet.set_clip(pygame.Rect(self.get_dead_frame(clipped_rect)))
			else:
				self.sheet.set_clip(pygame.Rect(self.get_attack_frame(clipped_rect)))
		else:
			self.sheet.set_clip(pygame.Rect(clipped_rect))
		return clipped_rect

	def get_dead_frame(self, frame_set):
		self.dead_frame += 1
		if self.dead_frame  > (len(frame_set) - 1):
			self.dead_frame = 0
			self.dead = False
		
		return frame_set[self.dead_frame] 

	def get_attack_frame(self, frame_set):
		self.attack_frame += 1
		if self.attack_frame  > (len(frame_set) - 1):
			self.attack_frame = 0
			self.attack = False
			self.enemy_wins = True
		
		return frame_set[self.attack_frame] 

	def update(self, y):
		self.rect.x += self.speed_x
		self.clip(self.enemy_states)

		if self.rect.bottom > alto_ventana:
			self.rect.bottom = alto_ventana

		if self.rect.centery != y:
					if self.rect.centery - y > 50:
						self.speed_y = -1
					if self.rect.centery - y < -50:
						self.speed_y = 1
					self.rect.y += self.speed_y

		self.image = self.sheet.subsurface(self.sheet.get_clip())

	def dead_move(self):
		self.clip(self.enemy_dead)
		self.image = self.sheet.subsurface(self.sheet.get_clip())

	def attack_move(self):
		self.clip(self.enemy_attack)
		self.image = self.sheet.subsurface(self.sheet.get_clip())

class Boss(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.sheet = pygame.image.load("images/NightBorne/NightBorne2.png")
		self.sheet.set_clip(pygame.Rect(0, 0, 360, 360))
		self.image = self.sheet.subsurface(self.sheet.get_clip())
		self.rect = self.image.get_rect()
		self.rect.topleft = (ancho_ventana - 105, random.randint(201, 340))
		self.frame = 0
		self.attack_frame = 0
		self.hit_frame = 0
		self.dead_frame = 0
		self.boss_status = {0: (6120, 360, 360, 360), 1: (7920, 360, 360, 360), 2: (7560 ,360 ,360 ,360 ), 3: (7200, 360, 360, 360), 4: (6840, 360, 360, 360), 5: (6480, 360, 360, 360) }
		self.boss_spawn = {0: (5040, 0, 360, 360), 1: (7920, 0, 360, 360), 2: (7560 ,0 ,360 ,360 ), 3: (7200, 0, 360, 360), 4: (6840, 0, 360, 360), 5: (6480, 0, 360, 360), 6: (6120, 0, 360, 360), 7: (5760, 0, 360, 360), 8: (5400, 0, 360, 360) }
		self.boss_attack = {0: (3960, 720, 360, 360), 1: (7920, 720, 360, 360), 2: (7560, 720, 360, 360 ), 3: (7200, 720, 360, 360), 4: (6840, 720, 360, 360), 5: (6120, 720, 360, 360), 6: (6120, 720, 360, 360), 7: (5760, 720, 360, 360), 8: (5400, 720, 360, 360), 9: (5040, 720, 360, 360), 10: (4680, 720, 360, 360), 11: (4320, 720, 360, 360) }
		self.boss_hit = {0: (6480, 1080, 360, 360), 1: (7920, 1080, 360, 360), 2: (7560 ,1080 ,360 ,360 ), 3: (7200, 1080, 360, 360), 4: (6840, 1080, 360, 360) }
		self.boss_dead = {0: (0, 1440, 360, 360), 1: (7920, 1440, 360, 360), 2: (7560, 1440, 360, 360 ), 3: (7200, 1440, 360, 360), 4: (6840, 1440, 360, 360), 5: (6120, 1440, 360, 360), 6: (6120, 1440, 360, 360),
			7: (5760, 1440, 360, 360), 8: (5400, 1440, 360, 360), 9: (5040, 1440, 360, 360), 10: (4680, 1440, 360, 360), 11: (4320, 1440, 360, 360), 12: (3960, 1440, 360, 360), 13: (3600, 1440, 360, 360),
			14: (3240, 1440, 360, 360), 15: (2880, 1440, 360, 360), 16: (2880, 1440, 360, 360), 17: (2160, 1440, 360, 360), 18: (1800, 1440, 360, 360), 19: (1440, 1440, 360, 360), 20: (1080, 1440, 360, 360),
			21: (720, 1440, 360, 360), 22: (360, 1440, 360, 360) }
		self.speed_x = -20
		self.speed_y = 0
		self.attack = False
		self.dead = False
		self.enemy_wins = False
		self.hit = False
		self.spawn = True
		self.dead = False
		self.hp = 100


	def clip(self, clipped_rect):
		if type(clipped_rect) is dict:
			if not self.dead and not self.attack and not self.hit:
				self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
			elif self.attack and not self.dead and not self.hit:
				self.sheet.set_clip(pygame.Rect(self.get_attack_frame(clipped_rect)))
			elif self.hit and not self.dead:
				self.sheet.set_clip(pygame.Rect(self.get_hit_frame(clipped_rect)))
			else:
				self.sheet.set_clip(pygame.Rect(self.get_dead_frame(clipped_rect)))
		else:
			self.sheet.set_clip(pygame.Rect(clipped_rect))
		return clipped_rect

	def get_frame(self, frame_set):
		self.frame += 1
		if self.frame > (len(frame_set) - 1):
			self.frame = 0
		return frame_set[self.frame]

	def get_attack_frame(self, frame_set):
		self.attack_frame += 1
		if self.attack_frame  > (len(frame_set) - 1):
			self.attack_frame = 0
			self.attack = False
		
		return frame_set[self.attack_frame] 

	def get_hit_frame(self, frame_set):
		self.hit_frame += 1
		if self.hit_frame  > (len(frame_set) - 1):
			self.hit_frame = 0
			self.hit = False
		
		return frame_set[self.hit_frame] 

	def get_dead_frame(self, frame_set):
		self.dead_frame += 1
		if self.dead_frame  > (len(frame_set) - 1):
			self.dead_frame = 0
			self.dead = False
		
		return frame_set[self.dead_frame] 

	def update(self, y):
		self.rect.x += self.speed_x
		if self.rect.left < -5:
			self.rect.x = ancho_ventana - self.rect.width
			self.rect.y = random.randrange(201, 340)

		if self.rect.right > ancho_ventana + 50:
			self.clip(self.boss_spawn)
		else:
			self.clip(self.boss_status)

		if self.rect.bottom > alto_ventana:
			self.rect.bottom = alto_ventana

		if self.rect.centery != y:
					if self.rect.centery - y > 50:
						self.speed_y = -1
					if self.rect.centery - y < -50:
						self.speed_y = 1
					self.rect.y += self.speed_y

		self.image = self.sheet.subsurface(self.sheet.get_clip())

	def attack_move(self):
		self.clip(self.boss_attack)
		self.image = self.sheet.subsurface(self.sheet.get_clip())

	def hit_move(self):
		self.clip(self.boss_hit)
		self.image = self.sheet.subsurface(self.sheet.get_clip())

		self.rect.centerx += 15

	def dead_move(self):
		self.clip(self.boss_dead)
		self.image = self.sheet.subsurface(self.sheet.get_clip())
		

class Arrow(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("images\Arcane archer\projectile1.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centery = y
		self.rect.left = x
		self.speedy = 20
		self.drop = False

	def update(self):
		self.rect.x += self.speedy

count_player_mts = 0

# Puntaje
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score :" + str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))

skeleton_list = []
arrow_list = []

player = Player()
arrow = Arrow(player.rect.right, player.rect.centery)
nums_enemys = random.randrange(1, 4)
boss = Boss()

spawn_enemys = False
background_move = False


# BARRA DE VIDA LO PUSE ARRIBA EN LA PANTALLA EN VEZ DE ARRIBA DE LA CABEZA DEL BOSS

def barra_hp(screen, hp):
		largo = 500
		ancho = 20
		calculo_barra = int((hp/100)*largo)
		borde = pygame.Rect(ancho_ventana/2 - 250, 30, largo, ancho)
		rectangulo = pygame.Rect(ancho_ventana/2 - 250, 30, calculo_barra, ancho)
		pygame.draw.rect(screen, COLOR, borde, 3)
		pygame.draw.rect(screen, (255, 255, 255), rectangulo)

for i in range(nums_enemys):
	skeleton = Enemy()
	skeleton_list.append(skeleton)


#LOS CONTACTOS ESTABAN MAL, ERA TODO CON ANDS

def isCollision(skeleton, arrow_list):
	collision = False
	index = 0

	while index < (len(arrow_list)) and not collision:

		distance_x = skeleton.rect.left-arrow_list[index].rect.right
		distance_y = skeleton.rect.centery-arrow_list[index].rect.centery
	
		if distance_x < 0 and distance_x > -30 and distance_y > -50 and distance_y < 50:
			arrow_list.pop(index)
			index -= 1
			collision = True

		index += 1
	
	return collision

def isCollisionBoss(boss, arrow_list):
	collision = False
	index = 0
	while index < (len(arrow_list)) and not collision:
		distance_x = boss.rect.left-arrow_list[index].rect.right
		distance_y = boss.rect.centery-arrow_list[index].rect.centery
	
		if distance_x < 0 and distance_x > -50 and distance_y > -150 and distance_y < 150:
			arrow_list.pop(index)
			index -= 1
			collision = True

		index += 1

	return collision

def skeletonAttack(skeleton, player):
	distance_x = skeleton.rect.left-player.rect.right
	distance_y = skeleton.rect.centery-player.rect.centery
	
	if distance_x < -50 and distance_x > -70 and distance_y > -25 and distance_y < 25:
		return True
	else:
		return False

def bossAttack(boss, player):
	distance_x = boss.rect.left-player.rect.right
	distance_y = boss.rect.centery-player.rect.centery
	
	if distance_x < -80 and distance_x > -100 and distance_y > -100 and distance_y < 100:
		return True
	else:
		return False
    

# Game Loop
running = True

while running:

	clock.tick(10)
	
	pygame.display.update()

	#LA PANTALLA SE VA CORRIENDO SI ES QUE NO APARECEN ENEMIGOS Y SE APRETA LA FLECHA DERECHA, SI APARECEN O SE DEJA DE APRETAR YA SE QUEDA CONGELADA
	#  Y EL JUGADOR PUEDE MOVERSE POR TODA LA PANTALLA

	if not spawn_enemys and player.move_right and not player.shooting:

		if(pos_background2 == 0):
			pos_background = 1200
		elif(pos_background == 0):
			pos_background2 = 1200

		pos_background -= speed_background
		pos_background2 -= speed_background

	#LA PANTALLA SE VA CORRIENDO SI ES QUE NO APARECEN ENEMIGOS Y SE APRETA LA FLECHA IZQUIERDA, SI APARECEN O SE DEJA DE APRETAR YA SE QUEDA CONGELADA
	#  Y EL JUGADOR PUEDE MOVERSE POR TODA LA PANTALLA

	if not spawn_enemys and player.move_left:

		if(pos_background2 == 0):
			pos_background = -1200
		elif(pos_background == 0):
			pos_background2 = -1200

		pos_background += speed_background
		pos_background2 += speed_background

	screen.blit(background, [pos_background, 0])
	screen.blit(background2, [pos_background2, 0])


	for event in pygame.event.get():
		if event.type == pygame.QUIT:

			running = False
			pygame.quit()
			sys.exit()

		elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					player.shooting = True

	if not player.dead:
		if not player.shooting: # or arrow.drop:

			player.shooting = False
		
			player.update(spawn_enemys)

			if player.move_right:
				count_player_mts += 3

			if count_player_mts > 105:
				spawn_enemys = True

			#if not arrow.drop:
			#	arrow.rect.right = player.rect.left - 50
			#	arrow.rect.y = player.rect.centery

		if player.shooting: # and not arrow.drop:
			player.shoot_move()
			if not player.shooting:
				arrow = Arrow(player.rect.right, player.rect.centery)
				arrow_list.append(arrow)
				# arrow.rect.left = player.rect.right
				# arrow.rect.y = player.rect.centery
				#arrow.drop = True

	#AHORA EL ENEMIGO HACE EL MOVIMIENTO DE ATAQUE, DESPUES CUANDO TERMINA RECIEN EL JUGADOR HACE TODO EL MOVIMIENTO DE MUERTE Y CUANDO TERMINA SE SALE DEL JUEGO
	else:
		player.dead_move()
		if not player.dead:
			running = False
			pygame.quit()
			sys.exit()

	screen.blit(player.image, (player.rect.x, player.rect.y))
	
	i_arrow = 0

	while i_arrow < (len(arrow_list)):
	#for i in range (len(arrow_list)):

		arrow_list[i_arrow].update()
		screen.blit(arrow_list[i_arrow].image, (arrow_list[i_arrow].rect.x, arrow_list[i_arrow].rect.y))

		if arrow_list[i_arrow].rect.right > ancho_ventana:
			#arrow.drop = False
			arrow_list.pop(i_arrow)
			i_arrow -= 1

		i_arrow += 1


	if score_value < 8 and spawn_enemys:

		i_skeleton = 0

		while i_skeleton < (len(skeleton_list)):
		#for i in range (len(skeleton_list)):

			if not skeleton_list[i_skeleton].dead and not skeleton_list[i_skeleton].attack:
				skeleton_list[i_skeleton].update(player.rect.centery)

			if skeleton_list[i_skeleton].attack:
				skeleton_list[i_skeleton].attack_move()
				if not skeleton_list[i_skeleton].attack:
					player.dead = True

			screen.blit(skeleton_list[i_skeleton].image, (skeleton_list[i_skeleton].rect.x, skeleton_list[i_skeleton].rect.y))

			if isCollision(skeleton_list[i_skeleton], arrow_list):

				# arrow.rect.right = player.rect.left - 50
				#arrow.drop = False
				skeleton_list[i_skeleton].dead = True
				score_value += 1

			if skeletonAttack(skeleton_list[i_skeleton], player):
				skeleton_list[i_skeleton].attack = True

			if skeleton_list[i_skeleton].dead:
				skeleton_list[i_skeleton].dead_move()
				if not skeleton_list[i_skeleton].dead:
					if (score_value + nums_enemys) == 9 and nums_enemys >= 0:
						nums_enemys -= 1
						#skeleton_list[i].rect.topleft = (-75, random.randint(450, 600))
						skeleton_list.pop(i_skeleton)
						i_skeleton -= 1
					else:
					# AHORA NO DESAPARECEN DE LA NADA LOS ESQUELETOS QUE QUEDAN VIVOS AL LLEGAR SCORE DONDE SALE EL BOSS, DESAPARECEN TODOS ANTES
					#EN REALIDAD NO DESAPARECEN, LOS MANDE AL FONDO A LA IZQUIERDA, POR FUERA DE LA PANTALLA, SIGUEN CAMINANDO PERO NO SE LOS VE
					#HAY QUE VER COMO ELIMINARLOS DE LA LISTA
					
						skeleton_list[i_skeleton].rect.topleft = (ancho_ventana - 105, random.randint(450, 600))

			i_skeleton += 1

	elif score_value >= 8 and spawn_enemys:

		barra_hp(screen, boss.hp)

		if isCollisionBoss(boss, arrow_list):
			#arrow.rect.right = player.rect.left - 50
			#arrow.drop = False
			boss.hp = boss.hp-5
			boss.hit = True
			if boss.hp <= 0:
				boss.dead = True

		if boss.dead:
			boss.dead_move()
			if not boss.dead:
				pygame.quit()
				sys.exit()

		if boss.hit and not boss.dead:
			boss.hit_move()

		if not boss.attack and not boss.hit:
			boss.update(player.rect.centery)

		if boss.attack:
			boss.attack_move()
			if not boss.attack:
					player.dead = True

		screen.blit(boss.image, (boss.rect.x, boss.rect.y))

		if bossAttack(boss, player):
				boss.attack = True

		
	# actualizar puntaje
	
	show_score(textX,textY)

	pygame.display.flip()
