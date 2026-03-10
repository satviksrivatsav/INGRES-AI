<div align="center">

# 💧 INGRES-AI
### *Intelligent Groundwater Resource Management System*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5--Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> **An AI-powered platform for groundwater monitoring, predictive analysis, and sustainable water resource management — built as a Final Year Project with a focus on Andhra Pradesh, India.**

[🚀 Features](#-features) · [🛠️ Tech Stack](#️-tech-stack) · [⚙️ Installation](#️-installation) · [🗺️ Project Structure](#️-project-structure) · [📡 API & Routes](#-api--routes) · [🤝 Contributing](#-contributing)

---

</div>

## 📖 Overview

**INGRES-AI** is a full-stack web application that empowers citizens, government officials, and researchers with real-time groundwater intelligence. The system combines **machine learning models**, **Google Gemini AI**, and **interactive geospatial visualizations** to tackle India's growing water crisis through data-driven decision-making.

The platform focuses on **Andhra Pradesh** as a proof-of-concept but is architected to scale nationally.

### 🎯 Problem Statement

India faces a rapidly worsening groundwater crisis — over 60% of its irrigation and 85% of rural drinking water depends on groundwater. Without accessible, intelligent tools, communities and planners lack the means to monitor extraction, forecast needs, and take preventive action.

### ✅ Solution

INGRES-AI provides a unified platform with:
- **Real-time status monitoring** across districts with alert flags
- **ML-driven predictions** for water needs and quality safety
- **AI chatbot** grounded in live database data (no hallucinations)
- **Interactive maps** and trend reports for evidence-based policy

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 User Authentication & Role Management
- **Three-tier role system** — Public (Citizens/Farmers), Researchers, and Government Officials
- **Email OTP verification** with 10-minute expiry
- Role-based routing to dedicated dashboards
- Researcher domains whitelisted; Officials require admin approval

</td>
<td width="50%">

### 🌊 Groundwater Intelligence Hub
- District-level groundwater **status categories**:
  - 🟢 **Safe** — Extraction < 70%
  - 🟡 **Semi-Critical** — 70–90%
  - 🟠 **Critical** — 90–100%
  - 🔴 **Over-Exploited** — > 100%
- Automatic alert flagging for critical zones
- Annual recharge value tracking (MCM)

</td>
</tr>
<tr>
<td width="50%">

### 🤖 Water Buddy — AI Chatbot (Gemini 2.5-Flash)
- **Retrieval-Augmented Generation (RAG):** Detects district names in user queries and injects live database values, preventing AI from fabricating water statistics
- Markdown-cleaned responses for professional UI
- Persistent conversation history
- Dual modes: Public (citizens) & Official (policy advisors)

</td>
<td width="50%">

### 📊 ML-Powered Predictive Tools
- **Water Resource Planner** — Predict water requirements for crops (Paddy, Wheat, Maize, Millets, Vegetables) across seasons using a 29 MB scikit-learn model trained on 50,000 rows
- **Water Safety Checker** — Assess safety of water sources (Borewell, Well, Tap, Tanker) using a 14 MB model trained on 50,000 rows

</td>
</tr>
<tr>
<td width="50%">

### 🗺️ Interactive Groundwater Map
- **Leaflet.js** visualization of 20+ Andhra Pradesh districts
- Color-coded markers by groundwater status
- Year selection for historical comparison
- Click-to-view district detail cards

</td>
<td width="50%">

### 📋 Government Schemes Directory
- Searchable database of national & state water schemes
- Pre-seeded entries: **Jal Jeevan Mission**, **Atal Bhujal Yojana**, **PMKSY**, **YSR Jala Kala**, **Mission Kakatiya**, and more
- Filter by location — national schemes + user's state schemes

</td>
</tr>
<tr>
<td width="50%">

### 📈 Trend Reports & Analytics
- Multi-year extraction vs. recharge trend charts
- District-specific downloadable **CSV exports**
- Data snapshots for audit trails
- Regional comparative analysis

</td>
<td width="50%">

### 💡 Conservation Advisor
- Personalized recommendations based on local groundwater status
- Evidence-based techniques:
  - 💧 Drip Irrigation (40–70% savings)
  - 🌧️ Rainwater Harvesting (100k+ litres/year)
  - 🌾 Mulching (30% moisture retention)

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Django 5.2 (Python) |
| **AI / Chatbot** | Google Gemini 2.5-Flash via `google-genai` SDK |
| **Machine Learning** | scikit-learn 1.6, NumPy, SciPy, Joblib |
| **Database (Dev)** | SQLite3 |
| **Database (Prod)** | PostgreSQL (AWS RDS) |
| **Frontend** | Django Templates, Bootstrap 5, Crispy Forms |
| **Maps** | Leaflet.js + OpenStreetMap Nominatim API |
| **Auth & Security** | Django Auth, bcrypt, Email OTP (SMTP) |
| **Reports** | ReportLab (PDF), Python csv module |
| **Deployment** | AWS Elastic Beanstalk (`.ebextensions` config) |
| **Environment** | python-dotenv |

---

## 🗺️ Project Structure

```
INGRES-AI/
│
├── core/                        # Django project configuration
│   ├── settings.py              # App settings, DB, i18n (English, Hindi, Telugu)
│   ├── urls.py                  # Root URL router
│   └── views.py                 # Landing page
│
├── accounts/                    # Authentication & role management
│   ├── models.py                # User, UserProfile, EmailOTP, Notification models
│   └── views.py                 # Login, signup, OTP verification, logout
│
├── portal/                      # Core dashboard & intelligence hub
│   ├── models.py                # GroundwaterData, WaterPlan, SafetyCheck models
│   ├── views.py                 # Dashboards, ML predictions, location updates
│   └── ml_models/               # Trained scikit-learn models (~43 MB)
│       ├── resource_planner_model.pkl
│       └── safety_checker_model.pkl
│
├── chatbot/                     # AI-powered Water Buddy
│   ├── models.py                # ChatConversation model
│   └── views.py                 # Gemini AI integration + RAG logic
│
├── maps/                        # Interactive geospatial visualization
│   └── views.py                 # Leaflet map rendering
│
├── schemes/                     # Government water schemes directory
│   ├── models.py                # WaterScheme model
│   └── views.py                 # Searchable scheme directory
│
├── reports/                     # Analytics & reporting
│   └── views.py                 # Trend reports, CSV export
│
├── tools/                       # Technical reference & glossary
│
├── templates/                   # Django HTML templates (41 files)
│   ├── landing.html
│   ├── accounts/                # Login, signup, OTP pages
│   ├── dashboards/              # Public, official, researcher dashboards
│   ├── chatbot/
│   ├── maps/
│   ├── schemes/
│   └── reports/
│
├── static/                      # CSS, JavaScript, images
├── docs/                        # Documentation
│
├── seed_groundwater.py          # Seed 13 Andhra Pradesh districts
├── seed_schemes.py              # Seed 6 government water schemes
├── requirements.txt             # 61 Python dependencies
├── manage.py                    # Django management utility
│
├── resource_planner_dataset.csv # 50,000-row training dataset
├── safety_checker_dataset.csv   # 50,000-row training dataset
│
└── WATER.ipynb                  # Jupyter notebook (ML experimentation)
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.11+
- pip
- Git
- A Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))
- Gmail account for SMTP (or any SMTP provider)

### 1. Clone the repository

```bash
git clone https://github.com/satviksrivatsav/INGRES-AI.git
cd INGRES-AI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Google Gemini AI
AI_API_KEY=your-gemini-api-key-here

# Email (SMTP)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# PostgreSQL (production only — leave unset for SQLite in development)
# RDS_HOSTNAME=your-rds-endpoint
# RDS_PORT=5432
# RDS_DB_NAME=ingres
# RDS_USERNAME=postgres
# RDS_PASSWORD=your-db-password
```

> **Tip:** For Gmail SMTP, generate an [App Password](https://support.google.com/accounts/answer/185833) instead of using your account password.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Seed the database

```bash
# Load 13 Andhra Pradesh districts with groundwater data
python seed_groundwater.py

# Load 6 government water schemes
python seed_schemes.py
```

### 7. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000/**

---

## 📡 API & Routes

| URL Pattern | View | Description |
|---|---|---|
| `/` | `landing` | Public landing page |
| `/admin/` | Django Admin | Admin panel |
| `/accounts/login/` | `login_view` | User login |
| `/accounts/signup/` | `signup_view` | Registration |
| `/accounts/verify-otp/` | `verify_otp_view` | Email OTP verification |
| `/accounts/logout/` | `logout_view` | Logout |
| `/portal/public/` | `public_dashboard` | Citizen/farmer dashboard |
| `/portal/official/` | `official_dashboard` | Government official dashboard |
| `/portal/researcher/` | `researcher_dashboard` | Academic researcher dashboard |
| `/portal/planner/` | `water_planner` | Water Resource Planner (ML) |
| `/portal/safety/` | `safety_checker` | Water Safety Checker (ML) |
| `/portal/advisor/` | `conservation_advisor` | Conservation recommendations |
| `/portal/profile/` | `profile` | User profile settings |
| `/chatbot/` | `chatbot_view` | Water Buddy AI chatbot |
| `/maps/` | `interactive_map` | Leaflet groundwater map |
| `/schemes/` | `scheme_directory` | Government schemes directory |
| `/reports/` | `trend_report` | Multi-year analytics & CSV export |
| `/tools/reference/` | `technical_reference` | Technical glossary |

---

## 🔑 Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ Yes | Django secret key |
| `DEBUG` | ✅ Yes | `True` for development, `False` for production |
| `AI_API_KEY` | ✅ Yes | Google Gemini API key |
| `EMAIL_HOST_USER` | ✅ Yes | Gmail address for sending OTP emails |
| `EMAIL_HOST_PASSWORD` | ✅ Yes | Gmail App Password |
| `RDS_HOSTNAME` | 🔵 Production | PostgreSQL host (triggers DB switch from SQLite) |
| `RDS_PORT` | 🔵 Production | PostgreSQL port (default: `5432`) |
| `RDS_DB_NAME` | 🔵 Production | PostgreSQL database name |
| `RDS_USERNAME` | 🔵 Production | PostgreSQL username |
| `RDS_PASSWORD` | 🔵 Production | PostgreSQL password |

---

## 👥 User Roles

| Role | Access | Sign-up Requirements |
|---|---|---|
| **Public** (Citizen/Farmer) | Public dashboard, chatbot, planner, safety checker, maps, schemes, advisor | Open registration |
| **Researcher** | All public features + researcher dashboard, trend reports, CSV export | Email from a whitelisted academic domain |
| **Official** | All features + official system overview, district-wide analytics | Admin approval after signup |

---

## 🚀 Deployment (AWS Elastic Beanstalk)

The project includes `.ebextensions/` configuration for AWS Elastic Beanstalk deployment.

1. Set all production environment variables in the Elastic Beanstalk console (especially `RDS_*` variables to switch the database to PostgreSQL)
2. Set `DEBUG=False` and configure `ALLOWED_HOSTS` with your domain
3. Run `python manage.py collectstatic` before deploying
4. Use `python manage.py migrate` on the production database after deployment

---

## 🧠 ML Models

Both models are pre-trained and stored as `.pkl` files in `portal/ml_models/`.

| Model | Size | Algorithm | Training Data | Task |
|---|---|---|---|---|
| `resource_planner_model.pkl` | 29 MB | Gradient Boosting / Random Forest | 50,000 rows | Water need & risk prediction |
| `safety_checker_model.pkl` | 14 MB | Gradient Boosting / Random Forest | 50,000 rows | Water safety classification |

Encoders and target label files are stored alongside each model. See `WATER.ipynb` for the full training pipeline.

---

## 🌐 Internationalization

INGRES-AI supports **three languages**:

- 🇬🇧 English
- 🇮🇳 Hindi (`hi`)
- 🇮🇳 Telugu (`te`)

Language files are stored in `locale/` and configured via Django's i18n framework.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m "feat: add your feature"`
4. **Push** to your fork: `git push origin feature/your-feature-name`
5. **Open** a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Google Gemini AI](https://ai.google.dev/) for the conversational intelligence layer
- [scikit-learn](https://scikit-learn.org/) for the ML prediction engine
- [Leaflet.js](https://leafletjs.com/) & [OpenStreetMap](https://www.openstreetmap.org/) for interactive mapping
- [Django](https://www.djangoproject.com/) for the robust web framework
- Central Ground Water Board (CGWB) for domain knowledge

---

<div align="center">

**Built with ❤️ for sustainable water resource management in India**

*INGRES-AI — Final Year Project*

</div>