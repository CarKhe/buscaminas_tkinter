import random
WIDTH = 5
HEIGH = 8 
MINES = 5


class UnopenedSquareValue:
    def __init__(self,value,range):
        self.__value = value
        self.__range = range
    
    def get_value(self):
        return self.__value
    
    def get_range(self):
        return self.__range
    
    def get_list(self):
        return [self.__value,self.__range]
        
        
class BoardGameMatriz:
    def __init__(self):
        if (HEIGH * WIDTH) < MINES: return
        only_bombs_matriz,self.__mines_place,self.__objects_matriz = self.__game_matriz()
        self.__board_matriz = self.__check_matriz(only_bombs_matriz)
        for y in range(HEIGH):
            for x in range(WIDTH):
                self.__objects_matriz[y][x] = UnopenedSquareValue(self.__board_matriz[y][x],[y,x])
            
    def get_board_matriz(self):
        return self.__board_matriz
    
    def get_mines_place(self):
        return self.__mines_place
    
    def get_objects_matriz(self):
        return  self.__objects_matriz
    
    def get_matriz_values(self):
        return [HEIGH,WIDTH,MINES]
    
    def __game_matriz(self):
        matriz = []
        obj_matriz = []
        for i in range(HEIGH):
            matriz.append([0]*WIDTH)
            obj_matriz.append([0]*WIDTH)
        mines_place = self.__mines_position()
        for val in mines_place:
            x = val[0]
            y = val[1]
            matriz[x][y] = 9
        return matriz,mines_place,obj_matriz
    
    def __mines_position(self):
        mines_place = []
        for i in range(MINES):
            while True:
                x = random.randint(0,(WIDTH - 1))
                y =random.randint(0,(HEIGH - 1))
                mines_place.append([y,x])
                if i == mines_place.index([y,x]):
                    break
                else:
                    mines_place.pop(i)
        return mines_place
    
    def __check_matriz(self,matriz):
        for y in range(HEIGH):
            for x in range(WIDTH):
                matriz = self.__bombs_around(matriz,y,x) 
        return matriz
    
    def __bombs_around(self,matriz,y,x):
        bombs = 0
        if matriz[y][x] == 9:
            return matriz
        else:
            around_val =self.__around(x,y)
            for val in around_val:
                if matriz[val[0]][val[1]]==9:
                    bombs = bombs + 1
            matriz[y][x] = bombs
            return matriz
        
    def __around(self,x,y):
        around = []
        to_remove = []
        around.append([(y-1),(x-1)])
        around.append([(y-1),(x)])
        around.append([(y-1),(x+1)])
        around.append([(y),(x-1)])
        around.append([(y),(x+1)])
        around.append([(y+1),(x-1)])
        around.append([(y+1),(x)])
        around.append([(y+1),(x+1)])
        for val in around:
            if val[0]==-1 or val[1]==-1 or (val[0]>=HEIGH) or (val[1]>=WIDTH):
                to_remove.append(val)
        for rem in to_remove:
            around.remove(rem)
        return  around


#print(BoardGameMatriz().get_board_matriz())




        