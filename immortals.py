import libtcodpy as libtcod
import dungeon

#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy, map):
        #move by a given amount
        if not map.tiles[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        #set the color and then draw the character that represents this object at its position
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
    
    def clear(self):
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

def render_all(objects, map, console, fov_recompute, fov_map, playerx, playery):
    #render a lit of objects to a console
    if fov_recompute:
        libtcod.map_compute_fov(fov_map, playerx, playery, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
        map.render_map_background(console, fov_map)

    #draw all objects in the list
    for object in objects:
        object.draw()

    #blit the contents of con to the root console
    libtcod.console_blit(console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def handle_keys():

    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit' #exit game

    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1, map)
        return 'recompute fov'
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1, map)
        return 'recompute fov'
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0, map)
        return 'recompute fov'
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0, map)
        return 'recompute fov'
    

#######################################
# Initialization and main loop
#######################################


libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Immortals', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

map = dungeon.Map(MAP_WIDTH, MAP_HEIGHT)
map.create_rect_dun(10, 6, 30)

fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x, y,
                not map.tiles[x][y].block_sight, not map.tiles[x][y].blocked)

player = Object(map.startingx, map.startingy, '@', libtcod.white)
#npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
#objects = [npc, player]
objects = [player]
recompute_fov = True

while not libtcod.console_is_window_closed():

    
    render_all(objects, map, con, recompute_fov, fov_map, player.x, player.y)   
    recompute_fov = False

    libtcod.console_flush()

    for object in objects:
        object.clear()

    #handle keys and exit game if needed
    result = handle_keys() # should probably fix this, weird global stuff
    if result == 'exit':
        break
    elif result == 'recompute fov':
        recompute_fov = True
