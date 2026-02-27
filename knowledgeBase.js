// knowledgeBase.js — Loads knowledgeBase.json synchronously via XHR for offline use
// Since we can't use fetch + async/await easily in a pure offline HTML file,
// we embed the knowledge base directly as a JS variable for maximum compatibility.

const KB = {
  "university": {
    "name": "KL University (Koneru Lakshmaiah Education Foundation)",
    "established": 1980,
    "deemed_status": 2009,
    "naac_grade": "A+",
    "nirf_ranking": "Top 50 Engineering Institutions in India",
    "location": "Green Fields, Vaddeswaram, Guntur District, Andhra Pradesh - 522302",
    "phone": "+91-863-2344700",
    "email": "admissions@kluniversity.in",
    "website": "www.kluniversity.in",
    "vice_chancellor": "Prof. K. Srinivasa Rao",
    "founder": "Dr. Koneru Satyanarayana",
    "president": "Shri K. L. Narasimha Rao",
    "tagline": "Empowering Minds, Building Futures",
    "type": "Deemed-to-be University (Private)",
    "ug_programs": 25,
    "pg_programs": 18,
    "phd_programs": 15,
    "total_acres": 78
  },

  "admissions": {
    "overview": "KL University offers admissions to UG, PG, and PhD programs every academic year. The university follows a merit-based, transparent admission process.",
    "ug_eligibility": {
      "engineering": "10+2 with Physics, Chemistry, Maths with minimum 60% marks",
      "science": "10+2 with PCB or PCM with minimum 55% marks",
      "management": "10+2 in any stream with minimum 55% marks",
      "arts": "10+2 in any stream with minimum 50% marks"
    },
    "pg_eligibility": {
      "mtech": "B.Tech/B.E with minimum 60% marks in relevant branch",
      "mba": "Any Bachelor's degree with minimum 55% marks + entrance test",
      "mca": "BCA/B.Sc CS/IT with minimum 55% marks",
      "msc": "B.Sc in relevant subject with minimum 55% marks"
    },
    "entrance_exams": [
      "EAMCET (AP/TS) - Primary route for local students",
      "JEE Main - All India Common Entrance",
      "KLUEEE - KL University's own entrance exam",
      "GATE - For M.Tech admissions",
      "CAT/MAT/XAT - For MBA admissions",
      "KLUMET - KL Management Entrance Test",
      "TOEFL/IELTS - For international students"
    ],
    "application_steps": [
      "Step 1: Visit www.kluniversity.in/admissions",
      "Step 2: Register with valid email and phone number",
      "Step 3: Fill the online application form",
      "Step 4: Upload required documents (certificates, photos, ID proof)",
      "Step 5: Pay application fee of ₹500 (non-refundable)",
      "Step 6: Appear for KLUEEE or submit qualifying exam scores",
      "Step 7: Attend counselling session",
      "Step 8: Pay fees and confirm seat"
    ],
    "counselling": {
      "mode": "Online and Offline both available",
      "rounds": 3,
      "documents_required": [
        "10th Marksheet & Certificate",
        "12th Marksheet & Certificate",
        "Transfer Certificate",
        "Migration Certificate",
        "Caste/Category Certificate (if applicable)",
        "Income Certificate (for scholarships)",
        "Passport size photographs (6 copies)",
        "Aadhar Card",
        "Entrance Exam Scorecard"
      ]
    },
    "deadlines": {
      "application_start": "January 15",
      "application_end": "June 30",
      "counselling_round1": "July 10-15",
      "counselling_round2": "July 22-27",
      "counselling_round3": "August 5-8",
      "classes_begin": "August 15"
    },
    "reservation_policy": {
      "sc_st": "15% seats reserved as per UGC norms",
      "obc": "27% seats reserved",
      "ews": "10% for Economically Weaker Sections",
      "management_quota": "15% Management Quota seats",
      "sports_quota": "2% for outstanding sports persons",
      "differently_abled": "3% for PwD candidates",
      "nri_foreign": "Separate quota for NRI/Foreign students"
    },
    "international_admissions": {
      "process": "International students can apply through the International Admissions Office",
      "requirements": "TOEFL minimum 80 / IELTS minimum 6.0 band",
      "contact": "international@kluniversity.in",
      "phone": "+91-863-2344800",
      "programs_offered": "B.Tech, MBA, M.Tech, MCA, Ph.D",
      "scholarship_amount": "Up to 50% tuition fee waiver for meritorious international students"
    },
    "contact": {
      "admissions_office": "+91-863-2344700",
      "helpline": "1800-425-2888 (Toll Free)",
      "email": "admissions@kluniversity.in",
      "office_hours": "Monday to Saturday: 9:00 AM – 5:00 PM"
    }
  },

  "courses": {
    "schools": [
      {
        "name": "School of Engineering",
        "ug_programs": [
          { "program": "B.Tech Computer Science & Engineering", "duration": "4 Years", "seats": 540, "specializations": ["AI & Machine Learning", "Data Science", "Cybersecurity", "Cloud Computing", "IoT", "Full Stack Development"] },
          { "program": "B.Tech Electronics & Communication Engineering", "duration": "4 Years", "seats": 360, "specializations": ["VLSI Design", "Embedded Systems", "Signal Processing", "5G & Communications"] },
          { "program": "B.Tech Electrical & Electronics Engineering", "duration": "4 Years", "seats": 180 },
          { "program": "B.Tech Mechanical Engineering", "duration": "4 Years", "seats": 180, "specializations": ["Thermal Engineering", "Manufacturing", "Robotics"] },
          { "program": "B.Tech Civil Engineering", "duration": "4 Years", "seats": 120 },
          { "program": "B.Tech Information Technology", "duration": "4 Years", "seats": 180 },
          { "program": "B.Tech Artificial Intelligence & Machine Learning", "duration": "4 Years", "seats": 180 },
          { "program": "B.Tech Data Science", "duration": "4 Years", "seats": 120 },
          { "program": "B.Tech Biotechnology", "duration": "4 Years", "seats": 60 }
        ],
        "pg_programs": [
          { "program": "M.Tech Computer Science & Engineering", "duration": "2 Years", "seats": 60 },
          { "program": "M.Tech VLSI Design", "duration": "2 Years", "seats": 30 },
          { "program": "M.Tech Structural Engineering", "duration": "2 Years", "seats": 30 }
        ]
      },
      {
        "name": "School of Management",
        "ug_programs": [
          { "program": "BBA (Bachelor of Business Administration)", "duration": "3 Years", "seats": 120, "specializations": ["Marketing", "Finance", "HR", "Operations", "International Business"] },
          { "program": "B.Com (Bachelor of Commerce)", "duration": "3 Years", "seats": 120 }
        ],
        "pg_programs": [
          { "program": "MBA (Master of Business Administration)", "duration": "2 Years", "seats": 180, "specializations": ["Finance", "Marketing", "HR", "Operations Management", "Business Analytics", "Digital Marketing"] }
        ]
      },
      {
        "name": "School of Sciences",
        "ug_programs": [
          { "program": "B.Sc Computer Science", "duration": "3 Years", "seats": 120 },
          { "program": "B.Sc Physics", "duration": "3 Years", "seats": 60 },
          { "program": "B.Sc Mathematics", "duration": "3 Years", "seats": 60 }
        ],
        "pg_programs": [
          { "program": "M.Sc Data Science", "duration": "2 Years", "seats": 60 },
          { "program": "M.Sc Mathematics", "duration": "2 Years", "seats": 30 }
        ]
      },
      { "name": "School of Law", "ug_programs": [{ "program": "BA.LLB (Hons.)", "duration": "5 Years", "seats": 120 }, { "program": "BBA.LLB (Hons.)", "duration": "5 Years", "seats": 120 }] },
      { "name": "School of Pharmaceutical Sciences", "ug_programs": [{ "program": "B.Pharm", "duration": "4 Years", "seats": 100 }], "pg_programs": [{ "program": "M.Pharm", "duration": "2 Years", "seats": 60 }] }
    ],
    "credit_system": {
      "type": "Choice Based Credit System (CBCS)",
      "total_credits_btech": "160 credits for B.Tech",
      "grading": "10-point grade scale (O, A+, A, B+, B, C, D, F)"
    },
    "industry_tieups": [
      "Microsoft Technology Associate Program", "IBM SkillsBuild Partnership", "Oracle Academy",
      "Amazon Web Services Educate", "Google Developer Student Clubs", "NASSCOM FutureSkills",
      "Cisco Networking Academy", "Red Hat Academy", "GitHub Student Developer Pack", "Infosys Springboard"
    ],
    "certifications": [
      "Microsoft Azure Fundamentals (AZ-900)", "AWS Certified Cloud Practitioner",
      "Google IT Support Certificate", "Oracle Java Certification",
      "IBM Data Science Professional Certificate", "Cisco CCNA"
    ]
  },

  "placements": {
    "overview": "KL University has an outstanding placement record. The Training and Placement Cell (TPC) maintains strong industry connections.",
    "placement_cell": { "director": "Dr. K. Nagi Reddy", "contact": "placements@kluniversity.in", "phone": "+91-863-2344750" },
    "yearly_stats": {
      "2025": { "students_eligible": 3800, "students_placed": 3496, "placement_percentage": "92%", "highest_package_lpa": 52, "highest_package_company": "Microsoft", "average_package_lpa": 7.8, "companies_visited": 380, "offers_made": 4200 },
      "2024": { "students_eligible": 3600, "students_placed": 3240, "placement_percentage": "90%", "highest_package_lpa": 48, "highest_package_company": "Amazon", "average_package_lpa": 7.4, "companies_visited": 350, "offers_made": 3900 },
      "2023": { "students_eligible": 3400, "students_placed": 2992, "placement_percentage": "88%", "highest_package_lpa": 45, "highest_package_company": "Microsoft", "average_package_lpa": 6.9, "companies_visited": 310, "offers_made": 3500 },
      "2022": { "students_eligible": 3200, "students_placed": 2752, "placement_percentage": "86%", "highest_package_lpa": 42, "highest_package_company": "Amazon", "average_package_lpa": 6.4, "companies_visited": 280, "offers_made": 3100 },
      "2021": { "students_eligible": 2800, "students_placed": 2296, "placement_percentage": "82%", "highest_package_lpa": 38, "highest_package_company": "Samsung", "average_package_lpa": 5.8, "companies_visited": 240, "offers_made": 2700 }
    },
    "top_recruiters": [
      { "company": "Microsoft", "role": "Software Engineer", "avg_package": "22–52 LPA" },
      { "company": "Amazon", "role": "SDE / Business Analyst", "avg_package": "18–48 LPA" },
      { "company": "Infosys", "role": "Systems Engineer", "avg_package": "4.5–8 LPA" },
      { "company": "TCS", "role": "Assistant System Engineer", "avg_package": "3.6–7 LPA" },
      { "company": "Wipro", "role": "Project Engineer", "avg_package": "3.5–6.5 LPA" },
      { "company": "Cognizant", "role": "Programmer Analyst", "avg_package": "4–6.5 LPA" },
      { "company": "Deloitte", "role": "Analyst / Consultant", "avg_package": "7–14 LPA" },
      { "company": "Capgemini", "role": "Analyst / Senior Analyst", "avg_package": "4–9 LPA" },
      { "company": "Oracle", "role": "Application Engineer", "avg_package": "10–22 LPA" },
      { "company": "HCL Technologies", "role": "Graduate Engineer Trainee", "avg_package": "3.8–6 LPA" },
      { "company": "Tech Mahindra", "role": "Software Engineer", "avg_package": "3.5–6 LPA" },
      { "company": "Accenture", "role": "Associate Software Engineer", "avg_package": "4.5–8.5 LPA" },
      { "company": "IBM", "role": "Software Developer", "avg_package": "7–16 LPA" },
      { "company": "Samsung", "role": "Software Engineer / R&D", "avg_package": "12–38 LPA" },
      { "company": "Adobe", "role": "Member of Technical Staff", "avg_package": "15–40 LPA" }
    ],
    "sector_wise": { "IT_software": "52%", "product_companies": "18%", "banking_finance": "10%", "core_engineering": "8%", "analytics_data": "7%", "consulting": "5%" },
    "internships": {
      "duration": "6-8 weeks (after 3rd year)",
      "stipend_range": "₹5,000 – ₹25,000 per month",
      "conversion_rate": "35% interns receive PPOs",
      "companies": ["TCS", "Infosys", "Wipro", "Amazon", "Microsoft", "Google", "Zoho", "Qualcomm"]
    },
    "training_programs": [
      { "name": "Aptitude Training", "desc": "30-hour aptitude, reasoning & verbal ability training" },
      { "name": "Technical Skill Development", "desc": "Coding bootcamps in C, Java, Python, DSA with SmartInterviews" },
      { "name": "Soft Skills & Communication", "desc": "GDs, mock interviews, presentation skills" },
      { "name": "Industry Certification Program", "desc": "AWS, Azure, Google Cloud certification prep" }
    ],
    "alumni_success": [
      { "name": "Ravi Kumar Teja", "batch": "2019", "company": "Microsoft", "role": "Senior Software Engineer", "package": "35 LPA" },
      { "name": "Priya Lakshmi", "batch": "2020", "company": "Amazon", "role": "SDE II", "package": "42 LPA" },
      { "name": "Sai Charan", "batch": "2021", "company": "Deloitte", "role": "Analyst – Technology", "package": "12 LPA" },
      { "name": "Sneha Reddy", "batch": "2018", "company": "Adobe", "role": "Product Manager", "package": "38 LPA" },
      { "name": "Kiran Babu", "batch": "2022", "company": "Samsung R&D", "role": "Software Engineer", "package": "18 LPA" }
    ]
  },

  "students": {
    "total_enrollment": 22000,
    "ug_students": 17000,
    "pg_students": 3500,
    "phd_scholars": 850,
    "international_students": 650,
    "countries_represented": 28,
    "graduation_rate": "94%",
    "female_student_percentage": "38%",
    "branch_wise": { "CSE": 4200, "ECE": 2800, "EEE": 1200, "Mechanical": 1400, "Civil": 900, "IT": 1500, "AI_ML": 1100, "Data_Science": 800, "MBA": 1200, "Others": 2900 },
    "achievements": [
      "Won National Smart India Hackathon 2023",
      "Students selected for ISRO internship programs",
      "KLU Cricket team won inter-university zonal championship 2024",
      "200+ research papers published in international journals",
      "50+ startups founded by KLU alumni and current students",
      "Won ACM ICPC Regional rounds multiple times",
      "Won Best Technical Fest Award at national level"
    ],
    "clubs": ["Google Developer Student Club (GDSC)", "IEEE Student Branch", "CSI Chapter", "Rotaract Club", "NSS", "NCC", "Photography Club", "Drama Club", "Music Club", "E-Cell", "Coding Club", "Robotics Club", "Data Science Club"]
  },

  "faculty": {
    "total_faculty": 1150,
    "phd_faculty": 680,
    "phd_percentage": "59%",
    "faculty_student_ratio": "1:19",
    "research_publications_per_year": 850,
    "scopus_indexed_papers": 1200,
    "patents_filed": 88,
    "patents_granted": 34,
    "visiting_professors": 45,
    "centers_of_excellence": [
      { "name": "Center of Excellence in AI & ML", "sponsor": "Microsoft & Google" },
      { "name": "Center of Excellence in Cybersecurity", "sponsor": "DRDO" },
      { "name": "Center of Excellence in IoT", "sponsor": "NASSCOM" },
      { "name": "Center of Excellence in Data Analytics", "sponsor": "IBM" },
      { "name": "Center of Excellence in Blockchain", "sponsor": "MeitY" }
    ]
  },

  "infrastructure": {
    "campus_area": "78 Acres lush green campus",
    "library": { "name": "Dr. K.L.N. Prasad Central Library", "books": "2,80,000+ volumes", "e_journals": "45,000+ e-journals", "seats": 1200, "access": "24/7 digital access" },
    "labs": { "total": 120, "major": ["AI & ML Lab", "Cloud Computing Lab", "Cybersecurity Lab", "Robotics Lab", "IoT Lab", "Big Data Lab", "VLSI Design Lab", "Networks Lab", "Biotechnology Lab"] },
    "incubation": { "name": "KL Innovation & Incubation Center (KLIC)", "startups": 72, "funding": "₹45 Crores+", "mentors": 30 },
    "sports": { "indoor": ["Badminton", "Table Tennis", "Gymnasium", "Chess", "Boxing"], "outdoor": ["Cricket Ground", "Football Field", "Basketball Courts", "Swimming Pool", "Athletics Track"] },
    "transport": { "buses": 85, "routes": 40, "gps_enabled": true, "areas": ["Guntur", "Vijayawada", "Tenali", "Mangalagiri"] },
    "hospital": { "beds": 60, "doctors": 12, "ambulance": 3, "free_for_students": true, "available": "24/7" },
    "cafeterias": { "count": 8, "capacity": 2500, "food_courts": 2, "tieups": ["Domino's outlet on campus", "Café Coffee Day", "KFC Express"] },
    "wifi": { "coverage": "100%", "speed": "10 Gbps backbone", "student_speed": "100 Mbps per device" },
    "classrooms": { "digital": 250, "smart_boards": true, "lms": "Moodle-based LMS" }
  },

  "campus_blocks": {
    "R_block": { "name": "R Block – Administration & Academic Hub", "floors": 7, "facilities": ["Vice Chancellor's Office", "Registrar Office", "Finance Department", "Controller of Examinations", "MBA Classrooms", "Smart Board Classrooms (250+ seating)"] },
    "C_block": { "name": "C Block – Engineering Labs & Lecture Halls", "floors": 6, "facilities": ["Core Engineering Labs", "Electronics Labs", "Mechanical Workshop", "Civil Engineering Lab", "CS Programming Labs", "Robotics Lab", "Project Rooms"] },
    "S_block": { "name": "S Block – Seminar, Student Services & Innovation", "floors": 5, "facilities": ["International Seminar Hall (1000+ capacity)", "Training & Placement Cell", "Grievance Cell", "Counselling Center", "E-Cell Office", "AI Innovation Lab"] },
    "K_block": { "name": "K Block – Knowledge & Research Center", "floors": 4, "facilities": ["Dr. K.L.N. Prasad Central Library", "Digital Library (45,000+ e-journals)", "Research Labs for Ph.D scholars", "E-Learning Studio"] },
    "T_block": { "name": "T Block – Technology & Computing", "floors": 5, "facilities": ["High-End Computing Cluster", "Data Center & Server Room", "AI & Big Data Lab", "Cloud Lab (AWS/Azure)", "Cybersecurity Lab"] }
  },

  "events": {
    "annual_fests": [
      {
        "name": "Samyak", "type": "Technical Fest", "month": "February",
        "participation": "10,000+ students from 200+ colleges",
        "prize_pool": "₹15 Lakhs+",
        "events": ["Hackathons (24hr & 48hr)", "Robo Wars", "Code Sprint", "Paper Presentation", "Project Expo", "Quiz Championships", "Web Design Contest", "AI/ML Challenge", "Gaming Tournament"],
        "clubs": ["IEEE", "CSI", "GDSC", "Coding Club", "Robotics Club"]
      },
      {
        "name": "Surabhi", "type": "Cultural Fest", "month": "March",
        "participation": "15,000+ students and guests",
        "prize_pool": "₹10 Lakhs+",
        "events": ["Battle of Bands", "Classical & Western Dance", "Antakshari", "Drama & Theatre", "Fashion Show", "Stand-up Comedy", "Photography Contest", "Street Play"],
        "clubs": ["Music Club", "Drama Club", "Photography Club", "Literary Club"]
      },
      {
        "name": "E-Summit", "type": "Entrepreneurship Summit", "month": "November",
        "events": ["Startup Pitches", "VC Panels", "Ideathon", "Business Plan Competition"],
        "prize_pool": "₹5 Lakhs + Funding Opportunities"
      }
    ],
    "hackathons": ["Smart India Hackathon (National)", "KLU Internal Hackathon", "AWS Cloud Hackathon", "Google Solution Challenge", "AI for Social Good", "Blockchain Innovation Workshop", "Cybersecurity CTF"],
    "guest_lectures": { "frequency": "Weekly", "speakers_per_sem": "100+ industry experts" }
  },

  "hostel": {
    "total_capacity": 8000,
    "boys_capacity": 5000,
    "girls_capacity": 3000,
    "blocks": { "boys": ["H1", "H2", "H3", "H4", "H5"], "girls": ["G1", "G2", "G3"] },
    "room_types": [
      { "type": "2-Sharing Room", "fee": "₹75,000/year", "facilities": ["Air Cooler", "Study Table", "Wardrobe", "WiFi", "Attached Bathroom"] },
      { "type": "3-Sharing Room", "fee": "₹55,000/year", "facilities": ["Fan", "Study Table", "Wardrobe", "WiFi", "Common Bathroom"] },
      { "type": "4-Sharing Room", "fee": "₹45,000/year", "facilities": ["Fan", "Study Table", "Shared Wardrobe", "WiFi", "Common Bathroom"] },
      { "type": "AC Single Room (PG)", "fee": "₹1,10,000/year", "facilities": ["AC", "Smart TV", "Mini Fridge", "WiFi", "Attached Bathroom"] }
    ],
    "facilities": ["24/7 WiFi (100 Mbps)", "24-hour security + CCTV (200 cameras)", "Biometric entry", "Laundry service (₹200/month)", "Gym (separate for boys & girls)", "RO Water on every floor", "Power backup 24hrs", "Common Room with TV", "Reading rooms", "Medical room on each block"],
    "rules": ["Boys curfew: 10 PM weekdays, 11 PM weekends", "Girls curfew: 9 PM weekdays, 10 PM weekends", "Visitors in lounge only: 9 AM – 5 PM", "Alcohol & smoking strictly prohibited", "Anti-ragging strictly enforced"],
    "warden": { "chief": "Dr. (Mrs.) Padmavathi Rao", "ratio": "1 per 200 students" }
  },

  "mess_food": {
    "overview": "Nutritious, hygienic, FSSAI-certified mess with dietitian-planned menu serving 3,000 students daily.",
    "cost": "₹3,200/month (₹38,400/year) included in hostel fee",
    "dining_capacity": 3000,
    "hygiene": ["FSSAI Certified", "Daily health officer inspection", "Pest control every 15 days", "Staff wear gloves, aprons, hairnets", "RO+UV water purification", "Organically sourced vegetables"],
    "weekly_menu": {
      "Monday": {
        "breakfast": "Idli (3 pcs) + Sambar + Coconut Chutney | Boiled Egg (non-veg) | Tea/Coffee/Milk",
        "lunch": "Rice + Dal Fry + Rajma Masala + Cabbage Stir-Fry + Papad | Chicken Curry (non-veg) | Banana",
        "snacks": "Samosa (2 pcs) + Masala Chai",
        "dinner": "Chapati (3) + Paneer Butter Masala + Rice + Buttermilk | Egg Curry (non-veg)"
      },
      "Tuesday": {
        "breakfast": "Upma with Ghee + Vada (2 pcs) + Coconut Chutney | Tea/Coffee/Milk",
        "lunch": "Rice + Sambar + Aloo Gobi + Tomato Rasam + Curd + Papad | Fruit Custard",
        "snacks": "Bread Pakoda + Nimbu Pani",
        "dinner": "Chapati + Dal Makhani + Fried Rice + Raita"
      },
      "Wednesday": {
        "breakfast": "Poha + Sprouts (veg) / Boiled Egg (non-veg) + Green Chutney | Tea/Coffee",
        "lunch": "Lemon Rice + Sambar + Bhindi Fry + Curd Rice | Fish Curry (non-veg) | Sweet Pongal",
        "snacks": "Veg Puffs + Chai",
        "dinner": "Roti + Chana Masala + Steamed Rice + Lassi"
      },
      "Thursday": {
        "breakfast": "Dosa (2) + Sambar + Tomato Chutney | Boiled Egg | Tea/Coffee/Milk",
        "lunch": "Rice + Rasam + Palak Dal + Potato Fry + Curd | Chicken Biryani (special) | Halwa",
        "snacks": "Mirchi Bajji + Tea",
        "dinner": "Chapati + Veg Korma + Rice + Buttermilk"
      },
      "Friday": {
        "breakfast": "Puri (3) + Aloo Bhaji + Coconut Chutney | Tea/Coffee/Milk",
        "lunch": "Rice + Tomato Dal + Mix Veg Curry + Rasam + Curd + Papad | Ice Cream (occasional)",
        "snacks": "Biscuits + Cold Drink / Juice",
        "dinner": "Veg Pulao + Paneer Curry + Chapati + Raita | Egg Bhurji (non-veg)"
      },
      "Saturday": {
        "breakfast": "Pesarattu + Upma + Ginger Chutney | Boiled Egg | Milk/Coffee/Tea",
        "lunch": "Rice + Sambar + Aloo Matar + Fish Gravy (non-veg) + Curd | Payasam / Kheer",
        "snacks": "Onion Pakoda + Chai",
        "dinner": "Chapati + Kadai Paneer + Dal Rice + Raita"
      },
      "Sunday": {
        "special_note": "SPECIAL SUNDAY MENU 🎉",
        "breakfast": "Idli (2) + Vada + Mini Medu Vada + Onion Uttapam + Sambar + Coconut & Tomato Chutney | Semiya Kheer / Suji Halwa | Badam Milk",
        "lunch": "Special Biryani (Veg/Chicken/Mutton) + Raita + Mirchi Ka Salan + Onion Salad | Chicken Kebab (non-veg) / Paneer Tikka (veg) starter | Gulab Jamun + Ice Cream 🍨",
        "snacks": "Popcorn + Fresh Juice Bar (Mango, Orange, Watermelon) 🥭",
        "dinner": "Naan + Butter Chicken / Shahi Paneer + Cucumber Raita + Fresh Salad | Rasmalai / Halwa as sweet 🍮"
      }
    },
    "special": ["Festival specials (Diwali sweets, Pongal meal, Holi thali)", "Vegan/Jain meals on 24-hr request", "Diabetic meal option available"]
  },

  "fees": {
    "tuition": {
      "BTech_CSE_AI_DS": "₹1,65,000/year",
      "BTech_ECE_EEE": "₹1,40,000/year",
      "BTech_Mech_Civil": "₹1,20,000/year",
      "BTech_IT": "₹1,45,000/year",
      "MTech": "₹90,000/year",
      "MBA": "₹95,000/year",
      "MCA": "₹75,000/year",
      "BBA_BCom": "₹55,000/year",
      "BSc": "₹45,000/year",
      "LLB": "₹70,000/year",
      "BPharm": "₹85,000/year"
    },
    "hostel": {
      "4_sharing": "₹45,000/year",
      "3_sharing": "₹55,000/year",
      "2_sharing": "₹75,000/year",
      "ac_single": "₹1,10,000/year",
      "mess": "₹38,400/year (₹3,200/month)"
    },
    "scholarships": [
      { "name": "Merit Scholarship (KLU)", "criteria": "JEE Rank < 5000 or 10+2 > 95%", "benefit": "100% tuition fee waiver (4 years)" },
      { "name": "Gold Scholarship (KLU)", "criteria": "JEE Rank 5001–15000 or 10+2 > 90%", "benefit": "50% tuition fee waiver" },
      { "name": "Silver Scholarship (KLU)", "criteria": "EAMCET rank < 10,000", "benefit": "25% tuition fee waiver" },
      { "name": "AP/TS State Government", "criteria": "Eligible AP/TS students", "benefit": "Full/partial tuition reimbursement" },
      { "name": "SC/ST Scholarship", "criteria": "SC/ST students with income < ₹2.5 LPA", "benefit": "Full fee waiver + stipend" },
      { "name": "Sports Quota Scholarship", "criteria": "National/State level sports achievement", "benefit": "25–50% fee waiver" }
    ],
    "payment_methods": ["Online via KLU portal", "Net Banking", "Credit/Debit Card", "UPI (GPay, PhonePe, Paytm)", "Demand Draft", "NEFT/RTGS", "Education Loan"],
    "installments": { "semesters": 2, "deadlines": ["July 31 (Semester 1)", "January 15 (Semester 2)"], "late_fee": "₹100/day" },
    "loan_partners": ["SBI", "HDFC Credila", "ICICI Bank", "Axis Bank", "Canara Bank"]
  },

  "academic_calendar": {
    "year": "August – May",
    "odd_semester": { "start": "August 15", "end": "January 15", "mid_exams": "October 1–10", "end_exams": "December 20 – January 10", "results": "January 25" },
    "even_semester": { "start": "January 20", "end": "June 15", "mid_exams": "March 1–10", "end_exams": "May 10 – June 5", "results": "June 20" },
    "add_drop": "First 2 weeks of each semester",
    "registration": "Online, 2 weeks before semester start",
    "holidays": ["Republic Day – Jan 26", "Ugadi", "Good Friday", "Independence Day – Aug 15", "Dussehra – 5 days", "Diwali – 3 days", "Christmas – Dec 25", "Sankranthi – 3 days", "Summer Vacation: May 20 – Aug 14", "Winter Vacation: Jan 11–19"]
  }
};
