"""
KLU Agent - College Database Module
SQLite database with structured college data for SQL-based queries.
The agent can query this database for real-time structured data.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


# ============================================
# Database Models
# ============================================

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    hod = Column(String(100))
    faculty_count = Column(Integer)
    description = Column(Text)
    courses = relationship("Course", back_populates="department")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    level = Column(String(20))  # UG, PG, PhD
    duration_years = Column(Integer)
    total_seats = Column(Integer)
    fee_per_year = Column(Float)
    description = Column(Text)
    department = relationship("Department", back_populates="courses")


class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    designation = Column(String(100))
    department_code = Column(String(10))
    qualification = Column(String(200))
    specialization = Column(String(200))
    email = Column(String(100))


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    event_type = Column(String(50))  # tech, cultural, workshop, seminar
    description = Column(Text)
    date = Column(String(20))
    venue = Column(String(100))
    is_upcoming = Column(Boolean, default=True)
    registration_link = Column(String(300))


class HostelInfo(Base):
    __tablename__ = "hostel_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hostel_name = Column(String(100), nullable=False)
    hostel_type = Column(String(20))  # boys, girls
    room_type = Column(String(50))
    fee_per_year = Column(Float)
    capacity = Column(Integer)
    amenities = Column(Text)


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(50))


# ============================================
# Database Initialization & Seeding
# ============================================

def init_db():
    """Create all tables."""
    Base.metadata.create_all(engine)


def seed_db():
    """Seed database with sample KLU data."""
    session = SessionLocal()

    # Check if already seeded
    if session.query(Department).count() > 0:
        session.close()
        return

    # --- Departments ---
    departments = [
        Department(name="Computer Science and Engineering", code="CSE", hod="Dr. CSE Head", faculty_count=120,
                    description="Flagship department offering cutting-edge programs in CS, AI/ML, Data Science, and Cybersecurity."),
        Department(name="Electronics and Communication Engineering", code="ECE", hod="Dr. ECE Head", faculty_count=90,
                    description="Strong department with focus on VLSI, Embedded Systems, IoT, and Signal Processing."),
        Department(name="Mechanical Engineering", code="ME", hod="Dr. ME Head", faculty_count=60,
                    description="Traditional engineering department covering Thermal, Design, Manufacturing, and Robotics."),
        Department(name="Civil Engineering", code="CE", hod="Dr. CE Head", faculty_count=45,
                    description="Department focused on Structural, Environmental, and Transportation Engineering."),
        Department(name="Electrical and Electronics Engineering", code="EEE", hod="Dr. EEE Head", faculty_count=55,
                    description="Department covering Power Systems, Control Systems, and Electrical Machines."),
        Department(name="Information Technology", code="IT", hod="Dr. IT Head", faculty_count=50,
                    description="Department focused on Web Technologies, Database Systems, and Networking."),
        Department(name="Business Administration", code="MBA", hod="Dr. MBA Head", faculty_count=40,
                    description="Management department offering MBA with specializations in Finance, Marketing, HR, and Analytics."),
        Department(name="Biotechnology", code="BT", hod="Dr. BT Head", faculty_count=30,
                    description="Department covering Genetic Engineering, Bioinformatics, and Pharma Biotech."),
    ]
    session.add_all(departments)
    session.flush()

    # --- Courses ---
    courses = [
        Course(name="B.Tech Computer Science and Engineering", code="BCSE", department_id=1, level="UG", duration_years=4, total_seats=480, fee_per_year=180000),
        Course(name="B.Tech CSE (AI & Machine Learning)", code="BCSE-AIML", department_id=1, level="UG", duration_years=4, total_seats=120, fee_per_year=200000),
        Course(name="B.Tech CSE (Data Science)", code="BCSE-DS", department_id=1, level="UG", duration_years=4, total_seats=120, fee_per_year=200000),
        Course(name="B.Tech CSE (Cyber Security)", code="BCSE-CS", department_id=1, level="UG", duration_years=4, total_seats=60, fee_per_year=200000),
        Course(name="M.Tech Computer Science", code="MCSE", department_id=1, level="PG", duration_years=2, total_seats=60, fee_per_year=120000),
        Course(name="B.Tech Electronics and Communication", code="BECE", department_id=2, level="UG", duration_years=4, total_seats=300, fee_per_year=170000),
        Course(name="B.Tech ECE (IoT)", code="BECE-IoT", department_id=2, level="UG", duration_years=4, total_seats=60, fee_per_year=190000),
        Course(name="M.Tech VLSI Design", code="MVLSI", department_id=2, level="PG", duration_years=2, total_seats=30, fee_per_year=120000),
        Course(name="B.Tech Mechanical Engineering", code="BME", department_id=3, level="UG", duration_years=4, total_seats=180, fee_per_year=160000),
        Course(name="B.Tech Civil Engineering", code="BCE", department_id=4, level="UG", duration_years=4, total_seats=120, fee_per_year=150000),
        Course(name="B.Tech EEE", code="BEEE", department_id=5, level="UG", duration_years=4, total_seats=180, fee_per_year=160000),
        Course(name="B.Tech Information Technology", code="BIT", department_id=6, level="UG", duration_years=4, total_seats=180, fee_per_year=170000),
        Course(name="MBA", code="MBA01", department_id=7, level="PG", duration_years=2, total_seats=120, fee_per_year=200000),
        Course(name="B.Tech Biotechnology", code="BBT", department_id=8, level="UG", duration_years=4, total_seats=60, fee_per_year=150000),
    ]
    session.add_all(courses)

    # --- Events ---
    events = [
        Event(name="SAMYAK 2026 - Annual Tech Fest", event_type="tech",
              description="The biggest technical festival at KLU featuring hackathons, coding contests, robotics, and guest lectures. Open for all students.",
              date="2026-03-15", venue="Main Campus", is_upcoming=True),
        Event(name="AI/ML Workshop - Hands-on Deep Learning", event_type="workshop",
              description="A 2-day hands-on workshop on Deep Learning using PyTorch, covering CNNs, RNNs, and Transformers.",
              date="2026-02-25", venue="CSE Seminar Hall", is_upcoming=True),
        Event(name="Cloud Computing Bootcamp", event_type="workshop",
              description="3-day bootcamp on AWS and Azure covering EC2, S3, Lambda, and Azure Functions with hands-on labs.",
              date="2026-03-05", venue="IT Lab Complex", is_upcoming=True),
        Event(name="Campus Recruitment Drive - TCS", event_type="placement",
              description="TCS campus recruitment for B.Tech final year students. Eligibility: 60%+ aggregate, no active backlogs.",
              date="2026-02-20", venue="Placement Cell", is_upcoming=True),
        Event(name="Cybersecurity Awareness Seminar", event_type="seminar",
              description="Expert seminar on latest cybersecurity threats, ethical hacking, and career paths in cybersecurity.",
              date="2026-03-10", venue="Main Auditorium", is_upcoming=True),
    ]
    session.add_all(events)

    # --- Hostel Info ---
    hostels = [
        HostelInfo(hostel_name="Boys Hostel Block A", hostel_type="boys", room_type="Single AC", fee_per_year=120000, capacity=200,
                   amenities="Wi-Fi, Hot water, Laundry, Common room, Study room, Power backup, Gym access"),
        HostelInfo(hostel_name="Boys Hostel Block B", hostel_type="boys", room_type="Double Sharing AC", fee_per_year=90000, capacity=500,
                   amenities="Wi-Fi, Hot water, Laundry, Common room, Study room, Power backup"),
        HostelInfo(hostel_name="Boys Hostel Block C", hostel_type="boys", room_type="Triple Sharing Non-AC", fee_per_year=60000, capacity=800,
                   amenities="Wi-Fi, Hot water, Common room, Study room, Power backup"),
        HostelInfo(hostel_name="Girls Hostel Block A", hostel_type="girls", room_type="Single AC", fee_per_year=120000, capacity=150,
                   amenities="Wi-Fi, Hot water, Laundry, Common room, Study room, Power backup, 24/7 security, CCTV"),
        HostelInfo(hostel_name="Girls Hostel Block B", hostel_type="girls", room_type="Double Sharing AC", fee_per_year=90000, capacity=400,
                   amenities="Wi-Fi, Hot water, Laundry, Common room, Study room, Power backup, 24/7 security, CCTV"),
    ]
    session.add_all(hostels)

    # --- FAQs ---
    faqs = [
        FAQ(question="What is the KLUEEE exam?", answer="KLUEEE (KL University Engineering Entrance Exam) is the university's own entrance exam for B.Tech admissions. It tests students on Physics, Chemistry, and Mathematics. The exam is conducted online and scores are valid for admission to all B.Tech programs.", category="admissions"),
        FAQ(question="Is KLU a government or private university?", answer="KLU (Koneru Lakshmaiah Education Foundation) is a Deemed-to-be-University with private funding. It received the 'Deemed University' status from UGC in 2009 and has NAAC A++ accreditation.", category="general"),
        FAQ(question="What is the hostel curfew time?", answer="The hostel curfew time is 9:00 PM for all students. Entry and exit are monitored through biometric systems. Late permissions can be obtained from the hostel warden with valid reasons.", category="hostel"),
        FAQ(question="How can I apply for a scholarship?", answer="Scholarships at KLU are awarded based on KLUEEE/JEE rank, sports achievements, and economic background. Merit scholarships are automatically applied based on entrance exam performance. For need-based scholarships, apply through the Financial Aid office with income certificates.", category="fees"),
        FAQ(question="What companies visit for placements?", answer="500+ companies visit KLU annually including Google, Microsoft, Amazon, TCS, Infosys, Wipro, Deloitte, Accenture, Capgemini, and many more. The highest package offered was 44 LPA and the average package is 6.5 LPA.", category="placements"),
        FAQ(question="Is there a dress code?", answer="Yes, KLU has a formal dress code. Students are expected to wear the university ID card at all times. Specific departments may have lab dress code requirements. Formals are required on placement days.", category="general"),
        FAQ(question="How do I access the LMS?", answer="The Learning Management System (LMS) can be accessed at the university portal using your student ID and password. It contains course materials, assignments, and recorded lectures. Contact the IT helpdesk if you face login issues.", category="academic"),
        FAQ(question="What is the anti-ragging policy?", answer="KLU has a strict zero-tolerance anti-ragging policy in compliance with UGC regulations. An Anti-Ragging Committee and Squad monitors the campus. Any ragging incidents can be reported through the online portal or the 24/7 helpline. Strict disciplinary action including expulsion is taken against offenders.", category="general"),
    ]
    session.add_all(faqs)

    session.commit()
    session.close()
    print("✅ Database seeded successfully!")


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_db()
