""" lowLevelGame.py """

import pygame, random
pygame.init()

screen = pygame.display.set_mode((720, 720))

class BlueBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image = self.image.convert()
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()

        self.rect.centerx = screen.get_width()/2
        self.rect.centery = screen.get_height()/2
        self.MAXSPEED = 8
        self.dx = 0
        self.dy = 0
        #self.collideRight = False
        #self.collideLeft = False

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

    def reset(self):
        return 0

class RedBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image = self.image.convert()
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, screen.get_width())
        self.rect.centery = random.randint(0, screen.get_height())

    def reset(self):
        self.rect.bottom = 0

    def update(self):
        return 0

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.points = 0
        self.font = pygame.font.SysFont("None", 50)

    def update(self):
        self.text = "Score: %d" % (self.points)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()

def main():
    pygame.display.set_caption("Low Level Game Demo")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0,0))

    playerBox = BlueBox()
    redBoxes = []
    for i in range(10):
        redBoxes.append(RedBox())

    score = Score()

    allSprites = pygame.sprite.Group(playerBox, redBoxes)
    scoreSprite = pygame.sprite.Group(score)

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

        for i in range(len(redBoxes)):
            if playerBox.rect.colliderect(redBoxes[i].rect):
                redBoxes[i].reset()
                score.points += 1

        allSprites.clear(screen, background)
        scoreSprite.clear(screen, background)

        allSprites.update()
        scoreSprite.update()

        allSprites.draw(screen)
        scoreSprite.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
