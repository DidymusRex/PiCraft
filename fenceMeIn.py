#!/usr/bin/env python
#
# fenceGame.py
#
"""
No, this is not the most *pythonic* way to program this game but it's
a start and I had fun doing it. There are a few items to clean up that
are left to you to figure out. If you have mad Python skillz and want
to show me the "right" way to do it I'm certainly up for a programming
lesson. If you come up with a fun or cool addition to the game please 
share, or not, it's your code now! Enjoy.

To Do:
    1. If the diamond block is destroyed Steve can't hit it, but 
       it is never regenerated. Stalemate. We can either reset the
       arena each time Steve is catapulted, or find a way to see
       the diamond is gone and replace it. mc.getBlock(x, y, z) == AIR
       might be a clue.

    2. fix the lazy arena reset on win and reposition the diamond. More
       code but more elegant. This code may also help above if the diamond
       disappears. Poll hits and get the block type where the diamond is
       supposed to be each loop. Then both a hit and a smash (right and left 
       click) can score.

    3. Determine what the extra data for a FENCE_GATE really means and face
       them the right way.
"""

# Import required modules for the game
import mcpi.minecraft as minecraft
import mcpi.block as block
import random
import time

# Create the arena given the center point as a Vec3 object (coodinate set)
#     and to desired size of the play area
def createArena(arenaCenter, arenaSize):
    print ("Arena center point is %d, %d, %d with size %d" % 
            (arenaCenter.x, arenaCenter.y, arenaCenter.z, arenaSize))

    # Single-letter variables for lazy typists
    # L is the distance from the center to the edge of the play area
    #     since we will use the arena center as the reference for the
    #     placement of all the blocks
    s = arenaSize
    L = int(s/2)
    x = arenaCenter.x
    y = arenaCenter.y
    z = arenaCenter.z

    # Clear an area twice as big as the arena by changing all the 
    #     blocks to AIR. setBlocks defines a 3D area by giving it 
    #     the corrdinates of two opposite corners and the type of
    #     block to fill it with. Then fill a 1 block high area under
    #     Steve's feet with GRASS.
    mc.setBlocks(x-s,y-1,z-s,x+s,y+s,z+s,block.AIR.id)
    mc.setBlocks(x-s,y-1,z-s,x+s,y-1,z+s,block.GRASS.id)

    # Place a fence around the arena by creating a layer of FENCE
    #     1 block deep, then "subtracting" a layer 1 block smaller
    #     from the middle. Easier than calculating the side of the 
    #     arena individually! Then place a gate in the middle of each
    #     side of the fence.
    mc.setBlocks(x-L,y,z-L,x+L,y,z+L,block.FENCE.id)
    mc.setBlocks(x-L+1,y,z-L+1,x+L-1,y,z+L-1,block.AIR.id)
    mc.setBlock(x,y-1,z,block.STONE.id)
    mc.setBlock(x,y,z+L+3,block.OBSIDIAN.id)

    mc.setBlock(x-L,y,z,block.FENCE_GATE,2)
    mc.setBlock(x+L,y,z,block.FENCE_GATE,2)
    mc.setBlock(x,y,z-L,block.FENCE_GATE,0)
    mc.setBlock(x,y,z+L,block.FENCE_GATE,0)

    # Place a diamond block in a random spot inside the arena. Subtract 1
    #     from L to keep the range inside the fence, then generate a random
    #     position N/S and E/W from -L to L. Keep the height(y) at eye level
    L = L-1
    diamondPos = (x + random.randint(-1*L, L), y+1, z + random.randint(-1*L,L))
    mc.setBlock(diamondPos[0], diamondPos[1], diamondPos[2], block.DIAMOND_BLOCK.id)

    # Don't leave Steve in the arena. Bounce him out to start
    #     each new game.
    catapultPlayer(arenaCenter, arenaSize)

    # Finally, tell the caller where the Diamond is.
    print "Diamond is placed at ", diamondPos
    return diamondPos


