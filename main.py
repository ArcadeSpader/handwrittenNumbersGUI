import window
import numpy
import ml
from tkinter import *
from tkinter import messagebox

w = window.ml_ui("HandWriting", 530, 430, "#121212","#1c1c1c") 
querydata = 0

v = IntVar()
learningrate = DoubleVar()
n_hiddenlayer = IntVar()

v.set(0)
learningrate.set(0.1)
n_hiddenlayer = 250

mnist_training_path = "mnist_datasheet/mnist_train_100.csv"

class GUI():
    
    def __init__(self):
        self.options_frame = LabelFrame(w.window, text = "Options", padx = 10, pady = 10, relief = FLAT)
        self.hiddenLabel   = Label(self.options_frame, text = "Hidden Nodes:")
        self.learningLabel   = Label(self.options_frame, text = "Learning Rate:")
        self.hiddenLayer_sc= Scale(self.options_frame, from_ = 100, 
                to = 300,bd = 0, 
                orient = HORIZONTAL, 
                sliderrelief = FLAT, 
                variable = n_hiddenlayer,
                highlightthickness = 0)
        self.learningrate_sc = Scale(self.options_frame, from_ = 0.1, 
                to = 1.0,bd = 0, 
                orient = HORIZONTAL, 
                sliderrelief = FLAT, 
                resolution = 0.01,
                variable = learningrate,
                highlightthickness = 0)

        self.weight_label    = Label(self.options_frame, text = "Weight:")
        self.randomize_weight = Button(self.options_frame, text = "Randomize??", width = 10)
        self.save_btn   = Button(self.options_frame, text = "Save Data", width = 10)
        
        self.toolbar_frame = Frame(w.window, width = 500 )
        self.train_btn     = Button(self.options_frame, text = "Train", width = 10, command = self.train)
        self.start_btn     = Button(self.toolbar_frame, text = "Test", height = 2, width = 10, command = self.train)

        self.open_btn   = Button(self.toolbar_frame, text = "Load\nDatabase", width = 10, height = 2, command = self.open)
        self.clear_btn  = Button(self.toolbar_frame, text = "Clear",width = 10, height = 2, command = w.g.deleteGridPoints)
        self.prepare_btn    = Button(self.toolbar_frame, text = "Prepare", width = 10, height = 2, command = self.getPoints)

        self.open_label    = Label(self.options_frame, text = "Database Type:")
        self.correct_label    = Label(self.options_frame, text = "Correctness:")
        self.option_mnist = Radiobutton(self.options_frame,
                                        text = "MNIST",
                                        value = 0,
                                        relief = FLAT,
                                        variable = v)

        self.option_self = Radiobutton(self.options_frame,
                                        text = "Self",
                                        relief = FLAT,
                                        value = 1,
                                        variable = v)

        self.check_entry = Entry(self.options_frame, width = 5)

        self.display_label = Label(w.canvas_frame, text = "Press Test to get results")

    def start(self):

        self.setTheme()

        self.options_frame.grid(row = 0, column = 1,padx = 5, sticky = NE, rowspan = 50)
        self.toolbar_frame.grid(row = 2, column = 0, sticky = W)
        self.hiddenLabel.grid(row = 3, column = 0, sticky = "W")
        self.learningLabel.grid(row = 6, column = 0, sticky = "W")
        self.start_btn.grid(row = 0, column = 3)
        self.hiddenLayer_sc.grid(row = 5, column = 0, pady = 5)
        self.learningrate_sc.grid(row = 7, column = 0, pady = 2)
        self.weight_label.grid(row = 8, column = 0, sticky = "W")
        self.randomize_weight.grid(row =9, column = 0, pady = 10)
        self.open_label.grid(row = 10, column = 0, sticky = "W")
        self.open_btn.grid(row = 0,column = 0)
        self.option_mnist.grid(row = 11, column = 0, sticky = "W")
        self.option_self.grid(row = 12, column = 0, sticky = "W")
        self.train_btn.grid(row = 13, column = 0)
        self.correct_label.grid(row = 14, column = 0, sticky = "W")
        self.check_entry.grid(row = 15, column = 0, pady = 10)
        self.save_btn.grid(row = 16, column = 0)
        self.display_label.grid(row = 5, column = 0)
        self.prepare_btn.grid(row = 0, column = 1)
        self.clear_btn.grid(row = 0, column = 2)
    
    def setTheme(self):
        w.window.config(bg = '#111111')
        self.options_frame.config(bg = '#1d1d1d', fg = "#d3d3d3")
        self.toolbar_frame.config(bg = '#1d1d1d')
        self.clear_btn.config(bg = '#202020', fg = "#d3d3d3")
        self.prepare_btn.config(bg = '#202020', fg = "#d3d3d3")
        self.save_btn.config(bg = '#202020', fg = "#d3d3d3")
        self.start_btn.config(bg = '#202020', fg = "#d3d3d3")
        self.train_btn.config(bg = '#202020', fg = "#d3d3d3")
        self.open_btn.config(bg = '#202020', fg = "#d3d3d3")
        self.randomize_weight.config(bg = '#202020', fg = "#d3d3d3")
        self.hiddenLabel.config(bg = '#202020', fg = "#d3d3d3")
        self.learningLabel.config(bg = '#202020', fg = "#d3d3d3")
        self.weight_label.config(bg = '#202020', fg = "#d3d3d3")
        self.open_label.config(bg = '#202020', fg = "#d3d3d3")
        self.correct_label.config(bg = '#202020', fg = "#d3d3d3")
        self.display_label.config(bg = '#151515', fg = "#d3d3d3")


        self.hiddenLayer_sc.config(bg = '#111111', fg = "#d3d3d3",troughcolor = "#202020", activebackground = "#73b5fa")
        self.learningrate_sc.config(bg = '#111111', fg = "#d3d3d3",troughcolor = "#202020", activebackground = "#73b5fa")
        
        self.option_mnist.config(bg = '#202020', fg = "#d3d3d3", 
                activeforeground = "#d3d3d3", 
                activebackground = "#202020",
                highlightcolor = "#d3d3d3",
                highlightbackground = "#202020",
                selectcolor = "#202020")

        self.option_self.config(bg = '#202020', fg = "#d3d3d3", 
                activeforeground = "#d3d3d3", 
                activebackground = "#202020",
                highlightcolor = "#d3d3d3",
                highlightbackground = "#73b5fa",
                selectcolor = "#202020")

        self.check_entry.config(bg = '#202020', fg = "#d3d3d3")

    def getPoints(self):
        grid = w.g.gridpoints_master
        print ("\n", grid)

    def train(self):

        global network = ml.neuralNetwork(784, 10, n_hiddenlayer, self.learningrate_sc.get())

        trainingdatafile = open(mnist_training_path, "r")
        trainingdatalist = trainingdatafile.readlines()
        trainingdatafile.close()

        for record in trainingdatalist:
            all_values = record.split(',')
            inputs = (numpy.asfarray(all_values[1:])/255.0 * 0.99) + 0.01
            targets = numpy.zeros(10)+ 0.01
            targets[int(all_values[0])] = 0.99
            network.train(inputs, targets)

        
        messagebox.showinfo(title = "Training Finished!", message = v.get())


    def query(self):


        self.display_label.config(text = "It is probably a " + str(querydata))

    def open(self):
        messagebox.showinfo(title = "Info", message = v.get())


def main():
    gui = GUI()

    gui.start()
    w.start()

    return

if __name__=='__main__':
    main()
