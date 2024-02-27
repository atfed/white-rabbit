import asyncio, pygame, sys, time, managers, config, scripts.scene

# ---------------------------- #
# -  Atfed's Alakajam Entry  - #
# ---------------------------- #

class Game:
    def __init__(self, GameManager):
        pygame.init()
        #pygame.mouse.set_visible(False) DO IF I HAVE TIME
         
        self.gman = GameManager
        self.display = pygame.display.set_mode((GameManager.config.data['xres']*3, GameManager.config.data['yres']*3))
        self.window = pygame.Surface((GameManager.config.data['xres'], GameManager.config.data['yres']))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(GameManager.config.data['gname'])
        pygame.display.set_icon(pygame.image.load('_internal/assets/game.ico'))

    async def run(self, lasttime):
        while True:
            dt = time.time()-lasttime
            dt *= 60
            lasttime = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.gman.hackingopacity != 0:
                        mpos = pygame.mouse.get_pos()
                        mpos = [mpos[0], mpos[1]]
                        self.gman.click_at(mpos)

            self.gman.update(self, dt)
            self.gman.render(self)
            self.clock.tick(100)
            await asyncio.sleep(0)

if __name__ == '__main__':
    config = config.Config('GameMain')
    config.add('gname', 'White Rabbit: Alakajam 19')
    config.add('xres', 320)
    config.add('yres', 240)
    config.add('stats', True)
    errmode = True

    gman = managers.GameManager(config)
    game = Game(gman)

    if errmode:
        lasttime = time.time()
        asyncio.run(game.run(lasttime))

    try:
        lasttime = time.time()
        asyncio.run(game.run(lasttime))
    except Exception as error:
        print(f'[{time.time()}] GAME RUNTIME ERROR: {error}')
    
sys.exit()
