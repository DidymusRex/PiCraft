#! /usr/bin/env python
import mcpi.minecraft as minecraft
import mcpi.block as block
mc = minecraft.Minecraft.create()

pos=mc.Player.getTilePos()
print pos.x, pos.y, pos.z
# Fancier ...
print “x is %d y is %d z is %d” % (pos.x, pos.y, pos.z)
