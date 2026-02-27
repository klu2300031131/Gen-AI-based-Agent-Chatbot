// ============================================
//  KLU Smart Assistant — Chatbot Engine
//  Keyword Detection + Rich Formatted Responses
// ============================================

'use strict';

// ---- State ----
let isTyping = false;
let messageCount = 0;
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

// ---- Sidebar Toggle ----
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');

// Create overlay element
const overlay = document.createElement('div');
overlay.className = 'sidebar-overlay';
document.body.appendChild(overlay);

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
});

overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
});

// ---- New Chat Button ----
document.getElementById('newChatBtn').addEventListener('click', () => {
    // Clear all messages
    chatMessages.innerHTML = '';
    messageCount = 0;
    isTyping = false;
    sendBtn.disabled = false;

    // Re-create welcome card
    const welcomeCard = document.createElement('div');
    welcomeCard.className = 'welcome-card';
    welcomeCard.id = 'welcomeCard';
    welcomeCard.innerHTML = `
      <div class="welcome-icon">🏫</div>
      <h2>Welcome to KLU Smart Assistant!</h2>
      <p>Your intelligent guide for everything about <strong>KL University</strong>. Ask me anything — admissions, placements, hostel, fees, and more!</p>
      <div class="welcome-chips">
        <span class="chip" onclick="sendChip('placements 2025')">📊 Placements 2025</span>
        <span class="chip" onclick="sendChip('mess menu')">🍛 Mess Menu</span>
        <span class="chip" onclick="sendChip('fees scholarships')">💰 Fees</span>
        <span class="chip" onclick="sendChip('admissions')">🎓 Admissions</span>
        <span class="chip" onclick="sendChip('hostel')">🏠 Hostel</span>
        <span class="chip" onclick="sendChip('events')">🎉 Events</span>
      </div>`;
    chatMessages.appendChild(welcomeCard);

    // Greet again after short delay
    setTimeout(() => {
        addBotMessage(`<p>🔄 Chat cleared! I'm ready to help you again. What would you like to know about <strong>KL University</strong>? 😊</p>`);
    }, 400);

    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
    }

    userInput.value = '';
    userInput.focus();
});

// ---- Sidebar Quick Topic Buttons ----
document.querySelectorAll('.topic-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const query = btn.getAttribute('data-query');
        sendChipOrQuery(query);
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        }
    });
});

// ---- Enter Key ----
userInput.addEventListener('keypress', e => {
    if (e.key === 'Enter' && !isTyping) handleSend();
});

// ---- Send from chip or suggestion ----
function sendChip(query) { sendChipOrQuery(query); }

function sendChipOrQuery(query) {
    userInput.value = query;
    handleSend();
}

// ---- Handle Send ----
function handleSend() {
    const text = userInput.value.trim();
    if (!text || isTyping) return;

    // Remove welcome card after first message
    const welcome = document.getElementById('welcomeCard');
    if (welcome) welcome.remove();

    addUserMessage(text);
    userInput.value = '';
    userInput.focus();

    // Disable input while responding
    isTyping = true;
    sendBtn.disabled = true;

    // Show typing indicator
    const typingId = showTyping();

    // Simulate human-like typing delay based on response size
    const delay = 700 + Math.random() * 700;

    setTimeout(() => {
        removeTyping(typingId);
        const response = generateResponse(text);
        addBotMessage(response);
        isTyping = false;
        sendBtn.disabled = false;
        userInput.focus();
    }, delay);
}

// ---- Add User Message ----
function addUserMessage(text) {
    messageCount++;
    const row = document.createElement('div');
    row.className = 'message-row user-row';
    row.innerHTML = `
    <div class="msg-avatar user-avatar-msg">👤</div>
    <div>
      <div class="message-bubble user-bubble">${escapeHtml(text)}</div>
      <div class="msg-time">${getTime()}</div>
    </div>
  `;
    chatMessages.appendChild(row);
    scrollToBottom();
}

// ---- Add Bot Message ----
function addBotMessage(html) {
    messageCount++;
    const row = document.createElement('div');
    row.className = 'message-row bot-row';
    row.innerHTML = `
    <div class="msg-avatar bot-avatar-msg">🤖</div>
    <div style="max-width: calc(100% - 50px);">
      <div class="message-bubble bot-bubble">${html}</div>
      <div class="msg-time">${getTime()}</div>
    </div>
  `;
    chatMessages.appendChild(row);
    scrollToBottom();
}

// ---- Typing Indicator ----
function showTyping() {
    const id = 'typing-' + Date.now();
    const row = document.createElement('div');
    row.className = 'typing-row';
    row.id = id;
    row.innerHTML = `
    <div class="msg-avatar bot-avatar-msg">🤖</div>
    <div class="typing-bubble">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>
  `;
    chatMessages.appendChild(row);
    scrollToBottom();
    return id;
}

function removeTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// ---- Helpers ----
function scrollToBottom() {
    chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
}

