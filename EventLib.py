from base_classes import *
import collections

#This is not very elegant
#Maybe just have the default event contain a dictionary that people can put whatever into

PLAY_NOTE = "PLAY_NOTE"
class NoteEvent(Event):
    def __init__(self, note):
        super().__init__(PLAY_NOTE)
        self.note = note

PLAYER_COLLIDED_APPLY_PHYSICS = "PLAYER_COLLIDED_APPLY_PHYSICS"


WALL_COLLISION = "PLAYER COLLIDED WITH WALL"

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

PLAYER_ON_TILE_EVENT = "PLAYER_ON_TILE_EVENT"
class PlayerOnTileEvent(Event):
    def __init__(self, tileRect):
        super().__init__("PLAYER_ON_TILE_EVENT")
        self.tileRect = tileRect


class GenericCollisionEvent:
    key = "GENERIC_COLLISION"

class DamageEvent:
    key = "DAMAGE"
    def __init__(self, damage):
        self.damage = damage
class FlinchEvent:
    key = "FLINCH"