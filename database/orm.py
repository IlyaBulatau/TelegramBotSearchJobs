from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session

from database.models import Base, User, Report, Request, Page


engine = create_engine(url='postgresql+psycopg2://postgres:1234@localhost/JobsBot', echo=True)
conn = engine.connect()

Base.metadata.create_all(engine)

def add_user_to_db(id, user_class, page_class):
    session = Session(bind=engine)
    user = user_class(id=id)

    page = page_class(
    current = 1,
    user_id = id
    )

    session.add(user)
    session.add(page)
    session.commit()

def update_current_page(user_id, page_class, page):
    session = Session(engine)
    current_page = update(page_class).where(page_class.user_id == user_id).values(current = page)
    session.execute(current_page)    
    session.commit()

def is_user_in_db(user_id, user_class):
    session = Session(bind=engine)
    id = session.query(user_class.id).filter(user_class.id == user_id).first()
    return id == None


def write_request_in_db(data, request_class, user_id, datetime_now):
    session = Session(engine)
    request = request_class(
        id = datetime_now,
        job = data['job'],
        sort = data['sort'],
        page = data['count'],
        user_id = user_id,
    )
    session.add(request)
    session.commit()

def write_report_in_db(data, report_class, datetime_now):
    session = Session(engine)
    report = report_class(
        title = data['title'],
        salary = data['salary'],
        description = data['description'],
        link = data['link'],
        request_id = datetime_now
    )
    session.add(report)
    session.commit()

def get_current_report_in_db(request_id, report_class, count):
    session = Session(engine)

    report = session.query(report_class.title,
                           report_class.salary,
                           report_class.link).filter(report_class.request_id == request_id).limit(count).all()
    
    return report

def get_request_in_db(user_id, request_class):
    session = Session(engine)
    requests = session.query(request_class.id).filter(user_id == request_class.user_id).all()
    return requests

def get_current_page_in_db(user_id, page_class):
    session = Session(engine)
    current_page = session.query(page_class.current).filter(user_id == page_class.user_id).first()
    return current_page[0]


