import pygame, os

# ---------------------------- #
# -   Atfed's Asset Script   - #
# ---------------------------- #

def load_asset(p):
    asset = pygame.image.load(p)
    asset.set_colorkey((0, 0, 0))
    return asset

def load_assets(p):
    assets = []
    for i in os.listdir(p):
        assets.append(load_asset(p+'/'+i))
    return assets