function getTime() {
    return new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ============================================
//  KEYWORD DETECTION ENGINE
// ============================================

const KEYWORD_MAP = [
    { keys: ['admission', 'apply', 'application', 'eligibility', 'entrance', 'joining', 'how to join', 'join klu', 'eamcet', 'jee', 'klueee', 'counselling', 'document', 'deadlin', 'reservation', 'quota', 'international', 'nri'], handler: respondAdmissions },
    { keys: ['course', 'program', 'btech', 'b.tech', 'mtech', 'm.tech', 'mba', 'mca', 'bba', 'bsc', 'b.sc', 'law', 'llb', 'pharm', 'school', 'department', 'branch', 'engineering', 'specializ', 'credit', 'certification', 'industry tie', 'curriculum'], handler: respondCourses },
    { keys: ['placement', 'recruit', 'package', 'salary', 'job', 'company', 'lpa', 'hiring', 'campus drive', 'offer', 'microsoft', 'amazon', 'infosys', 'tcs', 'wipro', 'cognizant', 'deloitte', 'capgemini', 'oracle', 'hcl', 'tech mahindra', 'accenture', 'ibm', 'samsung', 'adobe', 'internship', 'ppo', 'training', 'alumni'], handler: respondPlacements },
    { keys: ['student', 'enrollment', 'strength', 'total student', 'how many student', 'international student', 'graduation', 'achievement', 'club', 'society', 'nss', 'ncc'], handler: respondStudents },
    { keys: ['faculty', 'teacher', 'professor', 'phd', 'research', 'publication', 'patent', 'center of excellence', 'coe', 'visiting professsor', 'ratio'], handler: respondFaculty },
    { keys: ['infrastructure', 'campus', 'library', 'lab', 'incubation', 'sport', 'transport', 'bus', 'hospital', 'cafeteria', 'wifi', 'internet', 'classroom', 'facility', 'facilities'], handler: respondInfrastructure },
    { keys: ['block', 'r block', 'c block', 's block', 'k block', 't block', 'building', 'admin block', 'seminar hall'], handler: respondBlocks },
    { keys: ['event', 'fest', 'samyak', 'surabhi', 'festival', 'hackathon', 'cultural', 'technical', 'e-summit', 'esummit', 'workshop', 'guest lecture', 'coding contest', 'robo war'], handler: respondEvents },
    { keys: ['hostel', 'accomodation', 'accommodation', 'room', 'pg', 'warden', 'curfew', 'dormitory', 'dorm', 'staying', 'stay'], handler: respondHostel },
    { keys: ['mess', 'food', 'menu', 'breakfast', 'lunch', 'dinner', 'canteen', 'meal', 'diet', 'eat', 'weekly menu', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'biryani', 'idli', 'dosa', 'snack'], handler: respondMess },
    { keys: ['fee', 'fees', 'tuition', 'cost', 'scholarship', 'financial', 'payment', 'installment', 'loan', 'education loan', 'waiver', 'merit', 'gold', 'silver'], handler: respondFees },
    { keys: ['academic calendar', 'semester', 'exam', 'schedule', 'holiday', 'result', 'registration', 'add drop', 'supplementary', 'mid exam', 'end exam', 'calendar'], handler: respondCalendar },
    { keys: ['about klu', 'about kl university', 'kl university', 'klu', 'overview', 'general', 'naac', 'nirf', 'rank', 'established', 'founded', 'vice chancellor', 'founder'], handler: respondUniversity },
    { keys: ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'hii', 'helo', 'hai'], handler: respondGreeting },
    { keys: ['thank', 'thanks', 'thankyou', 'ty'], handler: respondThanks },
    { keys: ['help', 'what can you', 'what do you know', 'topics', 'what can i ask'], handler: respondHelp },
];

function generateResponse(input) {
    const lower = input.toLowerCase().trim();

    // Match keywords
    for (const entry of KEYWORD_MAP) {
        for (const key of entry.keys) {
            if (lower.includes(key)) {
                return entry.handler(lower);
            }
        }
    }

    return respondFallback(input);
}

// ============================================
//  RESPONSE GENERATORS
// ============================================

function respondGreeting(input) {
    const greetings = [
        'Hello! 👋 Welcome to KLU Smart Assistant. I\'m here to help you with everything about <strong>KL University</strong>.',
        'Hi there! 😊 I\'m your KLU AI guide. Ask me anything about admissions, placements, hostel, fees, events, and more!',
        'Hey! Welcome! 🎓 I have complete information about KL University. What would you like to know?',
    ];
    const g = greetings[Math.floor(Math.random() * greetings.length)];
    return `<p>${g}</p>
<h3>Quick topics you can ask about:</h3>
<ul>
<li>🎓 Admissions & Eligibility</li>
<li>💼 Placements & Salary Packages</li>
<li>🍛 Weekly Mess Menu</li>
<li>🏠 Hostel Facilities & Fees</li>
<li>💰 Tuition Fees & Scholarships</li>
<li>🎉 Events: Samyak & Surabhi</li>
<li>📚 Courses & Programs</li>
<li>📅 Academic Calendar</li>
</ul>`;
}

