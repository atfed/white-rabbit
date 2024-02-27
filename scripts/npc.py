import pygame

class NPC:
    def __init__(self, game, pos):
        self.game = game
        self.pos = [pos[0]*16+8, pos[1]*16]
        self.velocity = [0, 0]
        self.hacked = False
        self.direction = True

    def update(self, delta):
        self.velocity[1] += 0.15
        if self.hacked:
            if self.direction:
                self.velocity[0] = 2
            else:
                self.velocity[0] = -2
        
        self.pos[0] += self.velocity[0]*delta
        self.rect = self.get_rect()
        for rect in self.game.scene.physics_rects_around(self.pos):
            if self.rect.colliderect(rect):
                if self.velocity[0] > 0:
                    self.rect.right = rect.left
                    self.direction = False
                if self.velocity[0] < 0:
                    self.rect.left = rect.right
                    self.direction = True
                self.pos[0] = self.rect.x
                self.velocity[0] = 0
        
        self.pos[1] += self.velocity[1]*delta
        self.rect = self.get_rect()
        for rect in self.game.scene.physics_rects_around(self.pos):
            if self.rect.colliderect(rect):
                if self.velocity[1] > 0:
                    self.rect.bottom = rect.top
                    self.coyote = 15/delta
                if self.velocity[1] < 0:
                    self.rect.top = rect.bottom
                self.pos[1] = self.rect.y
                self.velocity[1] = 0

        if self.rect.colliderect(self.game.player.rect) and not self.hacked:
            self.game.reload_level()

        if self.hacked:
            for i in self.game.npcmanager.npcs:
                if self.rect != i.rect and self.rect.colliderect(i.rect):
                    self.game.npcmanager.npcs.remove(i)

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], 5, 12)

    def render(self, display, display2, camera):
        player_dir =  False

        if not self.hacked:
            if self.game.player.pos[0]-self.pos[0] < 0:
                player_dir = True
        else:
            player_dir = self.velocity[0] < 0
        #npc-hacked
        if not self.hacked:        
            display.blit(pygame.transform.flip(self.game.assets['npc-temp'], player_dir, False), (int(self.pos[0]-camera[0]), int(self.pos[1]-camera[1])))
            display2.blit(pygame.transform.flip(self.game.assets['npc-temp'], player_dir, False), (int(self.pos[0]-camera[0]), int(self.pos[1]-camera[1])))
        else:
            display.blit(pygame.transform.flip(self.game.assets['npc-hacked'], player_dir, False), (int(self.pos[0]-camera[0]), int(self.pos[1]-camera[1])))
            display2.blit(pygame.transform.flip(self.game.assets['npc-hacked'], player_dir, False), (int(self.pos[0]-camera[0]), int(self.pos[1]-camera[1])))
         









