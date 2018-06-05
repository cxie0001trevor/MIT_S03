import random
import math
import sys, getopt
import ast
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SA():
    '''
    This SA algorithm is mainly based on the pseudocode provided
    in Russell S. & Norvig P. Page 126 "SIMULATED-ANNEALING"
    '''
    def __init__(self, task_name, temp, cool_rate, func, prt=False, args=None,):
        if task_name in ['a','b','c','d']:
            self.task = task_name
        else:
            raise ValueError('invalid user response')
        self.startT = temp
        self.temp = temp  # initial temperature
        self.cool_rate = cool_rate # cool down rate
        self.func = func # Math function
        if args:
            self.current_args = args
        else:
            self.current_args = None
        self.print = prt
        self.best = []
        #self.args_history = []
        #self.z_history = []
    
    def default_start(self):
        if self.task == 'a':
            self.current_args = [0,1,1,1]
        elif self.task == 'b':
            self.current_args = [0,0,1,1]
        elif self.task == 'c':
            self.current_args = [0,0,0,1]
        else:
            self.current_args = [0,0,0,0]
        #self.args_history.append(self.current_args)
        
    def RNG(self, lower_bound, upper_bound):
        # random generator for argument
        return round(random.uniform(lower_bound,upper_bound), 5)
    
    def random_start(self):
        uvw,y = [-1,1], [-1,0,1]
        if self.task == 'a': # u
            self.current_args = [self.RNG(uvw[0], uvw[1]),1,1,1]
        elif self.task == 'b': # u, v
            self.current_args = [self.RNG(uvw[0], uvw[1]),
                                self.RNG(uvw[0], uvw[1]),1,1]
        elif self.task == 'c': # u, v, w
            self.current_args = [self.RNG(uvw[0], uvw[1]),
                                self.RNG(uvw[0], uvw[1]),
                                self.RNG(uvw[0], uvw[1]),1]
        else:    
            self.current_args = [self.RNG(uvw[0], uvw[1]),
                                self.RNG(uvw[0], uvw[1]),
                                self.RNG(uvw[0], uvw[1]), random.randint(-1,1)]
        #self.args_history.append(self.current_args)
        
    def get_vars(self):
        uvw,y = [-1,1], [-1,0,1]
        if self.task == 'a': # u
            return [self.RNG(uvw[0], uvw[1]),1,1,1]
        elif self.task == 'b': # u, v
            return [self.RNG(uvw[0], uvw[1]), self.RNG(uvw[0], uvw[1]),1,1]
        elif self.task == 'c': # u, v, w
            return [self.RNG(uvw[0], uvw[1]), self.RNG(uvw[0], uvw[1]), self.RNG(uvw[0], uvw[1]),1]
        else:    
            return [self.RNG(uvw[0], uvw[1]), self.RNG(uvw[0], uvw[1]), self.RNG(uvw[0], uvw[1]), random.randint(-1,1)]
    
    def findMax(self, mode=None):
        if mode:
            if mode == 'd':
                #default start with 0
                self.default_start()
            elif mode == 'r':
                #random start
                self.random_start()
        else:
            if self.current_args==None:
                #no mode, if no user input, back to random start
                self.random_start()
                
        if self.best==[]:        
            _u,_v,_w,_y = self.current_args #load current var values
            current = self.func(_u,_v,_w,_y) #get current z value
        else:
            current = self.best[1]
            
        u,v,w,y = self.get_vars()
        neighbor = self.func(u,v,w,y)
        pr_natural = random.uniform(0, 1)
        dE = neighbor - current 
        pr_dE = math.e**(dE/self.temp)
        #print("pr_natural=" + str(pr_natural))
        #print("pr_dE=" + str(pr_dE))
        if dE >= 0 or pr_dE > pr_natural:
            self.current_args = [u,v,w,y]
            if self.best == []: #for first loop
                self.best = [[u,v,w,y], neighbor]
            elif self.best[1] <= neighbor: # store greater one
                if self.best != [[u,v,w,y], neighbor]:#check if they are different: new best occur
                    self.best = [[u,v,w,y], neighbor]
                    n = (np.log(self.temp/self.startT))/(np.log(self.cool_rate)) #calculate number of loop
                    if self.print:
                        print("| u: %.5f | v: %.5f | w: %.5f | y: %.5f |" % (u,v,w,y))
                        print("| Current: %.5f | Neighbor %.5f |" % (current, neighbor))
                        print("UPDATE: %.5f  @loop %d" % (self.best[1], n))
                        print('Temperature: %.2f' % self.temp)
                        print("------------------------------------------------------")
        self.temp = self.temp*self.cool_rate
        #self.z_history.append(self.best[1])
        #self.args_history.append(self.current_args)

