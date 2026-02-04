/*********************************
 * GLOBAL STATE
 *********************************/
let currentQuestions = [];
let currentAnswers = [];

/*********************************
 * HELPERS
 *********************************/
function getCurrentTopic() {
    return window.currentTopic || 'general';
}

function escapeForJS(str = '') {
    return str
        .replace(/\\/g, '\\\\')
        .replace(/'/g, "\\'")
        .replace(/"/g, '\\"')
        .replace(/\n/g, ' ');
}

/*********************************
 * CSRF (REQUIRED FOR DJANGO POST)
 *********************************/
function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

/*********************************
 * API ENDPOINTS (MATCH urls.py)
 *********************************/
const API = {
    chat: '/psychometric/chat/',
    generate: '/psychometric/generate-question/',
    career: '/psychometric/career-advice/',
};

/*********************************
 * AI CHAT LOGIC
 *********************************/
async function sendMessage(topic = getCurrentTopic()) {
    const input = document.getElementById('chat-input');
    const message = input?.value.trim();
    if (!message) return;

    appendMessage('user', message);
    input.value = '';

    const chatBox = document.getElementById('chat-box');
    const typingId = 'typing-' + Date.now();

    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.id = typingId;
    typingDiv.textContent = 'AI is typing...';

    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch(API.chat, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ message, topic }),
        });

        const data = await response.json();
        document.getElementById(typingId)?.remove();

        appendMessage(
            'ai',
            data.response || data.error || 'No response from AI.'
        );

    } catch (err) {
        document.getElementById(typingId)?.remove();
        appendMessage('ai', 'Error connecting to AI tutor.');
    }
}

function appendMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');

    msgDiv.className = `chat-message ${sender}`;
    msgDiv.textContent = text;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/*********************************
 * QUESTION GENERATOR
 *********************************/
async function generateQuestion(topic = getCurrentTopic()) {
    const container = document.getElementById('question-container');
    container.innerHTML = '<p>Generating question...</p>';

    currentQuestions = [];
    currentAnswers = [];

    try {
        const response = await fetch(`${API.generate}?topic=${topic}`);
        const data = await response.json();

        if (!Array.isArray(data.questions)) {
            container.innerHTML = '<p class="error">No questions received.</p>';
            return;
        }

        currentQuestions = data.questions;
        currentAnswers = new Array(data.questions.length).fill(null);

        let html = '';

        data.questions.forEach((q, qIdx) => {
            html += `
                <div class="question-card" id="q-card-${qIdx}">
                    <p><strong>Q${qIdx + 1}: ${q.text}</strong></p>
                    <div class="options">
            `;

            q.options.forEach((opt, idx) => {
                html += `
                    <button class="option-btn"
                        onclick="checkAnswer(this, ${idx}, ${q.correct_index ?? -1}, 'q-card-${qIdx}')">
                        ${opt}
                    </button>
                `;
            });

            html += `
                    </div>
                    <div class="actions" style="margin-top: 15px;">
                        <button class="ask-ai-btn"
                            onclick="askTutor('${escapeForJS(
                'Help me understand this question: ' + q.text
            )}')">
                            Ask Tutor ✨
                        </button>
                    </div>
                </div>
                <hr class="separator">
            `;
        });

        html += `
            <div class="analyze-section" style="text-align:center; margin-top:50px; margin-bottom:50px;">
                <button class="analyze-btn" onclick="submitAnalysis('${topic}')" 
                    style="font-size: 1.2rem; padding: 15px 30px; font-weight: 700;">
                    Analyze Career Path 🚀
                </button>
                <div id="career-results" class="hidden"></div>
            </div>
        `;

        container.innerHTML = html;

    } catch (err) {
        console.error(err);
        container.innerHTML = '<p class="error">Failed to generate questions.</p>';
    }
}

/*********************************
 * ANSWER CHECKING
 *********************************/
function checkAnswer(btn, selectedIdx, correctIdx, cardId) {
    const card = document.getElementById(cardId);
    if (!card) return;

    const buttons = card.querySelectorAll('.option-btn');
    buttons.forEach(b => b.disabled = true);

    if (correctIdx === -1) {
        btn.classList.add('neutral');
    } else if (selectedIdx === correctIdx) {
        btn.classList.add('correct');
    } else {
        btn.classList.add('wrong');
    }

    const qIndex = Number(cardId.split('-')[2]);
    currentAnswers[qIndex] = {
        question: currentQuestions[qIndex].text,
        selected_option: btn.innerText,
        correct: selectedIdx === correctIdx,
        topic_category: currentQuestions[qIndex].type || 'general',
    };
}

/*********************************
 * CAREER ANALYSIS
 *********************************/
async function submitAnalysis(topic = getCurrentTopic()) {
    const resultsDiv = document.getElementById('career-results');
    resultsDiv.classList.remove('hidden');

    const answered = currentAnswers.filter(Boolean);
    if (answered.length < 3) {
        resultsDiv.innerHTML =
            '<p class="error">Please answer at least 3 questions.</p>';
        return;
    }

    resultsDiv.innerHTML =
        '<p class="typing-indicator">AI is analyzing your profile...</p>';

    try {
        const response = await fetch(API.career, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                topic,
                performance_data: answered,
            }),
        });

        const data = await response.json();

        if (!Array.isArray(data.careers) || data.careers.length === 0) {
            resultsDiv.innerHTML =
                '<p class="error">No strong matches found.</p>';
            return;
        }

        resultsDiv.innerHTML = `
            <h3>🌟 Your AI Career Match</h3>
            <div class="career-grid">
                ${data.careers.map(c => `
                    <div class="career-card">
                        <h4>${c.role}</h4>
                        <p><strong>${c.industry}</strong></p>
                        <p>${c.reason}</p>
                        <button onclick="askTutor('Why is ${escapeForJS(c.role)} a good fit for me?')">
                            Explore This Path
                        </button>
                    </div>
                `).join('')}
            </div>
        `;

    } catch (err) {
        resultsDiv.innerHTML =
            '<p class="error">Career analysis failed.</p>';
    }
}

/*********************************
 * AI TUTOR SHORTCUT
 *********************************/
function askTutor(text) {
    const input = document.getElementById('chat-input');
    if (!input) return;

    input.value = text;
    input.focus();

    document.getElementById('ai-tutor-widget')
        ?.scrollIntoView({ behavior: 'smooth' });
}

/*********************************
 * DYNAMIC STYLES
 *********************************/
const style = document.createElement('style');
style.innerHTML = `
.typing-indicator {
    padding: 10px;
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
    color: #aaa;
    font-style: italic;
}
.ask-ai-btn, .analyze-btn {
    cursor: pointer;
    border: none;
    border-radius: 8px;
}
`;
document.head.appendChild(style);