function respondHelp() {
    return `<h2>💡 How I Can Help You</h2>
<p>I'm a fully offline AI assistant with complete knowledge about <strong>KL University</strong>. Here's what I know:</p>
<ul>
<li><strong>🎓 Admissions</strong> — Eligibility, application process, counselling, documents, deadlines</li>
<li><strong>📚 Courses</strong> — All B.Tech, M.Tech, MBA, BBA programs and specializations</li>
<li><strong>💼 Placements</strong> — Year-wise stats (2021–2025), top recruiters, salaries, internships</li>
<li><strong>👨‍🎓 Students</strong> — Total enrollment, achievements, clubs and activities</li>
<li><strong>👩‍🏫 Faculty</strong> — Total teachers, PhD faculty, research, patents, CoEs</li>
<li><strong>🏛️ Infrastructure</strong> — Library, labs, sports, hospital, WiFi, transport</li>
<li><strong>🏢 Campus Blocks</strong> — R, C, S, K, T blocks details</li>
<li><strong>🎉 Events</strong> — Samyak, Surabhi, E-Summit, hackathons</li>
<li><strong>🏠 Hostel</strong> — Room types, fees, rules, facilities</li>
<li><strong>🍛 Mess Menu</strong> — Full 7-day weekly menu with all meals</li>
<li><strong>💰 Fees</strong> — Tuition, hostel, scholarships, payment options, loans</li>
<li><strong>📅 Academic Calendar</strong> — Semester dates, exams, holidays</li>
</ul>
<p>Just type your question naturally — I'll find the answer! 😊</p>`;
}

function respondThanks() {
    const replies = [
        'You\'re welcome! 😊 Feel free to ask anything else about KLU.',
        'Happy to help! 🎓 Is there anything else you\'d like to know about KL University?',
        'My pleasure! Ask me anything — I\'m here 24/7! 🤖'
    ];
    return `<p>${replies[Math.floor(Math.random() * replies.length)]}</p>`;
}

function respondUniversity() {
    const u = KB.university;
    return `<h2>🏫 About KL University</h2>
<p>${u.name} is one of India's premier deemed-to-be universities, established in <strong>${u.established}</strong> and granted deemed status in <strong>${u.deemed_status}</strong>.</p>

<div class="stat-box">
  <div class="stat-item"><div class="stat-value">${u.naac_grade}</div><div class="stat-label">NAAC Grade</div></div>
  <div class="stat-item"><div class="stat-value">Top 50</div><div class="stat-label">NIRF Ranking</div></div>
  <div class="stat-item"><div class="stat-value">${u.total_acres} Acres</div><div class="stat-label">Campus Area</div></div>
  <div class="stat-item"><div class="stat-value">${u.ug_programs}+ UG</div><div class="stat-label">Programs</div></div>
</div>

<h3>📍 Key Details</h3>
<ul>
<li><strong>Type:</strong> ${u.type}</li>
<li><strong>Location:</strong> ${u.location}</li>
<li><strong>Founder:</strong> ${u.founder}</li>
<li><strong>Vice Chancellor:</strong> ${u.vice_chancellor}</li>
<li><strong>Tagline:</strong> "${u.tagline}"</li>
<li><strong>Website:</strong> ${u.website}</li>
<li><strong>Phone:</strong> ${u.phone}</li>
<li><strong>Email:</strong> ${u.email}</li>
</ul>

<h3>🎓 Academic Portfolio</h3>
<ul>
<li><strong>UG Programs:</strong> ${u.ug_programs}+</li>
<li><strong>PG Programs:</strong> ${u.pg_programs}+</li>
<li><strong>Ph.D Programs:</strong> ${u.phd_programs}</li>
</ul>
<p>KLU is known for its world-class infrastructure, excellent placement record, and active research environment. 🌟</p>`;
}

function respondAdmissions() {
    const a = KB.admissions;
    return `<h2>🎓 KLU Admissions Guide</h2>
<p>${a.overview}</p>

<h3>📋 UG Eligibility</h3>
<ul>
<li><strong>Engineering:</strong> ${a.ug_eligibility.engineering}</li>
<li><strong>Science:</strong> ${a.ug_eligibility.science}</li>
<li><strong>Management:</strong> ${a.ug_eligibility.management}</li>
</ul>

<h3>📝 PG Eligibility</h3>
<ul>
<li><strong>M.Tech:</strong> ${a.pg_eligibility.mtech}</li>
<li><strong>MBA:</strong> ${a.pg_eligibility.mba}</li>
<li><strong>MCA:</strong> ${a.pg_eligibility.mca}</li>
</ul>

<h3>🧪 Accepted Entrance Exams</h3>
<ul>${a.entrance_exams.map(e => `<li>${e}</li>`).join('')}</ul>

<h3>📌 Application Steps</h3>
<ul>${a.application_steps.map(s => `<li>${s}</li>`).join('')}</ul>

<h3>📅 Important Deadlines</h3>
<ul>
<li><strong>Application Opens:</strong> ${a.deadlines.application_start}</li>
<li><strong>Application Closes:</strong> ${a.deadlines.application_end}</li>
<li><strong>Counselling Round 1:</strong> ${a.deadlines.counselling_round1}</li>
<li><strong>Counselling Round 2:</strong> ${a.deadlines.counselling_round2}</li>
<li><strong>Classes Begin:</strong> ${a.deadlines.classes_begin}</li>
</ul>

<h3>📂 Documents Required</h3>
<ul>${a.counselling.documents_required.map(d => `<li>${d}</li>`).join('')}</ul>

<h3>🔢 Reservation Policy</h3>
<ul>
<li><strong>SC/ST:</strong> ${a.reservation_policy.sc_st}</li>
<li><strong>OBC:</strong> ${a.reservation_policy.obc}</li>
<li><strong>EWS:</strong> ${a.reservation_policy.ews}</li>
<li><strong>Management Quota:</strong> ${a.reservation_policy.management_quota}</li>
<li><strong>Sports Quota:</strong> ${a.reservation_policy.sports_quota}</li>
</ul>

<h3>🌍 International Admissions</h3>
<ul>
<li><strong>Requirements:</strong> TOEFL ≥ 80 or IELTS ≥ 6.0</li>
<li><strong>Scholarship:</strong> ${a.international_admissions.scholarship_amount}</li>
<li><strong>Email:</strong> ${a.international_admissions.contact}</li>
</ul>

<h3>📞 Contact Admissions</h3>
<ul>
<li><strong>Phone:</strong> ${a.contact.admissions_office}</li>
<li><strong>Helpline:</strong> ${a.contact.helpline}</li>
<li><strong>Email:</strong> ${a.contact.email}</li>
<li><strong>Hours:</strong> ${a.contact.office_hours}</li>
</ul>`;
}

