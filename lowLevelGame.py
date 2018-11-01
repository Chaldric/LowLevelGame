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
        self.dx = 0
        self.dy = 10

    def checkKeys(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.dx = 10;

    def update(self):
        self.rect.centerx += self.dx
        if self.rect.right > screen.get_width():
            self.rect.left = 0
        elif self.rect.left < 0:
            self.rect.right = screen.get_width()

        self.rect.centery += self.dy
        if self.rect.bottom > screen.get_height():
            self.rect.top = 0
        elif self.rect.top < 0:
            self.rect.bottom = screen.get_height()

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
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    if event.key == pygame.K_RIGHT:
                        playerBox.dx = 10;
                    elif event.key == pygame.K_LEFT:
                        playerBox.dx = -10;
                else:
                    playerBox.dx = 0;
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if event.key == pygame.K_UP:
                        playerBox.dy = -10;
                    elif event.key == pygame.K_DOWN:
                        playerBox.dy = 10;
                else:
                    playerBox.dy = 0;

        ##playerBox.checkKeys()

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
