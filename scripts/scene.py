import pygame, scripts.assets, json, math

# ---------------------------- #
# -   Alfed's Scene Script   - #
# ---------------------------- #

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
FALL_BLOCKS = [0, 1, 2, 13, 26, 'hack']

class Scene:
    def __init__(self, game, path='NONE'):
        self.game = game
        self.path = path

        self.tiles = dict()

        if path == 'NONE':
            self.tiles['exit'] = ((0, 0))
            self.tiles['5;5'] = ((5,5), 0)
            self.tiles['6;5'] = ((6,5), 1)
            self.tiles['7;5'] = ((7,5), 2)
            
            self.tiles['5;6'] = ((5,6), 7)
            self.tiles['6;6'] = ((6,6), 8)
            self.tiles['7;6'] = ((7,6), 9)
            
            self.tiles['5;7'] = ((5,7), 14)#self.game.assets['tiles'][14])
            self.tiles['6;7'] = ((6,7), 15)#self.game.assets['tiles'][15])
            self.tiles['7;7'] = ((7,7), 16)#self.game.assets['tiles'][16])
            
            self.tiles['5;8'] = ((5,8), 28)#self.game.assets['tiles'][28])
            self.tiles['6;8'] = ((6,8), 29)#self.game.assets['tiles'][29])
            self.tiles['7;8'] = ((7,8), 30)#self.game.assets['tiles'][30])
        else:
            self.load_from_path()

        try:
            self.tiles['spawners']
        except:
            self.tiles['spawners'] = []

        self.doorrect = pygame.Rect(self.tiles['exit'][0]*16, self.tiles['exit'][1]*16, 16, 32)
        self.spawners = self.tiles['spawners']

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // 16), int(pos[1] // 16))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tiles:
                tiles.append(self.tiles[check_loc])
            if check_loc+';-1' in self.tiles:
                tiles.append(self.tiles[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        ishacking = False
        for tile in self.tiles_around(pos):
            if not tile[1] in FALL_BLOCKS:
                rects.append(pygame.Rect(tile[0][0] * 16, tile[0][1] * 16, 16, 16))
            if tile[1] == 'hack' and not self.game.hacked:
                ishacking = True
        self.game.hacking = ishacking
        return rects

    def load_from_path(self):
        f = open(self.path)
        self.tiles = json.load(f)
        f.close()

    def render(self, display, display2, camera):
        for key, value in self.tiles.items():
            if key != 'exit' and key != 'spawners' and value[1] != 'hack' and value[1] != 'box':
                display.blit(self.game.assets['tiles'][value[1]], (value[0][0]*16-camera[0], value[0][1]*16-camera[1]))
            elif key == 'spawners':
                pass
            elif value[1] == 'hack':
                if not self.game.hacked:
                    display.blit(self.game.assets['hack'], (value[0][0]*16-camera[0], value[0][1]*16-camera[1]+math.sin(self.game.ticks/60)*10))
            elif value[1] == 'box':
                display.blit(self.game.assets['box'], (value[0][0]*16-camera[0], value[0][1]*16-camera[1]))
                display2.blit(self.game.assets['box'], (value[0][0]*16-camera[0], value[0][1]*16-camera[1]))
            else:
                display.blit(self.game.assets['door'], (value[0]*16-camera[0], value[1]*16-camera[1]))
