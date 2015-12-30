from base_classes import *
PLAY_NOTE = "PLAY_NOTE"
class NoteEvent(Event):
	def __init__(self, note):
		super().__init__(PLAY_NOTE)
		self.note = note

PLAYER_COLLIDED_APPLY_PHYSICS = "PLAYER_COLLIDED_APPLY_PHYSICS"


SET_COLOR = "SET_COLOR"
class SetColorEvent(Event):
	def __init__(self, color):
		super().__init__(SET_COLOR)
		self.color = color

PLAYER_COLLISION_EVENT = "PLAYER_COLLISION_EVENT"
class PlayerCollisionEvent(Event):
	def __init__(self, player, collider):
		super().__init__(PLAYER_COLLISION_EVENT) #refactor

		#hmm, pass messages or directly
		self.player = player
		self.collider = collider