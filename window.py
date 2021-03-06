from tkinter import *
import numpy as np

current_x, current_y = 0,0

class grid28x28:

    def __init__(self,x_dimention, y_dimention, canvas):
        self.gridpoints_x = np.zeros((28,2)).astype(int)
        self.gridpoints_y = np.zeros((28,2)).astype(int)
        self.gridpoints_master = np.zeros((28,28)).astype(float)
        self.x_dimention = x_dimention
        self.y_dimention = y_dimention
        self.canvas      = canvas

    def populate_grid(self):

        initial_point = 0

        for i in range(28):
            self.gridpoints_x[i,0] = int(initial_point)
            self.gridpoints_x[i,1] = int(self.x_dimention/28 * (i+1))
        
            self.gridpoints_y[i,0] = int(initial_point)
            self.gridpoints_y[i,1] = int(self.x_dimention/28 * (i+1))

            initial_point = self.gridpoints_x[i,1]

    def draw_grid(self, color):
        for i in range(28):
            self.canvas.create_line(self.gridpoints_x[i,0], 0, self.gridpoints_x[i,0], self.y_dimention,fill= color)
            self.canvas.create_line(0, self.gridpoints_y[i,0], self.x_dimention, self.gridpoints_y[i,0], fill = color)

    def plot_grid(self, x, y, width, aa, live):

        if width == 0:
            xs_canvasScale = self.gridpoints_x[x,0]
            xe_canvasScale = self.gridpoints_x[x,1] 
            ys_canvasScale = self.gridpoints_y[y,0]
            ye_canvasScale = self.gridpoints_y[y,1]
            self.canvas.create_rectangle(xs_canvasScale,ys_canvasScale,xe_canvasScale,ye_canvasScale, fill = '#eeeeee')
            self.gridpoints_master[x,y] = 255

        else:
            for i in range(-width, width):
                if (x + i < 28 and x + i > -1):

                    xs_canvasScale = self.gridpoints_x[x+i,0]
                    xe_canvasScale = self.gridpoints_x[x+i,1]

                    for j in range(-width, width):
                        
                        if (y + j < 28 and y + j > -1):
                            ys_canvasScale = self.gridpoints_y[y+j,0]
                            ye_canvasScale = self.gridpoints_y[y+j,1]
                            self.canvas.create_rectangle(xs_canvasScale,ys_canvasScale,xe_canvasScale
                                    ,ye_canvasScale, fill = '#eeeeee')
                            self.gridpoints_master[x+i,y+j] = 1.00
        if aa:
            for ix in range(1,28):
                for iy in range(1,28):
                    direction = self.gridpoints_master[ix,iy] - self.gridpoints_master[ix - 1, iy -1]

                    if abs(direction) > 245:

                        if direction < 0:
                            if ix + 1 < 28 and iy + 1 < 28:
                                avg = (self.gridpoints_master[ix + 1,iy -1] +self.gridpoints_master[ix + 1,iy + 1] + 
                                self.gridpoints_master[ix-1,iy-1] + self.gridpoints_master[ix-1,iy+1] + 200 )//4 
                                s = hex(avg)

                                if s[0] == "-":
                                    s = s[2:] + "0"
                                self.canvas.create_rectangle(self.gridpoints_x[ix,0], self.gridpoints_y[iy,0],
                                        self.gridpoints_y[ix, 1], self.gridpoints_y[iy,1], fill = ('#' + s[2:]*3))

                                self.gridpoints_master[ix,iy] = (avg/255.0 * 0.99) + 0.01         
         
                        if direction > 0:
                            if ix + 1 < 28 and iy + 1 < 28:
                                avg = (self.gridpoints_master[ix ,iy -1] +self.gridpoints_master[ix,iy + 1] + 
                                self.gridpoints_master[ix-2,iy-1] + self.gridpoints_master[ix-2,iy+1]+200)//4 

                                s = hex(avg)
                                if s[0] == "-":
                                    s = s[2:] + "0"
                                
                                self.canvas.create_rectangle(self.gridpoints_x[ix - 1,0], self.gridpoints_y[iy - 1, 0],
                                    self.gridpoints_y[ix - 1, 1], self.gridpoints_y[iy - 1,1], fill =  ('#' + s[2:]*3))

                                self.gridpoints_master[ix - 1 ,iy - 1] = (avg/255.0 * 0.99) + 0.01        
                            
    def deleteGridPoints(self):
        for x in range(28):
            for y in range(28):

                self.gridpoints_master[x,y] = 0

        self.canvas.delete('all')
        self.draw_grid("#1c1c1c")

        print("\n",self.gridpoints_master)



class ml_ui:

    def __init__(self, title, x_dimention, y_dimention, c_bg, c_grid):
        self.title = title
        self.x_dimention = x_dimention
        self.y_dimention = y_dimention
        self.bg          = c_bg
        self.gridColor   = c_grid
        self.window      = Tk()
        self.canvas_x     = 350
        self.canvas_y     = 350
        self.canvas_frame = Frame(self.window, bg = self.bg)
        self.canvas      = Canvas(self.canvas_frame,width = self.canvas_x ,height = self.canvas_y, bg = self.bg)
        self.g           = grid28x28(self.canvas_x, self.canvas_y, self.canvas)
        
    def start(self):

        self.window.title(self.title)
        self.window.geometry(str(self.x_dimention) +"x"+str(self.y_dimention))
        self.window.rowconfigure(0 , weight = 1)
        self.window.columnconfigure(0, weight = 1)

        #self.canvas.grid(row = 0, column = 0,sticky = 'nsew') 
        self.canvas_frame.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.canvas.grid(row = 0, column = 0,sticky = N) 
        self.canvas.bind('<Button-1>',self.locate_xy)
        self.canvas.bind('<B1-Motion>',self.addLine)
        self.canvas.config(cursor = 'dot', bd = 1, highlightthickness = 2, highlightbackground = "#323232")

        self.g.populate_grid()
        self.g.draw_grid(self.gridColor)
        
        self.window.mainloop()


    def locate_xy(self, event):
        current_x,current_y = event.x,event.y
        i_current_x = int(current_x/self.canvas_x * 28)
        i_current_y = int(current_y/self.canvas_y * 28)


    def addLine(self, event):
        current_x = event.x
        current_y = event.y
        i_current_x = int(current_x/self.canvas_x * 28)
        i_current_y = int(current_y/self.canvas_y * 28)
        self.g.plot_grid(i_current_x, i_current_y, 1 , True, True)

