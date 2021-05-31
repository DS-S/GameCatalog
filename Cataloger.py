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


def new_catalog():
    # Get path
    path = input("Please enter the path to the directory where you would like the catalog to be stored\n"
                 "This includes the drive letter (e.g. C:\\Users\\<user>\\Documents):")
    # Checks path exists.
    if not os.path.exists(path):
        print("Path does not exist, please enter existing path.")  # Must be better way than to return, how ask again?
        return None
    # Get file name
    file = input("Please enter the catalog file name:")

    filepath = path + "\\" + file
    # Checks file doesn't already exists
    if not os.path.isfile(filepath):
        print(
            "File already exits in directory, please enter non-existing filename.")  # Must be better way than to return, how ask again?
        return None


    ###Create Engine###
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
        platforms = relationship("Platform", secondary="Game_Platform_link", back_populates="games")
        genres = relationship("Genre", secondary="Game_Genre_link", back_populates="games")

    class Platform(Base):
        __tablename__ = "platform"

        id = Column(Integer, primary_key=True, nullable=False)
        platform_name = Column(String, nullable=False)
        # relationship (<Class related to>, secondary=<Table that forms relation between 2 other tables>,
        # back_populates=<complimentary collection in related class>)
        games = relationship("Game", secondary="Game_Platform_link", back_populates="platforms")

    class Genre(Base):
        __tablename__ = "genre"

        id = Column(Integer, primary_key=True, nullable=False)
        platform_name = Column(String, nullable=False)
        # relationship (<Class related to>, secondary=<Table that forms relation between 2 other tables>,
        # back_populates=<complimentary collection in related class>)
        games = relationship("Game", secondary="Game_Genre_link", back_populates="genres")

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


def load_catalog():
    path = input("Please enter the path to the directory where the catalog is stored:")
    if not os.path.exists(path):
        print("Path does not exist, please enter existing path.")  # Must be better way than to return
        return None
    file = input("Please enter the catalog file name:")
    filepath = path + "\\" + file
    if not os.path.isfile(filepath):
        print("File does not exits in directory, please enter existing file or use the command to create a new file.")  # Must be better way than to return
        return None

def initial_menu(cmd):
    while cmd != "Quit":
        if cmd == "New":
            new_catalog()
            return
        elif cmd == "Load":
            load_catalog()
            return
        else:
            print("To start a new log enter the command: New")
            print("To use an existing catalog enter the command: Load")
            print("To quit the program enter the command: Quit\n")
            cmd = input("Enter Command:")

def main():
    print("SQLAlchemy: " + sqlalchemy.__version__ + "\nSQLite3: " + sqlite3.version)
    print("Welcome to the GameTracker!")
    print("To start a new log enter the command: New")
    print("To use an existing catalog enter the command: Load")
    print("To quit the program enter the command: Quit\n")
    cmd = input("Enter Command:")
    initial_menu(cmd)



if __name__ == "__main__":
    main()
