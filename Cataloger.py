"""
Main Program
Author: DS-S
"""
import os
from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, ForeignKey, select, and_
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
    """
    Creates the engine, which is the source of all connections to the database, using the provided filepath. Then
    creates/loads all metadata (e.g. Tables) in the database.
    :param filepath: The filepath to the database file.
    :return: The engine.
    """
    # Create engine
    engine = create_engine("sqlite+pysqlite:///" + filepath, echo=False, future=True)
    # Create all tables in the database
    Base.metadata.create_all(engine)
    # Return engine to connect to database later
    return engine


def display_all(engine):
    """
    Prints out all entries in the database in an easy to read format, while sorting all entries alphabetically
    descending by title.
    :param engine: The source of connections to the database.
    :return: The engine.
    """
    with Session(engine) as session:
        all_games = session.execute(select(Game.title, Game.played, Game.completed, Platform.platform_name,
                                           Genre.genre_name).join(Game.platforms).join(Game.genres)).all()
        print("")
        for row in all_games:
            print(f"Title: {row.title} || Played: {row.played} || Completed: {row.completed} || "
                  f"Platform: {row.platform_name} || Genre: {row.genre_name}")
    return


def new_path():
    """
    Takes input for a path and file name and then checks to make sure that a file does not exist at that location.
    :return: The file name concatenated with the path to locate the file to connect to the database file.
    """
    path = input("\nPlease enter the path to the directory where you would like the catalog to be stored\n"
                 "This includes the drive letter (e.g. C:\\Users\\<user>\\Documents):")
    # Check path exists
    if not os.path.exists(path):
        print("\nPath does not exist, please enter existing path.")  # Must be better way than to return, how ask again?
        return None
    # Get file name
    file = input("\nPlease enter the catalog file name:")
    # Check file name
    invalidChars = "\/:*?<>| "
    for char in file:
        if char in invalidChars:
            print("\nBad file name.")
            return None
    filepath = path + "\\" + file
    # Check that file does not exist
    if os.path.isfile(filepath):
        print(
            "\nFile already exits in directory, please enter non-existing filename.")
        return None
    return filepath


def load_path():
    """
    Takes input for a path and file name and then checks to make sure that a file does exist at that location.
    :return: The file name concatenated with the path to locate the file to connect to the database file.
    """
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
            return None
    # make file path
    filepath = path + "\\" + file
    # Check that file exists
    if not os.path.isfile(filepath):
        print(
            "\nFile does not exits in directory, please enter existing file or use the command to create a new file.")
        return None
    return filepath


def add_game(engine):
    """
    Adds a game to the database, as well as genre and platform entries if necessary.
    :param engine: The source of connections to the database.
    :return: The engine.
    """
    with Session(engine) as session:
        title = input("Enter game title:")
        played = input("Has this title been played(True/False):")
        if played == "True":
            played = True
        elif played == "False":
            played = False
        else:
            print("Invalid submission for played status, returning to sub-menu.")
            return

        completed = input("Has this title been completed(True/False):")
        if completed == "True":
            completed = True
        elif completed == "False":
            completed = False
        else:
            print("Invalid submission for completed status, returning to sub-menu.")
            return

        platform = input("Enter game platform:")
        genre = input("Enter game genre:")

        # Check if full game entry exists
        game = session.execute(select(Game,Platform,Genre).join(Game.platforms).join(Game.genres)
                               .where(and_(Game.title == title,Game.played == played, Game.completed == completed))
                               .where(and_(Platform.platform_name == platform,Genre.genre_name == genre))).one_or_none()

        if game is not None:
            print("\nFull entry already exists.")
            return

        # Check if game with title exists
        t = session.execute(select(Game).where(Game.title == title)).first()

        if t is not None:
            cont = input("\nEntry with this title exists.\nCreate new entry with this title(Y/N):")
            if cont == "N":
                print("\nExiting to sub-menu.")
                return
            elif cont == "Y":
                print("Continuing with entry creation.")
            else:
                print("Invalid input.\n Exiting to sub-menu.")
                return
        new_game = Game(title=title, played=played, completed=completed)
        session.add(new_game)

        # Check if platform exists
        p = session.execute(select(Platform).where(Platform.platform_name == platform)).first()

        if p is None:
            newPlat = Platform(platform_name=platform)
            session.add(newPlat)
            new_game.platforms.append(newPlat)
        else:
            new_game.platforms.append(p.Platform)

        g = session.execute(select(Genre).where(Genre.genre_name == genre)).first()

        if g is None:
            newGenre = Genre(genre_name=genre)
            session.add(newGenre)
            new_game.genres.append(newGenre)
        else:
            new_game.genres.append(g.Genre)

        # Commit changes to database
        session.commit()
        print("\nGame has been added.")
    return engine


def remove_game(engine):
    """
    Removes a game from the database, but does not removes the genre or platform.
    :param engine: The source of connections to the database.
    :return: The engine.
    """
    with Session(engine) as session:
        title = input("Enter game title:")
        played = input("Has this title been played(True/False):")
        if played == "True":
            played = True
        elif played == "False":
            played = False
        else:
            print("Invalid submission for played status, returning to sub-menu.")
            return

        completed = input("Has this title been completed(True/False):")
        if completed == "True":
            completed = True
        elif completed == "False":
            completed = False
        else:
            print("Invalid submission for completed status, returning to sub-menu.")
            return

        platform = input("Enter game platform:")
        genre = input("Enter game genre:")

        # check if full game entry exists
        game = session.execute(select(Game, Platform, Genre).join(Game.platforms).join(Game.genres)
                               .where(and_(Game.title == title, Game.played == played, Game.completed == completed))
                               .where(
            and_(Platform.platform_name == platform, Genre.genre_name == genre))).one_or_none()

        if game is None:
            print("\nEntry does not exist.")
            return
        print(f"Deleting:\nTitle {game.Game.title} || Played:{game.Game.played} || Completed:{game.Game.completed} || "
              f"Platform:{game.Platform.platform_name} || Genre:{game.Genre.genre_name}")
        session.delete(game.Game)
        print("\nEntry deleted.")
        session.commit()


