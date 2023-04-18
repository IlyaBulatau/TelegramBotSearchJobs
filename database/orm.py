from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session

from database.models import Base, User, Report, Request, Page


engine = create_engine(url='postgresql+psycopg2://postgres:1234@localhost/JobsBot', echo=True)
conn = engine.connect()

Base.metadata.create_all(engine)

def add_user_to_db(id, user_class, page_class):
    """
    Добавляет юзера в бд и устанавливает номер страницы 1
    """
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
    """
    Обновляет текущую страницу просмотра прошлых запросов юзера 
    """
    session = Session(engine)
    current_page = update(page_class).where(page_class.user_id == user_id).values(current = page)
    session.execute(current_page)    
    session.commit()

def is_user_in_db(user_id, user_class):
    """
    Проверят наличие юзера в бд
    """
    session = Session(bind=engine)
    id = session.query(user_class.id).filter(user_class.id == user_id).first()
    return id == None


def write_request_in_db(data, request_class, user_id, datetime_now):
    """
    Записывает запрос поиска работы в бд
    """
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

def write_report_in_db(data, report_class, user_id, datetime_now):
    """
    Записывает все найденные вакансии запроса в бд
    """
    session = Session(engine)
    report = report_class(
        title = data['title'],
        salary = data['salary'],
        description = data['description'],
        link = data['link'],
        request_id = datetime_now,
        user_id = user_id
    )
    session.add(report)
    session.commit()

def get_current_report_in_db(request_id, report_class, count):
    """
    Получает из базы данных текущиую вакансию юзера для добавленияее в закладки
    """
    session = Session(engine)

    report = session.query(report_class.title,
                           report_class.salary,
                           report_class.link).filter(report_class.request_id == request_id).limit(count).all()
    
    return report

def get_request_in_db(user_id, request_class):
    """
    Получает все запросы юзера
    """
    session = Session(engine)
    requests = session.query(request_class.id).filter(user_id == request_class.user_id).all()
    return requests

def get_request_job_in_db(user_id, request_class, request_id):
    """
    Получает все найденные вакансии по запросу юзера из бд
    """
    session = Session(engine)
    info = session.query(request_class.job).filter(user_id == request_class.user_id).filter(request_class.id == request_id).first()
    return info

def get_current_page_in_db(user_id, page_class):
    """
    Получает текущую страницу юзера
    """
    session = Session(engine)
    current_page = session.query(page_class.current).filter(user_id == page_class.user_id).first()
    return current_page[0]

def get_reports_in_db(request_id, report_class):
    """
    Получает все вакансии запроса
    """
    session = Session(engine)
    reports = session.query(report_class.title, report_class.salary, report_class.link).filter(report_class.request_id == request_id).all()
    return reports

def get_report_id_in_db(link, report_class):
    """
    Получает определенную вакансию по идентифицирующей ссылки
    """
    session = Session(engine)
    id = session.query(report_class.id).filter(report_class.link == link).first()
    return id

def update_report_bookmark_status_in_db(link, report_class, status):
    """
    Обновляет статус вакансии в закладках
    """
    session = Session(engine)
    bm_status = session.query(report_class).filter(report_class.link == link).first()
    bm_status.is_bookmarked = status
    session.commit()

def get_marks_reports(user_id, report_class):
    """
    Получает вакансии которые в закладках
    """
    session = Session(engine)
    reports = session.query(report_class.title, report_class.link).filter(report_class.user_id == user_id).filter(report_class.is_bookmarked == True).all()
    return reports
