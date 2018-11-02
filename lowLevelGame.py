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
        if self.rect.centerx > screen.get_width():
            self.rect.centerx = 0
        elif self.rect.centerx < 0:
            self.rect.centerx = screen.get_width()

        if self.rect.centery > screen.get_height():
            self.rect.centery = 0
        elif self.rect.centery < 0:
            self.rect.centery = screen.get_height()

    def bounceBound(self):
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
    def __init__(self, player, goal, powerUp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image = self.image.convert()
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0
        self.player = player
        self.powerUp = powerUp
        self.goal = goal
        self.reset()

    def reset(self):
        keepGoing = True
        while keepGoing:
            self.rect.centerx = random.randint(0, screen.get_width())
            self.rect.centery = random.randint(0, screen.get_height())

            keepGoing = False
            if self.rect.colliderect(self.player.rect):
                keepGoing = True
            if self.rect.colliderect(self.powerUp.rect):
                keepGoing = True
            if self.rect.colliderect(self.goal.rect):
                keepGoing = True

    def update(self):
        return 0

class YellowBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image = self.image.convert()
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0
        self.reset()

    def reset(self):
        self.rect.centerx = random.randint(0, screen.get_width())
        self.rect.centery = random.randint(0, screen.get_height())


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.points = 0
        self.font = pygame.font.SysFont("None", 50)

    def update(self, numboxes):
        self.text = "Score: %d  RedBoxes: %d" % (self.points, numboxes)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()

def buildRedBoxes(numboxes, playerBox, goalBox, powerUp):
    redBoxes = []
    for i in range(numboxes):
        redBoxes.append(RedBox(playerBox, goalBox, powerUp))
    return redBoxes

def main():
    NUMREDBOXES = 10
    pygame.display.set_caption("Low Level Game Demo")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0,0))

    playerBox = BlueBox()
    goalBox = YellowBox()
    redBoxes = buildRedBoxes(NUMREDBOXES, playerBox, goalBox, goalBox)

    score = Score()

    allSprites = pygame.sprite.Group(playerBox, goalBox, redBoxes)
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

        if playerBox.rect.colliderect(goalBox.rect):
            goalBox.reset()
            NUMREDBOXES += 2
            redBoxes = buildRedBoxes(NUMREDBOXES, playerBox, goalBox, goalBox)
            allSprites.clear(screen, background)
            allSprites = pygame.sprite.Group(playerBox, goalBox, redBoxes)
            score.points += 1

        allSprites.clear(screen, background)
        scoreSprite.clear(screen, background)

        allSprites.update()
        scoreSprite.update(NUMREDBOXES)

        allSprites.draw(screen)
        scoreSprite.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
