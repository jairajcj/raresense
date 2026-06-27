# RareSense AI

RareSense AI is a comprehensive platform designed to facilitate the management, analysis, and discovery of insights related to rare diseases. It provides advanced patient matching, NLP-driven analytics, and an intuitive dashboard for healthcare professionals.

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB (via Motor for async support)
- **Authentication**: JWT & Passlib (bcrypt)
- **Data Validation**: Pydantic

### Frontend
- **Framework**: React.js (via Vite)
- **Routing**: React Router
- **Data Visualization**: Recharts
- **Icons**: Lucide React

## Project Structure

```text
raresense-ai/
├── backend/
│   ├── app/
│   │   ├── models/       # Database schemas and Pydantic models
│   │   ├── routes/       # API endpoints (auth, patients, diseases, matching, etc.)
│   │   ├── services/     # Core business logic (NLP engine, matcher)
│   │   └── seed/         # Initial database seeding scripts
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Application views (Dashboard, Patients, etc.)
│   │   └── utils/        # Helper functions and API clients
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB instance running

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd raresense-ai/backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the development server:
   ```bash
   python run.py
   ```
   *The backend will be available at http://localhost:8000*

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd raresense-ai/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   *The frontend will be available at http://localhost:5173*

## Features

- **AI-Powered Matching**: Utilizes NLP to match patient profiles with known rare diseases and clinical trials.
- **Analytics Dashboard**: Visual representations of patient distributions, disease prevalence, and matching confidence scores.
- **Secure Authentication**: JWT-based user authentication and role management.
- **Patient Management**: Detailed patient dossiers, medical histories, and progress tracking.

## Team Contributions

This project was developed collaboratively by three team members:

### Member 1: Frontend & UI/UX Development
- Developed the React frontend using Vite and React Router.
- Designed the user interface and responsive layouts.
- Implemented data visualizations using Recharts.
- Integrated frontend components with backend REST APIs.

### Member 2: Backend API & Database Architecture
- Built the backend infrastructure using FastAPI.
- Designed database schemas and Pydantic models.
- Implemented user authentication (JWT) and secure routing.
- Developed core CRUD endpoints for patients and diseases, and managed MongoDB integrations.

### Member 3: AI/NLP Engine & Data Analytics
- Developed the core NLP matching engine (`nlp_engine.py`, `matcher.py`).
- Implemented algorithms to match patients with rare diseases and clinical trials.
- Created data seeding scripts for initial database population.
- Built analytics endpoints to provide insights and confidence scores.
