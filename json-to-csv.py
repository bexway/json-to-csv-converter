import json
import csv
from os import listdir
from os.path import isfile, join
import Tkinter as tk
import sys



def json_to_csv(directory="json/", destination=""):

    response = raw_input("Would you like to create an aggregate file containing all data?"+
        " This will only work if all of your data files have the same headers."+
        " (Enter 'y' for yes, and anything else for no.):")
    if response == "y":
        agg = True
    else:
        agg = False

    directory = raw_input("Please enter the path for the directory containing your json files."+
        " (Leave the input empty to look in the current directory.):")
    destination = raw_input("Please enter the path for the directory where the resulting csv files should be saved."+
        " (Leave the input empty to look in the current directory.):")

    #double-check that the directory ends in a '/' for filereading purposes
    if directory:
        if directory[-1] != "/":
            directory += "/"
    if destination:
        if destination[-1] != "/":
            destination += "/"

    #read in all the files from the directory
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    filepaths = []
    data_files = []
    for f in files:
        if f[-5:] == ".json":
            filepaths += [f]
        else:
            print "File " + f + " isn't a json file! It won't be included."

    #add all the data and filenames (for saving purposes) to one list
    for f in filepaths:
        jsonfile = open(directory + f)
        data_files.append({"data":json.load(jsonfile), "filename":f[:-5]})

    #Open a file for aggregate data, using headers from the first file
    if agg:
        agg_headers = data_files[0]["data"][0].keys()
        csvfile = open(destination + 'aggregate_data.csv', 'wb')
        aggregatewriter = csv.DictWriter(csvfile, agg_headers)
        aggregatewriter.writeheader()

    #For each file
    for d in data_files:
        data = d["data"]
        filename = d["filename"]
        headers = data[0].keys()

        subjectfile = open(destination + filename + '.csv', 'wb')
        subjectwriter = csv.DictWriter(subjectfile, headers)
        subjectwriter.writeheader()

        #for each row in the file's data
        for row in data:

            # for trial in curr_data:
            #     rowDict = {}
            #     for trial_key in trial.keys():
            #         rowDict[trial_key] = trial[trial_key]
            subjectwriter.writerow(row)
            if agg:
                aggregatewriter.writerow(row)
        #close the individual file before moving on
        subjectfile.close()



    if agg:
        csvfile.close()
    return



#Makes it so the function can be run from the terminal, but can be imported to other files
if __name__ == "__main__":
    json_to_csv()
