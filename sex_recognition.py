from __future__ import division
from scipy import *
import numpy as np
import os
import wave
import copy
import random
import sys

def analyze(file):

    audioFile = wave.open(file, 'r')
    signal = audioFile.readframes(-1)
    signal = fromstring(signal, 'Int16')
    fps = audioFile.getframerate()
    fragments = []
    FFTs = []
    globalAvgDistance = 0.0
    count = 0.0

    for i in range(1, len(signal)-10001, 10000): #signal fragmentation with strangth indication
        sum = 0
        for j in signal[i:i+10000]:
            if j > 0:
                sum += j
        if sum > 0:
            fragments.extend([[sum, signal[i:i+10000]]])

    fragments.sort(reverse=True) #loudest-first sorting

    for i in range(5): #for 5 loudest fragments
        if i < len(fragments): #if present
            FFTnew = []
            FFTs.append(fft(fragments[i][1])) #calculate FFTs
            FFTs[i] = abs(FFTs[i])
            FFTavg = np.mean(FFTs[i][:(400.0/fps) * 10000])*1.6 #(avg signal strength for 0-400Hz)*1.6
            for ind, val in enumerate(FFTs[i][:(400.0/fps)*10000]): #remove peaks under FFTavg
                if val < FFTavg:
                    FFTnew.append(0)
                else:
                    FFTnew.append(val)

            maxes = []
            for i in range(0, len(FFTnew)): #looking for local maximums
                if i+6<len(FFTnew):
                    if FFTnew[i]<FFTnew[i+1] and FFTnew[i+1]>FFTnew[i+2]:
                        maxes.append(i+1)

            maxesNew = copy.copy(maxes) #removing doubled maximums
            for i in range(len(maxes)-1):
                if maxes[i+1]-maxes[i]<9:
                    maxesNew.remove(maxes[i+1])

            avgDistance=0.0
            if (len(maxesNew) > 1): #calculating average distances between harmonics for the fragment
                count += 1
                for i in range(len(maxesNew)-1):
                    avgDistance += maxesNew[i+1]-maxesNew[i]
                avgDistance /= float(len(maxesNew)-1)
                globalAvgDistance += avgDistance

    if count > 0:
        globalAvgDistance /= float(count) #calculating average distances between harmonics for all fragments
    else:
        globalAvgDistance = random.uniform(10, 40)

    if globalAvgDistance < 25.5: #decision
        print "M"
    else:
        print "F"

analyze(sys.argv[1])