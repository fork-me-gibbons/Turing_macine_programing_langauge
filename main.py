import src
import pygame

chadEdit = print('I chad')

pygame.init()

while True :
	Input = input('TM:\ ')

	tokens = src.run(Input)
	print(tokens)
	chadEdit