import asyncio, pygame, sys, time, scripts.scene, scripts.assets, json

# ---------------------------- #
# -  Atfed's Alakajam Entry  - #
# ---------------------------- #

class Editor:
    def __init__(self):
        pygame.init()
        
        self.display = pygame.display.set_mode((960, 240*3))
        self.window = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Level Editor')
        pygame.display.set_icon(pygame.image.load('_internal/assets/game.ico'))

        self.assets = dict()
        self.assets['tiles'] = scripts.assets.load_assets('_internal/assets/tiles')
        self.assets['door'] = scripts.assets.load_asset('_internal/assets/door.png')
        self.assets['bg'] = scripts.assets.load_asset('_internal/assets/bg.png')
        self.assets['hack'] = scripts.assets.load_asset('_internal/assets/tiles/hack.png')
        self.assets['box'] = scripts.assets.load_asset('_internal/assets/box.png')
        
        self.scene = scripts.scene.Scene(self, path='NONE')
        self.scenecamera = [0, 0]

        self.tile = '0'
        self.hacked = False
        self.ticks = 0

    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                try:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        strpos = str(int((pos[0]+self.scenecamera[0]*3)/48))+';'+str(int((pos[1]+self.scenecamera[1]*3)/48))
                        if self.tile != 'door' and self.tile != 'box' and self.tile != 'spawner' and self.tile != 'hack':
                            self.scene.tiles[strpos] = ((int(strpos.split(';')[0]), int(strpos.split(';')[1])), int(self.tile))
                        elif self.tile == 'spawner':
                            self.scene.tiles['spawners'].append([int(strpos.split(';')[0]), int(strpos.split(';')[1])])
                            print(self.scene.tiles['spawners'])
                        elif self.tile == 'hack':
                            self.scene.tiles[strpos] = ((int(strpos.split(';')[0]), int(strpos.split(';')[1])), self.tile)
                        elif self.tile == 'box':
                            self.scene.tiles[strpos] = ((int(strpos.split(';')[0]), int(strpos.split(';')[1])), self.tile)
                        else:
                            self.scene.tiles['exit'] = ((int(strpos.split(';')[0]), int(strpos.split(';')[1])))
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        pos = pygame.mouse.get_pos()
                        strpos = str(int((pos[0]+self.scenecamera[0]*3)/48))+';'+str(int((pos[1]+self.scenecamera[1]*3)/48))
                        self.scene.tiles.pop(strpos)
                except Exception as e:
                    print(e)
                
##                try:
##                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
##                        pos = pygame.mouse.get_pos()
##                        strpos = str(int((pos[0]+self.scenecamera[0]*3)/48))+';'+str(int((pos[1]+self.scenecamera[1]*3)/48))
##                        if self.tile != 'door' and self.tile != 'spawner' and self.tile != 'hack':
##                            self.scene.tiles[strpos] = ((int(strpos.split(';')[0]), int(strpos.split(';')[1])), int(self.tile))
##                        elif self.tile == 'spawner':
##                            self.scene.tiles['spawners'].append([int(strpos.split(';')[0]), int(strpos.split(';')[1])])
##                            print(self.scene.tiles['spawners'])
##                        elif self.tile == 'hack':
##                            self.scene.tiles[strpos] = ((int(strpos.split(';')[0]), int(strpos.split(';')[1])), self.tile)
##                        else:
##                            self.scene.tiles['exit'] = ((int(strpos.split(';')[0]), int(strpos.split(';')[1])))
##                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
##                        pos = pygame.mouse.get_pos()
##                        strpos = str(int((pos[0]+self.scenecamera[0]*3)/48))+';'+str(int((pos[1]+self.scenecamera[1]*3)/48))
##                        self.scene.tiles.pop(strpos)
##                except Exception as e:
##                    print('idiot.')
##                    print(e)

            if pygame.key.get_pressed()[pygame.K_w]:
                self.scenecamera[1] -= 1
            if pygame.key.get_pressed()[pygame.K_a]:
                self.scenecamera[0] -= 1
            if pygame.key.get_pressed()[pygame.K_s]:
                self.scenecamera[1] += 1
            if pygame.key.get_pressed()[pygame.K_d]:
                self.scenecamera[0] += 1

            if pygame.key.get_pressed()[pygame.K_p]:
                self.tile = input('New Tile: ')

            self.window.fill((0, 0, 0))   

            camera_as_int = (int(self.scenecamera[0]), int(self.scenecamera[1]))
            self.scene.render(self.window, self.window, camera_as_int)

            self.display.blit(pygame.transform.scale_by(self.window, 3), (0, 0))
            pygame.display.update()
            
            self.clock.tick(120)
            await asyncio.sleep(0)

if __name__ == '__main__':
    editor = Editor()

    try:
        asyncio.run(editor.run())
    except:
        out_file = open("sav.json", "w")
        out_file.truncate(0)
        json.dump(editor.scene.tiles, out_file)       
        out_file.close() 
    
sys.exit()
