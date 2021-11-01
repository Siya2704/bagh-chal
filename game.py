import pygame
 
pygame.init()
screen = pygame.display.set_mode((1300,900))
color = (255,204,153)
screen.fill(color)
pygame.display.set_caption('Bagh-Chal')
done = False

img_board = pygame.image.load('img/board.png')
img_tiger = pygame.image.load('img/tiger.png')
img_tiger = pygame.transform.scale(img_tiger, (60,60))
img_goat = pygame.image.load('img/goat.png')
img_goat = pygame.transform.scale(img_goat, (60,60))

def get_coord():
	coord = [[(170,170),(295,170),(420,170),(545,170),(670,170)],[(170,295),(295,295),(420,295),(545,295),(670,295)],[(170,420),(295,420),(420,420),(545,420),(670,420)],[(170,545),(295,545),(420,545),(545,545),(670,545)],[(170,670),(295,670),(420,670),(545,670),(670,670)]] #2d array
	#left, right, top, down
	occupied = [['-' for col in range(5)] for row in range(5)]
	return coord,occupied

def moves(cur_pos):
	x = cur_pos[0];y = cur_pos[1]
	#left, right, up, down
	pos = [(-125,0),(125,0),(0,-125),(0,125),(-125,-125),(-125,125),(125,-125),(125,125)]
	pos_n = []
	for i in range(8):
		xn = x + pos[i][0];yn = x + pos[i][1]
		pos_n.append((xn,yn))
	return pos_n
	

def get_mouse_click(coord, occupied):
	x,y=pygame.mouse.get_pos()
	#board starting at 200,200
	for i in range(5):
		for j in range(5):
			k = coord[i][j]
			if(k[0] <= x and k[1] <= y and k[0]+60 >= x and k[1]+60 >= y):
				coord_tiger = (i,j)
				return coord_tiger
	return (-1,-1)


def board(screen,occupied,coord):
	pygame.draw.rect(screen, (255,255,255), pygame.Rect(90, 90, 1120, 720))
	screen.blit(img_board,(200,200))#size 500X500
	for i in range(5):
		for j in range(5):
			if(occupied[i][j] == 'T'):
				screen.blit(img_tiger,coord[i][j])
			if(occupied[i][j] == 'G'):
				screen.blit(img_goat,coord[i][j])



coord,occupied = get_coord()
occupied[0][4] = 'T';occupied[4][0] = 'T';
occupied[0][0]  ='T';occupied[4][4] = 'T';
while not done:
	board(screen,occupied,coord)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.MOUSEBUTTONDOWN:	
			cd = get_mouse_click(coord, occupied)
			dragging = True
		elif event.type == pygame.MOUSEBUTTONUP:
			dragging = False
			cu = get_mouse_click(coord, occupied)
			if (cd[0]==-1 and cd[1] == -1 and cu[0]==-1 and cu[1] == -1):
				pass
			else:
				move = moves(cd)
				for i in range(8):
					print(move[i], cu)
					a1 = coord[cu[0]][cu[1]]
					a2 = coord[cd[0]][cd[1]]
					a3 = move[i]
					if(a1[0]==a2[0]+a3[0] and a1[1]==a2[1]+a3[1] and occupied[cu[0]][cu[1]] == '-'):
						print("ok")
						occupied[cu[0]][cu[1]] = 'T';
						occupied[cd[0]][cd[1]] = '-';

	pygame.display.flip()
	

#add diagnol coordinate
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
