from Tree import BinarySearchTree, WorldTree
from Utility import FileReader, InputFormatter, Message
import re 


class Distributor: 
    def __init__(self, distributorName):
        self.distributorName = distributorName
        self.includes = BinarySearchTree() 
        self.excludes = [BinarySearchTree()]


    def addIncludePermission(self, startID, endID, parentDistributorNode):
        if(parentDistributorNode == None):
            self.includes.insertNode(self.includes.root ,startID, endID)
        else:
            isPresentInParentInclude = parentDistributorNode.includes.isInRange(parentDistributorNode.includes.root, startID, endID)
            isPresentInParentExclude = self.checkExcludes(parentDistributorNode, startID, endID)

            if(isPresentInParentInclude and not(isPresentInParentExclude)):
                self.includes.insertNode(self.includes.root, startID, endID)
            elif(isPresentInParentExclude):
                return 0 
        return 1


    def checkExcludes(self, node, startID, endID):
        for i in range(len(node.excludes)):
            isPresent = node.excludes[i].isInRange(node.excludes[i].root,startID, endID)
            if(isPresent):
                return isPresent
        return False 


    def addExcludePermission(self, startID, endID):
        isPresent = self.includes.isInRange(self.includes.root, startID, endID)
        if(isPresent):
            self.excludes[0].insertNode(self.excludes[0].root, startID, endID)
            return 1
        else:
            return 0



class Permission:
    def __init__(self):
        self.inputFormatter = InputFormatter()
        self.worldTree = WorldTree()
        self.message = Message()


    def findIDValue(self, place): 
        place = place.split('-')
        place = place[::-1]
        return self.worldTree.getID(place) 


    def checkPermission(self, lines, startIndex, endIndex, distributors):
        for i in range(startIndex, endIndex + 1):
            currentLine = lines[i].split(' ')
            distributorName, place = currentLine[0], currentLine[1]

            if(distributorName not in distributors):
                print("Permission for {} is not set up".format(distributorName))
                exit(0)

            distributorNode = distributors[distributorName]
            startID, endID = self.findIDValue(place)
            isPresentInInclude = distributorNode.includes.isInRange(distributorNode.includes.root  ,startID, endID)
            isPresentInExclude = distributorNode.checkExcludes(distributorNode, startID, endID)

            if(isPresentInInclude and not(isPresentInExclude)):
                print("Yes, {} has permission to access this {} region".format(distributorNode.distributorName, place))
            else:
                print("No, {} doesn't have permission to access this {} region".format(distributorNode.distributorName, place))


    def addPermissions(self, lines, startIndex, distributorNode, parentDistributorNode):
        while(lines[startIndex] != ''):
            permission = lines[startIndex]
            permissionType, place = self.inputFormatter.processPermission(permission)
            place = place.strip()
            startID, endID = self.findIDValue(place)
            
            if(permissionType == "INCLUDE"):
                status = distributorNode.addIncludePermission(startID, endID, parentDistributorNode) 
                if(status):
                    self.message.includeExcludeSuccess(lines[startIndex], distributorNode.distributorName)
                else:
                    self.message.includeWarning(lines[startIndex], distributorNode.distributorName)
            
            if(permissionType == "EXCLUDE"):
                status = distributorNode.addExcludePermission(startID, endID)
                if(status):
                    print("{} excluded from {}'s permission list".format(lines[startIndex], distributorNode.distributorName))
                else:
                    self.message.excludeWarning(lines[startIndex], distributorNode.distributorName)
            
            startIndex += 1
        
        while(lines[startIndex] == ''):
            startIndex += 1 
        
        return startIndex - 1


    def processPermissions(self, lines, startIndex, endIndex, distributors):
        while(startIndex <= endIndex):
            dist1, dist2, permissionType = self.inputFormatter.processPermissionFirstLine(lines[startIndex])
            dist1 = dist1.strip()
            dist2 = dist2.strip()
            
            if(dist1 in distributors):
                self.message.duplicateDistributor(dist1)

            print("\nAdd Permissions for {}".format(dist1))
            
            if(dist1 == -1):
                self.message.permissionSyntaxError(lines[startIndex])
                exit(0) 
            
            distributorNode = Distributor(dist1)
            startIndex += 1

            if(permissionType == "Direct"):   
                distributors[dist1] = distributorNode
                parentDistributorNode = None 
                startIndex = self.addPermissions(lines, startIndex, distributorNode, parentDistributorNode)
                
            elif(permissionType == "Inherit"):
                if(dist2 not in distributors):
                    print("You are trying to assign permission from {} which is not yet set".format(dist2))
                    exit(0)

                distributors[dist1] = distributorNode
                parentDistributorNode = distributors[dist2]
                startIndex = self.addPermissions(lines, startIndex, distributorNode, parentDistributorNode)
                
                for i in range(len(parentDistributorNode.excludes)):
                    distributorNode.excludes.append(parentDistributorNode.excludes[i])
            
            startIndex += 1

            
            
class Application:
    def __init__(self):
        self.distributors = dict()
        self.fileReader = FileReader()
        self.permission = Permission()


    def runApplication(self):
        print("Note: If you are running this program for the first time, I will suggest you to read the README.md file once to know what all you can do with this program :)")
        print("================================INPUT================================")
        lines = self.fileReader.readTxtFile()
        checkPermissionIndex = lines.index("###CHECK PERMISSIONS")
        print("================================OUTPUT================================")
        
        print("\n\t\t\tADD PERMISSIONS")
        self.permission.processPermissions(lines, 1, checkPermissionIndex - 1, self.distributors)
        
        print("\n\n\t\t\tCHECK PERMISSIONS")
        self.permission.checkPermission(lines, checkPermissionIndex + 1, len(lines) - 1, self.distributors)    


app = Application()
app.runApplication()
