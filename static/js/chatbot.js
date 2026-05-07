/* Chatbot Widget JS */
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('chatbot-toggle');
  const panel = document.getElementById('chatbot-panel');
  const input = document.getElementById('chatbot-input');
  const sendBtn = document.getElementById('chatbot-send');
  const msgs = document.getElementById('chatbot-messages');
  if (!toggle) return;

  let history = [];
  let isOpen = false;

  toggle.addEventListener('click', () => {
    isOpen = !isOpen;
    panel.classList.toggle('open', isOpen);
    toggle.innerHTML = isOpen ? '✕' : '💬';
    if (isOpen && msgs.children.length === 0) addBotMsg("Hi! I'm SmartBot 🤖 How can I help you today?");
  });

  function addBotMsg(text) {
    const div = document.createElement('div');
    div.className = 'chat-msg bot'; div.textContent = text;
    msgs.appendChild(div); msgs.scrollTop = msgs.scrollHeight;
  }

  function addUserMsg(text) {
    const div = document.createElement('div');
    div.className = 'chat-msg user'; div.textContent = text;
    msgs.appendChild(div); msgs.scrollTop = msgs.scrollHeight;
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;
    addUserMsg(text); input.value = '';
    history.push({ role: 'user', content: text });

    const typing = document.createElement('div');
    typing.className = 'chat-msg bot'; typing.innerHTML = '<em>Typing...</em>';
    msgs.appendChild(typing); msgs.scrollTop = msgs.scrollHeight;

    try {
      const resp = await fetch('/api/ai/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': window.getCSRF ? getCSRF() : '' },
        body: JSON.stringify({ message: text, history: history.slice(-6) })
      });
      const data = await resp.json();
      typing.remove();
      const reply = data.response || data.error || 'Sorry, I could not process that.';
      addBotMsg(reply);
      history.push({ role: 'assistant', content: reply });
    } catch {
      typing.remove();
      addBotMsg('Connection error. Please try again.');
    }
  }

  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
});
