#! /usr/bin/env python
#
# Don't Fence Me In
#
import mcpi.minecraft as minecraft
import mcpi.block as block
import random
import time

# ==============================================================================
# F U N C T I O N S
# ==============================================================================
def makeArena (arenaCenter, arenaSize):
    print "Arena center point is %d, %d, %d with size %d" % (arenaCenter.x, arenaCenter.y, arenaCenter.z, arenaSize)

    # single letter variables make the typing easier and fit on one line
    s = arenaSize
    l = int(s / 2)
    x = arenaCenter.x
    y = arenaCenter.y
    z = arenaCenter.z

    # Clear out a flat space around the arena, let's say... 2 X as big
    mc.setBlocks(x - s, y - 1, z - s, x + s, y + s, z + s, block.AIR.id)

    # Make it grassy
    mc.setBlocks(x - s, y - 1, z - s, x + s, y, z + s, block.GRASS.id)

    # Fence in a field
    mc.setBlocks(x - l, y + 1, z - l, x + l, y + 1, z + l, block.FENCE.id)
    mc.setBlocks(x - l + 1, y + 1, z - l + 1, x + l - 1, y + 1, z + l - 1, block.AIR.id)
    mc.setBlock(x, y, z, block.STONE.id)

    # Make a gate in each side
    # FENCE_GATE orientation is defined in the optional data
    # EAST GATE
    mc.setBlock(x - l, y + 1, z, block.FENCE_GATE.id, 1)
    # WEST GATE
    mc.setBlock(x + l, y + 1, z, block.FENCE_GATE.id, 1)
    # NORTH GATE
    # mc.setBlock(x, y + 1, z + l + 3, block.OBSIDIAN.id)
    mc.setBlock(x, y + 1, z + l, block.FENCE_GATE.id, 0)
    # SOUTH GATE
    mc.setBlock(x, y + 1, z - l, block.FENCE_GATE.id, 0)

    # Set a random diamond inside the fence (l - 1 makes it inside)
    l = l - 1
    diamondPos = (x + random.randint(-1 * l, l), y + 1, z + random.randint(-1 * l, l))
    mc.setBlock(diamondPos[0], diamondPos[1], diamondPos[2], block.DIAMOND_BLOCK.id)

    # Move the player out of the arena
    catapultPlayer(arenaCenter, arenaSize)

    # Tell the caller where the diamond is
    return diamondPos
# ------------------------------------------------------------------------------

def checkInBounds(playerPos, arenaCenter, arenaSize):
    l = int(arenaSize / 2)
    r = False

    # If the player's position x is between the center x +- 1/2 the arena size
    if (playerPos.x > arenaCenter.x - l) and (playerPos.x < arenaCenter.x + l):
        # And the player's position y is between the center y +- 1/2 the arena size
        if (playerPos.z > arenaCenter.z - l) and (playerPos.z < arenaCenter.z + l):
            # The player is in bounds
            r = True

    return r
# ------------------------------------------------------------------------------

def checkHits(diamondPos):
    r = False

    # Get the list of block hits
    hits = mc.events.pollBlockHits()
    for h in hits:
        # If the hit was on our diamond clear out the hits declare success
        if h.pos.x == diamondPos[0] and h.pos.y == diamondPos[1] and h.pos.z == diamondPos[2]:
            mc.events.clearAll()
            r = True

    return r
# ------------------------------------------------------------------------------

def catapultPlayer(arenaCenter, arenaSize):
    global startTime

    l = int(arenaSize / 2)

    # pick a random spot outside the arena. Center + 1/2 arena size + a random
    # number from 0 to 1/2 the size of the arena. Oh, and put them up in the
    # air 20 meters :)
    x = arenaCenter.x + l + random.randint(1, l)
    y = arenaCenter.y + 20
    z = arenaCenter.z + l + random.randint(1, l)

    # Put the player in the calculated position and let them drop.
    mc.postToChat('Wheeeeeee!')
    print "Current score is %f at %f" % (score, time.time())
    mc.player.setPos(x, y, z)

    # (re)Start the timer!
    startTime = time.time()

# ------------------------------------------------------------------------------

# ==============================================================================
# P L A Y   T H E   G A M E
# ==============================================================================
mc = minecraft.Minecraft.create()
napTime = 0.1
timeLimit = 15.0
startTime = 0.0
score = 0.0
ac = mc.player.getTilePos()

# returns a tuple with 3 integers for x, y, and z
dp = makeArena(ac, 10)

while True:
    # is player in field? (assume level field and ignore y=coord)
    if checkInBounds(mc.player.getTilePos(), ac, 10):
        score = score - napTime

    # has player hit treasure?
    if checkHits(dp):
        score = score + 10
        mc.postToChat('>> C L A N K <<')
        dp = makeArena(ac, 10)

    # has time expired? Use Time, not score here!
    if time.time() - startTime > timeLimit:
        print "Exceeded time limit at %f from %f" % (time.time(), startTime)
        catapultPlayer(ac, 10)

    # wait a bit. 1 sec for testing .1 sec for live play.
    time.sleep(napTime)
