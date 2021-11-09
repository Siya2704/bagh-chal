
import pygame
import sys,time,random
INF = 1e6
from copy import deepcopy
pygame.init()
screen = pygame.display.set_mode((1300,900))
color = (255,204,153)
screen.fill(color)
pygame.display.set_caption('Bagh-Chal')

img_board = pygame.image.load('img/board.png')
img_tiger = pygame.image.load('img/tiger.png')
img_tiger = pygame.transform.scale(img_tiger, (60,60))
img_goat = pygame.image.load('img/goat.png')
img_goat = pygame.transform.scale(img_goat, (60,60))
myfont = pygame.font.SysFont("Comic Sans MS", 50)

def get_coord():
	global coord
	coord = [[(170,170),(295,170),(420,170),(545,170),(670,170)],[(170,295),(295,295),(420,295),(545,295),(670,295)],[(170,420),(295,420),(420,420),(545,420),(670,420)],[(170,545),(295,545),(420,545),(545,545),(670,545)],[(170,670),(295,670),(420,670),(545,670),(670,670)]] #2d array
	#left, right, top, down
	global occupied
	occupied = [['-' for col in range(5)] for row in range(5)]

	return coord,occupied
def get_moves(cur_pos,coord,kill):
	x = cur_pos[0];y = cur_pos[1]
	kill_coord = []
	#left, right, up, down
	global pos
	global co
	pos1 = [(-125,0),(125,0),(0,-125),(0,125),(-125,-125),(-125,125),(125,-125),(125,125)]
	pos2 = [(-125,0),(125,0),(0,-125),(0,125)]
	co1 = [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(1,-1),(-1,1),(1,1)]
	co2 = [(0,-1),(0,1),(-1,0),(1,0)]
	pos_n = []
	pos_t = []
	c = coord[x][y]
	d =(x,y)
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
			pos_t.append((p,q))
		elif(p >= 0 and q >= 0 and p < 5 and q < 5 and occupied[p][q] == 'G'):
			p1 = p+co[i][0]
			q1 = q+co[i][1]
			if(p1 >= 0 and q1 >= 0 and p1 < 5 and q1 < 5 and occupied[p1][q1] == '-'):
				xn = c[0] + pos[i][0]*2;yn = c[1] + pos[i][1]*2
				pos_n.append((xn,yn,i))
				pos_t.append((p1,q1))
				kill = kill + 1
				kill_coord.append(((x,y),(p1,q1)))
	#print(pos_n)
	return pos_n,pos_t,kill,kill_coord
	
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


def board(screen,occupied,coord,score,goat_killed,goat_remaining):
	pygame.draw.rect(screen, (255,255,255), pygame.Rect(90, 90, 1120, 720))
	screen.blit(img_board,(200,200))#size 500X500
	label = myfont.render("Score:", 1, (0,0,0))
	screen.blit(label, (800, 350))
	sc = myfont.render(str(score), 1, (0,0,0))
	screen.blit(sc, (920, 350))
	label = myfont.render("Goats Killed:", 1, (0,0,0))
	screen.blit(label, (800, 400))
	sc = myfont.render(str(goat_killed), 1, (0,0,0))
	screen.blit(sc, (1030, 400))
	
	label = myfont.render("Goats Remaining:", 1, (0,0,0))
	screen.blit(label, (800, 450))
	sc = myfont.render(str(goat_remaining), 1, (0,0,0))
	screen.blit(sc, (1110, 450))
	label = myfont.render("Player1", 1, (0,0,255))
	screen.blit(label, (800, 260))
	screen.blit(img_goat, (800, 200))
	label = myfont.render("Player2", 1, (0,0,255))
	screen.blit(label, (970, 260))
	screen.blit(img_tiger, (980, 195))
	for i in range(5):
		for j in range(5):
			if(occupied[i][j] == 'T'):
				screen.blit(img_tiger,coord[i][j])
			if(occupied[i][j] == 'G'):
				screen.blit(img_goat,coord[i][j])

def isMoveLeft(arr):
	for i in range(5):
		for j in range(5):
			if(arr[i][j] == '-'):
				return True
	return False

#all possible moves of all tiger
def all_tiger_moves(arr):
	pos_tiger = []
	count = 0
	for i in range(5):
		for j in range(5):
			if(arr[i][j] == 'T'):
				m = get_moves((i,j),coord,0)
				for k in m[1]:
					pos_tiger.append(((i,j),k))
	return pos_tiger

#all possible moves of goat
def goat_moves(arr):
	pos_goat = []
	for i in range(5):
		for j in range(5):
			if(arr[i][j] == '-'):
				pos_goat.append((i,j))
	return pos_goat
def goal(kill):
	return kill == 5
	
def evaluate_kill(arr):
	kill = 0
	for i in range(5):
		for j in range(5):
			if(arr[i][j] == 'T'):
				m = get_moves((i,j),coord,0)
				kill += m[2]
	return kill

