import pygame, config, sys, scripts.scene, scripts.assets, scripts.player, scripts.npc
import time as tme

class GameManager:
    def __init__(self, gameconfig):
        pygame.font.init()
        self.fonts = {'stats': pygame.font.Font('_internal/fonts/PixeloidSans.ttf', 9)}

        # Check for required data ------------------ #
        caught = False
        for i in config.VITAL_DATA:
            if not i in gameconfig.data:
                print(f"[{time.time()}] STARTUP ERROR: Missing vital config data '{i}'")
                caught = True
        if caught:
            sys.exit()

        self.res = (gameconfig.data['xres'], gameconfig.data['yres'])
        self.config = gameconfig

        # Set Up Assets ---------------------------- #
        self.assets = dict()
        self.assets['tiles'] = scripts.assets.load_assets('_internal/assets/tiles')
        self.assets['bg'] = scripts.assets.load_asset('_internal/assets/bg.png')
        self.assets['player-temp'] = scripts.assets.load_asset('_internal/assets/player_temporary.png')
        self.assets['npc-temp'] = scripts.assets.load_asset('_internal/assets/npc.png')
        self.assets['npc-hacked'] = scripts.assets.load_asset('_internal/assets/npc-hacked.png')
        self.assets['door'] = scripts.assets.load_asset('_internal/assets/door.png')
        self.assets['hack'] = scripts.assets.load_asset('_internal/assets/tiles/hack.png')
        self.assets['box'] = scripts.assets.load_asset('_internal/assets/box.png')
        
        self.level = 1
        self.scene = self.load_level(self.level)
        self.scenecamera = [200, 200]

        print(self.scene.tiles['spawners'])
        self.npcmanager = NPCManager(self, self.scene.tiles['spawners'])

        # The Rest --------------------------------- #
        self.player = scripts.player.Player(self)

        # Outline Code ----------------------------- #
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 240))

        # Hacking Code ----------------------------- #
        self.hacking = False
        self.hacked = False
        self.hackingoverlay = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.hackingopacity = 0

        # Bells & Whistles ------------------------- #
        self.ticks = 0
        self.transition = -30
        self.completed = False

        self.starttime = tme.time()
        self.finished = False
        self.deaths = 0

    def load_level(self, num):
        try:
            return scripts.scene.Scene(self, path=f'w{num}.json')
            self.player = scripts.player.Player(self)
            self.hacked = False
            hck = pygame.mixer.Sound("_internal/assets/death.wav")
            hck.set_volume(2)
            pygame.mixer.Sound.play(hck)
        except:
            pygame.quit()
            sys.exit()

    def reload_level(self):
        self.completed = True
##        self.scene = self.load_level(self.level)
##        self.player = scripts.player.Player(self)
##        self.npcmanager = NPCManager(self, self.scene.tiles['spawners'])
        
    def click_at(self, pos):
        try:
            strpos = str(int((pos[0]+self.scenecamera[0]*3)/48))+';'+str(int((pos[1]+self.scenecamera[1]*3)/48))
            if str(int((pos[1]+self.scenecamera[1]*3)/48))[0] == '-':
                strpos = str(int((pos[0]+self.scenecamera[0]*3)/48))+';'+str(int((pos[1]+self.scenecamera[1]*3)/48)-1)
            else:
                strpos = str(int((pos[0]+self.scenecamera[0]*3)/48))+';'+str(int((pos[1]+self.scenecamera[1]*3)/48))

            try:
                if self.scene.tiles[strpos] and self.scene.tiles[strpos][1] and self.scene.tiles[strpos][1] == 'box':
                    self.scene.tiles[strpos][1] = 2
                    self.hacked = True
                    hck = pygame.mixer.Sound("_internal/assets/hack.wav")
                    hck.set_volume(0.6)
                    pygame.mixer.Sound.play(hck)
                    return
                else:
                    raise
            except:
                if str(int((pos[1]+self.scenecamera[1]*3)/48))[0] == '-':
                    strpos = str(int((pos[0]+self.scenecamera[0]*3)/48))+';'+str(int((pos[1]+self.scenecamera[1]*3)/48))
                print()
                print(strpos)
                for i in self.npcmanager.npcs:
    ##                npcpos = str(int((i.pos[0]*3)/48))+';'+str(int((i.pos[1]*3)/48)-1)
    ##                if strpos == npcpos:
    ##                    i.hacked = True
    ##                    self.hacked = True
    ##                print(npcpos)

                    npcpos = str(int((i.pos[0]*3)/48))+';'+str(int((i.pos[1]*3)/48))
                    if strpos == npcpos:
                        i.hacked = True
                        self.hacked = True
                        pygame.mixer.Sound.play(pygame.mixer.Sound("_internal/assets/hack.wav"))
                    print(npcpos)
                    print()
