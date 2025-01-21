# Python program to explain os.path.isfile() method
	
# importing os module
import os
	
# Path
path = 'D:/Pycharm projects/GeeksforGeeks/Nikhil/test_nikhil.txt'
	
# Check whether the
# specified path is
# an existing file
isFile = os.path.isfile(path)
print(isFile)
	
	
# Path
path = 'D:/Pycharm projects/GeeksforGeeks/Nikhil/'
	
# Check whether the
# specified path is
# an existing file
isFile = os.path.isfile(path)
print(isFile)
