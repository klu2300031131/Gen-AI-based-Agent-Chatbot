/* ========================================
   KLU Agent - Main Application Logic
   ======================================== */

// ==========================================
// KLU Knowledge Base (simulated for frontend)
// ==========================================
const KLU_KNOWLEDGE = {
    admissions: {
        keywords: ['admission', 'admit', 'apply', 'application', 'eligibility', 'entrance', 'enroll', 'registration', 'join'],
        responses: [
            `## Admissions at KL University 🎓\n\nKL University offers admissions across multiple programs. Here's what you need to know:\n\n**Undergraduate Programs (B.Tech):**\n- Eligibility: 10+2 with Physics, Chemistry, and Mathematics\n- Minimum aggregate: 60% in qualifying exam\n- Entrance: KLUEEE (KL University Engineering Entrance Exam) / JEE Main scores accepted\n\n**Postgraduate Programs (M.Tech/MBA):**\n- Valid GATE/CAT/MAT scores\n- Minimum 60% in graduation\n\n**Application Process:**\n1. Visit the official KLU website\n2. Fill out the online application form\n3. Pay the application fee\n4. Attend the entrance exam/interview\n5. Check merit list and confirm admission\n\n📅 Applications typically open in **January** each year.\n\n*Source: KLU Admissions Office*`
        ]
    },
    courses: {
        keywords: ['course', 'program', 'department', 'branch', 'stream', 'btech', 'mtech', 'mba', 'degree', 'engineering'],
        responses: [
            `## Programs Offered at KLU 📚\n\nKL University offers a wide range of programs:\n\n**Engineering & Technology (B.Tech):**\n- Computer Science & Engineering (CSE)\n- Electronics & Communication (ECE)\n- Mechanical Engineering\n- Civil Engineering\n- Artificial Intelligence & Machine Learning\n- Data Science\n- Cyber Security\n- Information Technology\n\n**Management:**\n- MBA (Various specializations)\n- BBA\n\n**Sciences:**\n- B.Sc / M.Sc (Multiple disciplines)\n- Biotechnology\n\n**Research:**\n- Ph.D programs in all departments\n\n🏆 **CSE and ECE** are among the top-rated departments with excellent placement records.\n\n*Source: KLU Academic Office*`
        ]
    },
    placements: {
        keywords: ['placement', 'job', 'recruit', 'company', 'salary', 'package', 'career', 'hire', 'offer'],
        responses: [
            `## Placement Statistics 📊\n\nKLU has an outstanding placement record:\n\n**2023-24 Highlights:**\n- **Highest Package:** ₹44 LPA (International)\n- **Average Package:** ₹6.5 LPA\n- **Placement Rate:** 85%+\n- **500+** companies visited campus\n\n**Top Recruiters:**\n| Company | Roles |\n|---------|-------|\n| Google | SDE, ML Engineer |\n| Microsoft | Software Engineer |\n| Amazon | SDE, Operations |\n| TCS | Developer, Analyst |\n| Infosys | Systems Engineer |\n| Wipro | Project Engineer |\n| Deloitte | Consultant |\n\n**Training & Support:**\n- Pre-placement training from 2nd year\n- Mock interviews & aptitude sessions\n- Industry mentorship programs\n\n*Source: KLU Training & Placement Cell*`
        ]
    },
    campus: {
        keywords: ['campus', 'facility', 'facilities', 'library', 'lab', 'sports', 'hostel', 'canteen', 'wifi', 'infrastructure', 'club'],
        responses: [
            `## Campus Facilities 🏛️\n\nKLU's campus in Vaddeswaram, Guntur District spans over **100+ acres** with world-class facilities:\n\n**Academic:**\n- 🖥️ State-of-the-art computer labs\n- 📖 Central Library with 1 lakh+ books & e-resources\n- 🔬 Advanced research laboratories\n- 📡 High-speed Wi-Fi across campus\n\n**Residential:**\n- 🏠 Separate hostels for boys & girls\n- 🍽️ Multiple canteens & food courts\n- 🏥 24/7 medical facility\n\n**Sports & Recreation:**\n- 🏏 Cricket ground, football field\n- 🏸 Indoor badminton & table tennis\n- 🏋️ Gymnasium & fitness center\n- 🏊 Swimming pool\n\n**Student Clubs:**\n- Coding Club, Robotics Club, Entrepreneurship Cell\n- Cultural clubs, Music & Dance societies\n- NSS & NCC units\n\n*Source: KLU Campus Administration*`
        ]
    },
    schedule: {
        keywords: ['schedule', 'timetable', 'calendar', 'academic', 'semester', 'exam', 'holiday', 'vacation', 'date'],
        responses: [
            `## Academic Schedule 📅\n\n**Academic Year 2025-26:**\n\n**Odd Semester (July - December):**\n- Classes Begin: July 15, 2025\n- Mid-Semester Exams: September 15-22\n- End-Semester Exams: November 25 - December 10\n- Winter Break: December 15 - January 5\n\n**Even Semester (January - June):**\n- Classes Begin: January 6, 2026\n- Mid-Semester Exams: March 10-17\n- End-Semester Exams: May 20 - June 5\n- Summer Break: June 10 - July 14\n\n**Important Dates:**\n- 🎉 University Foundation Day: February\n- 🏆 Annual Tech Fest (Samyak): March\n- 🎭 Cultural Fest: October\n- 🏅 Convocation: August\n\n*Source: KLU Academic Calendar*`
        ]
    },
    events: {
        keywords: ['event', 'fest', 'festival', 'celebration', 'workshop', 'seminar', 'hackathon', 'conference', 'samyak'],
        responses: [
            `## Upcoming Events & Fests 🎉\n\n**Major Annual Events:**\n\n🔥 **SAMYAK** (Annual Tech Fest)\n- One of the largest tech fests in AP\n- Hackathons, coding contests, robotics\n- Guest lectures by industry leaders\n\n🎭 **SURABHI** (Cultural Fest)\n- Music, dance, and drama competitions\n- Celebrity performances\n- Art exhibitions\n\n📚 **Regular Events:**\n- Weekly coding contests (CodeChef/LeetCode)\n- Monthly guest lectures\n- Quarterly hackathons\n- Industry workshops & seminars\n\n💡 **Upcoming Workshops:**\n- AI/ML Workshop - This Month\n- Cloud Computing - Next Month\n- Cybersecurity Bootcamp - Quarterly\n\n*Stay updated via the KLU Events Portal!*\n\n*Source: KLU Student Affairs*`
        ]
    },
    hostel: {
        keywords: ['hostel', 'room', 'mess', 'accommodation', 'stay', 'resident', 'boarding', 'lodging'],
        responses: [
            `## Hostel Information 🏠\n\n**KLU Hostel Facilities:**\n\n**Types of Accommodation:**\n- 🛏️ Single Occupancy (AC) - ₹1,20,000/year\n- 🛏️ Double Sharing (AC) - ₹90,000/year\n- 🛏️ Triple Sharing (Non-AC) - ₹60,000/year\n\n**Amenities:**\n- ✅ 24/7 Wi-Fi connectivity\n- ✅ Hot water supply\n- ✅ Laundry service\n- ✅ Common room with TV\n- ✅ Study rooms\n- ✅ Power backup\n- ✅ CCTV security\n\n**Mess Facility:**\n- Breakfast, Lunch, Snacks, and Dinner\n- Vegetarian & Non-vegetarian options\n- Special diet accommodations available\n\n**Rules:**\n- Entry/Exit timings are monitored\n- Visitors allowed during specified hours\n- Ragging-free zone with strict anti-ragging policies\n\n*Source: KLU Hostel Administration*`
        ]
    },
    fees: {
        keywords: ['fee', 'fees', 'cost', 'tuition', 'scholarship', 'financial', 'payment', 'expense'],
        responses: [
            `## Fee Structure 💰\n\n**B.Tech Fee Structure (per year):**\n\n| Category | Tuition Fee |\n|----------|------------|\n| General | ₹1,80,000 |\n| NRI | ₹3,50,000 |\n| International | $5,000 |\n\n**Additional Fees:**\n- Hostel + Mess: ₹60,000 - ₹1,20,000\n- Transport: ₹30,000 - ₹50,000\n- Exam Fee: ₹5,000/semester\n\n**Scholarships Available:**\n- 🏆 Merit-based (up to 100% tuition waiver)\n- 📊 JEE Main rank-based scholarships\n- 🎯 Sports quota scholarships\n- 💡 Research fellowships for PG students\n\n**Payment Options:**\n- Full payment / Semester-wise\n- Education loan assistance available\n- Online payment portal\n\n*Contact the Fee Section for detailed information.*\n\n*Source: KLU Finance Office*`
        ]
    },
    general: {
        keywords: [],
        responses: [
            `I appreciate your question! 😊\n\nI'm the **KLU Agent**, your AI-powered assistant for KL University. I can help you with:\n\n- 🎓 **Admissions** - Requirements, process, deadlines\n- 📚 **Courses** - Programs, departments, curriculum\n- 💼 **Placements** - Statistics, recruiters, packages\n- 🏛️ **Campus** - Facilities, clubs, infrastructure\n- 📅 **Schedule** - Academic calendar, exams\n- 🎉 **Events** - Fests, workshops, seminars\n- 🏠 **Hostel** - Accommodation, mess, fees\n- 💰 **Fees** - Fee structure, scholarships\n\nPlease ask me a specific question about any of these topics, and I'll provide you with accurate, up-to-date information!\n\n*All responses are grounded in KLU's institutional knowledge base.*`
        ]
    }
};

