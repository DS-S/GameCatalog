from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, ForeignKey, select, and_
from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy.ext.automap import automap_base

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
    completed = Column(Boolean,nullable=False)
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

def make():
    # Get path
    filepath = input("\nPlease enter the path to the directory where you would like the catalog to be stored\n"
                 "This includes the drive letter (e.g. C:\\Users\\<user>\\Documents):")

    engine = create_engine("sqlite+pysqlite:///" + filepath, echo=False, future=True)

    # Build tables

    Base.metadata.create_all(engine)
    return engine

def main():
    engine = make()
    with Session(engine) as session:
        # Doesn't work here
        g1 = Game(title="FE", played=False, completed=True)
        session.add(g1)
        p1 = Platform(platform_name="Switch")
        n1 = Genre(genre_name="RPG")
        g1.platforms.append(p1)
        g1.genres.append(n1)
        g2 = Game(title="DC", played=False, completed=True)
        session.add(g2)
        p2 = Platform(platform_name="Xbox")
        n2 = Genre(genre_name="Fighting")
        g2.platforms.append(p2)
        g2.genres.append(n2)
        print(g1.title)
        print(g1.platforms[0].platform_name)
        print(g1.genres[0].genre_name)
        result = session.execute(select(Game, Platform, Genre).where(and_(Game.id == Platform.id,Game.id ==
                Genre.id)).order_by(Game.title)).all()
        print("Result:")
        print(result)
        for row in result:
            print("Row.Game.title:")
            print(row.Game.title) # "DC" doesn't print if appending p1 and n1 instead of p2 and n2, why?
    return


if __name__ == "__main__":
    main()