#it will return all movable tigers
def movable_tiger(arr):
	Tiger = []
	m_T = 0
	for i in range(5):
		for j in range(5):
			if(arr[i][j] == 'T'):
				Tiger.append((i,j))
	for i in Tiger:
		move = get_moves(i,coord,0)
		if(len(move[0]) > 0):
			m_T = m_T + 1
	return m_T

###########				
def moves(cur_pos,coord,kill):
	x = cur_pos[0];y = cur_pos[1]
	#left, right, up, down
	global pos
	global co
	pos1 = [(-125,0),(125,0),(0,-125),(0,125),(-125,-125),(-125,125),(125,-125),(125,125)]
	pos2 = [(-125,0),(125,0),(0,-125),(0,125)]
	co1 = [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(1,-1),(-1,1),(1,1)]
	co2 = [(0,-1),(0,1),(-1,0),(1,0)]
	pos_n = []
	pos_t = []
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
			pos_t.append((p,q))
		elif(p >= 0 and q >= 0 and p < 5 and q < 5 and occupied[p][q] == 'G'):
			p1 = p+co[i][0]
			q1 = q+co[i][1]
			if(p1 >= 0 and q1 >= 0 and p1 < 5 and q1 < 5 and occupied[p1][q1] == '-'):
				xn = c[0] + pos[i][0]*2;yn = c[1] + pos[i][1]*2
				pos_n.append((xn,yn,i))
				pos_t.append((p1,q1))
				kill = kill + 1
	#print(pos_n)
	return pos_n,pos_t,kill

#this will return minimum score for min(goat)
def minimax(arr,depth,isMax,alpha,beta) :
	if(depth == 6):
		return 0

	if (isMoveLeft(arr) == False) :
		return 0

	if (isMax) :
		#tiger
		best = evaluate_kill(arr)+movable_tiger(arr)
		pos_tiger = all_tiger_moves(arr)
		for i in pos_tiger:
			old = i[0];new = i[1]
			arr[old[0]][old[1]] = '-'
			arr[new[0]][new[1]] = 'T'
			best = evaluate_kill(arr)+movable_tiger(arr)
			best = max(best,minimax(arr,depth,not isMax,alpha,beta))
			alpha = max(alpha,best)
			if beta <= alpha:
				arr[old[0]][old[1]] = 'T'
				arr[new[0]][new[1]] = '-'
				break
			arr[old[0]][old[1]] = 'T'
			arr[new[0]][new[1]] = '-'
		return best

	else :#goat
		best =  evaluate_kill(arr)
		moves = goat_moves(arr)
		for m in moves:
			arr[m[0]][m[1]] = 'G'
			best = min(best,minimax(arr,depth+1,not isMax,alpha,beta))
			if beta <= alpha:
				arr[m[0]][m[1]] = '-'
				break
			arr[m[0]][m[1]] = '-'
		return best

def goat_remove(arr):
	best1,best2,best3,best4 = 100,100,100,100
	old1,old2,old3,old4 = (-1,-1),(-1,-1),(-1,-1),(-1,-1)
	for i in range(2):
		for j in range(3):
			if(arr[i][j] == 'G'):
				arr[i][j] = '-'
				x = movable_tiger(arr)+ evaluate_kill(arr)
				if(x < best1):
					best1 = x
					old1=(i,j)
				arr[i][j] = 'G'
		for j in range(3,5):
			if(arr[i][j] == 'G'):
				arr[i][j] = '-'
				x = movable_tiger(arr)+ evaluate_kill(arr)
				if(x < best4):
					best4 = x
					old4=(i,j)
				arr[i][j] = 'G'
		if(best4 < best1):
			best1 = best4
			old1 = old4
	for i in range(2,5):
		for j in range(3):
			if(arr[i][j] == 'G'):
				arr[i][j] = '-'
				x = movable_tiger(arr)+ evaluate_kill(arr)
				if(x < best2):
					best2 = x
					old2=(i,j)
				arr[i][j] = 'G'
		for j in range(3,5):
			if(arr[i][j] == 'G'):
				arr[i][j] = '-'
				x = movable_tiger(arr)+ evaluate_kill(arr)
				if(x < best3):
					best3 = x
					old3=(i,j)
				arr[i][j] = 'G'
		if(best3 <= best2):
			best2 = best3
			old2 = old3
	if(best1 < best2):
		best2 = best1
		old2 = old1
	return old2

#it will chooose bestMove and return
def findBestMove(arr,kill,goat_remain) :
	bestVal1,bestVal2= 1000,1000
	bestMove1,bestMove2= (-1, -1), (-1, -1)
	for i in range(3):
		for j in range(5):
			if(arr[i][j] == '-'):
				occupied[i][j] = 'G'
				alpha = evaluate_kill(arr)+movable_tiger(arr)
				beta = evaluate_kill(arr)
				moveVal = minimax(arr, 0, False,alpha,beta)
				if(moveVal <= bestVal1):
					bestVal1 = moveVal
					bestMove1 = (i,j)
				occupied[i][j] = '-'
	for i in range(3,5):
		for j in range(5):
			if(arr[i][j] == '-'):
				occupied[i][j] = 'G'
				alpha = evaluate_kill(arr)+movable_tiger(arr)
				beta = evaluate_kill(arr)
				moveVal = minimax(arr, 0, False,alpha,beta)
				if(moveVal < bestVal2):
					bestVal2 = moveVal
					bestMove2 = (i,j)
				occupied[i][j] = '-'
	if(bestVal1 <= bestVal2):
		bestVal2 = bestVal1
		bestMove2 = bestMove1
	
	if goat_remain == False:
		old = goat_remove(arr)
		occupied[old[0]][old[1]] = '-'
	return bestMove2
					
	
