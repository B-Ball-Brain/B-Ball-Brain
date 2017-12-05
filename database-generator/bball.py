realPositions = dict(Forward=2, Guard=2, Center=1)


def playerLineupCSAT(playerPositions):
    '''playerPositions is a dict of lists'''

    badPositions = set(playerPositions.keys()) - set(realPositions.keys())
    extraPlayers = set(playerPositions.get('', []))

    # Remove excess players from the real positions into their own list
    for posName, posMaxNum in realPositions.items():
        while len(playerPositions[posName]) > posMaxNum:
            extraPlayers.add(playerPositions[posName].pop())

    # go through real positions that are not filled
    for realPosName, posMaxNum in realPositions.items():
        while len(playerPositions[realPosName]) < posMaxNum:
            changed = False

            # find a player in a similar named position to add to the real position
            for posName in playerPositions:
                if realPosName in posName and realPosName != posName:
                    if len(playerPositions[posName]) > 0:
                        playerPositions[realPosName].append(
                            playerPositions[posName].pop())
                        changed = True
                        break

            if not changed:
                break

    # leftovers that didn't get sorted into one of the hogwarts houses, put into extras
    for badPosName in badPositions:
        extraPlayers.update(playerPositions[badPosName])
        playerPositions[badPosName] = []

    for realPosName, posMaxNum in realPositions.items():
        # keep choosing from extras while position is still not filled
        while len(playerPositions[realPosName]) < posMaxNum:
            playerPositions[realPosName].append(extraPlayers.pop())

    # double check positions are good...
    for posName, players in playerPositions.items():
        if posName in realPositions:
            assert len(players) == realPositions[posName]
        else:
            assert len(players) == 0
