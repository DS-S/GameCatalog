from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, ForeignKey, select
from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy.ext.automap import automap_base


def make():
    # Get path
    filepath = input("\nPlease enter the path to the directory where you would like the catalog to be stored\n"
                 "This includes the drive letter (e.g. C:\\Users\\<user>\\Documents):")

    engine = create_engine("sqlite+pysqlite:///" + filepath, echo=True, future=True)

    # Build tables
    Base = declarative_base()

    gplink = Table("game_platform_link", Base.metadata,
                   Column("game_id", ForeignKey("game.id"), primary_key=True),
                   Column("platform_id", Integer, ForeignKey("platform.id"), primary_key=True))

    class Game(Base):
        __tablename__ = "game"
        id = Column(Integer, primary_key=True)
        title = Column(String, nullable=False)
        played = Column(Boolean, nullable=False)
        completed = Column(Boolean,nullable=False)
        platforms = relationship("Platform", secondary=gplink, back_populates="games")

    class Platform(Base):
        __tablename__ = "platform"
        id = Column(Integer, primary_key=True)
        console = Column(String, nullable=False)
        games = relationship("Game", secondary=gplink, back_populates="platforms")

    Base.metadata.create_all(engine)

    #work here
    with Session(engine) as session:
        g1 = Game(title="FE", played=False, completed=True)
        session.add(g1)
        p1 = Platform(console="Switch")
        g1.platforms.append(p1)
        print(g1.platforms[0].console)
    return engine

def main():
    engine = make()
    base = automap_base()
    base.prepare(engine, reflect=True)
    gplink = Table("game_platform_link", base.metadata, autoload_with=engine)
    Game = base.classes.game #Reflected Table missing platforms attribute while original does nto have this issue
    Platform = base.classes.platform
    with Session(engine) as session:
        # Doesn't work here
        g1 = Game(title="FE", played=False, completed=True)
        session.add(g1)
        p1 = Platform(console="Switch")
        g1.platforms.append(p1)
        print(g1.platforms[0].console)
    return


if __name__ == "__main__":
    main()