############
class reverse_game:	
	#it will chooose bestMove and return
	def findBestMove(self,arr) :
		cn = []
		for i in range(5):
			for j in range(5):
				if(arr[i][j] == 'T'):
					k = get_moves((i,j),coord,0)[2]
					k_l = get_moves((i,j),coord,0)[1]
					k_c = get_moves((i,j),coord,0)[3]
					if(k != 0):
						x = k_c[0]
						old = x[0]
						new = x[1]
						return old,new
					else:
						if(len(k_l) != 0):
							for l in k_l:	
								cn.append(((i,j),l))
		length = len(cn)
		i = random.randint(0,length-1)
		cn = cn[i]
		return cn[0],cn[1]
		
			  
def solve():
	rgamer = reverse_game()
	coord,occupied = get_coord()
	occupied[0][4] = 'T';occupied[4][0] = 'T';
	occupied[0][0]  ='T';occupied[4][4] = 'T';
	moves_left=10 #used when goats_remaining=0
	g = [(2,0),(0,2),(1,2),(2,1),(3,2),(2,3),(2,2),(4,2),(2,4)]
	i = random.randint(0,7)
	i = g[i]
	occupied[i[0]][i[1]] = 'G'
	done = False
	kill = 0
	flag = 1
	goat_remaining = 20
	done = False
	global score
	score = 0
	while not done:
		time.sleep(1)
		board(screen,occupied,coord,score,kill,goat_remaining)
		if(goal(kill)):
			myfont = pygame.font.SysFont("Comic Sans MS", 150)
			label = myfont.render("Tiger Won!!", 1, (255,0,0))
			screen.blit(label, (710, 400))
			done = True
			pygame.display.flip()
			time.sleep(5)
		elif(movable_tiger(occupied) == 0 or moves_left == 0):
			myfont = pygame.font.SysFont("Comic Sans MS", 150)
			label = myfont.render("Goat Won!!", 1, (255,0,0))
			screen.blit(label, (710, 400))
			done = True
			pygame.display.flip()
			time.sleep(5)
		elif(flag == 0 and goat_remaining != 0):
			bestMove = findBestMove(occupied,kill,True)
			#print(bestMove)
			occupied[bestMove[0]][bestMove[1]] = 'G'
			goat_remaining -= 1
			flag = 1
		elif(flag == 0 and goat_remaining == 0):
			moves_left -= 1
			bestMove = findBestMove(occupied,kill,False)
			#print(bestMove)
			occupied[bestMove[0]][bestMove[1]] = 'G'
			flag = 1
		elif(flag == 1):
			old_pos,new_pos = rgamer.findBestMove(occupied)
			#print(bestMove)
			occupied[old_pos[0]][old_pos[1]] = '-'
			occupied[new_pos[0]][new_pos[1]] = 'T'
			if(abs(old_pos[0] - new_pos[0]) == 2  or abs(old_pos[1]-new_pos[1]) == 2):#kill goat
				if((old_pos[0] - new_pos[0] == 2) and (old_pos[1] - new_pos[1] == 2)):
					occupied[new_pos[0]+1][new_pos[1]+1] = '-'
				elif((old_pos[0] - new_pos[0] == 2) and (new_pos[1] - old_pos[1] == 2)):
					occupied[new_pos[0]+1][new_pos[1]-1] = '-'
				elif((new_pos[0] - old_pos[0] == 2) and (old_pos[1] - new_pos[1] == 2)):
					occupied[new_pos[0]-1][new_pos[1]+1] = '-'
				elif((new_pos[0] - old_pos[0] == 2) and (new_pos[1] - old_pos[1] == 2)):
					occupied[new_pos[0]-1][new_pos[1]-1] = '-'
				elif(old_pos[0] - new_pos[0] == 2):
					occupied[new_pos[0]+1][new_pos[1]] = '-'
				elif(new_pos[0] - old_pos[0] == 2):
					occupied[new_pos[0]-1][new_pos[1]] = '-'
				elif(old_pos[1] - new_pos[1] == 2):
					occupied[new_pos[1]][new_pos[1]+1] = '-'
				elif(new_pos[1] - old_pos[1] == 2):
					occupied[new_pos[0]][new_pos[1]-1] = '-'
				kill = kill + 1
				score = score + 12 *1 - (4 - movable_tiger(occupied))*3
			flag = 0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
						
		pygame.display.flip()

def main():
	solve()
if __name__ == "__main__":
	main()

  
