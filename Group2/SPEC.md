# Student Guidance Dashboard — SPEC

## 1. Concept & Vision

A student services portal reimagined as a **creative studio** — not a generic dashboard. The student is treated as a whole person: their potential career paths, academic trajectory, and wellbeing. The app feels like a well-designed academic journal meets a modern creative tool — warm, approachable, with personality. Navigation is intuitive; each module is a distinct "department" you visit.

**Subject**: A university student navigating academic and career decisions
**Audience**: FPT University students (18-25), comfortable with tech but appreciate clarity
**Page's single job**: Help students understand themselves through predictions and chat with an AI advisor that knows their history.

---

## 2. Design Language

### Aesthetic Direction
**"Paper & Ink Studio"** — Inspired by architecture firm portfolios and academic journals. Warm paper-like backgrounds, deep ink-like text, with colorful module accents that feel like colored marker highlights.

### Color Palette
```
--paper:        #FAF9F6   /* Warm off-white, the "paper" */
--ink:          #1A1A2E   /* Deep navy-black, primary text */
--ink-muted:    #5C5C6D   /* Secondary text */
--teal:         #0D7377   /* Primary accent — stable, trustworthy */
--amber:        #E8A838   /* Energy accent — warm, optimistic */
--coral:        #E07A5F   /* Action accent — for CTAs */
--sage:         #81B29A   /* Success, positive predictions */
--blush:        #F2CC8F   /* Soft highlight, backgrounds */

/* Module-specific accent bars (left border + icon) */
--career-accent:    #0D7377  /* Teal */
--performance-accent: #E8A838 /* Amber */
--stress-accent:     #81B29A  /* Sage */
--chat-accent:       #E07A5F  /* Coral */
```

### Typography
- **Display**: `Fraunces` (Google Fonts) — Variable optical-size serif with personality
  - Hero headings: Fraunces 700, 3rem
  - Module titles: Fraunces 600, 1.5rem
- **Body**: `Plus Jakarta Sans` (Google Fonts) — Modern geometric sans
  - Body: 400, 1rem
  - Labels: 500, 0.875rem
  - Small: 400, 0.75rem

### Type Scale
```
--text-hero:    3rem / 1.1 line-height
--text-h1:      2rem / 1.2
--text-h2:      1.5rem / 1.3
--text-h3:      1.25rem / 1.4
--text-body:    1rem / 1.6
--text-small:   0.875rem / 1.5
--text-xs:      0.75rem / 1.4
```

### Spatial System
- Base unit: 8px
- Section padding: 32px (4 units)
- Card padding: 24px (3 units)
- Component gaps: 16px (2 units)
- Border radius: 4px (subtle, not rounded)

### Motion Philosophy
- **Page transitions**: Fade in 200ms ease-out
- **Card hover**: Slight lift (translateY -2px) + subtle shadow expansion, 150ms
- **Form inputs**: Border color transition 200ms
- **Result reveals**: Slide up + fade in, staggered 100ms
- **No ambient motion** — the design is already warm, extra animation feels AI-generated

### Visual Assets
- Icons: Phosphor Icons (via CDN) — consistent weight, friendly style
- No stock photos — modules use colored geometric shapes as visual anchors
- Dividers: 1px solid with 4px dot pattern for section breaks

---

## 3. Layout & Structure

### Global Layout
```
+------------------+----------------------------------------+
|  SIDEBAR         |  MAIN CONTENT                           |
|  (240px fixed)   |  (fluid)                                |
|                  |                                         |
|  Logo/Title      |  Module Title + Description              |
|                  |                                         |
|  Nav Items       |  [Form OR Result]                        |
|  (colored left   |                                         |
|   border)         |  [Secondary Content]                    |
|                  |                                         |
|  User Info       |                                         |
|  (bottom)        |                                         |
+------------------+----------------------------------------+
```

### Sidebar
- Fixed left, 240px
- Background: --ink (deep contrast)
- Text: --paper
- Active item: full --paper background with module accent on left (4px)
- Hover: 10% lighter background
- Bottom: Current date + user session indicator

### Content Area
- Max-width: 900px centered
- Background: --paper
- Module header with colored accent (4px left border + icon)

### Responsive Strategy
- Below 768px: Sidebar collapses to top nav bar (horizontal scroll)
- Forms stack vertically on mobile
- Cards remain single-column throughout

---

## 4. Features & Interactions

### Navigation
- Click sidebar item → navigate to module
- Active module highlighted with accent border
- No nested navigation within modules

### Module 1: Career Prediction
**Inputs** (grouped visually):
- Academic: Math_Score (0-100), Science_Score (0-100)
- Skills: Programming_Skill (1-5), Communication_Skill (1-5), Logical_Ability (1-5)
- RIASEC: R_score, I_score, A_score, S_score, E_score, C_score (0-10 each)

**Behavior**:
- Sliders for 1-5 and 0-10 scales
- Number inputs for scores
- "Predict My Career" button → calls model → shows result

**Result**:
- Large display of predicted career with confidence
- Brief explanation of why
- Save to history button (auto-saves anyway)

