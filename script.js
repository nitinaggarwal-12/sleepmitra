// Global variables
let currentAssessmentStep = 1;
let assessmentAnswers = {};
let diaryEntries = JSON.parse(localStorage.getItem('diaryEntries')) || [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeCharts();
    loadDiaryEntries();
    initializeBooking();
    setCurrentDate();
});

// Navigation functions
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            showPage(page);
            
            // Update active nav link
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function showPage(pageId) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    
    // Show selected page
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
    }
    
    // Update charts when switching to analytics
    if (pageId === 'analytics') {
        updateAnalyticsCharts();
    }
    
    // Update therapy page when switching to it
    if (pageId === 'therapy') {
        updateTherapyPage();
    }
}

// Chart initialization
function initializeCharts() {
    // KPI Sparkline Charts
    createSparklineChart('efficiencyChart', [85, 87, 86, 89, 88, 90, 87]);
    createSparklineChart('latencyChart', [15, 12, 14, 11, 13, 10, 12]);
    createSparklineChart('durationChart', [7.2, 7.5, 7.3, 7.8, 7.6, 7.9, 7.5]);
    createSparklineChart('wakeupsChart', [2, 1, 2, 1, 2, 0, 1]);
}

function createSparklineChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                data: data,
                borderColor: '#6C5CE7',
                backgroundColor: 'rgba(108, 92, 231, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    display: false
                }
            },
            elements: {
                point: {
                    radius: 0
                }
            }
        }
    });
}