def search_title(engine):
    """
    Take input for a title. Then searches if any entries with the given title exist. Should entries with the given title
    exist all of them will be printed out in a easy to read format.
    :param engine: The source of connections to the database.
    :return: Nothing.
    """
    with Session(engine) as session:
        title = input("\nEnter the title of the game you are searching for: ")

        entry = session.execute(select(Game.title, Game.played, Game.completed, Platform.platform_name,
                Genre.genre_name).join(Game.platforms).join(Game.genres).where(Game.title == title)).first()

        if entry is None:
            print("\nNo entries with that title.")
            return

        entries = session.execute(select(Game.title, Game.played, Game.completed, Platform.platform_name,
                Genre.genre_name).join(Game.platforms).join(Game.genres).where(Game.title == title)).all()

        print("")
        for row in entries:
            print(f"Title: {row.title} || Played: {row.played} || Completed: {row.completed} || "
                  f"Platform: {row.platform_name} || Genre: {row.genre_name}")
    return


def initial_menu():
    """
    Initial menu accessed by user allowing them to create a new game tracking log, load an old log, or quit the program.
    :return: Nothing.
    """
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
            else:
                engine = connect(filepath)
                display_all(engine)
                sub_menu(engine)
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
            else:
                engine = connect(filepath)
                display_all(engine)
                sub_menu(engine)
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


def sub_menu(engine):
    """
    Sub-menu accessed by user allowing them to search for a game by title, display stored games sorted in different
    manners, add a game to the catalog, remove a game from the catalog, display all games in the database (sorted
    alphabetically).
    :param engine: The source of connections ot the database.
    :return: Nothing
    """
    print("\nAll cataloged games have been displayed above.\nYou are now in the sub-menu.")
    print("\nTo search for a game by title enter the command: Search")
    print("To display the catalog sorted differently enter the command: Sort")
    print("To add a new game enter the command: AddGame")
    print("To remove a game enter the command: RemoveGame")
    print("To display the database enter the command: Display")
    print("Otherwise to return to the initial menu to create or load a different catalog enter the command: Exit")
    cmd = input("\nEnter Command:")
    while cmd != "Exit":
        if cmd == "Search":
            search_title(engine)
            print("\nTo search for a game by title enter the command: Search")
            print("To display the catalog sorted differently enter the command: Sort")
            print("To add a new game enter the command: AddGame")
            print("To remove a game enter the command: RemoveGame")
            print("To display the database enter the command: Display")
            print(
                "Otherwise to return to the initial menu to create or load a different catalog enter the command: Exit")
            cmd = input("\nEnter Command:")
        elif cmd == "Sort":
            # ToDo: create function to query database in manner besides alphabetically by title as done by display_all()
            print("\nTo search for a game by title enter the command: Search")
            print("To display the catalog sorted differently enter the command: Sort")
            print("To add a new game enter the command: AddGame")
            print("To remove a game enter the command: RemoveGame")
            print("To display the database enter the command: Display")
            print(
                "Otherwise to return to the initial menu to create or load a different catalog enter the command: Exit")
            cmd = input("\nEnter Command:")
        elif cmd == "AddGame":
            add_game(engine)
            print("\nTo search for a game by title enter the command: Search")
            print("To display the catalog sorted differently enter the command: Sort")
            print("To add a new game enter the command: AddGame")
            print("To remove a game enter the command: RemoveGame")
            print("To display the database enter the command: Display")
            print(
                "Otherwise to return to the initial menu to create or load a different catalog enter the command: Exit")
            cmd = input("\nEnter Command:")
        elif cmd == "RemoveGame":
            remove_game(engine)
            print("\nTo search for a game by title enter the command: Search")
            print("To display the catalog sorted differently enter the command: Sort")
            print("To add a new game enter the command: AddGame")
            print("To remove a game enter the command: RemoveGame")
            print("To display the database enter the command: Display")
            print(
                "Otherwise to return to the initial menu to create or load a different catalog enter the command: Exit")
            cmd = input("\nEnter Command:")
        elif cmd == "Display":
            display_all(engine)
            print("\nAll cataloged games have been displayed above.\nYou are now in the sub-menu.")
            print("\nTo search for a game by title enter the command: Search")
            print("To display the catalog sorted differently enter the command: Sort")
            print("To add a new game enter the command: AddGame")
            print("To remove a game enter the command: RemoveGame")
            print("To display the database enter the command: Display")
            print(
                "Otherwise to return to the initial menu to create or load a different catalog enter the command: Exit")
            cmd = input("\nEnter Command:")
        #ToDo: Add functions to remove/add a genre/platform
        else:
            print("\nTo search for a game by title enter the command: Search")
            print("To display the catalog sorted differently enter the command: Sort")
            print("To add a new game enter the command: AddGame")
            print("To remove a game enter the command: RemoveGame")
            print("To display the database enter the command: Display")
            print(
                "Otherwise to return to the initial menu to create or load a different catalog enter the command: Exit")
            cmd = input("\nEnter Command:")
    return


def main():
    """
    Prints welcome message then starts program at initial menu.
    :return:
    """
    print("Welcome to the GameTracker!")
    initial_menu()


if __name__ == "__main__":
    main()