function respondCourses() {
    const c = KB.courses;
    let schoolHTML = '';
    for (const school of c.schools) {
        const ugList = (school.ug_programs || []).map(p => {
            const spec = p.specializations ? ` <span class="info-tag">${p.specializations.slice(0, 2).join(', ')}</span>` : '';
            return `<li><strong>${p.program}</strong> (${p.duration}, ${p.seats} seats)${spec}</li>`;
        }).join('');
        const pgList = (school.pg_programs || []).map(p => `<li><strong>${p.program}</strong> (${p.duration})</li>`).join('');
        schoolHTML += `<h3>🏫 ${school.name}</h3>
<p><em>UG Programs:</em></p><ul>${ugList}</ul>
${pgList ? `<p><em>PG Programs:</em></p><ul>${pgList}</ul>` : ''}`;
    }

    return `<h2>📚 Courses & Programs at KLU</h2>
<p>KL University offers <strong>${KB.university.ug_programs}+ UG</strong> and <strong>${KB.university.pg_programs}+ PG</strong> programs across multiple schools.</p>

${schoolHTML}

<hr class="divider">
<h3>🎓 Credit System</h3>
<ul>
<li><strong>System:</strong> ${c.credit_system.type}</li>
<li><strong>Credits:</strong> ${c.credit_system.total_credits_btech}</li>
<li><strong>Grading:</strong> ${c.credit_system.grading}</li>
</ul>

<h3>🤝 Industry Tie-Ups</h3>
<div class="recruiter-grid">${c.industry_tieups.map(t => `<span class="recruiter-chip">${t}</span>`).join('')}</div>

<h3>🏅 Certifications Offered</h3>
<ul>${c.certifications.map(cert => `<li>${cert}</li>`).join('')}</ul>`;
}

function respondPlacements(input) {
    const p = KB.placements;

    // Detailed year-specific
    let yearStats = '';
    const years = Object.keys(p.yearly_stats).sort((a, b) => b - a);
    for (const yr of years) {
        const s = p.yearly_stats[yr];
        yearStats += `
    <div class="menu-day">
      <span class="menu-meal">📊 ${yr} Placements</span>
      <ul>
        <li>Students Eligible: <strong>${s.students_eligible.toLocaleString()}</strong></li>
        <li>Students Placed: <strong>${s.students_placed.toLocaleString()}</strong></li>
        <li>Placement %: <strong>${s.placement_percentage}</strong></li>
        <li>Highest Package: <strong>₹${s.highest_package_lpa} LPA</strong> (${s.highest_package_company})</li>
        <li>Average Package: <strong>₹${s.average_package_lpa} LPA</strong></li>
        <li>Companies Visited: <strong>${s.companies_visited}</strong></li>
        <li>Offers Made: <strong>${s.offers_made.toLocaleString()}</strong></li>
      </ul>
    </div>`;
    }

    const topRec = p.top_recruiters.map(r =>
        `<li><strong>${r.company}</strong> — ${r.role} | Avg: ${r.avg_package}</li>`
    ).join('');

    const alumni = p.alumni_success.map(a =>
        `<li><strong>${a.name}</strong> (${a.batch}) → ${a.company} as ${a.role} | 💰 ${a.package}</li>`
    ).join('');

    return `<h2>💼 KLU Placement Report (2021–2025)</h2>
<p>${p.overview}</p>

<div class="stat-box">
  <div class="stat-item"><div class="stat-value">92%</div><div class="stat-label">Placement 2025</div></div>
  <div class="stat-item"><div class="stat-value">₹52 LPA</div><div class="stat-label">Highest 2025</div></div>
  <div class="stat-item"><div class="stat-value">₹7.8 LPA</div><div class="stat-label">Avg 2025</div></div>
  <div class="stat-item"><div class="stat-value">380+</div><div class="stat-label">Companies 2025</div></div>
</div>

<h3>📈 Year-wise Placement Statistics</h3>
${yearStats}

<h3>🏢 Top Recruiters</h3>
<ul>${topRec}</ul>

<h3>📊 Sector-wise Hiring</h3>
<ul>
  <li><strong>IT & Software:</strong> ${p.sector_wise.IT_software}</li>
  <li><strong>Product Companies:</strong> ${p.sector_wise.product_companies}</li>
  <li><strong>Banking & Finance:</strong> ${p.sector_wise.banking_finance}</li>
  <li><strong>Core Engineering:</strong> ${p.sector_wise.core_engineering}</li>
  <li><strong>Data & Analytics:</strong> ${p.sector_wise.analytics_data}</li>
  <li><strong>Consulting:</strong> ${p.sector_wise.consulting}</li>
</ul>

<h3>💼 Internship Program</h3>
<ul>
  <li><strong>Duration:</strong> ${p.internships.duration}</li>
  <li><strong>Stipend:</strong> ${p.internships.stipend_range}</li>
  <li><strong>PPO Conversion Rate:</strong> ${p.internships.conversion_rate}</li>
  <li><strong>Key Intern Companies:</strong> ${p.internships.companies.join(', ')}</li>
</ul>

<h3>🧪 Training Programs</h3>
<ul>${p.training_programs.map(t => `<li><strong>${t.name}:</strong> ${t.desc}</li>`).join('')}</ul>

<h3>🌟 Alumni Success Stories</h3>
<ul>${alumni}</ul>

<h3>📞 Placement Cell Contact</h3>
<ul>
  <li><strong>Director:</strong> ${p.placement_cell.director}</li>
  <li><strong>Email:</strong> ${p.placement_cell.contact}</li>
  <li><strong>Phone:</strong> ${p.placement_cell.phone}</li>
</ul>`;
}

