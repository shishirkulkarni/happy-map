#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 21:30:44 2018

@author: gayatrigadre
Execution: python WordsPolarity.py <inputFile>

"""
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import os
import sys

def filter_stopwords(words_list):
    ''' Pre-processing step to remove unwanted words'''
    for word in words_list:
        if word in stopwords.words('english'):
            words_list.remove(word)
            
def get_scores(line,outputFile):
    ''' Use nltk library function to get scores per word'''
    words_list = tokenize.word_tokenize(line)
    filter_stopwords(words_list)
    sentimentAnalyzer = SentimentIntensityAnalyzer()

    for word in words_list:
        print(word)
        score = sentimentAnalyzer.polarity_scores(word)
        for k in sorted(score):
            # Omit words with 0.0 as score
            if score[k] != 0.0 and k=='compound':
                #print(word,'{0}: {1}, '.format(k, ss[k]))
                outputFile.write("\n"+word+"\t"'{0}'.format(score[k]))
    
def getOutputFileName(inputFile):
    ''' Get new output file name'''
    fname = sys.argv[1].split('.')
    fileName = fname[0]+"Output.txt"
    return fileName

def computePolarity(inputFileName):
    ''' Function to computer polarity of words and write to file '''
    with open(inputFileName,"r", encoding='ISO-8859-1') as file:
        try:
            if file.mode == 'r':
                outputFileName = getOutputFileName(inputFileName)
                outputFile = open(outputFileName,"w+")
                for line in file.readlines():
                    get_scores(line,outputFile)
                outputFile.close()
                print("Word score generated in",outputFileName,"file")
        except IOError: 
            print("File cannot be opened:",inputFileName)
    
        
# Read from a word count file
if __name__ == "__main__":
    if len(sys.argv)!=2:
         print("Input file not specified")
    else:
        inputFileName = sys.argv[1]
        print("Input File:",inputFileName)
        if os.path.exists(inputFileName):
            computePolarity(inputFileName)
        else:
            print("File not found:",inputFileName)