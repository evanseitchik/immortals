

##########
start the game
########

game = Game()
game.run()

#######

class Game:
    def __init__(self, CONFIGURATION):
        self.world = World(WORLD_CONFIGURATION)
        self.renderer = Renderer(RENDER_CONFIG)
        self.game_loop = GameLoop()

    def run(self):
        while self.game_loop.last_key is not 'q':
            self.game_loop.run()

###########
Gameworld.py is a  module

class GameWorld:
    def __init__(self, CONFIGURATION):
        self.CONFIGURATION = CONFIGURATION
        self.game_map = GameMap(MAP_CONFIGURATION)
        self.game_objects = self.initialize_game_objects(STARTING_OBJECT_CONFIGURATION)

    def initialize_game_objects
        collection = [GameObject(configuration)
                for configuration in self.configuration.objects]
        return collection

class GameMap:

class DungeonGenerator

class GameObject:
    def __init__(CONFIGURATION)
        item_make_a_game_object


class Player(GameObject):

###########
class Renderer:
    def __init__
    set_up_doryen(DORYEN_CONFIG)




