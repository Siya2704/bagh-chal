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
	global occupied
	occupied = [['-' for col in range(5)] for row in range(5)]

	return coord,occupied

def moves(cur_pos,coord):
	x = cur_pos[0];y = cur_pos[1]
	#left, right, up, down
	global pos
	global co
	pos1 = [(-125,0),(125,0),(0,-125),(0,125),(-125,-125),(-125,125),(125,-125),(125,125)]
	pos2 = [(-125,0),(125,0),(0,-125),(0,125)]
	co1 = [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(1,-1),(-1,1),(1,1)]
	co2 = [(0,-1),(0,1),(-1,0),(1,0)]
	pos_n = []
	c = coord[x][y]
	if((c[0]+c[1]) % 2 == 0):
		pos = pos1
		co = co1
		n = 8
	else:
		pos = pos2
		co = co2
		n = 4
	p = x
	q = y
	for i in range(n):
		p = x+co[i][0]
		q = y+co[i][1]
		#it checks if there is goat or not for possible moves
		if(p >= 0 and q >= 0 and p < 5 and q < 5 and occupied[p][q] == '-'):
			xn = c[0] + pos[i][0];yn = c[1] + pos[i][1]
			pos_n.append((xn,yn,i))
		elif(p >= 0 and q >= 0 and p < 5 and q < 5 and occupied[p][q] == 'G'):
			p1 = p+co[i][0]
			q1 = q+co[i][1]
			if(p1 >= 0 and q1 >= 0 and p1 < 5 and q1 < 5 and occupied[p1][q1] == '-'):
				xn = c[0] + pos[i][0]*2;yn = c[1] + pos[i][1]*2
				pos_n.append((xn,yn,i))
	#print(pos_n)
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

def goal(kill):
	return kill == 5

def minimax (curDepth, nodeIndex,maxTurn, scores,targetDepth):
 
    # base case : targetDepth reached
    if (curDepth == targetDepth):
        return scores[nodeIndex]
     
    if (maxTurn):
        return max(minimax(curDepth + 1, nodeIndex * 2,
                    False, scores, targetDepth),
                   minimax(curDepth + 1, nodeIndex * 2 + 1,
                    False, scores, targetDepth))
     
    else:
        return min(minimax(curDepth + 1, nodeIndex * 2,True, scores, targetDepth), minimax(curDepth + 1, nodeIndex * 2 + 1,True, scores,targetDepth))
   

def place_goat(occ):
	for i in range(5):
		for j in range(5):
			if(occ[i][j] == '-'):
				if(i == 0 and j == 0):#left top
					if (occ[i+1][j] == 'T' or occ[i][j+1] == 'T' or occ[i+1][j+1]):
						occ[i][j] = 'G'
						break
					elif((occ[i+1][j] == 'G' and occ[i+2][j] == 'T') or (occ[i][j+1] == 'G' and occ[i][j+2] == 'T')):
						occ[i][j] = 'G'
						break
				elif(i == 4 and j == 0):#right top
					if (occ[i-1][j] == 'T' or occ[i][j+1] == 'T' or occ[i-1][j+1]):
						occ[i][j] = 'G'
						break
					elif((occ[i-1][j] == 'G' and occ[i-2][j] == 'T') or (occ[i][j+1] == 'G' and occ[i][j+2] == 'T')):
						occ[i][j] = 'G'
						break
				elif(i == 0 and j ==4):#left bottom
					if (occ[i+1][j] == 'T' or occ[i][j-1] == 'T' or occ[i+1][j-1]):
						occ[i][j] = 'G'
						break
					elif((occ[i+1][j] == 'G' and occ[i+2][j] == 'T') or (occ[i][j-1] == 'G' and occ[i][j-2] == 'T')):
						occ[i][j] = 'G'
						break
				elif(i == 4 and j == 4):#right bottom
					if (occ[i-1][j] == 'T' or occ[i][j-1] == 'T' or occ[i-1][j-1]):
						occ[i][j] = 'G'
						break
					elif((occ[i-1][j] == 'G' and occ[i-2][j] == 'T') or (occ[i][j-1] == 'G' and occ[i][j-2] == 'T')):
						occ[i][j] = 'G'
						break
		
     
def solve():
	coord,occupied = get_coord()
	occupied[0][4] = 'T';occupied[4][0] = 'T';
	occupied[0][0]  ='T';occupied[4][4] = 'T';
	occupied[1][0] = 'G'
	kill = 0
	flag = 0
	goat_remaining = 20
	done = False
	while not done:
		board(screen,occupied,coord)
		if(goal(kill)):
			return True
		if(flag == 0):
			place_goat(occupied)
			flag = 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:	
				cd = get_mouse_click(coord, occupied)
				dragging = True
			elif event.type == pygame.MOUSEBUTTONUP:
				dragging = False
				cu = get_mouse_click(coord, occupied)
				if ((cd[0]==-1 and cd[1] == -1) or (cu[0]==-1 and cu[1] == -1)):
					pass
				else:
					a1 = coord[cu[0]][cu[1]]
					move = moves(cd, coord)
					#print(move)
					for i in range(len(move)):
						a3 = move[i]
						if(a1[0]==a3[0] and a1[1]==a3[1]):
							if(125 <abs(a1[0] - cd[0])<250  or 125<abs(a1[1]-cd[0])<250):
								kill = kill + 1
								#print(co[a3[2]])
								p = cd[0]+co[a3[2]][0]
								q = cd[1]+co[a3[2]][1]
								occupied[p][q] = '-'
							occupied[cu[0]][cu[1]] = 'T';
							occupied[cd[0]][cd[1]] = '-';
							flag = 0#next computer's move
							break

						
		pygame.display.flip()

def main():
	solve()
if __name__ == "__main__":
	main()
