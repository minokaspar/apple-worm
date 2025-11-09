from turtle import *
from sys import setrecursionlimit

setup(width = 0.9, height = 0.9)
setrecursionlimit(1000000)
tracer(0)
bgcolor("black")
penup()
listening = True # listen while listening
falling = False
worm_falling = False
blocks_falling = False
level = 1
# Constants
MAX_LEVEL = 9
SCALE = 60 # actual size of 1 block
DEATH_Y = -9 # if the worm falls until -9, it dies
FALL_SPEED = 100 # time for falling 1 unit

UP = 1
DOWN = 3
LEFT = 2
RIGHT = 0

level_creator_help = """
          0: {"grounds": [[], [], [], []],
              "goals": [[]],
              "apples": [],
              "worm": [[], []],
              "worm_dir": [[RIGHT]],
              "spikes": [],
              "spike_dirs": [],
              "moving_blocks": []}"""

LEVELS = {1: {"grounds": [[-4,-1], [-3,-1], [-2,-1], [-1,-1], [0,-1], [1,-1], [1,0], [2,0], [3,0]],
              "goals": [[3,1]],
              "apples": [],
              "worm": [[-4,0], [-3,0], [-2,0]],
              "worm_dir": [[RIGHT]],
              "spikes": [],
              "spike_dirs": [],
              "moving_blocks": []},
          
          2: {"grounds": [[-3,-1], [-2,-1], [-1,-1], [0,-1], [1,-1], [2,-1], [3,-1], [4,-1]],
              "goals": [[4,0]],
              "apples": [[1,0]],
              "worm": [[-3,0], [-2,0]],
              "worm_dir": [[RIGHT]],
              "spikes": [],
              "spike_dirs": [],
              "moving_blocks": []},
          
          3: {"grounds": [[-5,-1], [-4,-1], [-3,-1], [-2,-1], [1,-1], [2,-1], [3,-1]],
              "goals": [[4,-1]],
              "apples": [[-1,1]],
              "worm": [[-5,0], [-4,0]],
              "worm_dir": [[RIGHT]],
              "spikes": [],
              "spike_dirs": [],
              "moving_blocks": []},
          
          4: {"grounds": [[-4,1], [-3,1], [-2,1], [-1,1], [0,1], [1,1], [2,1], #upper platform
                          [-2,-3], [-1,-3], [0,-3], [1,-3], [2,-3], [3,-3]], #lower platform
              "goals": [[-2,-2]],
              "apples": [[-4,2]],
              "worm": [[-1,2], [0,2]],
              "worm_dir": [[RIGHT]],
              "spikes": [],
              "spike_dirs": [],
              "moving_blocks": []},
          
          5: {"grounds": [[-5,-1], [-4,-1], [-3,-1], [-2,-1], [-1,-1], [0,-1], [1,-1], [2,-1], [3,-1], [4,-1], [5,-1]],
              "goals": [[5,0]],
              "apples": [],
              "worm": [[-5,0], [-4,0], [-3,0], [-2,0]],
              "worm_dir": [[RIGHT]],
              "spikes": [[2,0]],
              "spike_dirs": [[RIGHT]],
              "moving_blocks": []},
          
          6: {"grounds": [[-4,1], [-3,1], [-2,1], [-1,1], [0,1], [1,1], [2,1], [4,1], # upper blocks
                          [2,-1], [4,-1], [2,-2], [2,-3], [3,-3]], # lower blocks
              "goals": [[2,0]],
              "apples": [[-4,2]],
              "worm": [[-1,2], [0,2]],
              "worm_dir": [[RIGHT]],
              "spikes": [],
              "spike_dirs": [],
              "moving_blocks": []},
          
          7: {"grounds": [[-5,1], [-4,1], [-3,1], [-2,1], [1,1], [2,1], [3,1], [4,1], [5,1], # upper platform
                          [-5,-3], [-4,-3], [-3,-3], [-2,-3], [-1,-3], [0,-3], [1,-3], [2,-3], [3,-3], [4,-3], [5,-3]], # lower platform
              "goals": [[5,2]],
              "apples": [[0,-1], [-6,4]],
              "worm": [[-5,-2], [-4,-2], [-3,-2]],
              "worm_dir": [[RIGHT]],
              "spikes": [],
              "spike_dirs": [],
              "moving_blocks": []},
          
          8: {"grounds": [[-6,1], [-5,1], [-4,1], [-3,1], [-2,1], [-1,1], [0,-2], [1,-2], [2,-2], [3,1], [4,1], [5,1], [6,1]],
              "goals": [[6,2]],
              "apples": [[4,4]],
              "worm": [[-6,2], [-5,2], [-4,2]],
              "worm_dir": [[RIGHT]],
              "spikes": [],
              "spike_dirs": [],
              "moving_blocks": [[-2,7]]},
          
          9: {"grounds": [[-4,-1], [-3,-4], [-2,-4], [-1,-4], [0,-4], [1,-4]],
              "goals": [[4,-5]],
              "apples": [[3,-4], [-5,3]],
              "worm": [[-4,1], [-3,1], [-2,1]],
              "worm_dir": [[RIGHT]],
              "spikes": [[0,-3]],
              "spike_dirs": [[RIGHT]],
              "moving_blocks": [[-2,8]]}
          }

