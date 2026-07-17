/* ============================================
   StudentPath - Centralized JavaScript
   ============================================ */

// --- Slider Utilities ---

function updateSlider(slider) {
  const value = slider.value;
  const min = parseInt(slider.min);
  const max = parseInt(slider.max);
  const percent = ((value - min) / (max - min)) * 100;
  const valueDisplay = document.getElementById(slider.id + '_value');

  slider.style.setProperty('--fill-percent', percent + '%');
  slider.setAttribute('data-filled', 'true');

  if (valueDisplay) {
    valueDisplay.textContent = value;
  }
}

function initSliders() {
  document.querySelectorAll('input[type="range"]').forEach(slider => {
    updateSlider(slider);
  });
}

// --- Sample Data ---

const SAMPLE_DATA = {
  career: {
    Math_Score: 85,
    Science_Score: 78,
    Programming_Skill: 4,
    Communication_Skill: 3,
    Logical_Ability: 4,
    R_score: 3,
    I_score: 8,
    A_score: 4,
    S_score: 5,
    E_score: 6,
    C_score: 7
  },
  stress: {
    anxiety_level: 15,
    self_esteem: 10,
    mental_health_history: 0,
    depression: 18,
    headache: 4,
    blood_pressure: 2,
    sleep_quality: 2,
    breathing_problem: 3,
    noise_level: 4,
    living_conditions: 3,
    safety: 4,
    basic_needs: 4,
    academic_performance: 3,
    study_load: 4,
    teacher_student_relationship: 3,
    future_career_concerns: 4,
    social_support: 1,
    peer_pressure: 3,
    extracurricular_activities: 2,
    bullying: 1
  },
  performance: {
    school: '1',
    sex: '1',
    age: '17',
    address: '1',
    famsize: '1',
    Pstatus: '1',
    Medu: '3',
    Fedu: '3',
    Mjob: 'teacher',
    Fjob: 'services',
    guardian: 'mother',
    traveltime: '2',
    studytime: '3',
    failures: '0',
    schoolsup: '1',
    famsup: '1',
    paid: '0',
    activities: '1',
    nursery: '1',
    higher: '1',
    internet: '1',
    romantic: '0',
    famrel: '4',
    freetime: '3',
    goout: '3',
    Dalc: '1',
    Walc: '2',
    health: '4',
    absences: '2',
    G1: '13',
    G2: '14',
    reason: 'course'
  }
};

function fillSampleData(module) {
  const data = SAMPLE_DATA[module];
  if (!data) return;

  const form = document.getElementById(module + '-form');
  if (!form) return;

  for (const [key, value] of Object.entries(data)) {
    const el = form.querySelector('[name="' + key + '"]');
    if (!el) continue;

    if (el.type === 'range') {
      el.value = value;
      updateSlider(el);
    } else if (el.tagName === 'SELECT') {
      el.value = String(value);
    } else {
      el.value = value;
    }
  }
}

// --- Radar Chart (RIASEC for Career) ---

