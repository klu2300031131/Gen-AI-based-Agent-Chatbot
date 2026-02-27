# ============================================================
#  KLU Smart Assistant — College Database Connector
#  MySQL + SQLAlchemy ORM
#  Fetches real-time structured data: timetables, results,
#  fee status, staff records, etc.
# ============================================================

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from sqlalchemy import (
    create_engine, Column, Integer, String, Float,
    Boolean, DateTime, Text, ForeignKey, text
)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.pool import QueuePool
from config import DB_CONFIG

logger = logging.getLogger("KLU.Database")
Base   = declarative_base()


# ============================================================
#  ORM MODELS (University Database Schema)
# ============================================================

class Student(Base):
    __tablename__ = "students"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    roll_number    = Column(String(20), unique=True, nullable=False, index=True)
    name           = Column(String(100), nullable=False)
    branch         = Column(String(60))
    year           = Column(Integer)
    section        = Column(String(5))
    email          = Column(String(120), unique=True)
    phone          = Column(String(15))
    hostel_block   = Column(String(10))
    room_number    = Column(String(10))
    fee_status     = Column(String(20), default="pending")
    cgpa           = Column(Float)
    active         = Column(Boolean, default=True)
    created_at     = Column(DateTime, default=datetime.utcnow)
    enrollments    = relationship("CourseEnrollment", back_populates="student")


class Faculty(Base):
    __tablename__ = "faculty"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    employee_id    = Column(String(20), unique=True, nullable=False, index=True)
    name           = Column(String(100), nullable=False)
    department     = Column(String(80))
    designation    = Column(String(80))
    phd            = Column(Boolean, default=False)
    email          = Column(String(120), unique=True)
    phone          = Column(String(15))
    cabin_number   = Column(String(20))
    publications   = Column(Integer, default=0)
    active         = Column(Boolean, default=True)
    courses        = relationship("Course", back_populates="instructor")


class Course(Base):
    __tablename__ = "courses"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    course_code    = Column(String(20), unique=True, nullable=False, index=True)
    course_name    = Column(String(150), nullable=False)
    department     = Column(String(80))
    credits        = Column(Integer)
    semester       = Column(Integer)
    instructor_id  = Column(Integer, ForeignKey("faculty.id"))
    max_seats      = Column(Integer)
    syllabus       = Column(Text)
    instructor     = relationship("Faculty", back_populates="courses")
    enrollments    = relationship("CourseEnrollment", back_populates="course")


class CourseEnrollment(Base):
    __tablename__ = "enrollments"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    student_id     = Column(Integer, ForeignKey("students.id"))
    course_id      = Column(Integer, ForeignKey("courses.id"))
    semester       = Column(Integer)
    grade          = Column(String(5))
    attendance_pct = Column(Float, default=0.0)
    enrolled_on    = Column(DateTime, default=datetime.utcnow)
    student        = relationship("Student", back_populates="enrollments")
    course         = relationship("Course", back_populates="enrollments")


class Timetable(Base):
    __tablename__ = "timetable"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    branch         = Column(String(60), nullable=False, index=True)
    year           = Column(Integer, nullable=False)
    section        = Column(String(5))
    day            = Column(String(15))
    period         = Column(Integer)
    start_time     = Column(String(10))
    end_time       = Column(String(10))
    course_code    = Column(String(20), ForeignKey("courses.course_code"))
    room           = Column(String(20))
    semester       = Column(Integer)


class ExamSchedule(Base):
    __tablename__ = "exam_schedule"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    exam_type      = Column(String(30))      # "mid1", "mid2", "end_sem"
    course_code    = Column(String(20), ForeignKey("courses.course_code"))
    branch         = Column(String(60))
    year           = Column(Integer)
    exam_date      = Column(DateTime)
    start_time     = Column(String(10))
    hall_number    = Column(String(20))
    semester       = Column(Integer)


class FeeRecord(Base):
    __tablename__ = "fee_records"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    student_id     = Column(Integer, ForeignKey("students.id"))
    semester       = Column(Integer)
    academic_year  = Column(String(15))
    amount_due     = Column(Float)
    amount_paid    = Column(Float, default=0.0)
    due_date       = Column(DateTime)
    paid_on        = Column(DateTime, nullable=True)
    payment_mode   = Column(String(30))
    receipt_no     = Column(String(40))
    status         = Column(String(20), default="pending")


class Hostel(Base):
    __tablename__ = "hostel"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    block          = Column(String(10), nullable=False)
    room_number    = Column(String(10), nullable=False)
    room_type      = Column(String(30))      # "2-sharing", "3-sharing", etc.
    capacity       = Column(Integer)
    current_count  = Column(Integer, default=0)
    floor          = Column(Integer)
    is_ac          = Column(Boolean, default=False)
    fee_per_year   = Column(Float)


