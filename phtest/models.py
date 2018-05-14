from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


var_to_qst_table = Table('variant_to_question', Base.metadata,
    Column('variant_id', Integer, ForeignKey('variants.id')),
    Column('question_id', Integer, ForeignKey('questions.id'))
)


user_right_qst_table = Table('user_right_questions', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('question_id', Integer, ForeignKey('questions.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    login = Column(String(20))
    attempts = Column(Integer)

    right_questions = relationship("Question", secondary=user_right_qst_table)


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    text = Column(String(1000))
    section_id = Column(Integer)
    answers = relationship("Answer", backref="question")


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    question_id = Column(Integer, ForeignKey('questions.id'))


class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    n_correct = Column(Integer)
    n_total = Column(Integer)
    datetime = Column(DateTime)

    user = relationship(User)


class Variant(Base):
    __tablename__ = 'variants'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    started = Column(DateTime)

    user = relationship(User)
    questions = relationship("Question", secondary=var_to_qst_table)