function respondStudents() {
    const s = KB.students;
    const bw = Object.entries(s.branch_wise).map(([k, v]) => `<li><strong>${k.replace('_', '/')}:</strong> ${v.toLocaleString()} students</li>`).join('');
    return `<h2>👨‍🎓 KLU Student Community</h2>

<div class="stat-box">
  <div class="stat-item"><div class="stat-value">${s.total_enrollment.toLocaleString()}</div><div class="stat-label">Total Students</div></div>
  <div class="stat-item"><div class="stat-value">${s.international_students}</div><div class="stat-label">International</div></div>
  <div class="stat-item"><div class="stat-value">${s.countries_represented}</div><div class="stat-label">Countries</div></div>
  <div class="stat-item"><div class="stat-value">${s.graduation_rate}</div><div class="stat-label">Grad Rate</div></div>
</div>

<h3>📊 Enrollment Breakdown</h3>
<ul>
  <li><strong>UG Students:</strong> ${s.ug_students.toLocaleString()}</li>
  <li><strong>PG Students:</strong> ${s.pg_students.toLocaleString()}</li>
  <li><strong>Ph.D Scholars:</strong> ${s.phd_scholars}</li>
  <li><strong>Female Students:</strong> ${s.female_student_percentage} of total</li>
</ul>

<h3>🏫 Branch-wise Strength</h3>
<ul>${bw}</ul>

<h3>🏆 Student Achievements</h3>
<ul>${s.achievements.map(a => `<li>${a}</li>`).join('')}</ul>

<h3>🎭 Student Clubs & Organizations</h3>
<div class="recruiter-grid">${s.clubs.map(c => `<span class="recruiter-chip">${c}</span>`).join('')}</div>`;
}

function respondFaculty() {
    const f = KB.faculty;
    return `<h2>👩‍🏫 Faculty at KL University</h2>

<div class="stat-box">
  <div class="stat-item"><div class="stat-value">${f.total_faculty.toLocaleString()}</div><div class="stat-label">Total Faculty</div></div>
  <div class="stat-item"><div class="stat-value">${f.phd_percentage}</div><div class="stat-label">PhD Faculty</div></div>
  <div class="stat-item"><div class="stat-value">${f.faculty_student_ratio}</div><div class="stat-label">Faculty:Student</div></div>
  <div class="stat-item"><div class="stat-value">${f.research_publications_per_year}+</div><div class="stat-label">Publications/Year</div></div>
</div>

<h3>📊 Faculty Statistics</h3>
<ul>
  <li><strong>Total Faculty:</strong> ${f.total_faculty} members</li>
  <li><strong>Ph.D Holders:</strong> ${f.phd_faculty} (${f.phd_percentage})</li>
  <li><strong>Visiting Professors:</strong> ${f.visiting_professors}</li>
  <li><strong>Faculty:Student Ratio:</strong> ${f.faculty_student_ratio}</li>
</ul>

<h3>📚 Research Output</h3>
<ul>
  <li><strong>Publications per year:</strong> ${f.research_publications_per_year}</li>
  <li><strong>Scopus-indexed papers:</strong> ${f.scopus_indexed_papers}</li>
  <li><strong>Patents Filed:</strong> ${f.patents_filed}</li>
  <li><strong>Patents Granted:</strong> ${f.patents_granted}</li>
</ul>

<h3>🏛️ Centers of Excellence</h3>
<ul>${f.centers_of_excellence.map(c => `<li><strong>${c.name}</strong> — Sponsored by ${c.sponsor}</li>`).join('')}</ul>`;
}