grounds = []
goals = []
spikes = []
spike_dirs = []
apples = []
worm = []
worm_dir = RIGHT
moving_blocks = []

def square(color, x, y, scale, typ = "normal"):
    goto(xcor() + SCALE * x, ycor() + SCALE * y)
    fillcolor(color)
    
    if typ == "normal":
        begin_fill()
        for _ in range(4): # draw square
            forward(scale)
            left(90)
        end_fill()
    
    elif typ == "rounded":
        forward(scale/4)
        begin_fill()
        for _ in range(4):
            forward(scale/2)
            circle(scale/4, 90)
        end_fill()

def draw_block(x, y, typ, direction = RIGHT):
    goto(SCALE * x, SCALE * y)
    setheading(0)
    for _ in range(direction): # direction is intended to be UP, DOWN, LEFT or RIGHT; -> a Value between 0 and 3
        forward(SCALE)
        left(90)
    
    if typ == "ground":
        square("gray50", 0, 0, SCALE)
    
    elif typ == "goal":
        square("cyan4", 0, 0, SCALE, "rounded")
        goto(SCALE * x, SCALE * y)
        square("cyan3", 0.2, 0.2, SCALE * 0.6, "rounded")
        goto(SCALE * x, SCALE * y)
        square("cyan1", 0.4, 0.4, SCALE * 0.2, "rounded")
    
    elif typ == "apple":
        left(90)
        forward(SCALE * (1/64))
        right(90)
        forward(SCALE * (22/64))
        fillcolor("red")
        begin_fill()
        circle(SCALE * (10/64), 90)
        left(180)
        circle(SCALE * (10/64), 90)
        circle(SCALE * (20/64), 60)
        circle(SCALE * (40/64), 10)
        circle(SCALE * (30/64), 40)
        circle(SCALE * (20/64), 100)
        circle(SCALE * (-3/64), 60)
        circle(SCALE * (20/64), 100)
        circle(SCALE * (30/64), 40)
        circle(SCALE * (40/64), 10)
        circle(SCALE * (20/64), 60)
        end_fill()

        fillcolor("brown")
        backward(SCALE * (1/64))
        circle(SCALE * (10/64), 50) # 50
        right(50)

        begin_fill()
        for _ in range(3):
            forward(SCALE * (6/64))
            left(120)
        end_fill()

        forward(SCALE * (1/64))
        left(90) # 90
        forward(SCALE * (42/64))

        begin_fill()
        circle(SCALE * (-50/64), 20)
        right(90)
        forward(SCALE * (5/64))
        right(90)
        circle(SCALE * (50/64), 18)
        end_fill()
    
    elif typ == "worm":
        square("green", 0, 0, SCALE, "rounded")
    
    elif typ == "spike":
        forward(SCALE)
        left(105)
        fillcolor("gray90")
        begin_fill()
        for i in range(6):
            forward(SCALE/1.5)
            left(150 - (i % 2) * 300)
        end_fill()
    
    elif typ == "moving_block":
        square("chocolate3", 0, 0, SCALE)
        square("chocolate4", 0.1, 0.1, SCALE * 0.8)
        setheading(45)
        pencolor("chocolate3")
        pensize(2)
        goto(SCALE * (x + 0.1), SCALE * (y + 0.1))
        pendown()
        goto(SCALE * (x + 0.9), SCALE * (y + 0.9))
        penup()
        goto(SCALE * (x + 0.9), SCALE * (y + 0.1))
        pendown()
        goto(SCALE * (x + 0.1), SCALE * (y + 0.9))
        penup()
    
    elif typ == "worm_head":
        square("black", 0, 0, SCALE)
        square("darkgreen", 0, 0, SCALE, "rounded")
        forward(SCALE/5)
        left(90)
        forward(SCALE/4)
        right(90)
        fillcolor("red")
        begin_fill()
        for i in range(3): # draw mouth
            forward(SCALE/1.8 if not i == 1 else SCALE/6)
            left(90)
        
        right(90)
        circle(SCALE/12, 180)
        end_fill()
        
        forward(SCALE/6)
        left(90)
        forward(SCALE/2.75)
        right(90)
        fillcolor("gray85")
        for _ in range(2): # draw eyes
            dot(SCALE/6, "gray85")
            forward(SCALE/4.5)
    elif typ == "empty":
        square("black", 0, 0, SCALE)


