from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

import sciqlop.collab.model.postgres_model as pgm
import sciqlop.collab.crdt.manager as cdrt_man

engine = create_engine("postgresql+psycopg2://postgres:banarama@0.0.0.0:5432/collab")

Session = sessionmaker(bind=engine)


def app():
    with Session() as session:
        session.add_all(
            [
                pgm.Catalogue(name="cat0", uuid=cdrt_man.uuid()),
                pgm.Catalogue(name="cat1", uuid=cdrt_man.uuid()),
            ]
        )
        session.commit()

    with engine.connect() as conn:
        stmt = select(pgm.Catalogue)
        print(conn.execute(stmt).fetchall())


if __name__ == "__main__":
    app()