function respondInfrastructure() {
    const inf = KB.infrastructure;
    return `<h2>🏛️ KLU Campus Infrastructure</h2>
<p>KL University boasts a <strong>${inf.campus_area}</strong> with world-class facilities.</p>

<h3>📚 Library</h3>
<ul>
  <li><strong>Name:</strong> ${inf.library.name}</li>
  <li><strong>Books:</strong> ${inf.library.books}</li>
  <li><strong>E-Journals:</strong> ${inf.library.e_journals}</li>
  <li><strong>Seating:</strong> ${inf.library.seats} seats</li>
  <li><strong>Access:</strong> ${inf.library.access}</li>
</ul>

<h3>🔬 Laboratories (${inf.labs.total} Total)</h3>
<ul>${inf.labs.major.map(l => `<li>${l}</li>`).join('')}</ul>

<h3>🚀 Incubation Center</h3>
<ul>
  <li><strong>Name:</strong> ${inf.incubation.name}</li>
  <li><strong>Startups Incubated:</strong> ${inf.incubation.startups}</li>
  <li><strong>Funding Raised:</strong> ${inf.incubation.funding}</li>
  <li><strong>Mentors:</strong> ${inf.incubation.mentors}</li>
</ul>

<h3>🏃 Sports Complex</h3>
<ul>
  <li><strong>Indoor:</strong> ${inf.sports.indoor.join(', ')}</li>
  <li><strong>Outdoor:</strong> ${inf.sports.outdoor.join(', ')}</li>
</ul>

<h3>🚌 Transport</h3>
<ul>
  <li><strong>Buses:</strong> ${inf.transport.buses} buses on ${inf.transport.routes} routes</li>
  <li><strong>GPS Tracking:</strong> Enabled</li>
  <li><strong>Areas Covered:</strong> ${inf.transport.areas.join(', ')}</li>
</ul>

<h3>🏥 Health Center</h3>
<ul>
  <li><strong>Beds:</strong> ${inf.hospital.beds}</li>
  <li><strong>Doctors:</strong> ${inf.hospital.doctors}</li>
  <li><strong>Ambulances:</strong> ${inf.hospital.ambulance}</li>
  <li><strong>Free for students:</strong> Yes | Available 24/7</li>
</ul>

<h3>🍕 Cafeterias</h3>
<ul>
  <li><strong>Count:</strong> ${inf.cafeterias.count} cafeterias + ${inf.cafeterias.food_courts} food courts</li>
  <li><strong>Capacity:</strong> ${inf.cafeterias.capacity.toLocaleString()} seats</li>
  <li><strong>Brands:</strong> ${inf.cafeterias.tieups.join(', ')}</li>
</ul>

<h3>📶 WiFi</h3>
<ul>
  <li><strong>Coverage:</strong> ${inf.wifi.coverage} of campus</li>
  <li><strong>Backbone Speed:</strong> ${inf.wifi.speed}</li>
  <li><strong>Per-Student:</strong> ${inf.wifi.student_speed}</li>
</ul>

<h3>🖥️ Digital Classrooms</h3>
<ul>
  <li><strong>Smart Classrooms:</strong> ${inf.classrooms.digital}</li>
  <li><strong>LMS Platform:</strong> ${inf.classrooms.lms}</li>
  <li><strong>Smart Boards & Projectors:</strong> All classrooms</li>
</ul>`;
}

function respondBlocks() {
    const blocks = KB.campus_blocks;
    let html = `<h2>🏢 KLU Campus Blocks</h2>
<p>The KLU campus is organized into specialized academic and administrative blocks:</p>`;

    for (const [key, block] of Object.entries(blocks)) {
        html += `
<div class="menu-day">
  <span class="menu-meal">${block.name}</span>
  <p><em>${block.floors} Floors</em></p>
  <ul>${block.facilities.map(f => `<li>${f}</li>`).join('')}</ul>
</div>`;
    }
    return html;
}

function respondEvents() {
    const e = KB.events;
    let festHTML = '';
    for (const fest of e.annual_fests) {
        festHTML += `
<div class="menu-day">
  <span class="menu-meal">${fest.name} — ${fest.type} | ${fest.month || ''}</span>
  <ul>
    <li><strong>Participation:</strong> ${fest.participation || 'N/A'}</li>
    <li><strong>Prize Pool:</strong> ${fest.prize_pool || 'N/A'}</li>
    <li><strong>Events:</strong> ${(fest.events || []).join(', ')}</li>
    ${fest.clubs ? `<li><strong>Organizing Clubs:</strong> ${fest.clubs.join(', ')}</li>` : ''}
  </ul>
</div>`;
    }

    return `<h2>🎉 Events & Fests at KLU</h2>
<p>KL University is known for its vibrant student life with annual festivals, hackathons, and weekly events.</p>

<h3>🎪 Annual Fests</h3>
${festHTML}

<h3>💻 Hackathons & Competitions</h3>
<ul>${e.hackathons.map(h => `<li>${h}</li>`).join('')}</ul>

<h3>🎤 Guest Lectures</h3>
<ul>
  <li><strong>Frequency:</strong> ${e.guest_lectures.frequency} across departments</li>
  <li><strong>Industry Experts:</strong> ${e.guest_lectures.speakers_per_sem} per semester</li>
  <li><strong>Speakers:</strong> Former ISRO Scientists, IIT/IIM Professors, Startup Founders, MNC Leaders</li>
</ul>
<p>✨ KLU offers students a well-rounded campus life alongside academic excellence!</p>`;
}