##                print(strpos)
##                if str(int((pos[1]+self.scenecamera[1]*3)/48))[0] == '-':
##                    for i in self.npcmanager.npcs:
##                        if strpos == str(int((i.pos[0]*3)/48))+';'+str(int((i.pos[1]*3)/48))-1:
##                            i.hacked = True
##                            self.hacked = True
##                else:
##                    for i in self.npcmanager.npcs:
##                        npcpos = str(int((i.pos[0]*3)/48))+';'+str(int((i.pos[1]*3)/48))
##                        if strpos == npcpos:
##                            i.hacked = True
##                            self.hacked = True
##                        print(npcpos)
##
##                        npcpos = str(int((i.pos[0]*3)/48))+';'+str(int((i.pos[1]*3)/48)-1)
##                        if strpos == npcpos:
##                            i.hacked = True
##                            self.hacked = True
##                        print(npcpos)
##                        print()
        except:
            pass

    def update(self, game, delta):
        self.delta = delta
        if self.delta == 0:
            self.delta = 1

        if self.hacking:
            self.delta = 0.9*self.delta

        # Bells & Whistles ------------------------- #
        if self.completed:
            self.transition += 1
            if self.transition > 30:      
                self.scene = self.load_level(self.level)
                self.player = scripts.player.Player(self)
                self.npcmanager = NPCManager(self, self.scene.tiles['spawners'])
                self.completed = False
                self.hacked = False
                self.transition = -30
        if self.transition < 0:
            self.transition += 1

        # Do Camera Movement ----------------------- #
        targetpos = [self.player.pos[0]+8-160, self.player.pos[1]+8-120]
        targetpos[1] = min(0, targetpos[1])

        movement = (7/self.delta)
        if movement == 0:
            movement = 1
        
        self.scenecamera[0] -= (self.scenecamera[0]-targetpos[0])/movement
        self.scenecamera[1] -= (self.scenecamera[1]-targetpos[1])/movement

        # General ---------------------------------- #
        self.npcmanager.update(self.delta)
        self.player.update(self.delta)
        self.ticks += 1

        # Death ------------------------------------ #
        if self.player.pos[1] > 320:
            self.reload_level()

    def render(self, game):
        # Initializing ----------------------------- #
        if self.hacking and self.hackingopacity < 160:
            self.hackingopacity += 4
        elif self.hacking and self.hackingopacity == 160:
            pass
        elif self.hackingopacity != 0 and not self.hacking:
            self.hackingopacity -= 4
        
        self.display.fill((0, 0, 0, 0))
        self.hackingoverlay.fill((0, 0, 0, int(self.hackingopacity)))

        # Render ----------------------------------- #
        if not self.finished:
            # Draw Game Statistics...--------------- #
            ct = tme.time()
            time = self.fonts['stats'].render(f'{int(ct-self.starttime)}s', False, (255, 255, 255))
            self.display.blit(time, (0+2, 0))
        
            camera_as_int = (int(self.scenecamera[0]), int(self.scenecamera[1]))
            self.npcmanager.render(self.display, self.hackingoverlay, camera_as_int)
            self.player.render(self.display, camera_as_int)
            self.scene.render(self.display, self.hackingoverlay, camera_as_int)
        else:
            ct = tme.time()
            time = ct-self.starttime
            while True:
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
                time = self.fonts['stats'].render(f'Time: {time}s', False, (255, 255, 255))
                self.display.blit(time, (200, game.window.get_height()/2-(time.get_height()/2)))
                
                game.display.blit(pygame.transform.scale_by(game.window, 3), (0, 0))
                pygame.display.update()

        # Do Outline ------------------------------- #
        self.display_2.blit(self.assets['bg'], (0, 0))

        display_mask = pygame.mask.from_surface(self.display)
        display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 205), unsetcolor=(0, 0, 0, 0))

        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.display_2.blit(display_sillhouette, offset)

        game.window.blit(self.display_2, (0, 0))
        game.window.blit(self.display, (0, 0))

        game.window.blit(self.hackingoverlay, (0, 0))

        # Level Transition ------------------------- #
        if self.transition:
            tran_surf = pygame.Surface(self.display.get_size())
            pygame.draw.circle(tran_surf, (255, 255, 255), (self.display.get_width()//2, self.display.get_height()//2), (30-abs(self.transition))*8)
            tran_surf.set_colorkey((255, 255, 255))
            game.window.blit(tran_surf, (0, 0))

        # Finalizing ------------------------------- #
        game.display.blit(pygame.transform.scale_by(game.window, 3), (0, 0))
        pygame.display.update()

class NPCManager:
    def __init__(self, game, positions):
        self.game = game
        self.npcs = []

        for i in positions:
            self.npcs.append(scripts.npc.NPC(self.game, i))

    def update(self, delta):
        for i in self.npcs:
            i.update(delta)

    def render(self, display, display2, camera):
        for i in self.npcs:
            i.render(display, display2, camera)
    







        