### Module 2: Performance Prediction
**Inputs** (categorical by nature, dropdowns/radio):
- Demographics: school, sex, age, address, famsize, Pstatus
- Family: Medu, Fedu, guardian
- Academic: studytime, failures, schoolsup, famsup, paid, activities, nursery, higher, internet, romantic
- Lifestyle: famrel, freetime, goout, Dalc, Walc, health, absences
- Prior grades: G1, G2 (if predicting G3)

**Behavior**:
- Organized in collapsible sections by category
- G1/G2 optional based on prediction mode

**Result**:
- Predicted G3 (0-20 grade)
- Visual gauge showing where they fall
- Comparison context (class average)

### Module 3: Stress Prediction
**Inputs** (20 slider inputs):
- Psychological: anxiety_level, self_esteem, depression
- Physical: headache, blood_pressure, sleep_quality, breathing_problem
- Environmental: noise_level, living_conditions, safety, basic_needs
- Academic: academic_performance, study_load, teacher_student_relationship, future_career_concerns
- Social: social_support, peer_pressure, extracurricular_activities, bullying

**Result**:
- Stress level: Low / Medium / High
- Visual indicator (colored badge)
- Key contributing factors highlighted

### Module 4: AI Advisor Chat
**Behavior**:
- Chat interface, messages appear in bubbles
- System prompt includes user's saved prediction history
- User can ask career advice, study tips, stress management
- Model: OpenAI-compatible API (configurable endpoint)

**Chat UI**:
- Message list with user (right, --teal bg) and AI (left, --ink bg)
- Input at bottom with send button
- Typing indicator while waiting

### History
- All predictions automatically saved to session
- Stored as JSON in session
- Used as context for LLM

---

## 5. Component Inventory

### Sidebar Nav Item
- Default: Paper text on ink background, 16px padding
- Hover: 10% lighter background
- Active: Full paper background, 4px left accent border in module color
- Icon + label layout

### Form Input (Number/Slider)
- Default: 1px border --ink-muted, white background
- Focus: Border becomes --teal, subtle glow
- Error: Border becomes --coral, error message below
- Label above in --text-small, --ink-muted

### Select/Dropdown
- Same border treatment as inputs
- Custom arrow icon
- Options: --paper background, hover: --blush

### Button (Primary)
- Background: --coral
- Text: --paper, uppercase, --text-small, 600 weight
- Padding: 12px 24px
- Hover: 10% darker
- Active: 15% darker
- Disabled: 50% opacity

### Button (Secondary)
- Background: transparent
- Border: 1px --ink
- Text: --ink
- Hover: Background --ink, Text --paper

### Card (Result)
- Background: white
- Border: 1px --ink-muted (20% opacity)
- Shadow: 0 2px 8px rgba(0,0,0,0.06)
- Padding: 24px
- Hover: Shadow expands, slight lift

### Chat Bubble (User)
- Background: --teal
- Text: --paper
- Max-width: 70%
- Border-radius: 12px 12px 4px 12px
- Right-aligned

### Chat Bubble (AI)
- Background: --ink
- Text: --paper
- Max-width: 70%
- Border-radius: 12px 12px 12px 4px
- Left-aligned

### Module Header
- Icon (40px, module accent color)
- Title: --text-h2, Fraunces
- Description: --text-body, --ink-muted
- Left border: 4px solid module accent

---

## 6. Technical Approach

### Stack
- **Backend**: Flask (Python)
- **Frontend**: Vanilla HTML/CSS/JS (no framework needed for this scope)
- **Models**: scikit-learn, CatBoost, joblib
- **LLM**: OpenAI-compatible API (configurable)

### Project Structure
```
Web/
├── app.py                  # Main Flask application
├── config.py               # Configuration (API keys, paths)
├── models/                  # Saved models
│   ├── career_model.pkl
│   ├── career_scaler.pkl
│   ├── career_label_encoder.pkl
│   ├── performance_model.pkl
│   ├── performance_scaler.pkl
│   ├── stress_model.pkl
│   └── stress_features.pkl
├── static/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── app.js          # Client-side JS
├── templates/
│   ├── base.html           # Base template with sidebar
│   ├── career.html         # Career prediction
│   ├── performance.html    # Performance prediction
│   ├── stress.html         # Stress prediction
│   └── chat.html           # AI chat
├── utils/
│   ├── models.py           # Model loading and prediction
│   ├── history.py          # History management
│   └── llm.py              # LLM interaction
├── train_models.py         # Script to train/export models
└── requirements.txt
```

### API Endpoints
- `GET /` → Redirect to /career
- `GET /career` → Career prediction page
- `POST /api/career/predict` → Career prediction
- `GET /performance` → Performance prediction page
- `POST /api/performance/predict` → Performance prediction
- `GET /stress` → Stress prediction page
- `POST /api/stress/predict` → Stress prediction
- `GET /chat` → Chat page
- `POST /api/chat/message` → Send message to LLM
- `GET /api/history` → Get prediction history (JSON)

### Data Model
Session stores prediction history:
```json
{
  "career": [
    {"inputs": {...}, "prediction": "Software Engineer", "timestamp": "..."}
  ],
  "performance": [...],
  "stress": [...]
}
```

### LLM System Prompt
Built dynamically from user's prediction history, formatted as a summary. Includes career prediction, latest performance prediction, stress level, and asks to provide personalized advice.