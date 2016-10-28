# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# http://blog.mayec.eu/2011/05/python-hamiltonian-cycles-in-graph.html#
#
# roelsch2015@gmail.com
# Modified for Python3 and PEP8

from __future__ import print_function

########################################################################

import sys

"""
Code written by Mayec Rancel. March 2011

Zones zA,zB,zC,zD,zE,zF,zG,zH,zI,zJ,zK
Bridges a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r

zA abc
zB afg
zC ijmn
zD pqr
zE der
zF fhi
zG lmp
zH bdhl
zI gjk
zJ noq
zK ceko

"""
# Zones connections:
zA = ['a', 'b', 'c']
zB = ['a', 'f', 'g']
zC = ['i', 'j', 'm', 'n']
zD = ['p', 'q', 'r']
zE = ['d', 'e', 'r']
zF = ['f', 'h', 'i']
zG = ['l', 'm', 'p']
zH = ['b', 'd', 'h', 'l']
zI = ['g', 'j', 'k']
zJ = ['n', 'o', 'q']
zK = ['c', 'e', 'k', 'o']
# Bridge connections:
a = ['zA', 'zB']
b = ['zA', 'zH']
c = ['zA', 'zK']
d = ['zH', 'zE']
e = ['zE', 'zK']
f = ['zB', 'zF']
g = ['zB', 'zI']
h = ['zF', 'zH']
i = ['zF', 'zC']
j = ['zC', 'zI']
k = ['zI', 'zK']
l = ['zH', 'zG']
m = ['zC', 'zG']
n = ['zC', 'zJ']
o = ['zJ', 'zK']
p = ['zD', 'zG']
q = ['zD', 'zJ']
r = ['zD', 'zE']

zones = {
    'zA': zA, 'zB': zB, 'zC': zC, 'zD': zD, 'zE': zE, 'zF': zF, 'zG': zG, 'zH':
    zH, 'zI': zI, 'zJ': zJ, 'zK': zK
}
#zones = {'zA':zA} #debug

bridges = {
    'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i,
    'j': j, 'k': k, 'l': l, 'm': m, 'n': n, 'o': o, 'p': p, 'q': q, 'r': r
}
# usedBridges & usedZones: 1 not yet used, 0 used

usedBridges = {
    'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1, 'i': 1,
    'j': 1, 'k': 1, 'l': 1, 'm': 1, 'n': 1, 'o': 1, 'p': 1, 'q': 1, 'r': 1
}

usedZones = {
    'zA': 1, 'zB': 1, 'zC': 1, 'zD': 1, 'zE': 1, 'zF': 1, 'zG': 1, 'zH': 1,
    'zI': 1, 'zJ': 1, 'zK': 1
}

limitRuns = False
maxRuns = 30
debugSwitch = False
pathNumbers = True
toFile = True
haltOnHamiltonianPath = False

# Book-Keeping:
runs = 0
hamiltonianPaths = 0
path = []


def debug(message):
    global debug
    if debugSwitch:
        print(message)
    else:
        return 0


def formatPath(path):
    myPath = ''
    for i in range(0, len(path)):
        myPath += (str(path[i]) + ' ')
    return myPath


