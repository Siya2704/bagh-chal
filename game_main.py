import pygame
import runpy
import auto_play
import os
import time
pygame.init()
screen = pygame.display.set_mode((450,400))
color = (235,245,255)
screen.fill(color)
pygame.display.set_caption('Bagh-Chal')
color = (100,100,100)

color_light = (100,100,100)
color_dark = (250,250,250)
width=screen.get_width()
height = screen.get_height()
font = pygame.font.SysFont("Corbel",35)
text = font.render('Choose Your Player',True, color)
screen.blit(text,(140,110))
font = pygame.font.SysFont("Corbel",35)
text = font.render('Auto Play',True, color)
pygame.draw.rect(screen,color,pygame.Rect(160,150,140,40) ,2)
screen.blit(text,(170,160))
font = pygame.font.SysFont("Corbel",35)
text = font.render('Tiger',True, color)
pygame.draw.rect(screen,color,pygame.Rect(160,200,140,40) ,2)
screen.blit(text,(170,210))
font = pygame.font.SysFont("Corbel",35)
text = font.render('Goat',True, color)
pygame.draw.rect(screen,color,pygame.Rect(160,250,140,40) ,2)
screen.blit(text,(170,260))
font = pygame.font.SysFont("Corbel",35)
text = font.render('Quit',True, color)
pygame.draw.rect(screen,color,pygame.Rect(160,300,140,40) ,2)
screen.blit(text,(170,310))
while True:
	mouse = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if(160 <=mouse[0] and mouse[0] <=300 and 150 <=mouse[1]and mouse[1]<=190):
				os.system('python3 auto_play.py')
			if(160 <=mouse[0] and mouse[0] <=300 and 200 <=mouse[1]and mouse[1]<=240):
				os.system('python3 baghchal.py')
			if(160 <=mouse[0] and mouse[0] <=300 and 250 <=mouse[1]and mouse[1]<=290):
				os.system('python3 reverse_baghchal.py')
			if(160 <=mouse[0] and mouse[0] <=300 and 200 <=mouse[1]and mouse[1]<=340):
				pygame.quit()
	#mouse = pygame.mouse.get_pos()
	#pygame.display.flip()
	pygame.display.update()