def func(u, v, w, y):
    '''
    This function is for task 2a, 2b, 2c, 2d function: 
    As:
    2a: z(u)= u * sin(1/(0.01 + u**2)) + u**3 * sin(1/(0.001 + u**4))
    2b: z(u,v)= (u*v) * sin(v/(0.01 + u**2)) + u**3 * v**2 * sin((v**3)/(0.001 + u**4))
    2c: z(u,v,w)= (u*v**2 + sin(w*π)) * sin(v/(0.01 + u**2)) * sin(0.5*w*π) + 
                   u**3 * v**2 * w * sin((v**3)/(0.001*(sin(0.5*w*π))**2 + u**4 + (w-1)**2))
    2d: z(u,v,w,y)= y * ((u*v**2 + sin(w*π)) * sin(v/(0.01 + u**2)) * sin(0.5*w*π) + 
                   u**3 * v**2 * w * sin((v**3)/(0.001*(sin(0.5*w*π))**2 + u**4 + (w-1)**2)))
    Then, to combine into one:
    z(u,v,w,y)= y * (
                (u*v**2 + sin(w*π)) * sin(v/(0.01 + u**2)) * sin(0.5*w*π) + 
                u**3 * v**2 * w * sin((v**3)/(0.001*(sin(0.5*w*π))**2 + u**4 + (w-1)**2))
                )
    > If v, w, y are not specified: v, w, y = 1, 1, 1, this function 2a
    > If w, y are not specified: w, y = 1, 1, this function 2b
    > If y are not specified: y = 1, this function 2c
    > If all arguments are specified: this function become 2d
    
    Default values 1 have been assigned except u.
    '''
    pi = np.pi
    z = y * ((u*v**2 + np.sin(w*pi)) * np.sin(v/(0.01 + u**2)) * np.sin(0.5*w*pi) + 
                u**3 * v**2 * w * np.sin((v**3)/(0.001*(np.sin(0.5*w*pi))**2 + u**4 + (w-1)**2)))
    return z

def input_interpreter(argv):
    try:
        opts, args = getopt.getopt(argv,'q:i:t:c:',["mode=", "print=", "user="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
        
    global n_loop, temp, cool_rate,mode,task_name,prt,var_values
    
    for opt, arg in opts:
        
        # specify which question
        if opt == "-q":
            if arg in ['a','b','c','d']:
                task_name = arg
            else:
                raise ValueError("Warning: Only 'a', 'b', 'c', 'd' are accepted")
        
        #setting number of iteration
        if opt == "-i":
            try:
                n_loop = int(arg)
            except ValueError:
                print("Warning: Iteration Must Be Interger")
        
        #setting temperature
        if opt == "-t":
            try:
                temp = int(arg)
            except ValueError:
                print("Warning: Temperature Must Be Interger")
        
        #setting cool rate
        if opt == "-c":
            try:
                arg = float(arg)
                if 0<arg and arg<1:
                    cool_rate = arg
            except ValueError:
                print("Warning: Cool Rate Must Be numeric(0~1)")
                
        # random start or default start: if input error just use random start
        if opt == "--mode" and (arg in ['r','d']):
            mode = arg
            
        #print the process of finding or not
        if opt == "--print" and (arg.lower() in ['t','f']):
            if arg.lower() == 't':
                prt = True
            else:
                prt = False
                
        # user defined 
        if opt == "--user" and arg != '':
            try:
                var_values = [float(x) for x in ast.literal_eval(arg)]
                if len(var_values)!=4:
                    raise ValueError("Must have 4 input for u,v,w,y")
            except ValueError:
                print("Must be a list of all variables [u,v,w,y] ")

def main():
    global n_loop, temp, cool_rate, mode, task_name, prt, var_values, best 
    # prevent from mode='r' | 'd' , overlaping values of user specified
    if mode!=None:
        var_value = None 
    results = []
    for i in range(n_loop):
        test = SA(task_name, temp, cool_rate, func, prt, var_values)
        # random start
        if mode == 'r':
            test.get_vars()
        #
        if mode == 'd':
            test.default_start()
            
        while test.temp >1:
            test.findMax()
        results.append(test.best)
    best = max(results, key = lambda x : x[1])
    print(" Question 2%s Maximum found: %.5f" % (test.task, best[1]))
    u,v,w,y = best[0]
    print("| u: %.5f | v: %.5f | w: %.5f | y: %.5f |" % (u,v,w,y ))

# for plotting: Only support 2D,3D
def plot_ab():
    global task_name,best
    if task_name == 'a':
        u = np.arange(-1,1,0.01)
        z = u*np.sin(1/(0.01 + u**2)) + u**3 * np.sin(1/(0.001+u**4))
        plt.plot(u, z)
        u = best[0][0]
        best_z = u*np.sin(1/(0.01 + u**2)) + u**3 * np.sin(1/(0.001+u**4))
        plt.plot(u, best_z, marker='*', c='red', label='Maximum')
        plt.show()

    if task_name == 'b':   
        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        #input
        u = np.arange(-1,1,0.01)
        v = np.arange(-1,1,0.01)
        u,v = np.meshgrid(u,v)
        z = u*v**2*np.sin(v/(0.01 + u**2)) + u**3 * v**2 * np.sin((v**3)/(0.001+u**4))
        # set axis label
        ax.set_zlabel('Z')
        ax.set_ylabel('Y')
        ax.set_xlabel('X')
        #plot mesh
        ax.plot_surface(u,v,z, cmap=plt.cm.jet, rstride=1, cstride=1)
        #for path: need set best test object to access the history
        #u_list = []
        #v_list = []
        #z_list = []
        #for each in test.args_history:
        #    u_list.append(each[0])
        #    v_list.append(each[1])
        #for u,v in zip(u_list,v_list):
        #    z = u*v**2*np.sin(v/(0.01 + u**2)) + u**3 * v**2 * np.sin((v**3)/(0.001+u**4))
        #    z_list.append(z)
        #ax.scatter(u_list,v_list,z_list, marker='v', c='black', s=20, label='Path')
        
        #plot best spot
        U,V,W,Y = best[0]
        Z = np.array(best[1])
        ax.scatter(U,V,Z,marker='*', c='black', s=1500, label='Max')
        ax.view_init(35,150)
        plt.show()
        fig.savefig('2b_plot.png')
        
#default valuss for arguments
if __name__ == '__main__':
    n_loop = 10
    temp = 100 # No float accepted
    cool_rate = 0.95
    mode = None #random start
    task_name = 'a'
    prt = True
    var_values = None
    best = None
    # extract user input
    argv = sys.argv[1:]
    input_interpreter(argv)
    main()
    plot_ab()