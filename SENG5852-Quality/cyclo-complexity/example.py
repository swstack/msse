def cyclo1():
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
    cyclo1()

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
