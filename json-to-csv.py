import json
import csv
from os import listdir
from os.path import isfile, join
import Tkinter as tk
import sys



def json_to_csv(directory="json/", destination=""):
    #directory = "json/"
    #double-check that the directory ends in a '/' for filereading purposes
    if directory[-1] != "/":
        directory += "/"

    #read in all the files from the directory
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    filepaths = []
    data = []
    for f in files:
        if f[-5:] == ".json":
            filepaths += [directory + f]
        else:
            print "File " + f + " isn't a json file! It won't be included."

    #add all the data and filenames (for saving purposes) to one list
    for f in filepaths:
        print f
        jsonfile = open(f)
        data += [json.load(jsonfile), f]

    #For each file
    for d in data:
        d_keys = d.keys()
        headers = []
        for x in xrange(0,len(d[d_keys[0]])):
            headers += [d[d_keys[0]][x].keys()]

        headers = [item for sublist in headers for item in sublist]
        headers = list(set(headers))

        csvfile = open('csv/aggregate_data.csv', 'wb')
        aggregatewriter = csv.DictWriter(csvfile, headers)
        aggregatewriter.writeheader()

        for data_key in d_keys:
            #for each subject
            curr_data = d[data_key]
            subjectfile = open("csv/" + str(data_key) + '.csv', 'wb')
            subjectwriter = csv.DictWriter(subjectfile, headers)
            subjectwriter.writeheader()
            for trial in curr_data:
                rowDict = {}
                for trial_key in trial.keys():
                    rowDict[trial_key] = trial[trial_key]
                subjectwriter.writerow(rowDict)
                aggregatewriter.writerow(rowDict)
            subjectfile.close()




        csvfile.close()
        return



#Makes it so the function can be run from the terminal, but can be imported to other files
if __name__ == "__main__":
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    json_to_csv()
