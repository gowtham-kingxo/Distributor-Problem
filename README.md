# Distributor Problem 

The problem statement can be viewed [here](https://github.com/realimage/challenge2016).

- [Requirements](#Requirements) 
- [Program Execution](#Program-Execution?)
- [Project Structure](#Project-Structure)
- [Operations Supported](#Operations-Supported)
- [Input Format](#Input-Format) 
- [Output Format](#Output-Format)
- [Algorithm](#Algorithm)
- [Algorithm Analysis](#Algorithm-Analysis) 

## **Requirements**

- python 3.5 or above

    If you don't have python 3 in your system, you can download and install it from [here](https://www.python.org/downloads/)
- termcolor (python module)
    
    It is used to get the output in colored text for easy understanding. If you don;t have termcolor in your system's python modules, you can install it with the help of this command `pip install termcolor`


## **Program Execution**
The entry point for running this application is app.py. Enter the following python command on the terminal after navigating to the /src directory from the parent directory.

` 
python app.py
`


## **Project Structure**
The project files are laid out in a straightforward manner as there are only few program files. 

    -- Distributor Problem
        -- src
            -- app.py
            -- Tree.py
            -- Utility.py
        -- input.txt
        -- README.md
        -- sampleInput.pdf 
        -- Dataset
            -- cities.csv 
        -- Screenshots
            -- output1.png
            -- output2.png
            -- output3.png

### app.py
It contains the core logic of the distributor Problem. This program contains three classes in it. The classes are as follows:

- Distributor 
- Permission 
- Application

### Tree.py
It is a supporting file serving the implementation of Binary Search Tree(BST) and World Tree. The classes in this file are as follows:

- BinarySearchTree
- WorldTree

### Utility.py
As the name of the program suggests, this file provides utility functions such as processing the permission, reading the csv file and input file and displaying error messages. The classes available in this file are as follows:

- FileReader
- Message
- InputFormatter

### input.txt
The input to the program is given through this file. Read the [Input Format](#Input-Format)

### cities.csv

This csv file located in the Dataset directory has made best efforts in recording almost all the places in the world. If you find to see some places missing you are encouraged to add the place in this csv file. 

### Screenshots
This directory contains the output screenshots. If you wish, you can add yours as well. 


### README.md 
Lol, you are reading me :) At times, self-introduction is great! So, I don't want to take any excuses. I serve as your friend by helping you in the following ways: 

 - Understanding the Project 
 - Running the program
 - Giving input to the program
 


## **Operations Supported**

The program supports two operations as follows: 

        - Adding Permission
        - Checking whether a Distributor has access to a particular region

## **Input Format** 

I have chosen to give the input to the program through a text file called `input.txt` for the ease of interaction. But, along with it, there comes some rules. The rules are as follows: 

- The syntax of adding/checking permission should be strictly followed, which can be viewed in the sampleInput.pdf file 

- Permission commands should be given only after `###Permissions`

- No blank lines should be left after `###Permissions/###CHECK PERMISSIONS`. The commands should follow immediately after that line.

- A blank line should be left in between a set of permission commands for each distributor.
    
    Example

    ``` 
    PERMISSIONS FOR D1
    INCLUDE: INDIA

    PERMISSIONS FOR D2 < D1
    INCLUDE: TAMILNADU-INDIA
    EXCLUDE: CHENNAI-TAMILNADU-INDIA
    ```  

- Don't leave space in between the name of a place like `TAMIL NADU`, instead give it like this `TAMILNADU`. 

- EXCLUDE commands should always follow only after the INCLUDE commands in setting the permission for a distributor. 

    Example
    ```
    PERMISSIONS FOR D4
    INCLUDE: INDIA
    INCLUDE: KARNATAKA-INDIA
    EXCLUDE: KANCHIPURAM-TAMILNADU-INDIA
    ```   

- Check commands should be given only after the `###CHECK PERMISSIONS`

- Blank lines should not be left between two subsequent check commands 

    Example 

    ```
    ### CHECK PERMISSIONS
    D1 INDIA
    D2 CHENNAI-TAMILNADU-INDIA
    ```

**NOTE**: If you accidentally collapse the input.txt file, sampleInput.pdf file will save you by getting you back to the track. 

**NOTE TO THE PROBLEM SETTER**: 
    
I have made some changes to the input format, which are  as follows: 

- In the problem statement, some of the words in the input are given in lowercase like `Permissions for Distributor1` which I have changed to `PERMISSIONS FOR DISTIBUTOR1`. I have made this change just to keep the typing at ease, instead of tapping the caps lock button often to switch cases. 

- Simplified the command `PERMISSIONS D3 < D2 < D1` to `PERMISSIONS D3 < D2`, as my program understands that D2 is a subset of D1 from the previous commands.


## **Output Format**

Output will be displayed in the terminal along with the input, when app.py is excuted. 

## **Algorithm**
Yet to write .....


## **Algorithm Analysis**

This section will talk about few areas of the algorithm which dominates the space and running time of the program. 

### **World Tree**
This tree provides the implementation for holding the places of the world in a tree data structure. 

**Properties**

- Technically, it's a n-array Tree. 
- The height of the tree is always 3. 

**Trade-offs**

- The node structure is as follows:

    ```
    startID: Integer
    endID: Integer
    children: Dictionary()
    ```

    **Argument**: `children` can be made List(), but it dominates the running-time in finding out the desired node. To put it in numbers, there are 195 countries in the world, so in the worst-case, it will take 195 iterations to find out the desired country node. Likewise, the same can be applied down the hierarchy for cities in a province. I preferred to relax the space and give way for better running-time. My opinion can be reversed based on the requirement of the application. 



**Analysis**

**Space Complexity - O(n)**, where n is the number of places recorded in cities.csv file. 

**Time Complexity - O(1)**, traversing the tree in both depth-wise and breadth-wise is constant, because the depth of the tree is constant(height of the tree is 3) and traversing breadth-wise is also constant due to the nature of Dictionary(), which return the value of a key in O(1). 

**Time Complexity for creating a tree is O(n)**, due to the constraints of the problem statement, which says not to use a database, we had to create the World Tree every time we run the program. 

### **Binary Search Tree**

The INCLUDE/EXCLUDE permissions for a distributor is stored in BST for a reason. 

**Trade-off**

- INCLUDE/EXCLUDE permissions for a distributor can be stored in the list, which is as simple as it is. But the real pain comes when a Distributor X assigns permissions to Distributor Y, because before adding the permissions to Distributor Y's permission list, we had to check the permission list of X, which takes O(n) time, where n is the number of permissions of Distributor X. 

- As the algorithm gives ID for every place, we can take advantage of that and store the permissions in a Binary Search Tree by following its property strictly. So that we can check whether the permission can be added to Y or not by checking the Distributor X's permission in O(log n) time. 

    **Argument**:
    The same running time of O(log n) can be achieved by storing it in the list itself and doing a binary search. But, binary search requires the list to be sorted, as there is no guarentee that the permissions will be added in a sorted order. But, it can be achieved by sorting the list in O(n logn) time after adding the permissions. So the running-time complexity will be O(n logn) + O(logn) = O(n logn). Hence, I chose to use BST, which will not introduce an additional cost of O(n logn) for sorting instead, it uses some overhead space for storing left and right child which can be saved when using list. 
    
    Again, I leave this argument open, because I can't claim which one is the best without knowing the exact requirements and resources of the application.

**Analysis**

**Time Complexity**
- Insertion - O(logn)
- Search = O(log n)

**Space Complexity - O(n)**

Say, k INCLUDE permissions are needed to be assigned to Distributor Y by Distributor X, then it will take O(k logn) time for this operation, where k is the number of permissions to be added to X's permission list and n is the number of INCLUDE permissions of X.  




