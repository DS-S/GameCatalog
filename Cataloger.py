"""
Main Program
Author: DS-S
"""
import os
from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

Base = declarative_base()

gplink = Table("game_platform_link", Base.metadata,
               Column("game_id", ForeignKey("game.id"), primary_key=True),
               Column("platform_id", Integer, ForeignKey("platform.id"), primary_key=True))

gglink = Table("game_genre_link", Base.metadata,
               Column("game_id", ForeignKey("game.id"), primary_key=True),
               Column("genre_id", Integer, ForeignKey("genre.id"), primary_key=True))

class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    played = Column(Boolean, nullable=False)
    completed = Column(Boolean, nullable=False)
    # relationship (<Class related to>, secondary=<Table that forms relation between 2 other tables>,
    # back_populates=<complimentary collection in related class>)
    platforms = relationship("Platform", secondary=gplink, back_populates="games")
    genres = relationship("Genre", secondary=gglink, back_populates="games")


class Platform(Base):
    __tablename__ = "platform"

    id = Column(Integer, primary_key=True)
    platform_name = Column(String, nullable=False)
    games = relationship("Game", secondary=gplink, back_populates="platforms")


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    genre_name = Column(String, nullable=False)
    games = relationship("Game", secondary=gglink, back_populates="genres")

def connect(filepath):
    # Create engine
    engine = create_engine("sqlite+pysqlite:///" + filepath, echo=False, future=True)
    # Create all tables in the database
    Base.metadata.create_all(engine)
    # Return engine to connect to database later
    return engine

def display_all(engine):
    with Session(engine) as session:
        return session.execute(select(Game.title, Game.played, Game.completed, Platform.platform_name, Genre.genre_name).join(
            Game.platforms).join(Game.genres)).all()

def new_path():
    # Get path
    path = input("\nPlease enter the path to the directory where you would like the catalog to be stored\n"
                 "This includes the drive letter (e.g. C:\\Users\\<user>\\Documents):")
    # Check path exists
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
    # Check that file does not exist
    if os.path.isfile(filepath):
        print(
            "\nFile already exits in directory, please enter non-existing filename.")
        return
    return  filepath

def load_path():
    # Get path
    path = input("\nPlease enter the path to the directory where the catalog is stored:")
    # Check path exists
    if not os.path.exists(path):
        print("\nPath does not exist, please enter existing path.")
        return
    # Get file name
    file = input("\nPlease enter the catalog file name:")
    # Check file name
    invalidChars = "\/:*?<>| "
    for char in file:
        if char in invalidChars:
            print("\nBad file name.")
            return
    # make file path
    filepath = path + "\\" + file
    # Check that file exists
    if not os.path.isfile(filepath):
        print(
            "\nFile does not exits in directory, please enter existing file or use the command to create a new file.")
        return
    return filepath


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
            filepath = new_path()
            if filepath is None:
                print("\nTo start a new catalog enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
                continue
            else:
                engine = connect(filepath)
                all_games = display_all(engine)
                print("")
                for row in all_games:
                    print(f"Title: {row.title} || Played: {row.played} || Completed: {row.completed} || "
                          f"Platform: {row.platform_name} || Genre: {row.genre_name}")
                sub_menu()
                print("\nTo start a new catalog enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
        elif cmd == "Load":
            filepath = load_path()
            if filepath is None:
                print("\nTo start a new catalog enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
                continue
            else:
                engine = connect(filepath)
                all_games = display_all(engine)
                print("")
                for row in all_games:
                    print(f"Title: {row.title} || Played: {row.played} || Completed: {row.completed} || "
                          f"Platform: {row.platform_name} || Genre: {row.genre_name}")
                sub_menu()
                print("\nTo start a new catalog enter the command: New")
                print("To use an existing catalog enter the command: Load")
                print("To quit the program enter the command: Quit\n")
                cmd = input("Enter Command:")
        else:
            print("\nTo start a new catalog enter the command: New")
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
    print("To display the catalog sorted differently enter the command: Sort")
    print("To add a new game enter the command: AddGame")
    print("To remove a game enter the command: RemoveGame")
    print("Otherwise to return to the initial menu to create or load a different catalog enter the command: Exit")
    cmd = input("\nEnter Command:")
    while cmd != "Exit":
        if cmd == "Search":
            # ToDo: query database for specific title
            return
        elif cmd == "Sort":
            # ToDo: create function to query database
            return
        elif cmd == "AddGame":
            # ToDo: create function to add new game to database
            return
        elif cmd == "RemoveGame":
            # ToDo: create function to remove game from database
            return
        else:
            print("\nTo search for a game by title enter the command: Search")
            print("To display the catalog sorted differently enter the command: Sort")
            print("To add a new game enter the command: AddGame")
            print("To remove a game enter the command: RemoveGame")
            print("Otherwise to return to the initial menu to create or load a different catalog enter the command: "
                  "Exit")
            cmd = input("Enter Command:")
    return


def main():
    print("Welcome to the GameTracker!")
    initial_menu()


if __name__ == "__main__":
    main()
