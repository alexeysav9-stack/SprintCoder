/**
 * SprintCoder — Typing Engine
 * Handles: character-by-character rendering, WPM/CPM/accuracy tracking,
 * error stats collection, auto-submit on completion.
 */

(function () {
  'use strict';

  /* ── Parse snippet data from the hidden <script> tag ── */
  const rawData = JSON.parse(document.getElementById('snippet-data').textContent);
  const SNIPPET_ID    = rawData.snippet_id;
  const CODE          = rawData.code;
  const SAVE_URL      = rawData.save_url;
  const RESULT_BASE   = rawData.result_base_url;   // e.g. /result/0/
  const CSRF          = rawData.csrf_token;

  /* ── DOM refs ─────────────────────────────────────────── */
  const display   = document.getElementById('code-display');
  const input     = document.getElementById('typing-input');
  const overlay   = document.getElementById('start-overlay');
  const hudWpm    = document.getElementById('hud-wpm').querySelector('.hud-value');
  const hudAcc    = document.getElementById('hud-acc').querySelector('.hud-value');
  const hudTime   = document.getElementById('hud-time').querySelector('.hud-value');
  const hudErrors = document.getElementById('hud-errors').querySelector('.hud-value');

  /* ── State ────────────────────────────────────────────── */
  let chars      = [];    // array of span elements
  let typed      = [];    // array of booleans (correct=true / wrong=false / null=not typed)
  let startTime  = null;
  let timerID    = null;
  let done       = false;
  let totalErrors = 0;
  const errorMap  = {};   // { char: count }

  /* ── Build character spans ────────────────────────────── */
  function buildDisplay() {
    display.innerHTML = '';
    chars = [];
    typed = [];

    for (let i = 0; i < CODE.length; i++) {
      const ch = CODE[i];
      const span = document.createElement('span');
      span.classList.add('char');

      // Render visible chars; spaces and newlines need special handling
      if (ch === '\n') {
        span.textContent = '\n';
      } else if (ch === ' ') {
        span.innerHTML = '&nbsp;';
      } else {
        span.textContent = ch;
      }

      display.appendChild(span);
      chars.push(span);
      typed.push(null);
    }

    // Put cursor on first char
    setCursor(0);
  }

  function setCursor(index) {
    chars.forEach(c => c.classList.remove('cursor'));
    if (index < chars.length) chars[index].classList.add('cursor');
  }

  /* ── Timer ────────────────────────────────────────────── */
  function startTimer() {
    startTime = performance.now();
    timerID = setInterval(updateHUD, 100);
  }

  function stopTimer() {
    clearInterval(timerID);
  }

  function getElapsedSeconds() {
    if (!startTime) return 0;
    return (performance.now() - startTime) / 1000;
  }

  function updateHUD() {
    const elapsed = getElapsedSeconds();
    const typedCount = typed.filter(t => t !== null).length;
    const correctCount = typed.filter(t => t === true).length;

    // WPM: standard 5 chars = 1 word
    const wpm = elapsed > 0 ? (correctCount / 5) / (elapsed / 60) : 0;
    const cpm = elapsed > 0 ? correctCount / (elapsed / 60) : 0;
    const acc = typedCount > 0 ? (correctCount / typedCount) * 100 : 100;

    hudWpm.textContent    = Math.round(wpm);
    hudAcc.textContent    = acc.toFixed(1);
    hudTime.textContent   = elapsed.toFixed(1);
    hudErrors.textContent = totalErrors;
  }

  /* ── Handle keydown ───────────────────────────────────── */
  input.addEventListener('keydown', function (e) {
    // Tab → insert 4 spaces at cursor position (IDE-style)
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = input.selectionStart;
      const end   = input.selectionEnd;
      input.value = input.value.slice(0, start) + '    ' + input.value.slice(end);
      input.selectionStart = input.selectionEnd = start + 4;
      // Manually fire input event so typing engine re-syncs
      input.dispatchEvent(new Event('input'));
      return;
    }
    // Ctrl+R → restart exercise
    if (e.key === 'r' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      resetExercise();
      return;
    }
    // Escape → go back to home
    if (e.key === 'Escape') {
      e.preventDefault();
      window.location.href = '/';
      return;
    }
  });

  /* ── Block paste (anti-cheat) ────────────────────────── */
  input.addEventListener('paste', function (e) {
    e.preventDefault();
    // Flash a brief warning on the display
    display.classList.add('paste-blocked');
    setTimeout(() => display.classList.remove('paste-blocked'), 600);
  });

  input.addEventListener('input', function (e) {
    if (done) return;

    const value = input.value;
    const pos   = value.length; // current typed length = cursor position

    // Start timer on first keystroke
    if (!startTime && pos > 0) {
      startTimer();
      overlay.classList.add('hidden');
    }

    // Sync each character
    for (let i = 0; i < CODE.length; i++) {
      if (i < pos) {
        const expected = CODE[i];
        const actual   = value[i];
        const correct  = actual === expected;
        typed[i] = correct;

        chars[i].classList.remove('char', 'correct', 'wrong', 'cursor');
        chars[i].classList.add('char', correct ? 'correct' : 'wrong');

        // Track error
        if (!correct && typed[i] !== null) {
          const key = expected === '\n' ? '↵' : expected === ' ' ? '·' : expected;
          errorMap[key] = (errorMap[key] || 0) + 1;
        }
      } else {
        // Not yet typed
        chars[i].classList.remove('correct', 'wrong', 'cursor');
        typed[i] = null;
      }
    }

    // Recount total errors
    totalErrors = typed.filter(t => t === false).length;
    setCursor(pos);
    updateHUD();

    // Check completion
    if (pos >= CODE.length) {
      finishExercise();
    }
  });

  /* ── Finish exercise ──────────────────────────────────── */
  function finishExercise() {
    if (done) return;
    done = true;
    stopTimer();

    const elapsed    = getElapsedSeconds();
    const correctCount = typed.filter(t => t === true).length;
    const typedCount   = typed.filter(t => t !== null).length;
    const wpm  = elapsed > 0 ? (correctCount / 5) / (elapsed / 60) : 0;
    const cpm  = elapsed > 0 ? correctCount / (elapsed / 60) : 0;
    const acc  = typedCount > 0 ? (correctCount / typedCount) * 100 : 100;

    // Disable input
    input.disabled = true;

    // Submit result
    fetch(SAVE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': CSRF,
      },
      body: JSON.stringify({
        snippet_id:   SNIPPET_ID,
        wpm:          wpm,
        cpm:          cpm,
        accuracy:     acc,
        time_seconds: elapsed,
        errors_json:  errorMap,
      }),
    })
    .then(r => r.json())
    .then(data => {
      if (data.status === 'ok') {
        const resultUrl = RESULT_BASE.replace('/0/', `/${data.attempt_id}/`);
        window.location.href = resultUrl;
      } else {
        console.error('Save error:', data.message);
        // Still navigate to result-less page; graceful fallback
        alert('Could not save result, but great job!');
      }
    })
    .catch(err => {
      console.error('Network error:', err);
      alert('Network error saving result.');
    });
  }

  /* ── Reset exercise ───────────────────────────────────── */
  function resetExercise() {
    done = false;
    stopTimer();
    startTime = null;
    totalErrors = 0;
    Object.keys(errorMap).forEach(k => delete errorMap[k]);
    input.value = '';
    input.disabled = false;
    input.style.pointerEvents = 'none';
    buildDisplay();
    updateHUD();
    overlay.classList.remove('hidden');
  }

  /* ── Overlay click to focus ───────────────────────────── */
  function dismissOverlay() {
    overlay.classList.add('hidden');
    input.style.pointerEvents = 'auto';
    input.focus();
  }

  overlay.addEventListener('click', dismissOverlay);
  overlay.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      dismissOverlay();
    }
  });

  display.addEventListener('click', function () {
    if (!overlay.classList.contains('hidden')) {
      dismissOverlay();
    }
  });

  /* ── Init ─────────────────────────────────────────────── */
  buildDisplay();
  updateHUD();
  // Don't auto-focus — wait for user to click overlay
})();