# Check to see if the player's coordinates are within the arena.
#     Return true or false
def checkInBounds(playerPos, arenaCenter, arenaSize):
    r = False
    L = int(arenaSize/2)

    # The player is east of the west fence and west of the east fence
    if(playerPos.x > arenaCenter.x - L) and (playerPos.x < arenaCenter.x + L):
        # The player is north of the south fence ans south of the north fence
        if(playerPos.z > arenaCenter.z - L) and (playerPos.z < arenaCenter.z + L):
            r = True

    return r


# Ask the server for the list of all hit events so we can see if 
#     Steve hit the diamond with his sword (it has to be a SWORD
#     right-click to count as a hit, then compare the coordinates
#     of the hit with the coordinates of the diamond.
def checkHits(diamondPos):
    r = False
    hits = mc.events.pollBlockHits()

    # Process each event in the list
    for h in hits:
        if h.pos.x == diamondPos[0] and h.pos.y == diamondPos[1] and h.pos.z == diamondPos[2]:
            # We found a hit, discard the rest of the list so we
            #     don't have to process the remainder next time.
            mc.events.clearAll()
            r = True

    return r



# Catapult Steve to a random N/S, E/W coordinate 20 blocks
#     above the arena floor and outside the fence. Why 20
#     meters in the air? Steve deserves it.
def catapultPlayer(arenaCenter, arenaSize):
    global inBounds

    L = int(arenaSize/2)
    x = arenaCenter.x + L + random.randint(1, L)
    y = arenaCenter.y + 20
    z = arenaCenter.z + L + random.randint(1, L)

    # Yes, flying is fun (at lease in creative mode). Also display
    #     the current score and mark Steve as out-of-bounds
    mc.postToChat("Wheeeeee")
    print "Sending Steve to %d, %d, %d" % (x,y,z)
    mc.player.setPos(x,y,z)
    inBounds = False


 
# ---------------------------------------------
# P L A Y   S T A R T S   H E R E
# ---------------------------------------------

# Connect to the Minecraft server
mc = minecraft.Minecraft.create()

# napTime is the loop delay between checking Steve's
#     whereabouts, whether the diamond has been hit,
#     and if it is time to catapult Steve out-of-bounds.
#     timeLimit is how many seconds Steve has once he
#     sets foot in the arena to hit the diamond. inBounds
#     tells if Steve is inside or outside the fence.
#     score ... duh. ac is Steve's position at startup
#     and will forever be the arena center. sz is the
#     arena size.
napTime = .1
timeLimit = 10
startTime = time.time()
inBounds = False
score = 0.0
ac = mc.player.getTilePos()
sz = 15

# Create the arena and learn where the diamond is. dPos
#     is a tuple with the x, y, z coordinates. Since it is
#     a tuple and not a Vec3 object we will need to reference
#     its contents by index, as we'll see later.
dPos = createArena(ac, sz)

# Forever is along, long time. Ctl-C will stop the program.
#     This loop will continue on and on until you stop it.
while True:

    # Find out if Steve is in the arena
    if checkInBounds(mc.player.getPos(), ac, sz):
        # He is, but he wasn't before. Mark him in-bounds,
        #     post to chat that stuff just got real and
        #     start the timer
        if inBounds == False:
            inBounds = True
            mc.postToChat("Go!")
            startTime = time.time()
        # He was already in-bounds so print the elapsed time.
        #     When it hit zero it's catapult time!
        else:
            print time.time() - startTime

        # The longer Steve is in-bounds the lower the score
        score = score - napTime

    # See if Steve has managed to hit the diamond
    if checkHits(dPos):
        # Yay! Score! Now reset the arena. We could just
        #     reposition the diamond, but this function
        #     works and it's already written... lazy.
        score = score + 100
        mc.postToChat(">>> CLANK <<<")
        dPos = createArena(ac,sz)

    # Finally, if timeLimit seconds have elapsed since
    #     Steve set foot in-bounds catapult him away.
    if time.time() - startTime > timeLimit and inBounds:
        catapultPlayer(ac, sz)

    # If you're a computer .1 seconds is a nice nap. Then
    #     get back to work harassing Steve.
    time.sleep(napTime)
