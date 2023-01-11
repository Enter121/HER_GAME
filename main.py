import math
import random

import pygame


globalWidth = globalHeight = 50

obstacleColor = (255, 162, 51)
playerColor = (51, 156, 255)

baseY = 10

tick = 30

failed = False
score=0


class InputState:
    def __init__(self, distanceFromNearestObstacle, isNearestObstacleOnFloor, passedObstacles):
        self.distanceFromNearestObstacle = distanceFromNearestObstacle
        self.isNearObstacleOnFloor = isNearestObstacleOnFloor
        self.passedObstacles = passedObstacles



class OutputState:
    def __init__(self, shouldJump, shouldCrouch):
        self.shouldJump = shouldJump
        self.shouldCrouch = shouldCrouch

    def reset(self):
        self.shouldCrouch = False
        self.shouldJump = False


class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def render(self):
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(self.x * globalWidth, self.y * globalHeight, globalWidth, globalHeight))


class Obstacle(Block):
    def __init__(self, x):
        self.onFloor = random.randint(0, 1)
        Block.__init__(self, x, baseY - (0 if self.onFloor else 1), obstacleColor)

    def tickUpdate(self):
        self.x -= 1
        pass


class Player(Block):
    def __init__(self, x):
        Block.__init__(self, x, baseY, playerColor)
        self.cr = False
        self.jmp = False

    def action(self, state):
        if state.shouldJump:
            self.y = baseY - 3
            self.jmp = True
        if state.shouldCrouch:
            self.cr = True

    def resetState(self):
        self.y = baseY
        self.cr = False
        self.jmp = False

    def tickUpdate(self, state):
        self.resetState()
        self.action(state)

    def render(self):
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(self.x * globalWidth, (self.y + (0 if not self.cr else 0.5)) * globalHeight,
                                     globalWidth,
                                     globalHeight / (1 if not self.cr else 2)))

def getInputState():
    nearestObstacle = None
    nearestObstacleDistance=99
    for o in obstacles:
        if obstacle.x-player.x>0:
            if nearestObstacleDistance>obstacle.x-player.x:
                nearestObstacleDistance=obstacle.x-player.x
                nearestObstacle=o
    if nearestObstacle==None:
        return InputState(-1,None,score)
    return InputState(nearestObstacleDistance,nearestObstacle.onFloor,score)

if __name__ == '__main__':
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([1280, 720])

    running = True

    obstacles = []
    player = Player(6)

    count = 0
    state = OutputState(False, False)
    obstacles.append(Obstacle(26))
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state.shouldJump = True
                if event.key == pygame.K_DOWN:
                    state.shouldCrouch = True

        screen.fill((0, 0, 0))

        if count == tick:
            count = 0
            for obstacle in obstacles:
                obstacle.tickUpdate()
            player.tickUpdate(state)
            #print(player.jmp,player.cr)
            failed=False
            for obstacle in obstacles:
                if obstacle.x < 0:
                    obstacles.remove(obstacle)
                    obstacles.append(Obstacle(26))
                if obstacle.x == player.x:
                    # print(player.cr)
                    if (not obstacle.onFloor and player.cr) or (obstacle.onFloor and player.jmp):
                        score+=1
                        print("point")
                    else:
                        failed=True
                        score=0


            tmp=getInputState()
            print(tmp.passedObstacles,tmp.distanceFromNearestObstacle,tmp.isNearObstacleOnFloor)
            state.reset()
            # if random.randint(0,100)<5:
            #     obstacles.append(Obstacle(26))

        player.render()
        for obstacle in obstacles:
            obstacle.render()

        if failed:
            pygame.draw.rect(screen, (255,0,0),pygame.Rect(615, 335,50,50))

        count += 1

        pygame.draw.line(screen, (125, 125, 125), (0, (baseY + 1) * globalHeight), (1280, (baseY + 1) * globalHeight), 4)

        pygame.display.flip()
    pygame.quit()