function updateAnalyticsCharts() {
    // Sleep Duration Chart
    const durationCtx = document.getElementById('sleepDurationChart').getContext('2d');
    new Chart(durationCtx, {
        type: 'line',
        data: {
            labels: ['8 जन', '9 जन', '10 जन', '11 जन', '12 जन', '13 जन', '14 जन'],
            datasets: [{
                label: 'नींद अवधि (घंटे)',
                data: [7.5, 8.0, 7.2, 7.8, 6.5, 8.5, 7.0],
                borderColor: '#6C5CE7',
                backgroundColor: 'rgba(108, 92, 231, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10
                }
            }
        }
    });

    // Sleep Efficiency Chart
    const efficiencyCtx = document.getElementById('sleepEfficiencyChart').getContext('2d');
    new Chart(efficiencyCtx, {
        type: 'line',
        data: {
            labels: ['8 जन', '9 जन', '10 जन', '11 जन', '12 जन', '13 जन', '14 जन'],
            datasets: [{
                label: 'नींद दक्षता (%)',
                data: [85, 90, 82, 88, 75, 92, 80],
                borderColor: '#00B894',
                backgroundColor: 'rgba(0, 184, 148, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // Wake-ups Chart
    const wakeupsCtx = document.getElementById('wakeupsAnalyticsChart').getContext('2d');
    new Chart(wakeupsCtx, {
        type: 'bar',
        data: {
            labels: ['8 जन', '9 जन', '10 जन', '11 जन', '12 जन', '13 जन', '14 जन'],
            datasets: [{
                label: 'जागने की संख्या',
                data: [2, 1, 3, 1, 4, 0, 2],
                backgroundColor: '#FDCB6E',
                borderColor: '#FDCB6E',
                borderWidth: 1,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Weekly Trends Chart
    const trendsCtx = document.getElementById('weeklyTrendsChart').getContext('2d');
    new Chart(trendsCtx, {
        type: 'bar',
        data: {
            labels: ['सप्ताह 1', 'सप्ताह 2', 'सप्ताह 3', 'सप्ताह 4'],
            datasets: [{
                label: 'औसत अवधि (घंटे)',
                data: [7.2, 7.5, 7.8, 8.0],
                backgroundColor: '#6C5CE7',
                borderRadius: 6
            }, {
                label: 'औसत दक्षता (%)',
                data: [82, 85, 88, 90],
                backgroundColor: '#00B894',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Diary functions
function setCurrentDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('sleepDate').value = today;
}

function saveDiaryEntry() {
    const entry = {
        date: document.getElementById('sleepDate').value,
        bedtime: document.getElementById('bedtime').value,
        sleepLatency: document.getElementById('sleepLatency').value,
        wakeTime: document.getElementById('wakeTime').value,
        wakeUps: document.getElementById('wakeUps').value,
        sleepQuality: document.getElementById('sleepQuality').value,
        notes: document.getElementById('notes').value,
        timestamp: new Date().toISOString()
    };

    // Validate required fields
    if (!entry.date || !entry.bedtime || !entry.wakeTime) {
        alert('कृपया सभी आवश्यक फील्ड भरें');
        return;
    }

    diaryEntries.unshift(entry);
    localStorage.setItem('diaryEntries', JSON.stringify(diaryEntries));
    loadDiaryEntries();
    
    // Clear form
    document.getElementById('sleepLatency').value = '';
    document.getElementById('wakeUps').value = '';
    document.getElementById('sleepQuality').value = '7';
    document.getElementById('notes').value = '';
    
    alert('नींद डायरी एंट्री सफलतापूर्वक सेव हो गई!');
}

function loadDiaryEntries() {
    const entriesContainer = document.getElementById('diaryEntries');
    entriesContainer.innerHTML = '';

    if (diaryEntries.length === 0) {
        entriesContainer.innerHTML = '<p style="text-align: center; color: #666;">अभी तक कोई एंट्री नहीं है</p>';
        return;
    }

    diaryEntries.slice(0, 5).forEach(entry => {
        const entryElement = document.createElement('div');
        entryElement.className = 'entry-item';
        
        const date = new Date(entry.date).toLocaleDateString('hi-IN');
        const sleepDuration = calculateSleepDuration(entry.bedtime, entry.wakeTime);
        
        entryElement.innerHTML = `
            <div class="entry-date">${date}</div>
            <div class="entry-details">
                सोने का समय: ${entry.bedtime} | जागने का समय: ${entry.wakeTime}<br>
                नींद की अवधि: ${sleepDuration} | गुणवत्ता: ${entry.sleepQuality}/10<br>
                ${entry.notes ? `टिप्पणी: ${entry.notes}` : ''}
            </div>
        `;
        
        entriesContainer.appendChild(entryElement);
    });
}

function calculateSleepDuration(bedtime, wakeTime) {
    if (!bedtime || !wakeTime) return 'N/A';
    
    const bed = new Date(`2000-01-01T${bedtime}`);
    const wake = new Date(`2000-01-01T${wakeTime}`);
    
    if (wake < bed) {
        wake.setDate(wake.getDate() + 1);
    }
    
    const diff = wake - bed;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    return `${hours} घंटे ${minutes} मिनट`;
}

// Assessment functions
function nextStep() {
    if (currentAssessmentStep < 3) {
        // Save current step answers
        saveCurrentStepAnswers();
        
        // Check if current step is complete
        if (!isCurrentStepComplete()) {
            alert('कृपया सभी प्रश्नों के उत्तर दें');
            return;
        }
        
        // Hide current step
        document.getElementById(`step${currentAssessmentStep}`).classList.remove('active');
        
        // Show next step
        currentAssessmentStep++;
        document.getElementById(`step${currentAssessmentStep}`).classList.add('active');
        
        // Update progress
        updateProgress();
        
        // Update navigation buttons
        updateNavigationButtons();
    } else {
        // Complete assessment
        completeAssessment();
    }
}

function previousStep() {
    if (currentAssessmentStep > 1) {
        // Hide current step
        document.getElementById(`step${currentAssessmentStep}`).classList.remove('active');
        
        // Show previous step
        currentAssessmentStep--;
        document.getElementById(`step${currentAssessmentStep}`).classList.add('active');
        
        // Update progress
        updateProgress();
        
        // Update navigation buttons
        updateNavigationButtons();
    }
}

function saveCurrentStepAnswers() {
    const currentStep = document.getElementById(`step${currentAssessmentStep}`);
    const questions = currentStep.querySelectorAll('input[type="radio"]:checked');
    
    questions.forEach(question => {
        assessmentAnswers[question.name] = parseInt(question.value);
    });
}

function isCurrentStepComplete() {
    const currentStep = document.getElementById(`step${currentAssessmentStep}`);
    const requiredQuestions = currentStep.querySelectorAll('input[type="radio"]');
    const answeredQuestions = currentStep.querySelectorAll('input[type="radio"]:checked');
    
    // Group by question name
    const questionGroups = {};
    requiredQuestions.forEach(q => {
        if (!questionGroups[q.name]) {
            questionGroups[q.name] = [];
        }
        questionGroups[q.name].push(q);
    });
    
    // Check if each question group has an answer
    for (let questionName in questionGroups) {
        const hasAnswer = questionGroups[questionName].some(q => q.checked);
        if (!hasAnswer) {
            return false;
        }
    }
    
    return true;
}

function updateProgress() {
    const progress = (currentAssessmentStep / 3) * 100;
    document.getElementById('assessmentProgress').style.width = `${progress}%`;
    document.getElementById('progressText').textContent = `चरण ${currentAssessmentStep} / 3`;
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    prevBtn.style.display = currentAssessmentStep > 1 ? 'block' : 'none';
    nextBtn.textContent = currentAssessmentStep === 3 ? 'पूर्ण करें' : 'अगला';
}

function completeAssessment() {
    // Save final step answers
    saveCurrentStepAnswers();
    
    // Calculate total score
    const totalScore = Object.values(assessmentAnswers).reduce((sum, score) => sum + score, 0);
    const maxScore = 20; // Maximum possible score
    const percentage = (totalScore / maxScore) * 100;
    
    // Determine severity
    let severity, recommendations;
    if (percentage <= 30) {
        severity = 'हल्का';
        recommendations = 'आपकी नींद की गुणवत्ता अच्छी है। नियमित दिनचर्या बनाए रखें।';
    } else if (percentage <= 60) {
        severity = 'मध्यम';
        recommendations = 'नींद की गुणवत्ता में सुधार की आवश्यकता है। CBT-I तकनीकों का उपयोग करें।';
    } else {
        severity = 'गंभीर';
        recommendations = 'तुरंत चिकित्सकीय सलाह लें। विशेषज्ञ से परामर्श करें।';
    }
    
    // Show results
    document.getElementById('totalScore').textContent = Math.round(percentage) + '%';
    document.getElementById('severityBadge').textContent = severity;
    document.getElementById('recommendations').textContent = recommendations;
    document.getElementById('resultsModal').style.display = 'block';
    
    // Save results for therapy page
    const assessmentResult = {
        totalScore: Math.round(percentage),
        severity: severity,
        recommendations: recommendations.split('. ').filter(r => r.trim()),
        timestamp: new Date().toISOString()
    };
    localStorage.setItem('lastAssessmentResult', JSON.stringify(assessmentResult));
    
    // Reset assessment
    currentAssessmentStep = 1;
    assessmentAnswers = {};
    document.querySelectorAll('.assessment-step').forEach(step => step.classList.remove('active'));
    document.getElementById('step1').classList.add('active');
    updateProgress();
    updateNavigationButtons();
}

function closeResults() {
    document.getElementById('resultsModal').style.display = 'none';
}

// Booking functions
function initializeBooking() {
    const timeSlots = document.querySelectorAll('.time-slot.available');
    timeSlots.forEach(slot => {
        slot.addEventListener('click', function() {
            // Remove previous selection
            timeSlots.forEach(s => s.classList.remove('selected'));
            
            // Select current slot
            this.classList.add('selected');
            
            // Show booking modal
            showBookingModal(this);
        });
    });
}

function showBookingModal(selectedSlot) {
    const time = selectedSlot.getAttribute('data-time');
    const type = selectedSlot.getAttribute('data-type');
    const dayElement = selectedSlot.closest('.day-column');
    const day = dayElement.querySelector('.day-header').textContent;
    const date = dayElement.querySelector('.day-date').textContent;
    
    document.getElementById('selectedDate').textContent = `${day}, ${date}`;
    document.getElementById('selectedTime').textContent = time;
    document.getElementById('selectedType').textContent = type === 'tele' ? 'टेलीकंसल्टेशन' : 'क्लिनिक विजिट';
    
    document.getElementById('bookingModal').style.display = 'block';
}

function closeBookingModal() {
    document.getElementById('bookingModal').style.display = 'none';
    document.querySelectorAll('.time-slot').forEach(slot => slot.classList.remove('selected'));
}

function confirmBooking() {
    // Close booking modal
    closeBookingModal();
    
    // Show success modal
    document.getElementById('successModal').style.display = 'block';
}

function closeSuccessModal() {
    document.getElementById('successModal').style.display = 'none';
}

// Close modals when clicking outside
window.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});

// Mobile navigation toggle
document.querySelector('.nav-toggle').addEventListener('click', function() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
});

// Utility functions
function formatDate(date) {
    return new Date(date).toLocaleDateString('hi-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatTime(time) {
    return new Date(`2000-01-01T${time}`).toLocaleTimeString('hi-IN', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Chatbot functionality
let chatbotState = 'closed'; // closed, minimized, normal, maximized
let chatHistory = [];

// Knowledge base for the chatbot
const chatbotKnowledge = {
    'नींद की गुणवत्ता कैसे सुधारें?': {
        answer: 'नींद की गुणवत्ता सुधारने के लिए ये उपाय अपनाएं:\n\n• नियमित सोने का समय निर्धारित करें\n• सोने से 1 घंटे पहले स्क्रीन से दूर रहें\n• बेडरूम को ठंडा, अंधेरा और शांत रखें\n• कैफीन और शराब से बचें\n• रिलैक्सेशन तकनीकों का उपयोग करें\n• नियमित व्यायाम करें लेकिन सोने से 3-4 घंटे पहले नहीं',
        suggestions: ['CBT-I क्या है?', 'अनिद्रा के लक्षण क्या हैं?', 'डॉक्टर से कब मिलना चाहिए?']
    },
    'CBT-I क्या है?': {
        answer: 'CBT-I (Cognitive Behavioral Therapy for Insomnia) नींद की समस्याओं के लिए एक प्रभावी उपचार है:\n\n• सोने के समय को नियंत्रित करना\n• बेडरूम को सिर्फ सोने के लिए उपयोग करना\n• नकारात्मक विचारों को बदलना\n• रिलैक्सेशन तकनीकें सीखना\n• नींद की स्वच्छता के नियमों का पालन करना\n\nयह दवा के बिना नींद की समस्याओं को ठीक करने का सबसे प्रभावी तरीका है।',
        suggestions: ['नींद की गुणवत्ता कैसे सुधारें?', 'अनिद्रा के लक्षण क्या हैं?']
    },
    'अनिद्रा के लक्षण क्या हैं?': {
        answer: 'अनिद्रा के मुख्य लक्षण हैं:\n\n• सोने में कठिनाई\n• रात में बार-बार जागना\n• जल्दी उठ जाना और फिर न सो पाना\n• दिन में थकान और नींद आना\n• एकाग्रता में कमी\n• मूड में बदलाव\n• चिंता और तनाव\n\nयदि ये लक्षण 3 सप्ताह से अधिक समय तक रहें तो डॉक्टर से सलाह लें।',
        suggestions: ['डॉक्टर से कब मिलना चाहिए?', 'CBT-I क्या है?']
    },
    'डॉक्टर से कब मिलना चाहिए?': {
        answer: 'नींद विशेषज्ञ से मिलने के लिए ये स्थितियां हैं:\n\n• 3 सप्ताह से अधिक समय तक नींद की समस्या\n• दिन में काम पर प्रभाव पड़ना\n• चिंता या अवसाद के लक्षण\n• नींद की गोलियों पर निर्भरता\n• सांस लेने में तकलीफ या खर्राटे\n• पैरों में बेचैनी\n\nहमारे पास डॉ. प्रिया शर्मा जैसे अनुभवी विशेषज्ञ हैं जो आपकी मदद कर सकते हैं।',
        suggestions: ['अपॉइंटमेंट कैसे बुक करें?', 'CBT-I क्या है?']
    },
    'अपॉइंटमेंट कैसे बुक करें?': {
        answer: 'अपॉइंटमेंट बुक करने के लिए:\n\n1. "अपॉइंटमेंट" पेज पर जाएं\n2. उपलब्ध समय स्लॉट चुनें\n3. टेलीकंसल्टेशन या क्लिनिक विजिट चुनें\n4. अपनी जानकारी भरें\n5. बुकिंग की पुष्टि करें\n\nहमारे पास सुबह 9 बजे से शाम 4 बजे तक स्लॉट उपलब्ध हैं।',
        suggestions: ['डॉक्टर से कब मिलना चाहिए?', 'टेलीकंसल्टेशन क्या है?']
    },
    'टेलीकंसल्टेशन क्या है?': {
        answer: 'टेलीकंसल्टेशन एक वीडियो कॉल के माध्यम से डॉक्टर से मिलने का तरीका है:\n\n• घर बैठे डॉक्टर से सलाह\n• समय और पैसे की बचत\n• सुरक्षित और सुविधाजनक\n• उतनी ही प्रभावी जितनी व्यक्तिगत मुलाकात\n• सभी जरूरी जांच और सलाह मिलती है\n\nआप अपने मोबाइल या कंप्यूटर से आसानी से जुड़ सकते हैं।',
        suggestions: ['अपॉइंटमेंट कैसे बुक करें?', 'डॉक्टर से कब मिलना चाहिए?']
    },
    'default': {
        answer: 'मुझे खेद है, मैं आपके सवाल को पूरी तरह समझ नहीं पाया। कृपया नीचे दिए गए विकल्पों में से कोई चुनें या अपना सवाल दोबारा पूछें।',
        suggestions: ['नींद की गुणवत्ता कैसे सुधारें?', 'CBT-I क्या है?', 'अनिद्रा के लक्षण क्या हैं?', 'डॉक्टर से कब मिलना चाहिए?']
    }
};

// Chatbot functions
function toggleChatbot() {
    const widget = document.getElementById('chatbot-widget');
    const toggle = document.getElementById('chatbot-toggle');
    
    if (chatbotState === 'closed') {
        widget.classList.remove('minimized', 'maximized');
        widget.style.display = 'flex';
        toggle.style.display = 'none';
        chatbotState = 'normal';
    } else {
        closeChatbot();
    }
}

function minimizeChatbot() {
    const widget = document.getElementById('chatbot-widget');
    const toggle = document.getElementById('chatbot-toggle');
    
    widget.classList.add('minimized');
    widget.classList.remove('maximized');
    toggle.style.display = 'flex';
    chatbotState = 'minimized';
}

function maximizeChatbot() {
    const widget = document.getElementById('chatbot-widget');
    
    if (widget.classList.contains('maximized')) {
        widget.classList.remove('maximized');
        chatbotState = 'normal';
    } else {
        widget.classList.add('maximized');
        widget.classList.remove('minimized');
        chatbotState = 'maximized';
    }
}

function closeChatbot() {
    const widget = document.getElementById('chatbot-widget');
    const toggle = document.getElementById('chatbot-toggle');
    
    widget.style.display = 'none';
    toggle.style.display = 'flex';
    chatbotState = 'closed';
}

function askQuickQuestion(question) {
    const inputField = document.getElementById('chatbot-input-field');
    inputField.value = question;
    sendChatbotMessage();
}

function sendChatbotMessage() {
    const inputField = document.getElementById('chatbot-input-field');
    const message = inputField.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage(message, 'user');
    inputField.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Simulate bot response delay
    setTimeout(() => {
        hideTypingIndicator();
        const response = getBotResponse(message);
        addMessage(response.answer, 'bot', response.suggestions);
    }, 1500);
}

function handleChatbotKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatbotMessage();
    }
}

function addMessage(content, sender, suggestions = null) {
    const messagesContainer = document.getElementById('chatbot-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chatbot-message ${sender}-message`;
    
    const avatar = sender === 'bot' ? '🤖' : '👤';
    
    let suggestionsHtml = '';
    if (suggestions && sender === 'bot') {
        suggestionsHtml = `
            <div class="quick-questions">
                ${suggestions.map(suggestion => 
                    `<button class="quick-btn" onclick="askQuickQuestion('${suggestion}')">${suggestion}</button>`
                ).join('')}
            </div>
        `;
    }
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <p>${content}</p>
            ${suggestionsHtml}
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Store in chat history
    chatHistory.push({ content, sender, timestamp: new Date() });
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatbot-messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chatbot-message bot-message';
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="typing-indicator">
            <span>टाइप कर रहा है</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function getBotResponse(message) {
    // Simple keyword matching for responses
    const lowerMessage = message.toLowerCase();
    
    // Check for exact matches first
    if (chatbotKnowledge[message]) {
        return chatbotKnowledge[message];
    }
    
    // Check for keyword matches
    if (lowerMessage.includes('नींद') && (lowerMessage.includes('सुधार') || lowerMessage.includes('बेहतर'))) {
        return chatbotKnowledge['नींद की गुणवत्ता कैसे सुधारें?'];
    }
    
    if (lowerMessage.includes('cbt') || lowerMessage.includes('थेरेपी')) {
        return chatbotKnowledge['CBT-I क्या है?'];
    }
    
    if (lowerMessage.includes('लक्षण') || lowerMessage.includes('समस्या')) {
        return chatbotKnowledge['अनिद्रा के लक्षण क्या हैं?'];
    }
    
    if (lowerMessage.includes('डॉक्टर') || lowerMessage.includes('विशेषज्ञ')) {
        return chatbotKnowledge['डॉक्टर से कब मिलना चाहिए?'];
    }
    
    if (lowerMessage.includes('अपॉइंटमेंट') || lowerMessage.includes('बुक')) {
        return chatbotKnowledge['अपॉइंटमेंट कैसे बुक करें?'];
    }
    
    if (lowerMessage.includes('टेली') || lowerMessage.includes('वीडियो')) {
        return chatbotKnowledge['टेलीकंसल्टेशन क्या है?'];
    }
    
    // Default response
    return chatbotKnowledge['default'];
}

// Therapy page functionality
let therapyProgress = JSON.parse(localStorage.getItem('therapyProgress')) || {
    videosWatched: 0,
    daysActive: 0,
    techniquesLearned: 0,
    lastActiveDate: null
};

function updateTherapyPage() {
    // Update assessment results if available
    const lastAssessment = JSON.parse(localStorage.getItem('lastAssessmentResult'));
    if (lastAssessment) {
        document.getElementById('therapyScore').textContent = lastAssessment.totalScore;
        document.getElementById('therapySeverity').textContent = lastAssessment.severity;
        document.getElementById('therapyRecommendation').textContent = lastAssessment.recommendations.join(' ');
        
        // Update severity badge color
        const severityElement = document.getElementById('therapySeverity');
        severityElement.className = 'severity-value';
        if (lastAssessment.severity === 'मध्यम') {
            severityElement.style.background = 'rgba(253, 203, 110, 0.1)';
            severityElement.style.color = '#FDCB6E';
        } else if (lastAssessment.severity === 'गंभीर') {
            severityElement.style.background = 'rgba(225, 112, 85, 0.1)';
            severityElement.style.color = '#E17055';
        }
    }
    
    // Update progress stats
    document.getElementById('videosWatched').textContent = therapyProgress.videosWatched;
    document.getElementById('daysActive').textContent = therapyProgress.daysActive;
    document.getElementById('techniquesLearned').textContent = therapyProgress.techniquesLearned;
}

function startTherapySession() {
    // Track therapy session start
    const today = new Date().toDateString();
    if (therapyProgress.lastActiveDate !== today) {
        therapyProgress.daysActive++;
        therapyProgress.lastActiveDate = today;
        localStorage.setItem('therapyProgress', JSON.stringify(therapyProgress));
        updateTherapyPage();
    }
    
    // Show therapy session modal or redirect to first video
    alert('चिकित्सा सत्र शुरू हो रहा है! पहले वीडियो से शुरुआत करें।');
    
    // Open first CBT-I video
    window.open('https://www.youtube.com/watch?v=GyxqKoQAxTk', '_blank');
    
    // Track video watch
    trackVideoWatch('CBT-I का परिचय');
}

function downloadTherapyPlan() {
    const lastAssessment = JSON.parse(localStorage.getItem('lastAssessmentResult'));
    let therapyPlan = '';
    
    if (lastAssessment) {
        therapyPlan = `नींद साथी - व्यक्तिगत चिकित्सा योजना
        
आकलन परिणाम:
- ISI स्कोर: ${lastAssessment.totalScore}
- गंभीरता: ${lastAssessment.severity}

अनुशंसित चिकित्सा:
${lastAssessment.recommendations.map(rec => `• ${rec}`).join('\n')}

चिकित्सा कार्यक्रम:
सप्ताह 1: नींद स्वच्छता
• नियमित सोने का समय निर्धारित करें
• बेडरूम को ठंडा और अंधेरा रखें
• सोने से 1 घंटे पहले स्क्रीन से दूर रहें
• कैफीन का सेवन कम करें

सप्ताह 2: रिलैक्सेशन तकनीकें
• प्रगतिशील मांसपेशी रिलैक्सेशन सीखें
• गहरी सांस लेने की तकनीक अभ्यास करें
• मेडिटेशन शुरू करें
• सोने से पहले रिलैक्सेशन रूटीन बनाएं

सप्ताह 3-4: CBT-I तकनीकें
• नींद प्रतिबंध तकनीक सीखें
• संज्ञानात्मक पुनर्गठन अभ्यास करें
• नींद डायरी रखना जारी रखें
• प्रगति का मूल्यांकन करें

वीडियो लिंक्स:
1. CBT-I का परिचय: https://www.youtube.com/watch?v=GyxqKoQAxTk
2. नींद प्रतिबंध तकनीक: https://www.youtube.com/watch?v=DdtHsaZ_Xp4
3. नींद स्वच्छता: https://www.youtube.com/watch?v=s2dQPI9ZPO0
4. प्रगतिशील मांसपेशी रिलैक्सेशन: https://www.youtube.com/watch?v=STPuP0kUnTo
5. गहरी सांस लेने की तकनीक: https://www.youtube.com/watch?v=kQUae5zodJ8
6. बेडरूम का वातावरण: https://www.youtube.com/watch?v=dxsR_l5bu7w
7. दिनचर्या और नींद: https://www.youtube.com/watch?v=KVfDhbFRfy0
8. संज्ञानात्मक पुनर्गठन: https://www.youtube.com/watch?v=SclJBsQYI_Q
9. नींद प्रतिबंध चिकित्सा: https://www.youtube.com/watch?v=7okjM6Tq14E

तैयार किया गया: ${new Date().toLocaleDateString('hi-IN')}
नींद साथी - SleepMitra`;
    } else {
        therapyPlan = `नींद साथी - सामान्य चिकित्सा योजना

सामान्य नींद स्वच्छता सुझाव:
• नियमित सोने का समय निर्धारित करें
• बेडरूम को ठंडा, अंधेरा और शांत रखें
• सोने से 1 घंटे पहले स्क्रीन से दूर रहें
• कैफीन और शराब से बचें
• रिलैक्सेशन तकनीकों का उपयोग करें
• नियमित व्यायाम करें

वीडियो लिंक्स:
1. CBT-I का परिचय: https://www.youtube.com/watch?v=GyxqKoQAxTk
2. नींद प्रतिबंध तकनीक: https://www.youtube.com/watch?v=DdtHsaZ_Xp4
3. नींद स्वच्छता: https://www.youtube.com/watch?v=s2dQPI9ZPO0
4. प्रगतिशील मांसपेशी रिलैक्सेशन: https://www.youtube.com/watch?v=STPuP0kUnTo
5. गहरी सांस लेने की तकनीक: https://www.youtube.com/watch?v=kQUae5zodJ8
6. बेडरूम का वातावरण: https://www.youtube.com/watch?v=dxsR_l5bu7w
7. दिनचर्या और नींद: https://www.youtube.com/watch?v=KVfDhbFRfy0
8. संज्ञानात्मक पुनर्गठन: https://www.youtube.com/watch?v=SclJBsQYI_Q
9. नींद प्रतिबंध चिकित्सा: https://www.youtube.com/watch?v=7okjM6Tq14E

तैयार किया गया: ${new Date().toLocaleDateString('hi-IN')}
नींद साथी - SleepMitra`;
    }
    
    // Create and download file
    const blob = new Blob([therapyPlan], { type: 'text/plain;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sleepmitra-therapy-plan-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

function trackVideoWatch(videoTitle) {
    therapyProgress.videosWatched++;
    localStorage.setItem('therapyProgress', JSON.stringify(therapyProgress));
    updateTherapyPage();
    
    // Show notification
    showNotification(`"${videoTitle}" वीडियो देखने के लिए धन्यवाद!`);
}

function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #6C5CE7;
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        font-family: 'Noto Sans Devanagari', sans-serif;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add CSS for notifications
const notificationCSS = `
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}
`;

// Add notification CSS to head
const style = document.createElement('style');
style.textContent = notificationCSS;
document.head.appendChild(style);

// Track video clicks
document.addEventListener('click', function(e) {
    if (e.target.closest('.video-link')) {
        const videoLink = e.target.closest('.video-link');
        const videoTitle = videoLink.querySelector('h6').textContent;
        trackVideoWatch(videoTitle);
    }
});

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Hide chatbot widget initially
    document.getElementById('chatbot-widget').style.display = 'none';
    
    // Update therapy page if it's the current page
    if (document.getElementById('therapy').classList.contains('active')) {
        updateTherapyPage();
    }
});
