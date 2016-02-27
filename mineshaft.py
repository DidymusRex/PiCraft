#! /usr/bin/env python

import mcpi.minecraft as minecraft
import mcpi.block as block
import random
import time

mc = minecraft.Minecraft.create()

# ----------------------------------------------------------------------
# S E T   U P
# ----------------------------------------------------------------------

# Where Am I?
pos = mc.player.getTilePos()
print "Game center point is %d, %d, %d" % (pos.x, pos.y, pos.z)

limit=256

mc.setBlocks(pos.x, pos.y, pos.z, pos.x+10, pos.y-256, pos.z+10, block.AIR.id)
mc.setBlocks(pos.x, pos.y, pos.z, pos.x-10, pos.y+256, pos.z-10, block.DIAMOND_ORE.id)