# ============================================================
#  DATABASE CONNECTION & QUERY MANAGER
# ============================================================

class UniversityDB:
    """
    Database access layer for KLU's university database.
    Provides structured queries for the RAG + Agent pipeline.
    """

    def __init__(self):
        self.engine  = None
        self.Session = None
        self._connect()

    def _connect(self):
        dsn = (
            f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        logger.info(f"🔗 Connecting to MySQL: {DB_CONFIG['host']}:{DB_CONFIG['port']}"
                    f"/{DB_CONFIG['database']}")
        self.engine = create_engine(
            dsn,
            pool_size       = DB_CONFIG["pool_size"],
            pool_pre_ping   = True,
            pool_recycle    = 3600,
            poolclass       = QueuePool,
            connect_args    = {"connect_timeout": DB_CONFIG["timeout"]},
        )
        self.Session = sessionmaker(bind=self.engine)
        logger.info("✅ Database engine created successfully")

    def create_tables(self):
        """Create all tables if they don't exist."""
        Base.metadata.create_all(self.engine)
        logger.info("📋 All university DB tables ensured")

    # ── Student Queries ──────────────────────────────────────
    def get_student(self, roll_number: str) -> Optional[Dict]:
        with self.Session() as s:
            student = s.query(Student).filter_by(roll_number=roll_number).first()
            if not student:
                return None
            return {
                "roll_number"  : student.roll_number,
                "name"         : student.name,
                "branch"       : student.branch,
                "year"         : student.year,
                "section"      : student.section,
                "cgpa"         : student.cgpa,
                "fee_status"   : student.fee_status,
                "hostel_block" : student.hostel_block,
                "room_number"  : student.room_number,
            }

    def search_students(self, branch: str = None, year: int = None) -> List[Dict]:
        with self.Session() as s:
            q = s.query(Student).filter_by(active=True)
            if branch: q = q.filter(Student.branch.ilike(f"%{branch}%"))
            if year  : q = q.filter_by(year=year)
            return [{"name": st.name, "roll": st.roll_number,
                     "branch": st.branch} for st in q.limit(50).all()]

    # ── Faculty Queries ──────────────────────────────────────
    def get_faculty_by_dept(self, department: str) -> List[Dict]:
        with self.Session() as s:
            rows = s.query(Faculty).filter(
                Faculty.department.ilike(f"%{department}%"),
                Faculty.active == True
            ).all()
            return [{"name": f.name, "designation": f.designation,
                     "email": f.email, "phd": f.phd} for f in rows]

    # ── Timetable Queries ────────────────────────────────────
    def get_timetable(self, branch: str, year: int, day: str) -> List[Dict]:
        with self.Session() as s:
            rows = s.query(Timetable).filter_by(
                branch=branch, year=year, day=day
            ).order_by(Timetable.period).all()
            return [{"period": r.period, "start": r.start_time,
                     "end": r.end_time, "course": r.course_code,
                     "room": r.room} for r in rows]

    # ── Exam Schedule ────────────────────────────────────────
    def get_exam_schedule(self, branch: str, year: int) -> List[Dict]:
        with self.Session() as s:
            rows = s.query(ExamSchedule).filter_by(
                branch=branch, year=year
            ).order_by(ExamSchedule.exam_date).all()
            return [{"course": r.course_code, "type": r.exam_type,
                     "date": str(r.exam_date), "hall": r.hall_number} for r in rows]

    # ── Fee Records ──────────────────────────────────────────
    def get_fee_status(self, roll_number: str) -> Optional[Dict]:
        with self.Session() as s:
            student = s.query(Student).filter_by(roll_number=roll_number).first()
            if not student:
                return None
            record = s.query(FeeRecord).filter_by(
                student_id=student.id
            ).order_by(FeeRecord.due_date.desc()).first()
            if not record:
                return {"roll": roll_number, "status": "no_records"}
            return {
                "roll"        : roll_number,
                "amount_due"  : record.amount_due,
                "amount_paid" : record.amount_paid,
                "due_date"    : str(record.due_date),
                "status"      : record.status,
                "receipt"     : record.receipt_no,
            }

    # ── Generic SQL Execution (for Agent tool use) ───────────
    def execute_query(self, sql: str, params: dict = None) -> List[Dict]:
        """
        Safe read-only SQL execution.
        Used by the LangChain SQL agent for natural language → SQL queries.
        """
        if any(kw in sql.upper() for kw in
               ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]):
            raise PermissionError("Only SELECT queries are allowed.")

        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            cols   = result.keys()
            return [dict(zip(cols, row)) for row in result.fetchall()]

    def close(self):
        self.engine.dispose()
        logger.info("🔌 Database connection pool closed.")
