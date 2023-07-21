class Settings():
	"""Класс для хранения всех настроек игры Alien Invasion"""
	def __init__(self):
		"""Инициализирует статические настройки игры"""
		# Параметры экрана
		self.screen_width = 1920
		self.screen_height = 1020
		self.bg_color = (150, 200, 230)

		# Настройки корабля
		self.ship_limit = 2

		# Параметры снарядов
		self.bullet_width = 15
		self.bullet_height = 50
		self.bullet_color = (60, 30, 30)
		self.bullets_allowed = 8
		
		# Настройки пришельцев
		self.fleet_drop_speed = 50
		

		# Темп ускорения игры
		self.speedup_scale = 1.1
		# Темп роста стоимости пришельцев
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Инициализирует настройки, изменяющиеся в ходе игры"""
		self.ship_speed = 5.5
		self.bullet_speed = 10
		self.alien_speed = 2.0

		# fleet_direction = 1 обозначает движение вправо, а -1 - влево
		self.fleet_direction = 1

		# Подсчет очков
		self.alien_points = 50

	def increase_speed(self):
		"""Увеличивает настройки скорости и стоимоси пришельцев"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
