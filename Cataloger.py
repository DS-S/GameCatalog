"""
Main Program
Author: Dennis Santos-Sanchez
"""
import os
import sqlite3

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.automap import automap_base

"""
Creates and connects to new database
"""


def new_catalog():
    # Get path
    path = input("\nPlease enter the path to the directory where you would like the catalog to be stored\n"
                 "This includes the drive letter (e.g. C:\\Users\\<user>\\Documents):")
    # Checks path exists.
    if not os.path.exists(path):
        print("\nPath does not exist, please enter existing path.")  # Must be better way than to return, how ask again?
        return False
    # Get file name
    file = input("\nPlease enter the catalog file name:")
    invalidChars = "\/:*?<>| "
    for char in file:
        if char in invalidChars:
            print("\nBad file name.")
            return False
    filepath = path + "\\" + file
    # Checks file doesn't already exists
    if os.path.isfile(filepath):
        print(
            "\nFile already exits in directory, please enter non-existing filename.")
        # Must be better way than to return, how ask again?
        return False

    ### Create Engine ###
    # Create engine object that acts as central source of connections to the database
    engine = create_engine("sqlite+pysqlite:///" + filepath, echo=False, future=True)

    #### Building Tables ####
    Base = declarative_base()

    class Game(Base):
        __tablename__ = "game"

        id = Column(Integer, primary_key=True)
        title = Column(String, nullable=False)
        played = Column(Boolean, nullable=False)
        completed = Column(Boolean, nullable=False)
        # relationship (<Class related to>, secondary=<Table that forms relation between 2 other tables>,
        # back_populates=<complimentary collection in related class>)
        platform = relationship("Platform", secondary="Game_Platform_link", back_populates="games")
        genre = relationship("Genre", secondary="Game_Genre_link", back_populates="games")

    class Platform(Base):
        __tablename__ = "platform"

        id = Column(Integer, primary_key=True, nullable=False)
        platform_name = Column(String, nullable=False)
        # relationship (<Class related to>, secondary=<Table that forms relation between 2 other tables>,
        # back_populates=<complimentary collection in related class>)
        game = relationship("Game", secondary="Game_Platform_link", back_populates="platforms")

    class Genre(Base):
        __tablename__ = "genre"

        id = Column(Integer, primary_key=True, nullable=False)
        platform_name = Column(String, nullable=False)
        # relationship (<Class related to>, secondary=<Table that forms relation between 2 other tables>,
        # back_populates=<complimentary collection in related class>)
        game = relationship("Game", secondary="Game_Genre_link", back_populates="genres")

    class GamePlatform(Base):
        __tablename__ = "Game_Platform_link"

        game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
        platform_id = Column(Integer, ForeignKey("platform.id"), primary_key=True)

    class GameGenre(Base):
        __tablename__ = "Game_Genre_link"

        game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
        platform_id = Column(Integer, ForeignKey("genre.id"), primary_key=True)

    #### Create all tables in the engine/database ####
    Base.metadata.create_all(engine)

    # with Session(engine) as session: Seesion?

    return


"""
Connects to existing database
"""


def load_catalog():
    path = input("\nPlease enter the path to the directory where the catalog is stored:")
    if not os.path.exists(path):
        print("\nPath does not exist, please enter existing path.")  # Must be better way than to return
        return False
    file = input("\nPlease enter the catalog file name:")
    invalidChars = "\/:*?<>| "
    for char in file:
        if char in invalidChars:
            print("\nBad file name.")
            return False
    filepath = path + "\\" + file
    if not os.path.isfile(filepath):
        print(
            "\nFile does not exits in directory, please enter existing file or use the command to create a new file.")
        # Must be better way than to return
        return False

    engine = create_engine("sqlite+pysqlite:///" + filepath, echo=False, future=True)

    ### Using built in automated system to reflect tables from existing database###
    Base = automap_base()
    Base.prepare(engine, reflect = True)

    Game = Base.classess.game
    Platform = Base.clasees.platform
    Genre = Base.classes.genre

### MENU SYSTEM ###

def initial_menu():
    print("\nTo start a new log enter the command: New")
    print("To use an existing catalog enter the command: Load")
    print("To quit the program enter the command: Quit\n")
    cmd = input("Enter Command:")
    while cmd != "Quit":
        if cmd == "New":
            if new_catalog() == False:
                print("\nTo start a new log enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
                continue
            # ToDo: display entire catalog
            else:
                sub_menu()
                print("\nTo start a new log enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
        elif cmd == "Load":
            if load_catalog() == False:
                print("\nTo start a new log enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
                continue
            # ToDo: display entire catalog
            else:
                sub_menu()
                print("\nTo start a new log enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
        else:
            print("\nTo start a new log enter the command: New")
            print("To use an existing catalog enter the command: Load")
            print("To quit the program enter the command: Quit\n")
            cmd = input("Enter Command:")
    return


def sub_menu():
    print("\nAll cataloged games have been displayed above.\nYou are now in the sub-menu.")
    print("\nTo search for a game by title enter the command: Search")
    print("To display the catalog using filters enter the command: Filter")
    print("Otherwise to return to the initial menu to create or load a different catalog enter the command: Exit")
    cmd = input("\nEnter Command:")
    while cmd != "Exit":
        if cmd == "Search":
            # ToDo: create database search function
            return
        elif cmd == "Filter":
            # ToDo: create database filter function
            return
        else:
            print("\nTo search for a game by title enter the command: Search")
            print("To display the catalog using filters enter the command: Filter")
            print("Otherwise to return to the initial menu to create or load a different catalog enter the command: "
                  "Exit")
            cmd = input("Enter Command:")
    return


def main():
    print("SQLAlchemy: " + sqlalchemy.__version__ + "\nSQLite3: " + sqlite3.version)
    print("Welcome to the GameTracker!")
    initial_menu()


if __name__ == "__main__":
    main()
