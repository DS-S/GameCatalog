"""
Main Program
Author: Dennis Santos-Sanchez
"""
import sqlalchemy
import sqlite3
import os

def new_catalog():
    path = input("Please enter the path to the directory where you would like the catalog to be stored\n"
                 "This includes the drive letter (e.g. C:\\user\\<user>\\Documents):")
    if(not os.path.exists(path)):
        print("Path does not exist, please enter existing path.")
        return None
    file = input("Please enter the catalog file name:")
    filepath = path + "\\" + file
    # create GameTable
    # create Genre Table
    # create Platforms Table

    return

def load_catalog():
    path = input("Please enter the path to the directory where the catalog is stored:")
    if not os.path.exists(path):
        print("Path does not exist, please enter existing path.")
        return None
    file = input("Please enter the catalog file name:")
    filepath = path + "\\" + file
    if not os.path.isfile(filepath):
        print("File does not exits in directory, please enter existing file.")
        return None

def main():
    print("Welcome to the GameCataloger!")
    print(sqlalchemy.__version__+"\n"+sqlite3.version)
    print("If you would like to start a new catalog enter the command: New")
    print("If you would like to use an existing catalog enter the command: Load")
    cmd = input("Enter Command:")
    if cmd == "New":
        new_catalog()
        return
    if cmd == "Load":
        load_catalog()
        return

if __name__ == "__main__":
    main()