// ==========================================
// Application State
// ==========================================
class KLUAgent {
    constructor() {
        this.conversations = JSON.parse(localStorage.getItem('klu_conversations') || '[]');
        this.currentConversationId = null;
        this.currentMessages = [];
        this.isProcessing = false;
        this.theme = localStorage.getItem('klu_theme') || 'dark';

        this.init();
    }

    init() {
        this.cacheDOM();
        this.bindEvents();
        this.applyTheme(this.theme);
        this.renderChatHistory();
        this.autoResizeInput();
    }

    // ==========================================
    // DOM Caching
    // ==========================================
    cacheDOM() {
        // Sidebar
        this.sidebar = document.getElementById('sidebar');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.newChatBtn = document.getElementById('newChatBtn');
        this.chatHistory = document.getElementById('chatHistory');
        this.settingsBtn = document.getElementById('settingsBtn');
        this.themeToggleBtn = document.getElementById('themeToggleBtn');

        // Chat Area
        this.chatContainer = document.getElementById('chatContainer');
        this.welcomeScreen = document.getElementById('welcomeScreen');
        this.messagesWrapper = document.getElementById('messagesWrapper');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.voiceBtn = document.getElementById('voiceBtn');
        this.attachBtn = document.getElementById('attachBtn');
        this.typingStatus = document.getElementById('typingStatus');
        this.clearChatBtn = document.getElementById('clearChatBtn');
        this.exportChatBtn = document.getElementById('exportChatBtn');

        // Mobile
        this.mobileMenuBtn = document.getElementById('mobileMenuBtn');
        this.mobileOverlay = document.getElementById('mobileOverlay');

        // Settings Modal
        this.settingsModal = document.getElementById('settingsModal');
        this.closeSettingsBtn = document.getElementById('closeSettingsBtn');
        this.fontSizeSlider = document.getElementById('fontSizeSlider');
    }

