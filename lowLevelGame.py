""" lowLevelGame.py """

import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))

class BlueBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image = self.image.convert()
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_width()/2
        self.rect.centery = screen.get_height()/2
        self.MAXSPEED = 10
        self.dx = 0
        self.dy = 0

    def checkKeys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                self.dx = self.MAXSPEED
            elif keys[pygame.K_LEFT]:
                self.dx = -self.MAXSPEED
        else:
            self.dx = 0
        if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            if keys[pygame.K_UP]:
                self.dy = -self.MAXSPEED
            elif keys[pygame.K_DOWN]:
                self.dy = self.MAXSPEED
        else:
            self.dy = 0
        if keys[pygame.K_SPACE]:
            self.dx = 0
            self.dy = 0

    def moveBox(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

    def checkBounds(self):
        if self.rect.right > screen.get_width():
            self.rect.left = 0
        elif self.rect.left < 0:
            self.rect.right = screen.get_width()

        if self.rect.bottom > screen.get_height():
            self.rect.top = 0
        elif self.rect.top < 0:
            self.rect.bottom = screen.get_height()

    def update(self):
        self.checkKeys()
        self.moveBox()
        self.checkBounds()

def main():
    pygame.display.set_caption("Low Level Game Demo")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0,0))

    playerBox = BlueBox()
    allSprites = pygame.sprite.Group(playerBox)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