function drawRadarChart(canvasId, scores, labels) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;
  const cx = w / 2;
  const cy = h / 2;
  const radius = Math.min(cx, cy) - 30;
  const n = scores.length;
  const angleStep = (2 * Math.PI) / n;

  ctx.clearRect(0, 0, w, h);

  // Grid circles
  for (let level = 1; level <= 5; level++) {
    const r = (radius / 5) * level;
    ctx.beginPath();
    for (let i = 0; i <= n; i++) {
      const angle = i * angleStep - Math.PI / 2;
      const x = cx + r * Math.cos(angle);
      const y = cy + r * Math.sin(angle);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.strokeStyle = 'rgba(26, 26, 46, 0.1)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // Axis lines
  for (let i = 0; i < n; i++) {
    const angle = i * angleStep - Math.PI / 2;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + radius * Math.cos(angle), cy + radius * Math.sin(angle));
    ctx.strokeStyle = 'rgba(26, 26, 46, 0.15)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // Data polygon
  const maxScore = 10;
  ctx.beginPath();
  for (let i = 0; i < n; i++) {
    const angle = i * angleStep - Math.PI / 2;
    const r = (scores[i] / maxScore) * radius;
    const x = cx + r * Math.cos(angle);
    const y = cy + r * Math.sin(angle);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.closePath();
  ctx.fillStyle = 'rgba(13, 115, 119, 0.15)';
  ctx.fill();
  ctx.strokeStyle = 'rgba(13, 115, 119, 0.6)';
  ctx.lineWidth = 2;
  ctx.stroke();

  // Data points
  for (let i = 0; i < n; i++) {
    const angle = i * angleStep - Math.PI / 2;
    const r = (scores[i] / maxScore) * radius;
    const x = cx + r * Math.cos(angle);
    const y = cy + r * Math.sin(angle);
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, 2 * Math.PI);
    ctx.fillStyle = '#0D7377';
    ctx.fill();
  }

  // Labels
  ctx.fillStyle = '#1A1A2E';
  ctx.font = '11px Plus Jakarta Sans, sans-serif';
  ctx.textAlign = 'center';
  for (let i = 0; i < n; i++) {
    const angle = i * angleStep - Math.PI / 2;
    const labelR = radius + 20;
    const x = cx + labelR * Math.cos(angle);
    const y = cy + labelR * Math.sin(angle);
    ctx.fillText(labels[i], x, y + 4);
  }
}

// --- Gauge Chart ---

function drawGauge(svgId, value, maxValue, label, color) {
  const svg = document.getElementById(svgId);
  if (!svg) return;

  const size = 200;
  const strokeWidth = 16;
  const cx = size / 2;
  const cy = size / 2 + 10;
  const r = 70;
  const startAngle = -135;
  const endAngle = 135;
  const angleRange = endAngle - startAngle;

  const percent = Math.min(value / maxValue, 1);
  const fillAngle = startAngle + (angleRange * percent);

  const startRad = (startAngle * Math.PI) / 180;
  const endRad = (endAngle * Math.PI) / 180;
  const fillRad = (fillAngle * Math.PI) / 180;

  const bgStartX = cx + r * Math.cos(startRad);
  const bgStartY = cy + r * Math.sin(startRad);
  const bgEndX = cx + r * Math.cos(endRad);
  const bgEndY = cy + r * Math.sin(endRad);
  const fillEndX = cx + r * Math.cos(fillRad);
  const fillEndY = cy + r * Math.sin(fillRad);

  svg.setAttribute('viewBox', '0 0 ' + size + ' ' + size);
  svg.innerHTML = '';

  // Background arc
  const bgPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  bgPath.setAttribute('d', describeArc(cx, cy, r, startAngle, endAngle));
  bgPath.setAttribute('fill', 'none');
  bgPath.setAttribute('stroke', 'rgba(26, 26, 46, 0.1)');
  bgPath.setAttribute('stroke-width', strokeWidth);
  bgPath.setAttribute('stroke-linecap', 'round');
  svg.appendChild(bgPath);

  // Fill arc
  const fillPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  fillPath.setAttribute('d', describeArc(cx, cy, r, startAngle, fillAngle));
  fillPath.setAttribute('fill', 'none');
  fillPath.setAttribute('stroke', color);
  fillPath.setAttribute('stroke-width', strokeWidth);
  fillPath.setAttribute('stroke-linecap', 'round');
  svg.appendChild(fillPath);

  // Value text
  const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  text.setAttribute('x', cx);
  text.setAttribute('y', cy + 5);
  text.setAttribute('text-anchor', 'middle');
  text.setAttribute('font-family', 'Fraunces, serif');
  text.setAttribute('font-size', '36');
  text.setAttribute('font-weight', '700');
  text.setAttribute('fill', color);
  text.textContent = value;
  svg.appendChild(text);

  // Label
  const labelText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  labelText.setAttribute('x', cx);
  labelText.setAttribute('y', cy + 28);
  labelText.setAttribute('text-anchor', 'middle');
  labelText.setAttribute('font-family', 'Plus Jakarta Sans, sans-serif');
  labelText.setAttribute('font-size', '12');
  labelText.setAttribute('fill', '#5C5C6D');
  labelText.textContent = label;
  svg.appendChild(labelText);
}

function polarToCartesian(cx, cy, r, angleDeg) {
  const rad = (angleDeg * Math.PI) / 180;
  return {
    x: cx + r * Math.cos(rad),
    y: cy + r * Math.sin(rad)
  };
}

function describeArc(cx, cy, r, startAngle, endAngle) {
  const start = polarToCartesian(cx, cy, r, endAngle);
  const end = polarToCartesian(cx, cy, r, startAngle);
  const largeArcFlag = endAngle - startAngle <= 180 ? '0' : '1';
  return [
    'M', start.x, start.y,
    'A', r, r, 0, largeArcFlag, 0, end.x, end.y
  ].join(' ');
}

// --- Time Update ---

function updateTime() {
  const el = document.getElementById('current-time');
  if (!el) return;
  const now = new Date();
  const options = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
  el.textContent = now.toLocaleDateString('en-US', options);
}

// --- Init ---

document.addEventListener('DOMContentLoaded', function() {
  initSliders();
  updateTime();
  setInterval(updateTime, 60000);

  // Form reset handling
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('reset', function() {
      setTimeout(initSliders, 0);
    });
  });
});

// --- Smooth scroll for landing nav ---

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
