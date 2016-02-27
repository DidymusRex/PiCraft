#! /usr/bin/env python
import mcpi.minecraft as minecraft
import mcpi.block as block
mc = minecraft.Minecraft.create()

# remember we imported mcpi.block

# put a stone block 5 meters north
mc.setBlock(pos.x, pos.y, pos.z+5, block.STONE.id)

# stack coal on top of it
mc.setBlock(pos.x, pos.y+1, pos.z+5, block.COAL_ORE.id)
