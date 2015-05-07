def cyclo23():
    """Simple program that has a Cyclomatic Complexity of 23

    GRADE: D
    """

    for i in range(500):

        if i and i > 100 or True:
            if i and i > 99 or True:
                if i and i > 98 or True:
                    if i and i > 97 or True:
                        if i and i > 96 or True:
                            if i and i > 95 or True:
                                if i and i > 94 or True:
                                    pass


def cyclo9():
    """Simple program that has a Cyclomatic Complexity of 9

    GRADE: B
    """

    for i in range(500):

        if i and i > 100:
            if i and i > 99:
                if i and i > 98:
                    if i and i > 97:
                        if i and i > 96:
                            if i and i > 95:
                                if i and i > 94:
                                    pass


def cyclo2():
    """Simple program that has a Cyclomatic Complexity of 2

    GRADE: A
    """

    for i in range(500):
        print(i)


def cyclo3():
    """Simple program that has a Cyclomatic Complexity of 3

    GRADE: A
    """

    print('A')

    if True:
        print('B')

    print('C')

    if True:
        print('D')
    else:
        print('E')

    print ('F')


def cyclo5():
    """Simple program that has a Cyclomatic Complexity of 5

    GRADE: A

    Note: see an example of this in graph form @cyclo-graph.png
    """

    print('A')

    if True:
        print('B')

    print('C')

    if True:
        print('D')
    else:
        print('E')

    print ('F')

    if True:
        if True:
            print('G')
        print('H')

    print('I')


if __name__ == '__main__':
    cyclo5()

    # Outputs:
    # > A
    # > B
    # > C
    # > D
    # > E
    # > F
    # > G
    # > H
    # > I
