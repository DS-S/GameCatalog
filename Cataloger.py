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
Creates New Database
"""
def new_catalog():
    # Get path
    path = input("\nPlease enter the path to the directory where you would like the catalog to be stored\n"
                 "This includes the drive letter (e.g. C:\\Users\\<user>\\Documents):")

    # Check path exists.
    if not os.path.exists(path):
        print("\nPath does not exist, please enter existing path.")  # Must be better way than to return, how ask again?
        return

    # Get file name
    file = input("\nPlease enter the catalog file name:")

    # Check file name
    invalidChars = "\/:*?<>| "
    for char in file:
        if char in invalidChars:
            print("\nBad file name.")
            return

    filepath = path + "\\" + file

    # Check file does not already exist
    if os.path.isfile(filepath):
        print(
            "\nFile already exits in directory, please enter non-existing filename.")
        return

    # Create engine
    engine = create_engine("sqlite+pysqlite:///" + filepath, echo=False, future=True)

    # Build tables
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
        game = relationship("Game", secondary="Game_Platform_link", back_populates="platforms")

    class Genre(Base):
        __tablename__ = "genre"

        id = Column(Integer, primary_key=True, nullable=False)
        platform_name = Column(String, nullable=False)
        game = relationship("Game", secondary="Game_Genre_link", back_populates="genres")

    class GamePlatform(Base):
        __tablename__ = "Game_Platform_link"

        game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
        platform_id = Column(Integer, ForeignKey("platform.id"), primary_key=True)

    class GameGenre(Base):
        __tablename__ = "Game_Genre_link"

        game_id = Column(Integer, ForeignKey("game.id"), primary_key=True)
        platform_id = Column(Integer, ForeignKey("genre.id"), primary_key=True)

    # Create all tables in the database
    Base.metadata.create_all(engine)

    # Return engine to connect to database later
    return engine


"""
Connects to existing database
"""
def load_catalog():
    path = input("\nPlease enter the path to the directory where the catalog is stored:")

    if not os.path.exists(path):
        print("\nPath does not exist, please enter existing path.")
        return

    file = input("\nPlease enter the catalog file name:")

    invalidChars = "\/:*?<>| "
    for char in file:
        if char in invalidChars:
            print("\nBad file name.")
            return

    filepath = path + "\\" + file

    if not os.path.isfile(filepath):
        print(
            "\nFile does not exits in directory, please enter existing file or use the command to create a new file.")
        return

    engine = create_engine("sqlite+pysqlite:///" + filepath, echo=False, future=True)

    # Use automap to copy tables from existing database
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Copy main tables
    Game = Base.classess.game
    Platform = Base.clasees.platform
    Genre = Base.classes.genre
    # Copy Association tables
    GamePlatform = Base.classes.Game_Platform_link  # Unsure if should be table name or class name
    GameGenre = Base.classes.Game_Genre_link

    return engine


"""
Initial menu accessed by user
"""
def initial_menu():
    print("\nTo start a new log enter the command: New")
    print("To use an existing catalog enter the command: Load")
    print("To quit the program enter the command: Quit\n")
    cmd = input("Enter Command:")
    while cmd != "Quit":
        if cmd == "New":
            engine = new_catalog()
            if engine is None:
                print("\nTo start a new log enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
                continue
            else:
                # ToDo: display entire catalog
                sub_menu()
                print("\nTo start a new log enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
        elif cmd == "Load":
            engine = load_catalog()
            if engine is None:
                print("\nTo start a new log enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
                continue
            else:
                # ToDo: display entire catalog
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


"""
Menu accessed by user after having created or loaded a catalog
"""
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
