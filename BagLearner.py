#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np 			  		 			     			  	   		   	  			  	

class BagLearner():

    def __init__(self, learner, kwargs, bags = 20, boost = False, verbose = False):
        self.bags = bags
        self.verbose = verbose;
        self.learners = self.set_learners(kwargs, learner, bags)

    def author(self):
        return 'agizatulina3'
    
    def set_learners(self, kwargs, learner, bags):
        learners = []

        for i in range(0,bags):
            learners.append(learner(**kwargs))
        return learners;
    
    def get_samples(self, size):
        return np.random.choice(size, size, replace=True)
    
    def addEvidence(self, dataX, dataY):
        i = 0

        for learner in self.learners:
            i = i + 1
            indexes = self.get_samples(dataX.shape[0])
            # debug
            if self.verbose: 
                print i
                print learner
                print dataX[indexes]
                
            learner.addEvidence(dataX[indexes], dataY[indexes])


    def query(self,Xtest):
        results = [];

        for learner in self.learners:
            results.append(learner.query(Xtest)) 
            
        return np.mean(np.asarray(results, dtype=np.float32), axis=0)
    
    