def restart():
    global grounds, goals, spikes, spike_dirs, apples, worm, worm_dir, moving_blocks, falling, blocks_falling
    falling, blocks_falling = False, False
    # change lists to original state
    grounds = LEVELS[level]["grounds"].copy()
    goals = LEVELS[level]["goals"].copy()
    spikes = LEVELS[level]["spikes"].copy()
    spike_dirs = LEVELS[level]["spike_dirs"].copy()
    apples = LEVELS[level]["apples"].copy()
    worm = LEVELS[level]["worm"].copy()
    worm_dir = LEVELS[level]["worm_dir"][0][0]
    moving_blocks = LEVELS[level]["moving_blocks"].copy()
    clear()
    # draw all blocks
    for block in grounds:
        draw_block(*block, "ground") # type: ignore
    for block in goals:
        draw_block(*block, "goal") # type: ignore
    for i in range(len(spikes)):
        draw_block(*spikes[i], "spike", spike_dirs[i][0]) # type: ignore
    for block in apples:
        draw_block(*block, "apple") # type: ignore
    for block in worm:
        draw_block(*block, "worm") # type: ignore
    draw_block(*worm[-1], "worm_head", worm_dir) # type: ignore
    for block in moving_blocks:
        draw_block(*block, "moving_block") # type: ignore
    # level number
    goto(-500, 200)
    pencolor("white")
    write(level, font = ("Arial", 50, "bold"))
    hideturtle()
    update()
    # make things fall
    fall_step()
    moving_block_fall_step()


def block_beneath(x, y, typ):
    if typ == worm:
        return([x, y-1] in [*grounds, *apples, *goals, *moving_blocks])
    else:
        return([x, y-1] in [*grounds, *worm, *apples, *goals, *moving_blocks])


def on_ground(typ):
    for part in typ:
        if block_beneath(*part, typ): # type: ignore # check for every worm / moving_blocks part if there is a block beneath
            return(True)
    return(False)


def dead(typ):
    spiked = False
    for i in range(len(spikes)):
        draw_block(*spikes[i], "spike", spike_dirs[i][0]) # type: ignore # draw all spikes again
    for part in typ:
        if part in spikes:
            spiked = True
    if typ == worm:
        if spiked:
            return(True) # if a worm part touches spikes, return "I'm dead", hence True
        x, y = worm[-1]
        for escape_block in [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]:
            if not (escape_block in grounds or escape_block in worm): # if I can escape, return "I'm not dead", hence False
                return(False)
        return(True) # if I cannot escape, return "I'm dead", hence True
    return(None)


def check_death():
    if dead(worm):
        bindings("remove")
        update()
        ontimer(lambda: (bindings("create"), restart()), 300) # sleep doesn't work, but ontimer works.


def in_goal():
    for goal in goals:
        if worm[-1] == goal and not apples:
            global level
            bindings("remove")
            if level < MAX_LEVEL:
                level += 1 # corresponds to: level = level + 1
                ontimer(lambda: (bindings("create"), restart()), 500) # sleep doesn't work, but ontimer works.
            else: # if level == MAX_LEVEL
                ontimer(finish_game, 500) # sleep doesn't work, but ontimer works.
            return(True)
    return(False)


def finish_game():
    clear()
    goto(-333, 0)
    pencolor("white")
    write("You did it!", font = ("Arial", 100, "bold"))
    done()


