import pygame
from pygame.sprite import Sprite


class HealthPoint(Sprite):
	"""Описывает объект, обозначающий жизни игрока"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('images/hp.png')
		self.rect = self.image.get_rect()
