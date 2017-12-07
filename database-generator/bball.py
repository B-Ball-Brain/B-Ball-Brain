realPositions = dict(Forward=2, Center=1, Guard=2)

def getFixedPlayers(oldPositions):
    extraPlayers = set()

    goodPositions = {pos: [] for pos in realPositions}
    badPositions = set(oldPositions.keys()) - set(goodPositions.keys())
    for realPos, posMaxNum in realPositions.items():
        if realPos in oldPositions:
            # copy over the good positions
            while len(oldPositions[realPos]) > 0:
                if len(goodPositions[realPos]) < posMaxNum:
                    goodPositions[realPos].append(oldPositions[realPos].pop())
                else:
                    # excess players go to the extras
                    extraPlayers.add(oldPositions[realPos].pop())

    # Add players from bad position that look similiar to good positions
    for realPos, maxNum in realPositions.items():
        for badPos in badPositions:
            # bad position is close to a good position
            if realPos in badPos:
                while len(goodPositions[realPos]) < maxNum and len(oldPositions[badPos]) > 0:
                    goodPositions[realPos].append(oldPositions[badPos].pop())

    # Now move the rest of the bad everything into the extras list
    for badPos in badPositions:
        extraPlayers.update(oldPositions[badPos])

    # move the extras to the unfilled positions
    for realPos, maxNum in realPositions.items():
        while len(goodPositions[realPos]) < maxNum:
            goodPositions[realPos].append(extraPlayers.pop())

    # check that all positions are filled
    for realPos, maxNum in realPositions.items():
        assert len(goodPositions[realPos]) == maxNum

    return goodPositions
