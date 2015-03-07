import libtcodpy as libtcod

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Map:
    #a map for our roguelike
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[ Tile(True)
            for y in range(height) ]
                for x in range(width) ]
        self.startingx = width / 2
        self.startingy = height / 2
        self.color_dark_wall = libtcod.Color(0, 0, 100)
        self.color_dark_ground = libtcod.Color(50, 50, 150)
        self.color_light_wall = libtcod.Color(130, 110, 50)
        self.color_light_ground = libtcod.Color(200, 180, 50)
    def render_map_background(self, console, fov_map):
        for y in range(self.height):
            for x in range(self.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = self.tiles[x][y].block_sight
                if not visible:
                    if self.tiles[x][y].explored:
                    #only show not visible if explored
                        if wall:
                            libtcod.console_set_char_background(console,
                                x, y, self.color_dark_wall, libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(console,
                                x, y, self.color_dark_ground, libtcod.BKGND_SET)
                else:
                    #it is visible
                    if wall:
                        libtcod.console_set_char_background(console,
                            x, y, self.color_light_wall, libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(console,
                            x, y, self.color_light_ground, libtcod.BKGND_SET)
                    self.tiles[x][y].explored = True

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_rect_room(self, rect):
        #go through the tiles in the rectangle and make them passable
        for x in range(rect.x1 + 1, rect.x2):
            for y in range(rect.y1 + 1, rect.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
    
    def create_rect_dun(self, room_max_size, room_min_size, max_rooms):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            #random width and height
            w = libtcod.random_get_int(0, room_min_size, room_max_size)
            h = libtcod.random_get_int(0, room_min_size, room_max_size)
            #random position without going out of the boundaries of the map
            x = libtcod.random_get_int(0, 0, self.width - w - 1)
            y = libtcod.random_get_int(0, 0, self.height - h - 1)

            new_room = Rect(x, y, w, h)
            #run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                #this means there are no intersections, so this room is valid

                #paint it to the map's tiles
                self.create_rect_room(new_room)

                #center coordinates will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    #this is the first room, where the player starts at
                    self.startingx = new_x
                    self.startingy = new_y
                else:
                    #all rooms after the first, connect it to the prev
                    #room with a tunnel
                    (prev_x, prev_y) = rooms[num_rooms-1].center()

                    #flip a coin
                    if libtcod.random_get_int(0, 0, 1) == 1:
                        #first move horiz, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                rooms.append(new_room)
                num_rooms += 1


class Rect:
    # a rectangle on the map
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


