import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random



SIZE = 20
WIDTH = 12
HEIGH = 15 
MINES = 25


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
    

class View:
    def __init__(self) -> None:
        self.bgm =BoardGameMatriz()
        self.mines_mines = 0
        self.values = self.bgm.get_matriz_values()
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.root.iconbitmap("assets/Minesweeper_1992.ico")
        self.root.geometry("280x380")

        self.planted_mines = tk.Frame(self.root,bg="#AFA8A8")
        self.planted_mines.place(x=10,y=10,width=90,height=50)

        self.mines_remain = tk.Label(self.planted_mines,font=('digital-7',30,'bold'),
            background='black',foreground='red',text=MINES)
        self.mines_remain.pack()

        self.restart_button = tk.Button(self.root,text="(ツ)",command=lambda: self.restart())
        self.restart_button.place(x=110,y=10,height=50,width=50)

        self.time = tk.Frame(self.root,bg="#AFA8A8")
        self.time.place(x=170,y=10,width=90,height=50)

        self.lbl_time = tk.Label(self.time,font=('digital-7',30,'bold'),
            background='black',foreground='red')
        self.lbl_time.pack()

        self.board = tk.Frame(self.root,bg="#AFA8A8")
        self.board.place(x=10,y=70,height=300,width=250)
        
        
        self.matriz = self.bgm.get_objects_matriz()
        self.to_gameplay =self.matriz_to_gameplay()
        
        self.mines_place = self.bgm.get_mines_place()
        
        self.to_gameplay = self.matriz_objets()
        
        
        self.root.mainloop()
        
    def set_mines_mine(self,val):
        if val:
            self.mines_mines = MINES + 1
        else:
            self.mines_mines = MINES - 1  
        self.mines_remain.config(text=self.mines_mines)   
    
    def matriz_to_gameplay(self):
        obj_matriz = []
        for i in range(self.values[0]):
            obj_matriz.append([0]*self.values[1])
            
        return obj_matriz
    
    def matriz_objets(self):
        for y in range(self.values[1]):
            for x in range(self.values[0]):
                self.to_gameplay[x][y] = Button(self.board,self.matriz[x][y].get_value(),(SIZE*x),(SIZE*y),x,y)
        for y in range(self.values[1]):
            for x in range(self.values[0]):
                self.to_gameplay[x][y].set_objs(self.to_gameplay)
                self.to_gameplay[x][y].set_mines_place(self.mines_place)
        return self.to_gameplay
    
    def get_to_gameplay(self):
        return self.to_gameplay
    
    def restart(self):
        del self.bgm
        self.bgm =BoardGameMatriz()
        self.matriz = self.bgm.get_objects_matriz()
        self.mines_place = self.bgm.get_mines_place()
        self.to_gameplay =self.matriz_to_gameplay()
        self.to_gameplay = self.matriz_objets()
    
     
       
       

class Gameplay:  
    def click(objs,h,w):
        obj = objs[h][w]
        val = objs[h][w].get_val()
        if val == 9:
            obj.click()
            mines = obj.get_mines_place()
            messagebox.showinfo(title="Game Over",message="You Lost")
            for min in mines:
                try:
                    objs[min[0]][min[1]].click()
                except:
                    pass
            
        
        elif val == 0:
            
            Gameplay.floodfill(objs,h,w)
            
        else:
            obj.click()
    
    def floodfill(objs,h,w):
        
        if h==-1 or w==-1 or (h>=HEIGH) or (w>=WIDTH):
            return

        btn = objs[h][w]
        val = btn.get_val()
        if val == 10:
            return
        if val !=9 and val !=0:
            btn.click()
        if val == 0 :
            btn.click()
            Gameplay.floodfill(objs,h-1,w)
            Gameplay.floodfill(objs,h-1,w+1)
            Gameplay.floodfill(objs,h,w+1)
            Gameplay.floodfill(objs,h+1,w+1)
            Gameplay.floodfill(objs,h+1,w)
            Gameplay.floodfill(objs,h+1,w-1)
            Gameplay.floodfill(objs,h,w-1)
            Gameplay.floodfill(objs,h-1,w-1)
    

        
          
        

class Button:
    def __init__(self,frame,val,y,x,w,h):
        self.frame = frame
        self.val = val
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.objs = ""
        self.mines_place = ""
        self.button = tk.Button(self.frame,command =lambda :Gameplay.click(self.objs,w,h))
        self.button.bind("<Button-3>",lambda x:self.red_flag())
        self.button.place(x=self.x,y=self.y,height=SIZE,width=SIZE)
        
    
    def set_objs(self,objs):
        self.objs = objs 
        
    def set_mines_place(self,mines):
        self.mines_place = mines
    
    def get_mines_place(self):
        return self.mines_place
    def get_objs(self):
        return self.objs
    
    def get_val(self):
        return self.val
            
    def click(self):
        if self.val == 9:
            self.photo = self.image("assets/mine_revealed.png")
            self.button.config(image=self.photo)
            
        elif self.val == 0:
            self.photo = self.image("assets/blank.png")
            self.button.config(image=self.photo)

        else:
            self.photo = self.image(f"assets/{self.val}.png")
            self.button.config(image=self.photo)
            
        self.result = tk.Label(self.frame,image=self.photo)
        self.result.place(x=self.x,y=self.y,height=SIZE,width=SIZE)    
        self.val = 10
        #self.label_change()
        
    def label_change(self):
        self.result = tk.Label(self.frame,
            text=self.val,font=('digital-7',SIZE,'bold'))
        self.result.place(x=self.x,y=self.y,height=SIZE,width=SIZE)
        if self.val == 0:
            self.result.config(text="") 
        elif self.val ==1:
            self.result.config(foreground='blue')
        elif self.val ==2:
            self.result.config(foreground='green') 
        elif self.val ==3:
            self.result.config(foreground='red') 
        elif self.val ==4:
            self.result.config(foreground='dark blue') 
        elif self.val ==5:
            self.result.config(foreground='brown') 
        elif self.val ==6:
            self.result.config(foreground='cyan') 
        elif self.val ==7:
            self.result.config(foreground='black') 
        elif self.val ==8:
            self.result.config(foreground='gray') 
        self.val = 10
    
    def red_flag(self):
        self.photo = self.image("assets/redflag.png")
        self.button.config(image=self.photo,state="disabled")
        self.button.bind("<Button-3>",lambda x:self.unopened())
        
        
        
    def unopened(self):
        self.button.config(image="",state="normal")
        self.button.bind("<Button-3>",lambda x:self.red_flag())
        
    
        
        
    def image(self,img_route):
        my_img_pc = Image.open(img_route)
        resize_pc=my_img_pc.resize((SIZE,SIZE))
        photo_pc = ImageTk.PhotoImage(resize_pc)
        return photo_pc






View()        
    
    
    

    


    



