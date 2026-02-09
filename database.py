import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    full_name = Column(String)
    username = Column(String)
    registration_date = Column(DateTime, default=datetime.utcnow)
    subscription_end = Column(DateTime, nullable=True)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(Integer, index=True)
    user_name = Column(String)
    file_id = Column(String)  
    status = Column(String, default='pending')  
    profile_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StaticProfile(Base):
    __tablename__ = 'static_profiles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    vless_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

from config import DB_PATH
db_dir = os.path.dirname(DB_PATH)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    logger.info("Database initialized at %s", DB_PATH)

class TransactionHelper:
    @staticmethod
    def create_pending(user_telegram_id: int, user_name: str, file_id: str):
        with Session() as session:
            tx = Transaction(user_telegram_id=user_telegram_id, user_name=user_name, file_id=file_id, status='pending')
            session.add(tx)
            session.commit()
            session.refresh(tx)
            return tx

    @staticmethod
    def get_by_id(tx_id: int):
        with Session() as session:
            return session.query(Transaction).filter(Transaction.id==tx_id).first()

    @staticmethod
    def mark_confirmed(tx_id: int, profile_id: int=None):
        with Session() as session:
            tx = session.query(Transaction).filter(Transaction.id==tx_id).first()
            if not tx:
                return None
            tx.status = 'confirmed'
            tx.profile_id = profile_id
            tx.updated_at = datetime.utcnow()
            session.commit()
            return tx


class UserHelper:
    @staticmethod
    def get_or_create(telegram_id: int, full_name: str = None, username: str = None):
        with Session() as session:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                user = User(
                    telegram_id=telegram_id,
                    full_name=full_name,
                    username=username,
                    registration_date=datetime.utcnow()
                )
                session.add(user)
                session.commit()
                session.refresh(user)
            return user

    @staticmethod
    def mark_rejected(tx_id: int):
        with Session() as session:
            tx = session.query(Transaction).filter(Transaction.id==tx_id).first()
            if not tx:
                return None
            tx.status = 'rejected'
            tx.updated_at = datetime.utcnow()
            session.commit()
            return tx

class UserHelper:
    @staticmethod
    def get_or_create(telegram_id: int, full_name: str, username: str):
        with Session() as session:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                user = User(
                    telegram_id=telegram_id,
                    full_name=full_name,
                    username=username,
                    registration_date=datetime.utcnow(),
                    subscription_end=None
                )
                session.add(user)
                session.commit()
                logger.info(f"👤 Новый пользователь добавлен в БД: {telegram_id}")
            return user

    @staticmethod
    def set_subscription(telegram_id: int, days: int):
        with Session() as session:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                return None
            user.subscription_end = datetime.utcnow() + timedelta(days=days)
            session.commit()
            logger.info(f"✅ Подписка пользователю {telegram_id} обновлена до {user.subscription_end}")
            return user


class StaticProfileHelper:
    @staticmethod
    def add_profile(name: str, vless_url: str):
        with Session() as session:
            profile = StaticProfile(name=name, vless_url=vless_url)
            session.add(profile)
            session.commit()
            logger.info(f"📡 Новый профиль сохранён в БД: {name}")
            return profile
