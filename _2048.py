from numpy import array, zeros, random, any

class _2048(object):
    ''' A class of 2048 ( and its extension). 
    Here we set {'u'(up):0, 'd'(down):1, 'l'(left):2, 'r'(right):3}.
    It will return -1 when you take an invalid move, and -2 when game over.'''

    def __init__(self, length = 4):         
        self.length = length
        self.board = zeros((length, length))
        self.point = 0        
        self.__aar()
        self.__aar()

    def reset(self):
        '''reset the chess board and add two 2/4'''
        self.board = zeros((self.length, self.length))
        self.point = 0
        self.__aar()
        self.__aar()

    def get_board(self):
        '''return the borad'''
        return self.board

    def get_point(self):
        return self.point

    def move(self, order):
        '''return the board and the total point you get'''
        if type(order).__name__ == 'str':
            order = {'u':0, 'd':1, 'l':2, 'r':3}[order]
        p = self.__jtv( [self.up, self.down, self.left, self.right][order] )
        if p != -1:
            self.point += p           
            self.__aar()
            return self.point
        else:
            if self.__alive():
                return -1
            else:
                print 'Game over.'
                return -2

    def __getitem__(self, order):
        '''predict the chessboard after move'''
        if type(order).__name__ == 'str':
            try:
                return self[{'u':0, 'd':1, 'l':2, 'r':3}[order]]
            except:
                print 'Error when predicting moving.'
        elif type(order).__name__ == 'int':
            try:
                return [self.up, self.down, self.left, self.right][order]()
            except:
                print 'Error when predicting moving.'

    def __alive(self):                
        '''lack of efficiency'''
        acc = 0
        for ele in [self.up, self.down, self.left, self.right]:
            acc += self.__jtv(ele, change = False)
        return acc != -4        

    def __jtv(self, movement, change = True):
        '''judge the validity'''
        tmp, p = movement()
        if any(tmp != self.board):
            if change:
                self.board = tmp
            return p
        else:
            return -1

    def __aar(self):
        '''add a 2/4 at random available block'''
        if (self.board == 0).sum() > 0:
            rx = random.randint(0, self.length)
            ry = random.randint(0, self.length)
            while (self.board[rx, ry] != 0):
                rx = random.randint(0, self.length)
                ry = random.randint(0, self.length)
            self.board[rx, ry] = random.choice([2, 4], 1, p=[0.9, 0.1])


    @staticmethod
    def gravity(l):
        p = 0
        new_l = []
        ind = 0
        stack = 0
        for ele in l:
            if ele == 0:
                pass
            elif ele == stack:
                new_l.append(stack * 2)
                p += stack * 2
                stack = 0
            elif stack != 0:
                new_l.append(stack)
                stack = ele
            else:
                stack = ele                    
        if stack != 0 :
            new_l.append(stack)
        return array(new_l), p

    def left(self):
        point = 0
        tmp = self.board.copy()
        for i in xrange(self.length):
            l, p = self.gravity(tmp[i, :])
            point += p
            tmp[i, :] = zeros(self.length)
            tmp[i, :len(l)] = l
        return tmp, point    

    def up(self):
        point = 0
        tmp = self.board.copy()
        for i in xrange(self.length):
            l, p = self.gravity(tmp[:, i])
            point += p
            tmp[:, i] = zeros(self.length).T
            tmp[:len(l), i] = l.T
        return tmp, point               
            
    def right(self):
        point = 0
        tmp = self.board.copy()
        for i in xrange(self.length):
            l, p = self.gravity(tmp[i, ::-1])
            point += p
            tmp[i, :] = zeros(self.length)
            tmp[i, ::-1][:len(l)] = l
        return tmp, point               

    def down(self):
        point = 0
        tmp = self.board.copy()
        for i in xrange(self.length):
            l, p = self.gravity(tmp[::-1, i].T)
            point += p
            tmp[:, i] = zeros(self.length).T
            tmp[::-1, i][:len(l)] = l.T
        return tmp, point 
