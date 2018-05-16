from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Table, \
        ForeignKey, Boolean
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
    name = Column(String(50), nullable=False)
    group = Column(String(20), nullable=False)
    login = Column(String(20), nullable=False)
    attempts = Column(Integer, nullable=False)

    right_questions = relationship("Question", secondary=user_right_qst_table)

    def __str__(self):
        return f"{self.name} ({self.group})"


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    text = Column(Text(1000), nullable=False)
    section_id = Column(Integer, nullable=False)
    answers = relationship("Answer", backref="question")

    def is_multi(self):
        return True
        #return sum(int(ans.is_correct) for ans in self.answers) > 1
    
    def answer_correct(self, ans_ids):
        right_ids = {ans.id for ans in self.answers if ans.is_correct}
        wrong_ids = {ans.id for ans in self.answers if not ans.is_correct}
        return not (right_ids - ans_ids) and not (wrong_ids & ans_ids)

    def to_dict(self):
        return {"text": self.text, "section_id": self.section_id,
                "answers": [a.to_dict() for a in self.answers]}

    @classmethod
    def from_dict(cls, d):
        return cls(text=d["text"], section_id=d["section_id"],
                   answers=[Answer.from_dict(a) for a in d["answers"]])
    

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    is_correct = Column(Boolean, nullable=False)

    def __str__(self):
        return f"#{self.id}. {self.text}"

    def to_dict(self):
        return {"text": self.text, "is_correct": self.is_correct}

    @classmethod
    def from_dict(cls, d):
        return cls(text=d["text"], is_correct=d["is_correct"])

class Variant(Base):
    __tablename__ = 'variants'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    started = Column(DateTime, nullable=False)

    user = relationship(User)
    questions = relationship("Question", secondary=var_to_qst_table)

    def make_result(self, n_correct):
        return Result(variant=self, user=self.user, n_correct=n_correct,
                      n_total=len(self.questions), datetime=datetime.now())


class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    variant_id = Column(Integer, ForeignKey('variants.id'), nullable=True)
    n_correct = Column(Integer, nullable=False)
    n_total = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=False)

    variant = relationship(Variant)
    user = relationship(User)
