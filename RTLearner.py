#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 14:48:41 2019

@author: a
"""

# =============================================================================
# import RTLearner as rt
# learner = rt.RTLearner(leaf_size = 1, verbose = False) # constructor
# learner.addEvidence(Xtrain, Ytrain) # training step
# Y = learner.query(Xtest) # query
# =============================================================================


import numpy as np 			  		 			     			  	   		   	  			  	

class RTLearner(object):
    leaf = -1

    def __init__(self, leaf_size = 1, verbose = False): 		
        self.verbose = verbose
        self.leaf_size = leaf_size	  		 			     			  	   		   	  			  	
        pass # move along, these aren't the drones you're looking for 			  		 			     			  	   		   	  			  	
   			  		 			     			  	   		   	  			  	
    def author(self): 			  		 			     			  	   		   	  			  	
        return 'agizatulina3' 			  		 			     			  	   		   	  			  	
   		
    def find_rand(self, X):
        return np.random.randint(X.shape[1])
            
    def find_split_value(self, col):
        return np.median(col)
    
    def build_tree(self, data):
        dataX = data[:,: -1]
        Y = data[:, -1]
        
        if dataX.shape[0] <= self.leaf_size:
            return np.array([[self.leaf, Y.mean(), np.nan, np.nan]])
        if np.unique(Y).size == 1:
            return np.array([[self.leaf, Y[0], np.nan, np.nan]])
        else:
            index = self.find_rand(dataX)
            split = self.find_split_value(dataX[:, index])
            
            rightData = data[data[:, index] > split]
            leftData = data[data[:,index] <= split]

            if (rightData).shape[0] == 0 or (leftData).shape[0] == 0:
                return np.array([[self.leaf, Y.mean(), np.nan, np.nan]])
            
            leftTree = self.build_tree(leftData)
            rightTree = self.build_tree(rightData)
    
            root = np.array([[index, split, 1, leftTree.shape[0] + 1]])
            return np.vstack([root, leftTree, rightTree])

    def addEvidence(self, dataX, dataY):
         self.tree = self.build_tree(np.column_stack([dataX, dataY]))

    def query(self, Xtest):
        result = []
        
        for row in Xtest:
            i = 0
            b = 0
            while (b != self.leaf):
                b = int(self.tree[i][0])
                split = self.tree[i][1]

                if (b != self.leaf):
                    # go to the left 
                    if (row[b] <= split):
                        i = int(i + self.tree[i][2])
                    # go to the right
                    else:
                        i = int(i + self.tree[i][3])
            
            result = np.append(result, split)
        return result
    

