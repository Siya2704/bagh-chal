import pygame
 
pygame.init()
screen = pygame.display.set_mode((1300,900))
color = (255,204,153)
screen.fill(color)
done = False

img_board = pygame.image.load('img/board.png')
img_tiger = pygame.image.load('img/tiger.png')
img_tiger = pygame.transform.scale(img_tiger, (60,60))
img_goat = pygame.image.load('img/goat.png')
img_goat = pygame.transform.scale(img_goat, (70,70))
def board(screen):
	pygame.draw.rect(screen, (255,255,255), pygame.Rect(90, 90, 1120, 720))
	screen.blit(img_board,(200,200))#size 500X500
	screen.blit(img_tiger,(170,170))
	screen.blit(img_tiger,(170,670))
	screen.blit(img_tiger,(670,170))
	screen.blit(img_tiger,(670,670))

while not done:
	board(screen)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	#flip call is required in order for any updates that we make to the game screen to become visible.
	pygame.display.flip()
	