    // ==========================================
    // Event Binding
    // ==========================================
    bindEvents() {
        // Send message
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Input auto-resize & button enable
        this.messageInput.addEventListener('input', () => {
            this.autoResizeInput();
            this.sendBtn.disabled = !this.messageInput.value.trim();
        });

        // New chat
        this.newChatBtn.addEventListener('click', () => this.startNewChat());

        // Sidebar toggle
        this.sidebarToggle.addEventListener('click', () => this.toggleSidebar());

        // Mobile menu
        this.mobileMenuBtn.addEventListener('click', () => this.toggleMobileSidebar());
        this.mobileOverlay.addEventListener('click', () => this.toggleMobileSidebar());

        // Theme toggle
        this.themeToggleBtn.addEventListener('click', () => {
            const newTheme = this.theme === 'dark' ? 'light' : 'dark';
            this.applyTheme(newTheme);
        });

        // Settings
        this.settingsBtn.addEventListener('click', () => this.settingsModal.classList.add('active'));
        this.closeSettingsBtn.addEventListener('click', () => this.settingsModal.classList.remove('active'));
        this.settingsModal.addEventListener('click', (e) => {
            if (e.target === this.settingsModal) this.settingsModal.classList.remove('active');
        });

        // Theme options in settings
        document.querySelectorAll('.theme-option').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.theme-option').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const theme = btn.dataset.theme;
                if (theme === 'system') {
                    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                    this.applyTheme(prefersDark ? 'dark' : 'light');
                } else {
                    this.applyTheme(theme);
                }
            });
        });

        // Font size slider
        this.fontSizeSlider.addEventListener('input', (e) => {
            document.documentElement.style.setProperty('--font-size-base', e.target.value + 'px');
        });

        // Suggestion cards
        document.querySelectorAll('.suggestion-card, .topic-chip').forEach(card => {
            card.addEventListener('click', () => {
                const query = card.dataset.query;
                if (query) {
                    this.messageInput.value = query;
                    this.sendBtn.disabled = false;
                    this.sendMessage();
                }
            });
        });

        // Clear chat
        this.clearChatBtn.addEventListener('click', () => this.clearCurrentChat());

        // Export chat
        this.exportChatBtn.addEventListener('click', () => this.exportChat());

        // Voice input
        this.voiceBtn.addEventListener('click', () => this.toggleVoiceInput());
    }

    // ==========================================
    // Theme Management
    // ==========================================
    applyTheme(theme) {
        this.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('klu_theme', theme);

        const icon = this.themeToggleBtn.querySelector('i');
        icon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
    }

    // ==========================================
    // Sidebar Management
    // ==========================================
    toggleSidebar() {
        this.sidebar.classList.toggle('collapsed');
        const icon = this.sidebarToggle.querySelector('i');
        icon.classList.toggle('fa-chevron-left');
        icon.classList.toggle('fa-chevron-right');
    }

    toggleMobileSidebar() {
        this.sidebar.classList.toggle('open');
        this.mobileOverlay.classList.toggle('active');
    }

    // ==========================================
    // Chat History Management
    // ==========================================
    renderChatHistory() {
        this.chatHistory.innerHTML = '';

        if (this.conversations.length === 0) {
            this.chatHistory.innerHTML = `
                <div style="padding: 16px; text-align: center; color: var(--text-tertiary); font-size: 0.8rem;">
                    <i class="fas fa-comments" style="font-size: 1.5rem; margin-bottom: 8px; display: block; opacity: 0.3;"></i>
                    No chat history yet.<br>Start a new conversation!
                </div>
            `;
            return;
        }

        this.conversations.slice().reverse().forEach(conv => {
            const item = document.createElement('div');
            item.className = `history-item ${conv.id === this.currentConversationId ? 'active' : ''}`;
            item.innerHTML = `
                <i class="fas fa-message"></i>
                <span class="history-text">${this.escapeHTML(conv.title)}</span>
                <button class="history-delete" title="Delete chat" data-id="${conv.id}">
                    <i class="fas fa-trash-alt"></i>
                </button>
            `;

            item.addEventListener('click', (e) => {
                if (!e.target.closest('.history-delete')) {
                    this.loadConversation(conv.id);
                }
            });

            const deleteBtn = item.querySelector('.history-delete');
            deleteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.deleteConversation(conv.id);
            });

            this.chatHistory.appendChild(item);
        });
    }

    startNewChat() {
        this.currentConversationId = null;
        this.currentMessages = [];
        this.messagesWrapper.innerHTML = '';
        this.welcomeScreen.classList.remove('hidden');
        this.renderChatHistory();

        // Close mobile sidebar
        if (this.sidebar.classList.contains('open')) {
            this.toggleMobileSidebar();
        }
    }

    loadConversation(id) {
        const conv = this.conversations.find(c => c.id === id);
        if (!conv) return;

        this.currentConversationId = id;
        this.currentMessages = [...conv.messages];
        this.welcomeScreen.classList.add('hidden');
        this.messagesWrapper.innerHTML = '';

        this.currentMessages.forEach(msg => {
            this.appendMessage(msg.role, msg.content, false);
        });

        this.renderChatHistory();
        this.scrollToBottom();

        // Close mobile sidebar
        if (this.sidebar.classList.contains('open')) {
            this.toggleMobileSidebar();
        }
    }

    deleteConversation(id) {
        this.conversations = this.conversations.filter(c => c.id !== id);
        localStorage.setItem('klu_conversations', JSON.stringify(this.conversations));

        if (this.currentConversationId === id) {
            this.startNewChat();
        } else {
            this.renderChatHistory();
        }
    }

    saveConversation() {
        if (this.currentMessages.length === 0) return;

        // Get title from first user message
        const firstUserMsg = this.currentMessages.find(m => m.role === 'user');
        const title = firstUserMsg ? firstUserMsg.content.substring(0, 50) + (firstUserMsg.content.length > 50 ? '...' : '') : 'New Chat';

        if (!this.currentConversationId) {
            this.currentConversationId = 'conv_' + Date.now();
            this.conversations.push({
                id: this.currentConversationId,
                title: title,
                messages: [...this.currentMessages],
                createdAt: new Date().toISOString()
            });
        } else {
            const conv = this.conversations.find(c => c.id === this.currentConversationId);
            if (conv) {
                conv.messages = [...this.currentMessages];
                conv.title = title;
            }
        }

        localStorage.setItem('klu_conversations', JSON.stringify(this.conversations));
        this.renderChatHistory();
    }

    // ==========================================
    // Message Handling
    // ==========================================
    async sendMessage() {
        const text = this.messageInput.value.trim();
        if (!text || this.isProcessing) return;

        // Hide welcome screen
        this.welcomeScreen.classList.add('hidden');

        // Add user message
        this.currentMessages.push({ role: 'user', content: text });
        this.appendMessage('user', text);

        // Clear input
        this.messageInput.value = '';
        this.sendBtn.disabled = true;
        this.autoResizeInput();

        // Show typing indicator
        this.isProcessing = true;
        this.showTypingIndicator();

        // Simulate AI response
        const response = await this.generateResponse(text);

        // Remove typing indicator and add response
        this.hideTypingIndicator();
        this.currentMessages.push({ role: 'bot', content: response.text });
        this.appendMessage('bot', response.text, true, response.source);

        this.isProcessing = false;
        this.saveConversation();
    }

    appendMessage(role, content, animate = true, source = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role} ${animate ? 'fade-in' : ''}`;

        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const avatarIcon = role === 'bot' ? 'fa-robot' : 'fa-user';

        let sourceHTML = '';
        if (source) {
            sourceHTML = `<div class="source-badge"><i class="fas fa-database"></i> ${this.escapeHTML(source)}</div>`;
        }

        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas ${avatarIcon}"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">${role === 'bot' ? this.renderMarkdown(content) : this.escapeHTML(content)}</div>
                ${sourceHTML}
                <div class="message-meta">
                    <span>${time}</span>
                    <div class="message-actions">
                        <button class="msg-action-btn" title="Copy" onclick="navigator.clipboard.writeText(\`${content.replace(/`/g, '\\`').replace(/\\/g, '\\\\')}\`)">
                            <i class="fas fa-copy"></i>
                        </button>
                        ${role === 'bot' ? `<button class="msg-action-btn" title="Thumbs up"><i class="fas fa-thumbs-up"></i></button>
                        <button class="msg-action-btn" title="Thumbs down"><i class="fas fa-thumbs-down"></i></button>` : ''}
                    </div>
                </div>
            </div>
        `;

        this.messagesWrapper.appendChild(messageDiv);
        this.scrollToBottom();
    }

    // ==========================================
    // AI Response Generation (Backend API + Local Fallback)
    // ==========================================
    async generateResponse(query) {
        // Try backend API first
        try {
            const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
                ? 'http://localhost:8000'
                : window.location.origin;

            const response = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: query })
            });

            if (response.ok) {
                const data = await response.json();
                const sources = data.sources && data.sources.length > 0
                    ? data.sources.join(', ')
                    : 'KLU Knowledge Base';
                return {
                    text: data.answer,
                    source: `${sources} (${data.response_time}s)`
                };
            }

            // If API returns error, fall through to local fallback
            console.warn('Backend API returned error, using local fallback');
        } catch (err) {
            // Backend not available, use local fallback
            console.warn('Backend not available, using local fallback:', err.message);
        }

        // Local fallback using built-in knowledge base
        const delay = 800 + Math.random() * 1200;
        await new Promise(resolve => setTimeout(resolve, delay));

        const lowerQuery = query.toLowerCase();

        // Search through knowledge base
        for (const [category, data] of Object.entries(KLU_KNOWLEDGE)) {
            if (category === 'general') continue;

            const matched = data.keywords.some(keyword => lowerQuery.includes(keyword));
            if (matched) {
                const resp = data.responses[Math.floor(Math.random() * data.responses.length)];
                return {
                    text: resp,
                    source: `KLU Knowledge Base — ${category.charAt(0).toUpperCase() + category.slice(1)} (offline)`
                };
            }
        }

        // Default fallback
        return {
            text: KLU_KNOWLEDGE.general.responses[0],
            source: 'KLU Knowledge Base (offline)'
        };
    }

    // ==========================================
    // Typing Indicator
    // ==========================================
    showTypingIndicator() {
        this.typingStatus.innerHTML = `
            <span class="status-dot online"></span>
            Thinking...
        `;

        const typingMsg = document.createElement('div');
        typingMsg.className = 'message bot fade-in';
        typingMsg.id = 'typingMessage';
        typingMsg.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        this.messagesWrapper.appendChild(typingMsg);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingStatus.innerHTML = `
            <span class="status-dot online"></span>
            Ready to help
        `;

        const typingMsg = document.getElementById('typingMessage');
        if (typingMsg) typingMsg.remove();
    }

    // ==========================================
    // Utilities
    // ==========================================
    autoResizeInput() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }

    scrollToBottom() {
        requestAnimationFrame(() => {
            this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        });
    }

    escapeHTML(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    renderMarkdown(text) {
        // Simple markdown renderer
        let html = this.escapeHTML(text);

        // Headers
        html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

        // Bold
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

        // Italic
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

        // Code blocks
        html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');

        // Inline code
        html = html.replace(/`(.+?)`/g, '<code>$1</code>');

        // Tables
        html = html.replace(/\|(.+)\|/g, (match) => {
            const cells = match.split('|').filter(c => c.trim());
            if (cells.every(c => /^[-\s]+$/.test(c))) return '';
            const tag = 'td';
            const row = cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join('');
            return `<tr>${row}</tr>`;
        });
        html = html.replace(/(<tr>.*<\/tr>\s*)+/g, '<table>$&</table>');

        // Unordered lists
        html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.*<\/li>\s*)+/g, '<ul>$&</ul>');

        // Ordered lists
        html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

        // Line breaks
        html = html.replace(/\n\n/g, '</p><p>');
        html = html.replace(/\n/g, '<br>');

        // Wrap in paragraphs
        if (!html.startsWith('<')) {
            html = '<p>' + html + '</p>';
        }

        return html;
    }

    clearCurrentChat() {
        if (this.currentMessages.length === 0) return;

        this.currentMessages = [];
        this.messagesWrapper.innerHTML = '';
        this.welcomeScreen.classList.remove('hidden');

        if (this.currentConversationId) {
            this.deleteConversation(this.currentConversationId);
        }
    }

    exportChat() {
        if (this.currentMessages.length === 0) return;

        let exportText = `KLU Agent - Chat Export\n${'='.repeat(50)}\nExported: ${new Date().toLocaleString()}\n\n`;

        this.currentMessages.forEach(msg => {
            const role = msg.role === 'user' ? '👤 You' : '🤖 KLU Agent';
            exportText += `${role}:\n${msg.content}\n\n${'─'.repeat(40)}\n\n`;
        });

        const blob = new Blob([exportText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `klu-agent-chat-${Date.now()}.txt`;
        a.click();
        URL.revokeObjectURL(url);
    }

    toggleVoiceInput() {
        if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
            alert('Voice input is not supported in your browser.');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;

        this.voiceBtn.classList.add('recording');

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            this.messageInput.value = transcript;
            this.sendBtn.disabled = false;
            this.voiceBtn.classList.remove('recording');
        };

        recognition.onerror = () => {
            this.voiceBtn.classList.remove('recording');
        };

        recognition.onend = () => {
            this.voiceBtn.classList.remove('recording');
        };

        recognition.start();
    }
}

// ==========================================
// Initialize Application
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    window.kluAgent = new KLUAgent();
});
