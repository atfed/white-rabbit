import pygame, math, scripts.scene

class Player:
    def __init__(self, game):
        self.game = game

        self.pos = [85, 0]
        self.velocity = [0, 0]
        self.rect = self.get_rect()

        self.collisions = dict()
        self.coyote = 7
        self.direction = True

        self.slam = False

    def update(self, delta):
        self.collisions['up'] = False
        self.collisions['down'] = False
        self.collisions['left'] = False
        self.collisions['right'] = False
        
        self.velocity[0] = (pygame.key.get_pressed()[pygame.K_d]-pygame.key.get_pressed()[pygame.K_a])*2

        if self.velocity[0] > 0:
            self.direction = False
        if self.velocity[0] < 0:
            self.direction = True

        if self.velocity[1] < 0 and pygame.key.get_pressed()[pygame.K_SPACE]:
            gravity = 0.10
        elif self.velocity[1] < 0:
            gravity = 0.26
        else:
            gravity = 0.25

        if not self.slam:
            self.velocity[1] += gravity*delta

            # Cap the Velocity
            self.velocity[1] = min(self.velocity[1], 5.5)

        if not self.slam:
            self.pos[0] += self.velocity[0]*delta
            self.rect = self.get_rect()
            for rect in self.game.scene.physics_rects_around(self.pos):
                if self.rect.colliderect(rect):
                    if self.velocity[0] > 0:
                        self.rect.right = rect.left
                        self.collisions['right'] = True
                    if self.velocity[0] < 0:
                        self.rect.left = rect.right
                        self.collisions['left'] = True
                    self.pos[0] = self.rect.x
                    self.velocity[0] = 0
        
        self.pos[1] += self.velocity[1]*delta
        self.rect = self.get_rect()
        for rect in self.game.scene.physics_rects_around(self.pos):
            if self.rect.colliderect(rect):
                if self.velocity[1] > 0:
                    self.rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.coyote = 15/delta
                if self.velocity[1] < 0:
                    self.rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = self.rect.y
                self.velocity[1] = 0

        if self.rect.colliderect(self.game.scene.doorrect):
            self.game.level = int(self.game.scene.path.split('.')[0].replace('w', ''))+1
            self.game.reload_level()

        if not self.collisions['down']:
            self.coyote -= 1
        else:
            self.slam = False

        if pygame.key.get_pressed()[pygame.K_SPACE] and (self.collisions['down'] or self.coyote > 0):
            self.velocity[1] = -3.6
            self.coyote = 0
            jmp = pygame.mixer.Sound("_internal/assets/jump.wav")
            jmp.set_volume(0.5)
            pygame.mixer.Sound.play(jmp)

        if pygame.key.get_pressed()[pygame.K_s] and not self.collisions['down'] and self.coyote < 0:
            self.slam = True
            self.velocity[1] = 5

        # Slam Attack Code
        if self.slam:
            for i in self.game.npcmanager.npcs:
                if self.rect.colliderect(i.get_rect()):
                    self.game.npcmanager.npcs.remove(i)
                    pygame.mixer.Sound.play(pygame.mixer.Sound("_internal/assets/slam.wav"))
                
    def render(self, display, camera):
        display.blit(pygame.transform.flip(self.game.assets['player-temp'], self.direction, False), (int(self.pos[0]-camera[0]), int(self.pos[1]-camera[1])))

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], 5, 12)
