from sqlalchemy import Column, ForeignKey, Integer, String, create_engine ,Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


db_url = "sqlite:///student.db"  

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session=Session()

Base = declarative_base()

student_course_assocciation = Table (
    "student_course", Base.metadata,
    Column('student_id', ForeignKey('students.id'), primary_key= True),
    Column('course_id', ForeignKey('courses.id'), primary_key= True)
    
)

# Student model
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique= True)
    age = Column(Integer, nullable =True)

    profile = relationship('Profile', uselist=False , back_populates= 'student')
    
    courses = relationship('Course', secondary = student_course_assocciation, back_populates='students')

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.name}, age={self.age})>"


# Profile model
class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    bio = Column(String(255))
    address = Column(String)
    phone_number = Column(String)


    student= relationship('Student', cascade="all, delete", back_populates='profile')


# Course model
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    students = relationship('Student', secondary = student_course_assocciation, back_populates='courses')



    