function respondHostel() {
    const h = KB.hostel;
    const rooms = h.room_types.map(r => `
<div class="menu-day">
  <span class="menu-meal">🛏️ ${r.type}</span>
  <ul>
    <li><strong>Fee:</strong> ${r.fee}</li>
    <li><strong>Facilities:</strong> ${r.facilities.join(', ')}</li>
  </ul>
</div>`).join('');

    return `<h2>🏠 Hostel Facilities — KLU</h2>
<p>KL University provides excellent on-campus hostel facilities for <strong>${h.total_capacity.toLocaleString()}</strong> students.</p>

<div class="stat-box">
  <div class="stat-item"><div class="stat-value">${h.total_capacity.toLocaleString()}</div><div class="stat-label">Total Capacity</div></div>
  <div class="stat-item"><div class="stat-value">${h.boys_capacity.toLocaleString()}</div><div class="stat-label">Boys Seats</div></div>
  <div class="stat-item"><div class="stat-value">${h.girls_capacity.toLocaleString()}</div><div class="stat-label">Girls Seats</div></div>
  <div class="stat-item"><div class="stat-value">200+</div><div class="stat-label">CCTV Cameras</div></div>
</div>

<h3>📋 Hostel Blocks</h3>
<ul>
  <li><strong>Boys Hostels:</strong> ${h.blocks.boys.join(', ')}</li>
  <li><strong>Girls Hostels:</strong> ${h.blocks.girls.join(', ')}</li>
</ul>

<h3>🛏️ Room Types & Fees</h3>
${rooms}

<h3>✅ Hostel Facilities</h3>
<ul>${h.facilities.map(f => `<li>${f}</li>`).join('')}</ul>

<h3>📜 Hostel Rules</h3>
<ul>${h.rules.map(r => `<li>${r}</li>`).join('')}</ul>

<h3>👮 Security & Warden</h3>
<ul>
  <li><strong>Chief Warden:</strong> ${h.warden.chief}</li>
  <li><strong>Warden Ratio:</strong> ${h.warden.ratio}</li>
  <li><strong>CCTV Cameras:</strong> 200+ throughout campus</li>
  <li><strong>Biometric Entry:</strong> Enabled at all blocks</li>
</ul>`;
}

function respondMess(input) {
    const m = KB.mess_food;
    const days = Object.keys(m.weekly_menu);

    // Check if asking about specific day
    const dayNames = { monday: 'Monday', tuesday: 'Tuesday', wednesday: 'Wednesday', thursday: 'Thursday', friday: 'Friday', saturday: 'Saturday', sunday: 'Sunday' };
    let specificDay = null;
    for (const [key, val] of Object.entries(dayNames)) {
        if (input.includes(key)) { specificDay = val; break; }
    }

    if (specificDay) {
        const menu = m.weekly_menu[specificDay];
        const isSpecial = specificDay === 'Sunday';
        return `<h2>🍛 ${isSpecial ? '🎉 Special ' : ''}${specificDay} Mess Menu</h2>
${isSpecial ? `<p><strong>${menu.special_note || 'Special Day!'}</strong></p>` : ''}
<div class="menu-day"><span class="menu-meal">☀️ Breakfast</span><p>${menu.breakfast}</p></div>
<div class="menu-day"><span class="menu-meal">🌞 Lunch</span><p>${menu.lunch}</p></div>
<div class="menu-day"><span class="menu-meal">🌙 Dinner</span><p>${menu.dinner}</p></div>
<div class="menu-day"><span class="menu-meal">🍿 Snacks</span><p>${menu.snacks}</p></div>
${menu.special_note === 'SPECIAL SUNDAY MENU 🎉' ? '<p>😋 Sunday is the best meal day at KLU — enjoy!</p>' : ''}`;
    }

    // Full weekly menu
    let menuHTML = '';
    for (const day of days) {
        const menu = m.weekly_menu[day];
        menuHTML += `
<div class="menu-day">
  <span class="menu-meal">${day === 'Sunday' ? '🎉 ' : ''}${day}</span>
  <ul>
    <li><strong>Breakfast:</strong> ${menu.breakfast}</li>
    <li><strong>Lunch:</strong> ${menu.lunch}</li>
    <li><strong>Snacks:</strong> ${menu.snacks}</li>
    <li><strong>Dinner:</strong> ${menu.dinner}</li>
  </ul>
</div>`;
    }

    return `<h2>🍛 KLU Weekly Mess Menu</h2>
<p>${m.overview}</p>
<p><strong>💰 Cost:</strong> ${m.cost}</p>
<p><strong>🪑 Dining Capacity:</strong> ${m.dining_capacity.toLocaleString()} students</p>

<h3>🗓️ Full 7-Day Menu</h3>
${menuHTML}

<h3>🧹 Hygiene & Quality</h3>
<ul>${m.hygiene.map(h => `<li>${h}</li>`).join('')}</ul>

<h3>🌟 Special Occasions</h3>
<ul>${m.special.map(s => `<li>${s}</li>`).join('')}</ul>

<p>💡 <em>Tip: Sunday Special Biryani + Gulab Jamun + Ice Cream is the most popular meal!</em> 😋</p>`;
}

