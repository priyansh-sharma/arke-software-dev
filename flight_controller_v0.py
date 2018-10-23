import mission_cmds_v0 as cmds

sitl = None
lat = 39.720643
lon = -75.146264

vehicle = cmds.connect_vehicle("")

cmds.arm_and_takeoff(vehicle, 10)

cmds.simple_goto(vehicle, lat, lon)