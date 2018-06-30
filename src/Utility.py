"""
"""
import re
import csv


class FileReader:
    def readCSVFile(self, path):
        places = []
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',',)
            flag = True 

            for place in reader:
                if(flag):
                    flag = False 
                    continue
                places.append([place[-1], place[-2], place[-3]])

        return places


    def readTxtFile(self):
        lines = list()
        
        with open('./../input.txt', newline = None) as inputFile:
            for line in inputFile:
                if('\n' in line):
                    line = line[: len(line)-1]          
                lines.append(line) 
                print(line)  
        return lines



class Message:
    def invalidPlaceError(self, place):
        print("Error: {} is not present in the cities.csv file. I only know what's in the cities.csv file located in the Dataset Directory. I will become Jarvis one day :sunglasses:".format(place))
        print("Possible mistakes: \n\t1. Typo\n\t2. Invalid Location\n\t3. Place not recorded in the cities.csv file")
        print("Try to figure out the mistake and run me again.")
        exit(0)
    
    def permissionSyntaxError(self, line):
        print("Error: Invalid syntax - {}".format(line))
        print("Description: I will strongly recommend you to have a look at the README.md")
        exit(0)


    def excludeWarning(self, line, distributorName):
        print("Warning: {}".format(line))
        print("Description: {}'s EXCLUDE permission doesn't work, as this region or superset of this region is not included in the first place :(".format(distributorName))


    def includeWarning(self, line, distributorName):
        print("Warning: {}".format(line))
        print("Description: {} can't include this region".format(distributorName)) 


    def includeExcludeSuccess(self, line, distributorName):
        print("{} included to {}'s permission list".format(line, distributorName))
          
                

class InputFormatter: 
    def __init__(self):
        self.error = Message()
        self.firstLineFormat = re.compile(r'PERMISSIONS FOR (.*)( < .*)?')
        self.permissionLineFormat = re.compile(r'(INCLUDE|EXCLUDE): (.*)(-.*-.*)?')
    

    def getPermissionType(self, line):
        permissionType = "Direct"
        dist1 = dist2 = ""
        
        if(' < ' in line):
            permissionType = "Inherit"
            result = line.split(' < ')
            dist1, dist2 = result[0], result[1]
        else:
            dist1 = line
        
        return dist1, dist2, permissionType


    def processPermissionFirstLine(self, line):
        permissionFistLineInput = self.firstLineFormat.findall(line)
        
        if(len(permissionFistLineInput) == 0):
            self.error.permissionSyntaxError(line)
            
        dist1, dist2, permissionType = self.getPermissionType(permissionFistLineInput[0][0])
        return(dist1, dist2, permissionType)


    def processPermission(self, permission):
        result = self.permissionLineFormat.findall(permission)
        
        if(len(result) != 0):
            return result[0][0], result[0][1]
        
        self.error.permissionSyntaxError(permission)
           

# fileReader = FileReader()
# print(fileReader.readTxtFile())