from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine("sqlite:///requests.db")

session = sessionmaker(engine)



class Base(DeclarativeBase):
    pass



class ChatRequests(Base):
    __tablename__ = "chat_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_adress: Mapped[str] = mapped_column(index=True)
    prompt: Mapped[str]
    response: Mapped[str]


def get_user_requests(ip_adress: str):  # Получаем все запросы пользователя по его IP-адресу. Возвращаем список объектов ChatRequests.
    with session() as new_session:
        query = select(ChatRequests).filter_by(ip_adress=ip_adress)
        results = new_session.execute(query)
        return results.scalars().all()

def add_request_data(ip_adress: str, prompt: str, response: str) -> None:
    with session() as new_session:
        new_request = ChatRequests(
            ip_adress=ip_adress,
            prompt=prompt,
            response=response
        )
        new_session.add(new_request)
        new_session.commit()