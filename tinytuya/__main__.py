# TinyTuya Module
# -*- coding: utf-8 -*-
"""
 Python module to interface with Tuya WiFi smart devices

 Author: Jason A. Cox
 For more information see https://github.com/jasonacox/tinytuya

 Run TinyTuya Setup Wizard:
    python -m tinytuya wizard
 This network scan will run if calling this module via command line:
    python -m tinytuya <max_time>

"""

# Modules
import sys
import tinytuya
from . import wizard
from . import scanner

retries = 0
state = 0
color = True
retriesprovided = False
force = False
force_list = []
last_force = False
broadcast_listen = True
assume_yes = False

for i in sys.argv:
    if i==sys.argv[0]:
        continue
    this_force = False
    if i.lower() == "wizard":
        state = 1
    elif i.lower() == "scan":
        state = 0
    elif i.lower() == "-nocolor":
        color = False
    elif i.lower() == "-force":
        force = True
        this_force = True
    elif i.lower() == "-no-broadcasts":
        broadcast_listen = False
    elif i.lower() == "snapshot":
        state = 2
    elif i.lower() == "devices":
        state = 3
    elif i.lower() == "json":
        state = 4
    elif i.lower() == "-yes":
        assume_yes = True
    elif last_force and len(i) > 6:
        this_force = True
        force_list.append( i )
    else:
        try:
            retries = int(i)
            retriesprovided = True
        except:
            state = 10

    last_force = this_force

if force and len(force_list) > 0:
    force = force_list

# State 0 = Run Network Scan
if state == 0:
    if retriesprovided:
        scanner.scan(scantime=retries, color=color, forcescan=force, discover=broadcast_listen, assume_yes=assume_yes)
    else:
        scanner.scan(color=color, forcescan=force, discover=broadcast_listen, assume_yes=assume_yes)

# State 1 = Run Setup Wizard
if state == 1:
    if retriesprovided:
        wizard.wizard(color=color, retries=retries, forcescan=force)
    else:
        wizard.wizard(color=color, forcescan=force)

# State 2 = Snapshot Display and Scan
if state == 2:
    scanner.snapshot(color=color)

# State 3 = Scan All Devices
if state == 3:
    if retriesprovided:
        scanner.alldevices(color=color, scantime=retries)
    else:
        scanner.alldevices(color=color)

# State 4 = Scan All Devices
if state == 4:
    scanner.snapshotjson()

# State 10 = Show Usage
if state == 10:
    print("TinyTuya [%s]\n" % (tinytuya.version))
    print("Usage:\n")
    print("    python -m tinytuya <command> [<max_time>] [-nocolor] [-force [192.168.0.0/24 192.168.1.0/24 ...]] [-h]")
    print("")
    print("      wizard         Launch Setup Wizard to get Tuya Local KEYs.")
    print("      scan           Scan local network for Tuya devices.")
    print("      devices        Scan all devices listed in devices.json file.")
    print("      snapshot       Scan devices listed in snapshot.json file.")
    print("      json           Scan devices listed in snapshot.json file [JSON].")
    print("      <max_time>     Maximum time to find Tuya devices [Default=%s]" % tinytuya.SCANTIME)
    print("      -nocolor       Disable color text output.")
    print("      -force         Force network scan for device IP addresses.  Auto-detects network range if none provided.")
    print("      -no-broadcasts Ignore broadcast packets when force scanning.")
    print("      -h             Show usage.")
    print("")

# End
