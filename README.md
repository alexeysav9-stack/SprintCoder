# ⌨️ SprintCoder

<div align="center">

**Type Code. Ship Faster.**  
*A typing speed trainer and muscle memory builder built specifically for software engineers.*

[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

---

## 📌 Overview

**SprintCoder** trains your coding speed and muscle memory using **real, functional code snippets** instead of random generic words or *Lorem Ipsum*. Practice typical syntax patterns, brackets, semicolons, indentations, and language idioms across **8 language options** and **3 difficulty tiers**.

In addition to built-in code snippets, SprintCoder allows you to connect your **public GitHub repositories** to automatically parse, classify, and practice typing with **your own codebase**!

---

## 📸 Screenshots & Showcase

<!-- ================================================================= -->
<!-- SCREENSHOT PLACEHOLDERS: Replace image URLs with your screenshots -->
<!-- ================================================================= -->

### 1. Home & Language Picker
Select your target programming language, difficulty tier, and optionally toggle the "From my repos" switch.

> <!-- INSERT SCREENSHOT: Main dashboard with language grid and difficulty buttons -->
> ![Home Page Screenshot](https://via.placeholder.com/900x500/13151f/9e92ff?text=Screenshot:+Home+Page+&+Language+Selector)

---

### 2. Live Typing Exercise & HUD
Real-time character-by-character validation, live WPM, Accuracy, CPM, and elapsed timer. Tab indentation and anti-paste protection are built-in.

> <!-- INSERT SCREENSHOT: Exercise page with syntax display and live stats HUD -->
> ![Exercise Page Screenshot](https://via.placeholder.com/900x500/13151f/9e92ff?text=Screenshot:+Live+Typing+Exercise)

---

### 3. Session Results & Mistyped Character Breakdown
After finishing, review your final WPM, accuracy percentage, time spent, and a frequency breakdown of mistyped characters to spot recurring errors.

> <!-- INSERT SCREENSHOT: Results page with score badges and top error characters -->
> ![Results Page Screenshot](https://via.placeholder.com/900x500/13151f/9e92ff?text=Screenshot:+Session+Results+&+Error+Breakdown)

---

### 4. Profile & Interactive Progress Charts
Track your typing speed progression over time with rolling average charts powered by Chart.js, broken down by programming language.

> <!-- INSERT SCREENSHOT: Profile page with WPM progress charts and stats -->
> ![Profile Progress Charts Screenshot](https://via.placeholder.com/900x500/13151f/9e92ff?text=Screenshot:+Profile+&+WPM+Progress+Charts)

---

### 5. Personal GitHub Repositories (Settings)
Connect public GitHub repositories (e.g. `username/repository`). SprintCoder fetches real files, parses complete logical blocks, and categorizes snippets by difficulty.

> <!-- INSERT SCREENSHOT: Settings page with GitHub repo list and import status -->
> ![Settings Page Screenshot](https://via.placeholder.com/900x500/13151f/9e92ff?text=Screenshot:+GitHub+Repositories+Settings)

---

### 6. Practice History
A comprehensive table recording all previous practice sessions with timestamps, language, difficulty, WPM, and accuracy.

> <!-- INSERT SCREENSHOT: History table listing past practice attempts -->
> ![History Page Screenshot](https://via.placeholder.com/900x500/13151f/9e92ff?text=Screenshot:+Practice+History+Table)

---

## 🚀 Key Features

- **⚡ Real Code Snippets**: Real algorithms, utility functions, classes, and styles — no artificial filler text.
- **🎨 8 Supported Language Modes**:
  - 🐍 **Python** (functions, list comprehensions, decorators, dataclasses)
  - 🟨 **JavaScript / TypeScript** (async/await, closures, promises, types)
  - ☕ **Java** (OOP structures, streams, builder pattern)
  - ⚙️ **C++** (algorithms, pointers, templates, vectors)
  - 🐹 **Go** (goroutines, channels, structs, error handling)
  - 🗄️ **SQL** (joins, aggregations, window functions, schema design)
  - 🎨 **CSS** (flexbox, grid, animations, responsive design)
  - 🎲 **Random** (fairly chooses a random language on every attempt)
- **🎯 3 Difficulty Tiers**:
  - **Easy**: 4–10 lines (compact functions, single CSS rules, short queries)
  - **Medium**: 11–20 lines (standard algorithms, component logic)
  - **Hard**: 21–35 lines (complex pipelines, multi-block structures)
- **🐙 Practice with Your Own Repositories**:
  - Add public GitHub repositories (`owner/repo`) in Settings.
  - Automatically fetches source files via GitHub REST API.
  - Smart language parser: extracts well-formed blocks (functions, classes, CSS rules) without breaking syntax.
  - Balances snippet counts across all languages and difficulty levels.
- **⏱️ High-Performance Typing Engine**:
  - Ultra-low latency character-by-character validation (pure vanilla JS).
  - Starts timing automatically on the first keypress.
  - Supports `Tab` key (inserts 4 spaces IDE-style).
  - Anti-cheat sanity checks (rejects automated paste exploits and unrealistic timings).
- **📊 Analytics & Insights**:
  - Live HUD during typing (WPM, Accuracy %, Elapsed Time, Errors).
  - Top mistyped characters breakdown (`[·]` spaces, `[↵]` newlines, braces, symbols).
  - Per-language interactive line charts with rolling averages (Chart.js).
- **🌓 Dark / Light Theme**:
  - Built-in theme switcher with persistent local storage state.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, [Django 5](https://www.djangoproject.com/), [psycopg3](https://www.psycopg.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) (SQLite supported for tests)
- **Frontend**: Vanilla JavaScript (ES6+), HTML5, Custom CSS with CSS variables
- **Visuals & Charts**: [Chart.js](https://www.chartjs.org/), [Devicon](https://devicon.dev/), [Highlight.js](https://highlightjs.org/)
- **GitHub API**: [Requests](https://requests.readthedocs.io/) for automated repository code extraction

---

## 📂 Project Structure

```text
SprintCoder/
├── accounts/               # User authentication (registration, login, logout)
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── sprintcoder/            # Django project settings & root routing
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/
│   │   └── main.css        # Core design system, themes, and layouts
│   └── js/
│       └── trainer.js      # Real-time typing engine & HUD controller
├── templates/
│   ├── base.html           # Base layout, navbar, messages, dark mode
│   ├── accounts/           # Auth templates (login, register)
│   └── trainer/            # Trainer templates (index, exercise, result, history, profile, settings)
├── trainer/                # Main application
│   ├── management/
│   │   └── commands/
│   │       ├── seed_snippets.py         # Populates standard code snippets
│   │       └── fetch_github_snippets.py # Fetches curated snippets from popular OSS repos
│   ├── migrations/
│   ├── models.py           # Language, Snippet, Attempt, UserProfile
│   ├── templatetags/       # Custom templatetags (devicon, jsonify)
│   ├── tests.py            # Unit & integration tests
│   ├── urls.py
│   └── views.py            # Typing views, random routing, and GitHub repo parser
├── manage.py
├── requirements.txt
└── .env.example
```

---

## ⚡ Getting Started

### 1. Prerequisites

- **Python 3.10+** (tested on Python 3.12 and 3.14)
- **PostgreSQL 14+** (running locally or in Docker)
- **Git**

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/SprintCoder.git
cd SprintCoder
```

### 3. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Open `.env` and fill in your database credentials and optional GitHub token:

```env
SECRET_KEY=your-secure-secret-key-here
DEBUG=True

DB_NAME=sprintcoder
DB_USER=sprintcoder
DB_PASSWORD=sprintcoder
DB_HOST=localhost
DB_PORT=5432

# Optional: GitHub token to increase API rate limits when importing repos
GITHUB_TOKEN=ghp_yourPersonalAccessTokenHere
```

> **Tip:** A GitHub Personal Access Token (classic or fine-grained with `Public Repositories (read-only)` access) is recommended so you won't hit GitHub's unauthenticated 60 requests/hour rate limit.

### 6. Set Up PostgreSQL Database

Ensure PostgreSQL is running and create the database:

```bash
# Using PostgreSQL CLI (psql):
psql -U postgres -c "CREATE USER sprintcoder WITH PASSWORD 'sprintcoder';"
psql -U postgres -c "CREATE DATABASE sprintcoder OWNER sprintcoder;"
```

### 7. Run Migrations

```bash
python manage.py migrate
```

### 8. Seed Default Code Snippets

Populate the database with hundreds of curated code snippets across all languages and difficulty levels:

```bash
python manage.py seed_snippets
```

*(Optional)* You can also pull additional real snippets from popular open-source repositories:

```bash
python manage.py fetch_github_snippets --per-lang 20
```

### 9. Start the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to **`http://127.0.0.1:8000/`**.

---

## 🧪 Running Tests

The test suite covers snippet parsing, CSS block extraction, random language routing, and personal repository fallbacks. An in-memory SQLite database is automatically configured during test execution:

```bash
python manage.py test
```

---

## 🎯 How "From My Repos" Works

1. Sign up and log in to your SprintCoder account.
2. Go to **Settings** (`/settings/`).
3. Enter your public GitHub repositories in `owner/repo` format (one per line, e.g. `torvalds/linux` or `yourusername/my-project`).
4. Click **Save & Import**. SprintCoder will:
   - Recursively discover files in the repository.
   - Filter out vendor, build artifacts, test suites, and minified code.
   - Cleanly extract complete functions, classes, and CSS rule blocks.
   - Categorize snippets into **Easy**, **Medium**, and **Hard** tiers.
   - Store them tied to your user account.
5. On the home page, flip the **"From my repos"** switch on and click **Start Practice**!

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
