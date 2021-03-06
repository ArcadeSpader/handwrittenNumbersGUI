import numpy as np
import scipy.special

class neuralNetwork():

    def __init__(self, inputnodes, outputnodes, hiddennodes, learningrate):

        self.inodes = inputnodes
        self.onodes = outputnodes
        self.hnodes = hiddennodes
        self.lr     = learningrate

        self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))
        
        self.activationfunction = lambda x: scipy.special.expit(x)


    def train(self, input_list, target_list):

        inputs = np.array(input_list, ndmin = 2).T
        targets = np.array(target_list, ndmin = 2).T

        hiddeninputs = np.dot(self.wih, inputs)
        hiddenoutputs = self.activationfunction(hiddeninputs)

        finalinputs = np.dot(self.who, hiddenoutputs)
        finaloutputs = self.activationfunction(finalinputs)
       
        output_errors = targets - finaloutputs
        
        hidden_errors = np.dot(self.who.T, output_errors)

        self.who += self.lr * np.dot((output_errors * finaloutputs * 
            (1 - finaloutputs)), np.transpose(hiddenoutputs))

        self.wih += self.lr * np.dot((hidden_errors * hiddenoutputs * 
            (1 - hiddenoutputs)), np.transpose(inputs))


    def query(self, input_list):

        inputs = np.array(input_list, ndmin = 2).T

        hiddeninputs = np.dot(self.wih, inputs)
        hiddenoutputs = self.activationfunction(hiddeninputs)

        finalinputs = np.dot(self.who, hiddenoutputs)
        finaloutputs = self.activationfunction(finalinputs)


        return finaloutputs;


