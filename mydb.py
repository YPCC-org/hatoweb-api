import os

from sqlalchemy import Column, DateTime, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
ENGINE = create_engine(DB_URL)
Base = declarative_base()


class Class_Ten(Base):
    __tablename__ = "class_ten"
    class_name = Column(Text, primary_key=True)
    status = Column(Integer)
    comment = Column(Text)
    updated_at = Column(DateTime)


Session = sessionmaker(bind=ENGINE)
session = Session()


def get_class_ten(class_name):
    x = session.query(Class_Ten).get(class_name)
    return x.status, x.comment, x.updated_at


def update_class_ten(class_name, status, comment, delete, updated_at):
    x = session.query(Class_Ten).get(class_name)
    x.status = status
    if delete:
        x.comment = ''
    elif comment:
        x.comment = comment
    x.updated_at = updated_at
    session.commit()
    return 0


if __name__ == "__main__":
    status, comment, updated_at = get_class_ten('21')
    print(status, comment, updated_at)