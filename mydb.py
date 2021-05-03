import datetime
import os

from sqlalchemy import Column, DateTime, Integer, Text, create_engine, inspect
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
    status_updated = Column(DateTime)
    comment_updated = Column(DateTime)


class Info(Base):
    __tablename__ = "info"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    value = Column(Text)
    updated_at = Column(DateTime)


Session = sessionmaker(bind=ENGINE)
session = Session()


def fix_class_ten():
    insert_list = list()
    default_class_names = [
        "1A",
        "1B",
        "2A",
        "2B",
        "3A",
        "3B",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
    ]
    exist_class_names = list()
    for i in session.query(Class_Ten.class_name).all():
        exist_class_names.append(i[0])
    class_names = list(set(default_class_names) - set(exist_class_names))
    if class_names:
        timestamp = datetime.datetime.now()
        for class_name in class_names:
            row = dict()
            row["class_name"] = class_name
            row["status"] = 5
            row["comment"] = ""
            row["status_updated"] = timestamp
            row["comment_updated"] = timestamp
            insert_list.append(row)
        session.execute(Class_Ten.__table__.insert(), insert_list)
        session.commit()
    session.close()


def get_class_ten():
    if not inspect(ENGINE).has_table("class_ten"):
        Base.metadata.tables["class_ten"].create(bind=ENGINE)
    fix_class_ten()
    resdict = {}
    result = session.query(Class_Ten).all()
    for row in result:
        resdict[row.class_name] = {
            "status": row.status,
            "comment": row.comment,
            "status_updated": row.status_updated,
            "comment_updated": row.comment_updated,
        }
    return resdict


def update_class_ten(class_name, status, comment, delete, timestamp):
    if not inspect(ENGINE).has_table("class_ten"):
        Base.metadata.tables["class_ten"].create(bind=ENGINE)
    fix_class_ten()
    x = session.query(Class_Ten).get(class_name)
    x.status = status
    if delete:
        x.comment = ""
        x.comment_updated = timestamp
    elif comment:
        x.comment = comment
        x.comment_updated = timestamp
    x.status_updated = timestamp
    session.commit()
    session.close()
    return 0


def get_info():
    resdict = {}
    result = session.query(Info).all()
    count = session.query(Info).count() - 1
    for row in result:
        resdict[count - row.id] = {
            "title": row.title,
            "value": row.value,
            "updated_at": row.updated_at,
        }
    return resdict


def add_info(title, value, updated_at):
    id = session.query(Info).count()
    ncolmn = Info(id=id, title=title, value=value, updated_at=updated_at)
    session.add(ncolmn)
    session.commit()
    session.close()
    return 0


def reset_class_ten():
    if not inspect(ENGINE).has_table("class_ten"):
        Base.metadata.tables["class_ten"].create(bind=ENGINE)
    else:
        session.query(Class_Ten).delete()
    session.commit()
    session.close()
    fix_class_ten()
    return 0


def reset_info():
    if not inspect(ENGINE).has_table("info"):
        Base.metadata.tables["info"].create(bind=ENGINE)
    session.query(Info).delete()
    session.commit()
    session.close()
    return 0


if __name__ == "__main__":
    print(get_class_ten(), get_info())
