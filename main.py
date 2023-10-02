import pygame as pg
import random
pg.init()

#settings
scale = 1
clockspeed = 100

starspeed = 1.3
starprobability = 22
starsize = 4


playersize = 30
playerspeed = 5
playeryoffset = 10
playercolor = (255,255,0)

asteroidcolor = (150,150,150)
asteroidcolor2 = (100,100,100)
asteroidmaxcooldown = 40
asteroidminradius = 22
asteroidmaxradius = 44 
asteroidminspeed = 1
asteroidmaxspeed = 2

laserthickness = 20
lasermaxcooldown = 300
lasercolor = (255,0,0)
laserlifetime = 25



debug = False
#functions
def draw_background():
    global stars
    display.fill((0,0,0))

    if random.randint(0,100) <= starprobability:
        stars.append([random.randint(0,displaysize[0]),0])

    for star in stars:
        star[1] += starspeed
        pg.draw.rect(display,(255,255,255),[star[0],star[1],starsize,starsize])


def draw_player():
    
    #playership = [[playersize/2,0],[playersize,playersize],[playersize/2,playersize*0.8],[0,playersize]]

    playership = [[0*playersize,0*playersize],[0.1*playersize,0.5*playersize],[0.3*playersize,0.5*playersize],[0.5*playersize,0*playersize],[0.7*playersize,0.5*playersize],[0.9*playersize,0.5*playersize],[1*playersize,0*playersize],[1*playersize,1*playersize],[0.7*playersize,0.8*playersize],[0.7*playersize,1*playersize],[0.3*playersize,1*playersize],[0.3*playersize,0.8*playersize],[0*playersize,1*playersize]]

    #apply offset
    for point in playership:
        for t in range(2):
            point[t] = point[t] + playerpos[t]
    
    pg.draw.polygon(display,playercolor,playership,0)

def move_player():
    if (keystate[pg.K_a] or keystate[pg.K_LEFT]) and playerpos[0] > 0:
        playerpos[0] -= playerspeed
    if (keystate[pg.K_d] or keystate[pg.K_RIGHT]) and playerpos[0] < displaysize[0]-playersize:
        playerpos[0] += playerspeed

    if playerpos[0] > displaysize[0]-playersize:
        playerpos[0] = displaysize[0]-playersize
    if playerpos[0] < 0:
        playerpos[0] = 0




def process_asteroids():
    global asteroidcooldown,asteroids
    asteroidcooldown -= 1
    if asteroidcooldown <= 0:
        asteroidcooldown = asteroidmaxcooldown
        asteroid_data = [random.randrange(asteroidmaxradius,displaysize[0]-asteroidmaxradius),-2*asteroidmaxradius,random.randint(asteroidminradius,asteroidmaxradius),random.randint(asteroidminspeed,asteroidmaxspeed)]
        asteroids.append(asteroid_data)


    for asteroid in asteroids:
        if asteroid[1] > displaysize[1]+2*asteroidmaxradius:
            asteroids.pop(asteroids.index(asteroid))
            break
        asteroid[1]+= asteroid[3]



    

def draw_asteroids():
    for asteroid in asteroids:
        pg.draw.circle(display,asteroidcolor,[asteroid[0],asteroid[1]],asteroid[2])
        pg.draw.circle(display,asteroidcolor2,[asteroid[0],asteroid[1]],asteroid[2],round(playersize/7))



def process_laser():
    global lasercooldown,lasertemplifetime,shootlaser,asteroids
    pg.draw.rect(display,(255,0,0),[10,10,displaysize[0]/8,displaysize[1]/20])

    barsize = ((displaysize[0]/8)*lasercooldown)/lasermaxcooldown
    
    pg.draw.rect(display,(0,255,0),[10,10,barsize,displaysize[1]/20])

    if lasercooldown < lasermaxcooldown:
        lasercooldown += 1

    if shootlaser:
        curthick = (laserthickness*lasertemplifetime)/laserlifetime
        pg.draw.line(display,lasercolor,[laserpos,displaysize[1]-(playersize+playeryoffset)],[laserpos,0],round(curthick))


        lasertemplifetime -= 1
        if lasertemplifetime == 0:
            shootlaser = False


        linelaser = pg.Rect(laserpos-curthick,0,curthick*2,displaysize[1])
        for asteroid in asteroids:
            selfrect = pg.Rect(asteroid[0]-asteroid[2],asteroid[1]-asteroid[2],2*asteroid[2],2*asteroid[2])
            if debug:
                pg.draw.rect(display,(255,0,0),selfrect)
                pg.draw.rect(display,(255,0,255),linelaser)
                
            if selfrect.colliderect(linelaser):
                asteroids.pop(asteroids.index(asteroid))



def detect_death():
    global dead
    playerrect = pg.Rect(playerpos[0],playerpos[1],playersize,playersize)
    if debug:
        pg.draw.rect(display,(100,255,0),playerrect)
    for asteroid in asteroids:
        selfrect = pg.Rect(asteroid[0]-asteroid[2],asteroid[1]-asteroid[2],2*asteroid[2],2*asteroid[2])
        if debug:
            pg.draw.rect(display,(255,100,100),selfrect)
        
        if selfrect.colliderect(playerrect) and not debug:
            dead = True
            break
        

def draw_home():
    display.fill((255,100,100))



#all initializations and starting conditions
displaysize = (800*scale,500*scale)
display = pg.display.set_mode(displaysize)
clock = pg.time.Clock()
stars = []
asteroids = []
playerpos = [displaysize[0]/2,displaysize[1]-playersize-playeryoffset]
asteroidcooldown = asteroidmaxcooldown
lasercooldown = lasermaxcooldown
dead = False
dead2 = False



#home menu
while not dead2:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            dead2 = True
            dead = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                dead2 = True
                dead = True
            if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                dead2 = True
                print("game started")


    draw_home()



shootlaser = False
lasertemplifetime = 0
laserpos = []

#main loop
while not dead:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            dead = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                debug = not debug
            if event.key == pg.K_ESCAPE:
                dead = True

            if event.key == pg.K_SPACE:
                if lasercooldown == lasermaxcooldown:
                    lasercooldown = 0
                    shootlaser = True
                    laserpos = playerpos[0]+playersize/2
                    lasertemplifetime = laserlifetime


    #get the current keyboard state
    keystate = pg.key.get_pressed()
    

    #graphic function calls
    draw_background()
    draw_player()
    draw_asteroids()

    #logic function calls
    move_player()
    process_asteroids()
    process_laser()
    detect_death()


    #update screen and advance time
    pg.display.update()
    clock.tick(clockspeed)


#quit
pg.quit()
quit()