function respondFees() {
    const f = KB.fees;
    const tuition = Object.entries(f.tuition).map(([k, v]) => `<li><strong>${k.replace(/_/g, ' ')}:</strong> ${v}</li>`).join('');
    const hostelFees = Object.entries(f.hostel).map(([k, v]) => `<li><strong>${k.replace(/_/g, ' ')}:</strong> ${v}</li>`).join('');
    const scholars = f.scholarships.map(s => `<li><strong>${s.name}</strong><br>Criteria: ${s.criteria}<br>Benefit: <span class="info-tag">${s.benefit}</span></li>`).join('');

    return `<h2>💰 KLU Fee Structure & Scholarships</h2>

<h3>📘 Tuition Fees (Per Year)</h3>
<ul>${tuition}</ul>

<h3>🏠 Hostel Fees (Per Year)</h3>
<ul>${hostelFees}</ul>

<h3>🎓 Scholarships Available</h3>
<ul>${scholars}</ul>

<h3>💳 Payment Methods</h3>
<div class="recruiter-grid">${f.payment_methods.map(p => `<span class="recruiter-chip">${p}</span>`).join('')}</div>

<h3>📆 Fee Installments</h3>
<ul>
  <li><strong>Semesters:</strong> ${f.installments.semesters} installments per year</li>
  <li><strong>Semester 1 Deadline:</strong> ${f.installments.deadlines[0]}</li>
  <li><strong>Semester 2 Deadline:</strong> ${f.installments.deadlines[1]}</li>
  <li><strong>Late Fee:</strong> ${f.installments.late_fee}</li>
</ul>

<h3>🏦 Education Loan Partners</h3>
<div class="recruiter-grid">${f.loan_partners.map(l => `<span class="recruiter-chip">${l}</span>`).join('')}</div>`;
}

function respondCalendar() {
    const ac = KB.academic_calendar;
    return `<h2>📅 KLU Academic Calendar</h2>
<p>The academic year at KLU runs from <strong>August to May</strong>, divided into two semesters.</p>

<h3>📙 Odd Semester (Aug – Jan)</h3>
<ul>
  <li><strong>Start Date:</strong> ${ac.odd_semester.start}</li>
  <li><strong>Mid Exams:</strong> ${ac.odd_semester.mid_exams}</li>
  <li><strong>End Exams:</strong> ${ac.odd_semester.end_exams}</li>
  <li><strong>Results:</strong> ${ac.odd_semester.results}</li>
  <li><strong>Semester End:</strong> ${ac.odd_semester.end}</li>
</ul>

<h3>📗 Even Semester (Jan – Jun)</h3>
<ul>
  <li><strong>Start Date:</strong> ${ac.even_semester.start}</li>
  <li><strong>Mid Exams:</strong> ${ac.even_semester.mid_exams}</li>
  <li><strong>End Exams:</strong> ${ac.even_semester.end_exams}</li>
  <li><strong>Results:</strong> ${ac.even_semester.results}</li>
  <li><strong>Semester End:</strong> ${ac.even_semester.end}</li>
</ul>

<h3>📝 Registration</h3>
<ul>
  <li><strong>Add/Drop Period:</strong> ${ac.add_drop}</li>
  <li><strong>Registration:</strong> ${ac.registration}</li>
</ul>

<h3>🎉 Holidays</h3>
<ul>${ac.holidays.map(h => `<li>${h}</li>`).join('')}</ul>`;
}

function respondFallback(input) {
    const suggestions = [
        'admissions', 'placements', 'mess menu', 'hostel', 'fees', 'courses', 'events', 'faculty', 'campus', 'academic calendar'
    ];
    const suggestionChips = suggestions.map(s => `<span class="chip" onclick="sendChip('${s}')">${s}</span>`).join('');
    return `<p>🤔 Hmm, I didn't quite find information about "<strong>${escapeHtml(input)}</strong>" in my KLU knowledge base.</p>
<p>Try asking about one of these popular topics:</p>
<div class="welcome-chips" style="justify-content: flex-start; margin: 10px 0;">${suggestionChips}</div>
<p>Or contact KLU directly:</p>
<ul>
  <li>📞 <strong>+91-863-2344700</strong></li>
  <li>📧 <strong>admissions@kluniversity.in</strong></li>
  <li>🌐 <strong>www.kluniversity.in</strong></li>
</ul>`;
}

// ---- Initial welcome bot message ----
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        addBotMessage(`<p>👋 Welcome to <strong>KLU Smart Assistant</strong>! I'm your intelligent guide for everything about KL University.</p>
<p>I can answer questions about <strong>admissions</strong>, <strong>placements</strong>, <strong>hostel</strong>, <strong>mess menu</strong>, <strong>fees</strong>, <strong>events</strong>, and much more — all offline! 🎓</p>
<p>What would you like to know today?</p>`);
    }, 500);
});
