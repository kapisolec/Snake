import pygame, random
pygame.init()
res = (800, 600)
screen = pygame.display.set_mode(res, pygame.RESIZABLE)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
size = (20,20)
leftWall = 50
rightWall = 700
upWall = 50
downWall = 500
BUFFER_RIGHTWALL = 0
BUFFER_DOWNWALL = 0
zjedzone = False

class Snake():
    def __init__(self):
        self.lenght = 1
        self.position = [((res[0]//2), (res[1]//2))]
        self.dir = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (0,125,0)
        self.segList = []
        self.zjedzone = zjedzone
        self.lastScore = 0
    def headPos(self):
        return self.position[0]

    def turn(self, point):
        if self.lenght > 1 and (point[0] * -1, point[1] * -1) == self.dir:
            return
        else:
            self.dir = point

    def movement(self):
        curPos = self.headPos()
        x, y = self.dir
        curX, curY = self.headPos()
        new = ((curPos[0] + x*size[0]),(curPos[1] + y*size[1]))
        if len(self.position) > 2 and new in self.position[2:]:
            self.reset()
        else:
            self.position.insert(0,new)
            if len(self.position) > self.lenght:
                self.position.pop()
        if curX == 0 or curX == res[0]-size[0] or curY == 0 or curY == res[1]-size[1]:
            self.reset()



    def reset(self):
        self.lastScore = score
        self.lenght = 1
        self.position = [((res[0]//2),(res[1]//2))]
        self.dir = random.choice([UP, DOWN, LEFT, RIGHT])


    def draw(self):
        for p in self.position:
            r = pygame.Rect((p[0], p[1]), size)
            pygame.draw.rect(screen, self.color, r)
            pygame.draw.rect(screen, (255,255,255), r, 1)



    def headRect(self):
        x, y = self.headPos()
        h, w = size
        return pygame.Rect(x,y,h,w)

    def keys(self):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.turn(UP)
            elif event.key == pygame.K_DOWN:
                self.turn(DOWN)
            elif event.key == pygame.K_LEFT:
                self.turn(LEFT)
            elif event.key == pygame.K_RIGHT:
                self.turn(RIGHT)

class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomPos()

    def randomPos(self):
        self.position = (random.randint(leftWall, rightWall-20+BUFFER_RIGHTWALL), random.randint(upWall, downWall-20+BUFFER_DOWNWALL))
        return self.position


    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (size))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)


    def foodRect(self):
        x, y = self.position
        w, h = size
        return pygame.draw.rect(screen, self.color, (x,y,h,w))

class Plansza():
    def __init__(self, leftWall, upWall, downWall, rightWall):
        self.x = leftWall
        self.y = upWall
        self.h = downWall
        self.w = rightWall
    def draw(self):
        pygame.draw.rect(screen, (0,0,0), (self.x,self.y,self.w,self.h))
        pygame.draw.rect(screen, (255, 0, 0),(self.x-1,self.y-1,self.w+1,self.h+1), 3)
    def rect(self):
        planszaRect = pygame.Rect(self.x, self.y, self.w, self.h)
        return planszaRect

    def coords(self):
        return (self.x,self.y,self.h,self.w)
    


FPS = 60
clock = pygame.time.Clock()
run = True
snake = Snake()

food = Food()
score = 0
myfont = pygame.font.SysFont('monospace',20)
timer = 0
speed = 6
bufferScore = 0
bufferSpeed = 0
bestScore = 0

keyPressed = False
i = 0
z = 0

while (run):
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    #print("timer {}".format(timer))
    plansza = Plansza(leftWall, upWall, downWall, rightWall)
    plansza.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()
    if leftWall > rightWall-30 or upWall > downWall-30:
        pass
    else:
        if keyPressed == False:
            keyPressed = True

            if keys[pygame.K_UP]:
                downWall -= 5

            elif keys[pygame.K_DOWN]:
                 upWall += 5
                 downWall -=5
                 BUFFER_DOWNWALL +=5

            elif keys[pygame.K_LEFT]:
                rightWall -= 5

            elif keys[pygame.K_RIGHT]:
                leftWall += 5
                rightWall -= 5
                BUFFER_RIGHTWALL += 5

    for pos in snake.position:
        foodPos = pygame.Rect(food.position, (20, 20))
        snakePos = pygame.Rect(pos, (20, 20))
        if pygame.Rect.colliderect(foodPos, snakePos):
            food.randomPos()

    snake.keys()
    timer +=1
    if (score == 2 and speed == 6) or (score == bufferScore + 2 and speed == bufferSpeed + 1):
        bufferScore = score
        bufferSpeed = speed
        speed += 1



    snake.draw()
    if int(FPS/speed) == timer:
        timer = 0
        keyPressed = False
        snake.movement()




    if pygame.Rect.colliderect(snake.headRect(), food.foodRect()):
        snake.lenght +=1
        score +=1
        food.randomPos()
        snake.zjedzone = True
        #print(snake.zjedzone)

    if snake.lenght == 1:
        score = 0
        speed = 6
        leftWall = 50
        rightWall = 700
        upWall = 50
        downWall = 500


    if not pygame.Rect.contains(plansza.rect(),snake.headRect()):

        snake.reset()
        snake.lastScore = score
        score = 0
        speed = 6
        leftWall = 50
        rightWall = 700
        upWall = 50
        downWall = 500

    scoreText = myfont.render("Score: {0}".format(score), 1, (255,255,255))
    speedText = myfont.render("Speed: {0}".format(speed-5), 1, (255,255,255))
    lastScoreText = myfont.render("Last score: {0}".format(snake.lastScore), 1, (255, 255, 255))
    screen.blit(scoreText, (5,10))
    screen.blit(lastScoreText, (140, 10))
    if speed < 15:
        screen.blit(speedText, (700,10))
    else:
        screen.blit(speedText, (690,10))

    pygame.display.update()

pygame.quit()