def exploreBridges(zone, firstBranch):
    global runs, maxRuns, hamiltonianPaths, path, usedZones, usedBridges, file

    # mark this zone as used
    usedZones[zone] = 0
    debug("usedZones: " + str(usedZones))

    if firstBranch:
        print("")
        print(" -- ALL PATHS STARTING AT " + zone + " -- ")
        print("")

    path.append(zone)
    usableBridges = zones[zone]
    # update list of usable bridges - removing those that have been used
    debug("bridges in this zone: " + str(usableBridges))
    debug("see bridges:")
    newUsableBridges = list(usableBridges)
    for bridge in usableBridges:
        #debug( "used? " + bridge + "," + str(usedBridges[bridge]) )
        # remove bridge from usable bridges if it has been used
        if usedBridges[bridge] == 0:
            newUsableBridges.remove(bridge)
        # remove bridge from usable bridges if connects to a used zone
        elif (
            (bridges[bridge][0] == zone) and
            (not usedZones[bridges[bridge][1]])
        ) or (
            (bridges[bridge][1] == zone) and
            (not usedZones[bridges[bridge][0]])
        ):
            newUsableBridges.remove(bridge)

    usableBridges = newUsableBridges
    debug("unused bridges in this zone:" + str(usableBridges))
    # if any available bridges to test
    if len(usableBridges) > 0:
        for bridge in usableBridges:
            debug("now in zone " + zone)
            debug("cross " + bridge)
            #cross first available bridge
            path.append(bridge)
            usedBridges[bridge] = 0
            debug("usedBridges: " + str(usedBridges))
            #find out which zone is across bridge
            if zone == bridges[bridge][0]:
                newZone = bridges[bridge][1]
            else:
                newZone = bridges[bridge][0]
            #explore that zone
            exploreBridges(newZone, 0)
        # once done with all bridges:
        if len(path) > 1:
            # remove last zone visited
            # reset last zone visited to not used
            usedZones[path[len(path) - 1]] = 1
            # remove last zone from path
            removed = path.pop()
            debug("remove " + removed)
            # remove last bridge crossed
            # reset last bridge passed to not used
            usedBridges[path[len(path) - 1]] = 1
            removed = path.pop()
            debug("remove " + removed)

    # else, we are in a dead end
    else:

        runs += 1
        print("*PATH", end="")
        if toFile:
            file.write("*PATH ")
        if pathNumbers:
            print("(" + str(runs) + ")", end="")
            if toFile:
                file.write("(" + str(runs) + ")")
        print(":", end="")
        if toFile:
            file.write(":\t")
        print(formatPath(path), end="")
        if toFile:
            file.write(formatPath(path) + "\t")
        # print number of zones visited
        zonesCount = 0
        for zone in zones:
            if usedZones[zone] == 0:
                zonesCount += 1
        print(str(zonesCount) + " zones")
        if toFile:
            if zonesCount < 5:
                file.write("\t")
            if zonesCount < 6:
                file.write("\t")
            if zonesCount < 7:
                file.write("\t")
            if zonesCount < 9:
                file.write("\t")
            if zonesCount < 10:
                file.write("\t")
            file.write(str(zonesCount) + " zones" + "\n")

        if zonesCount == 11:
            # Test for Hamiltonian Cycle - Hamiltonian path that ends at the
            # same zone where it started
            lastZone = path[len(path) - 1]
            firstZone = path[0]
            lastZoneBridges = zones[lastZone]
            for bridge in lastZoneBridges:
                bridgeZones = bridges[bridge]
                if (
                    bridgeZones[0] == firstZone
                ) or (
                    bridgeZones[1] == firstZone
                ):
                    print("Hamiltonian Cycle found!")
                    sys.exit()
                else:
                    print("Test for Hamiltonian Cycle returned negative")
                    if toFile:
                        file.write(
                            "Test for Hamiltonian Cycle returned negative\n"
                        )
            # End of test for Hamiltonian Cycle

            # Test for Hamiltonian Path - if all zones have been visited
            hamiltonianPaths += 1
            print ("Hamiltonian path found!")
            if toFile:
                file.write("Hamiltonian Path!\n")
            if (haltOnHamiltonianPath):
                sys.exit()
            #End of test for Hamiltonian Path

        #if we have reached specified max. # of runs, stop execution
        if limitRuns and (runs == maxRuns):
            sys.exit(0)

        # undo last bridge crossed
        # remove last zone visited
        # reset last zone visited to not used
        usedZones[path[len(path) - 1]] = 1
        #remove last zone from path
        removed = path.pop()
        debug("remove " + removed)
        # remove last bridge crossed
        # reset last bridge passed to not used
        usedBridges[path[len(path) - 1]] = 1
        removed = path.pop()
        debug("remove " + removed)

    # if here, we have tried all bridges for this node at this level
    # undo last bridge crossed
    debug("level exhausted.")
    # if not back at beginning of path, undo last move
    debug("closeLevel")


#------------ MAIN LOOP ------------

if toFile:
    file = open('hamiltonian.txt', 'w')

for zone in zones:
    # reinitialize path and usedBridges
    path = []
    usedBridges = {
        'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1, 'i': 1,
        'j': 1, 'k': 1, 'l': 1, 'm': 1, 'n': 1, 'o': 1, 'p': 1, 'q': 1, 'r': 1
    }
    usedZones = {
        'zA': 1, 'zB': 1, 'zC': 1, 'zD': 1, 'zE': 1, 'zF': 1, 'zG': 1, 'zH': 1,
        'zI': 1, 'zJ': 1, 'zK': 1
    }

    # try paths from zone
    exploreBridges(zone, True)

if toFile:
    file.write('total Hamiltonian paths = ' + str(hamiltonianPaths) + '\n')

if toFile:
    file.close()

# end of file
