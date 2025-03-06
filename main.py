from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import click
from models import Student, Profile, Course, Base, engine

# Create all tables in the database
Base.metadata.create_all(engine)

# Create an SQLite engine (or any other DB engine)
SessionLocal = sessionmaker(bind=engine)

@click.group()
def cli():
    """
    CLI for student management system
    """
    pass

# Command to add a new student
@cli.command()
@click.option('--name', prompt='Student Name')
@click.option('--age', prompt='Student Age', type=int)
def add_student(name, age):
    session = SessionLocal()
    try:
        student = Student(name=name, age=age)
        session.add(student)
        session.commit()
        click.echo(f"Added student: {student.name}, Age: {student.age}")
    except Exception as e:
        session.rollback()  # In case of an error, rollback the transaction
        click.echo(f"Error adding student: {e}")
    finally:
        session.close()  # Ensure the session is always closed

# Command to add a profile for a student
@cli.command()
@click.option('--student_id', prompt='Student ID', type=int)
@click.option('--bio', prompt='Student Bio')
@click.option('--address', prompt='Student Address')
@click.option('--phone_number', prompt='Student Phone Number')
def add_profile(student_id, bio, address, phone_number):
    session = SessionLocal()
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        click.echo('Student Not Found')
        return
    profile = Profile(bio=bio, address=address, phone_number=phone_number, student=student)
    session.add(profile)
    session.commit()
    click.echo(f'Added profile for {student.name}: Bio: {profile.bio}, Address: {profile.address}, Phone Number: {profile.phone_number}')

    session.close()

# Command to add a new course
@cli.command()
@click.option('--name', prompt='Course Name')
@click.option('--description', prompt='Course Description')
def add_course(name, description):
    session = SessionLocal()
    course = Course(name=name, description=description)
    session.add(course)
    session.commit()
    click.echo(f"Added course: {course.name} (ID: {course.id})")
    session.close()

# Command to list all students
@cli.command()
def list_students():
    session = SessionLocal()
    students = session.query(Student).all()
    for s in students:
        profile_details = (
            f"Bio: {s.profile.bio}, Address: {s.profile.address}, Phone Number: {s.profile.phone_number}"
            if s.profile
            else "No profile"
        )
        courses = ", ".join([course.name for course in s.courses]) if s.courses else "No courses"
        click.echo(f"ID: {s.id}, Name: {s.name}, Age: {s.age} | Profile: {profile_details} | Courses: {courses}")
    
    session.close()

@cli.command()
@click.option('--student_id', prompt='Student ID', type=int)
@click.option('--course_id', prompt='Course ID', type=int)

def enroll_student(student_id, course_id):
    session = SessionLocal()
    student = session.query(Student).filter(Student.id == student_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()
    if not student or not course:
        click.echo("Student or Course not found")
        return
    student.courses.append(course)
    session.commit()
    click.echo(f"Enrolled student {student.name} in course {course.name}")

    session.close()

if __name__ == '__main__':
    cli()