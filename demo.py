from _2048 import _2048
from numpy.random import choice

def show(game):                             #visualize the chessboard
    print game.get_point()                  #or just game.point
    print game.get_board()                  #or just game.board

if __name__ == '__main__':
    
    game = _2048(length = 4)                #create a length * length board    
    while True:
        show(game)

        order = raw_input()
        if order == 'reset':
            game.reset()                    #reset the game
        elif order == 'quit':
            break
        else:
            game.move(order)                #here we set {'u'(up):0, 'd'(down):1, 'l'(left):2, 'r'(right):3}
                                            #if the move is valid, it will return the total point until now,
                                            #   otherwise it will return -1 when the move is invalid
                                            #   and -2 when game over


    #===================the greedy strategy=====================   #believe it or not, it once reachs 4400+
    game.reset()
    maximum = 0
    while True:        
        t = []
        for i in xrange(4):
            t.append( game[i][1] )          #game[ind] return the prediction(board, delta_point) after the movement ind without execute it
        t = map(lambda x: x+4, t)           #avoid the situation that sum(t) == 0
        t = map(lambda x: float(x)/sum(t), t)
        if game.move(int(choice(range(4), p = t))) == -2:            
            if maximum < game.point:
                maximum = game.point
            game.reset()                
        print maximum
        show(game)
