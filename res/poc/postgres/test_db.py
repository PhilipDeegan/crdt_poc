from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

from models import Student

engine = create_engine("postgresql+psycopg2://postgres:banarama@0.0.0.0:5432/collab")

Session = sessionmaker(bind=engine)


def app():
    with Session() as session:
        session.add_all(
            [
                Student(name="John Smith", age=19, note=""),
                Student(name="Sophia Ava", age=20, note=""),
            ]
        )
        session.commit()

    with engine.connect() as conn:
        stmt = select(Student)
        print(conn.execute(stmt).fetchall())


if __name__ == "__main__":
    app()
