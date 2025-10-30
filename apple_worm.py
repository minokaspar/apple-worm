from turtle import *
from time import sleep

setup(width = 0.9, height = 0.9)
tracer(0)
bgcolor("black")
penup()
listening = True # listen while listening
falling = 0
level = 1
MAX_LEVEL = 6
SCALE = 40 # actual size of 1 block
DEATH_Y = -9 # if the worm falls until -9, it dies

LEVELS = {1: {"grounds": [[-4,-1], [-3,-1], [-2,-1], [-1,-1], [0,-1], [1,-1], [1,0], [2,0], [3,0]],
              "goals": [[3,1]],
              "apples": [],
              "worm": [[-4,0], [-3,0], [-2,0]],
              "spikes": []},
          2: {"grounds": [[-3,-1], [-2,-1], [-1,-1], [0,-1], [1,-1], [2,-1], [3,-1], [4,-1]],
              "goals": [[4,0]],
              "apples": [[1,0]],
              "worm": [[-3,0], [-2,0]],
              "spikes": []},
          3: {"grounds": [[-5,-1], [-4,-1], [-3,-1], [-2,-1], [1,-1], [2,-1], [3,-1]],
              "goals": [[4,-1]],
              "apples": [[-1,1]],
              "worm": [[-5,0], [-4,0]],
              "spikes": []},
          4: {"grounds": [[-4,1], [-3,1], [-2,1], [-1,1], [0,1], [1,1], [2,1], #upper platform
                          [-2,-3], [-1,-3], [0,-3], [1,-3], [2,-3], [3,-3]], #lower platform
              "goals": [[-2,-2]],
              "apples": [[-4,2]],
              "worm": [[-1,2], [0,2]],
              "spikes": []},
          5: {"grounds": [[-5,-1], [-4,-1], [-3,-1], [-2,-1], [-1,-1], [0,-1], [1,-1], [2,-1], [3,-1], [4,-1], [5,-1]],
              "goals": [[5,0]],
              "apples": [],
              "worm": [[-5,0], [-4,0], [-3,0], [-2,0]],
              "spikes": [[2,0]]},
          6: {"grounds": [[-4,1], [-3,1], [-2,1], [-1,1], [0,1], [1,1], [2,1], [4,1], # upper blocks
                          [2,-1], [4,-1], [2,-2], [2,-3], [3,-3]], # lower blocks
              "goals": [[2,0]],
              "apples": [[-4,2]],
              "worm": [[-1,2], [0,2]],
              "spikes": []}
          }

grounds = []
goals = []
spikes = []
apples = []
worm = []

def draw_block(x, y, typ):
    color_for_typ = {"ground": "blue", "goal": "grey", "apple": "red", "worm":"green", "worm_head": "darkgreen", "spike": "darkgrey", "empty": "black"}
    fillcolor(color_for_typ[typ])
    goto(SCALE * x, SCALE * y)
    setheading(0)
    begin_fill()
    if typ == "spike":
        forward(SCALE)
        left(105)
        for i in range(6):
            forward(SCALE/1.5)
            left(150 - (i % 2) * 300)
        end_fill()
    else:
        for _ in range(4):
            forward(SCALE)
            left(90)
        end_fill()
        if typ == "worm_head":
            goto(xcor() + SCALE/6, ycor() + SCALE/4)
            fillcolor("red")
            begin_fill()
            for i in range(3):
                forward(SCALE/1.5 if not i == 1 else SCALE/6)
                left(90)
            end_fill()
            goto(xcor() + SCALE/12, ycor() + SCALE/6)
            setheading(0)
            fillcolor("white")
            for _ in range(2):
                begin_fill()
                for _ in range(4):
                    forward(SCALE/6)
                    left(90)
                end_fill()
                forward(SCALE/3)


