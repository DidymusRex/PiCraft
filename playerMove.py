#! /usr/bin/env python
import mcpi.minecraft as minecraft
import mcpi.block as block
mc = minecraft.Minecraft.create()

pos=mc.Player.getTilePos()

# remember pos is Steve’s location
mc.player.setTilePos(pos.x, pos.y+20, pos.y)
mc.player.setTilePos(pos.x, pos.y-20, pos.y)