def fall_step():
    global worm, falling, worm_falling
    falling = True
    worm_falling = False
    update()
    if not on_ground(worm):
        if dead(worm):
            update()
            ontimer(restart(), 300) # sleep doesn't work, but ontimer works.
        else:
            for part in worm:
                draw_block(*part, "empty") # type: ignore # erase the falling worm
            worm = [[x, y-1] for x, y in worm] # update the worm
            for part in worm:
                draw_block(*part, "worm") # type: ignore # draw the updated worm
            draw_block(*worm[-1], "worm_head", worm_dir) # type: ignore # add the worm head
            worm_falling = True
            if worm[-1][1] < DEATH_Y: # worm[-1][1] is the y value of the worm head
                restart()
                return
            check_death()
    if worm_falling:
        ontimer(lambda: (fall_step(), moving_block_fall_step() if not blocks_falling else None), FALL_SPEED) # next step after 100 ms
        worm_falling = False
    else:
        falling = False
    update()


def moving_block_fall_step():
    global moving_blocks, blocks_falling
    blocks_falling = True
    any_falling = False
    new_blocks = []
    update()
    for block in moving_blocks:
        if not on_ground([block]):
            draw_block(*block, "empty") # type: ignore
            block = [block[0], block[1]-1]
            draw_block(*block, "moving_block") # type: ignore
            any_falling = True
        new_blocks.append(block)
    moving_blocks = new_blocks
    dead(moving_blocks)
    if any_falling:
        if not worm_falling:
            ontimer(moving_block_fall_step, FALL_SPEED) # next step after 100 ms
    else:
        blocks_falling = False
    update()


def walk(direction):
    if not listening or direction == None or dead(worm):
        return
    bindings("remove")
    global falling, blocks_falling
    if not falling:
        global worm_dir
        worm_dir = direction
    
    x, y = worm[-1]
    new_block_for_direction = {UP: [x, y+1], DOWN: [x, y-1], LEFT: [x-1, y], RIGHT: [x+1, y]} # directions: 0 == right, 1 == up, 2 == left, 3 == down
    new_block = new_block_for_direction[direction]
    
    new_block_plus_for_direction = {UP: [x, y+2], DOWN: [x, y-2], LEFT: [x-2, y], RIGHT: [x+2, y]}
    new_block_plus = new_block_plus_for_direction[direction]
    
    pushing = False
    if new_block in moving_blocks:
        pushing = True
    if not (new_block in worm or new_block in grounds or (new_block in goals and apples) or falling # check if new_block isn't at any forbidden place and check if the worm is falling
            or direction == UP and (worm[-1][1] - worm[0][1]) == len(worm) - 1
            or pushing and (new_block_plus in [*worm, *grounds, *goals, *moving_blocks, *apples])):
        worm.append(new_block)
        draw_block(*worm[-1], "worm_head", worm_dir) # type: ignore # add the worm head
        draw_block(*worm[-2], "worm") # type: ignore # delete the previous worm head by making a normal worm block
        if new_block in apples:
            apples.remove(new_block)
        else:
            draw_block(*worm[0], "empty") # type: ignore # delete the worm tail
            worm.pop(0)
            if pushing:
                draw_block(*new_block_plus, "moving_block") # type: ignore
                moving_blocks.remove(new_block)
                moving_blocks.append(new_block_plus)
                dead(moving_blocks)
    
    update()
    bindings("create")
    if in_goal():
        bindings("remove")
        return
    check_death()
    if not falling:
        falling = True
        update()
        ontimer(fall_step, FALL_SPEED)
    if not (blocks_falling or worm_falling):
        blocks_falling = True
        update()
        ontimer(moving_block_fall_step, FALL_SPEED)


def bindings(typ):
    global listening
    if typ == "remove":
        listening = False # stop callbacks
    elif typ == "create":
        listening = True # enable callbacks


hideturtle()
update()
restart()
listen()
bindings("create")
# directions: 0 == right, 1 == up, 2 == left, 3 == down
onkey(lambda: walk(UP) ,"w"); onkey(lambda: walk(UP) ,"Up")
onkey(lambda: walk(DOWN) ,"s"); onkey(lambda: walk(DOWN) ,"Down")
onkey(lambda: walk(LEFT) ,"a"); onkey(lambda: walk(LEFT) ,"Left")
onkey(lambda: walk(RIGHT) ,"d"); onkey(lambda: walk(RIGHT) ,"Right")
onkey(restart, "r"); onkey(restart,"space")

mainloop()