def restart():
    global grounds, goals, spikes, apples, worm
    #change lists to original state
    grounds = LEVELS[level]["grounds"].copy()
    goals = LEVELS[level]["goals"].copy()
    spikes = LEVELS[level]["spikes"].copy()
    apples = LEVELS[level]["apples"].copy()
    worm = LEVELS[level]["worm"].copy()
    clear()
    #draw all blocks
    for block in (grounds):
        draw_block(*block,"ground")
    for block in (goals):
        draw_block(*block,"goal")
    for block in (spikes):
        draw_block(*block,"spike")
    for block in (apples):
        draw_block(*block,"apple")
    for block in (worm):
        draw_block(*block, "worm")
    draw_block(*worm[-1], "worm_head")
    #level number
    goto(-500, 200)
    pencolor("white")
    write(level, font = ("Arial", 50, "bold"))
    hideturtle()
    update()


def block_beneath(x,y):
    return([x, y-1] in grounds or [x, y-1] in apples or [x, y-1] in goals)

def on_ground():
    for part in range(len(worm)):
        if block_beneath(*worm[part]): # check for every worm part if there is a block beneath
            return(True)
    return(False)

def fall():
    global worm, falling
    while not on_ground():
        falling = True
        for part in worm:
            draw_block(*part, "empty") # erase the falling worm
        worm = [[x, y-1] for x, y in worm] # update the worm
        for part in worm:
            draw_block(*part, "worm") # draw the updated worm
        draw_block(*worm[-1], "worm_head") #add the worm head
        if worm[-1][1] < DEATH_Y: # worm[-1][1] is the y value of the worm head
            restart()
            break
        check_death()
        update()
        sleep(0.1)
    falling = False


def dead():
    spiked = False
    for part in worm:
        if part in spikes:
            spiked = True
            draw_block(*part, "spike")
    if spiked:
        return(True) # if a worm part touches spikes, return "I'm dead", hence True
    x, y = worm[-1]
    for escape_block in [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]:
        if not (escape_block in grounds or escape_block in worm): # if I can escape, return "I'm not dead", hence False
            return(False)
    return(True) # if I cannot escape, return "I'm dead", hence True


def check_death():
    if dead():
        bindings("remove")
        update()
        ontimer(lambda: (bindings("create"), restart()), 300) # sleep doesn't work, but ontimer works.


def in_goal():
    for goal in goals:
        if worm[-1] == goal and len(apples) == 0:
            update()
            global level
            if level < MAX_LEVEL:
                level += 1 # corresponds to: level = level + 1
                bindings("remove")
                ontimer(lambda: (bindings("create"), restart()), 500) # sleep doesn't work, but ontimer works.
            else: # if level == MAX_LEVEL
                bindings("remove")
                ontimer(finish_game, 500) # sleep doesn't work, but ontimer works.
            return(True)


def finish_game():
    clear()
    goto(-333, 0)
    pencolor("white")
    write("You did it!", font = ("Arial", 100, "bold"))
    done()


def walk(direction):
    if not listening:
        return
    x, y = worm[-1]
    new_block_for_direction = {"up": [x, y+1], "down": [x, y-1], "left": [x-1, y], "right": [x+1, y]}
    new_block = new_block_for_direction[direction]
    if not (new_block in worm or new_block in grounds or (new_block in goals and len(apples) != 0) or falling): # check if new_block isn't at any forbidden place and check if the worm is falling
        worm.append(new_block)
        draw_block(*worm[-1], "worm_head") # add the worm head
        draw_block(*worm[-2], "worm") # delete the previous worm head by making a normal worm block
        if new_block in apples:
            apples.remove(new_block)
        else:
            draw_block(*worm[0], "empty") # delete the worm tail
            worm.pop(0)
    if in_goal():
        return
    check_death()
    fall()


def bindings(typ):
    global listening
    if typ == "remove":
        listening = False # stop callbacks
    elif typ == "create":
        listening = True # enable callbacks


restart()
listen()
bindings("create")
onkey(lambda: walk("up") ,"w"); onkey(lambda: walk("up") ,"Up")
onkey(lambda: walk("down") ,"s"); onkey(lambda: walk("down") ,"Down")
onkey(lambda: walk("left") ,"a"); onkey(lambda: walk("left") ,"Left")
onkey(lambda: walk("right") ,"d"); onkey(lambda: walk("right") ,"Right")
onkey(restart, "r"); onkey(restart,"space")

mainloop()

