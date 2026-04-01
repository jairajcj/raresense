# Dev Log
## 2026-04-01
- Initialized Flask app structure
- Set up project scaffold and folder hierarchy


## 2026-04-02
- Drafted patient model schema with fields: id, name, dob, symptoms, diagnosis


## 2026-04-04
- Configured MongoDB connection via PyMongo
- Added .env template for DB URI


## 2026-04-07
- Implemented JWT-based auth
- Added login and register endpoints


## 2026-04-08
- Integrated bcrypt for password hashing
- Secured register route


## 2026-04-10
- Scaffolded CRUD routes for patients
- GET /patients, POST /patients, GET /patients/:id


## 2026-04-11
- Added request validation for patient creation
- Error handling for missing fields


## 2026-04-14
- Created disease model with ORPHA codes
- Added diseases listing endpoint


## 2026-04-15
- Implemented search by symptoms
- Used MongoDB text search index


## 2026-04-16
- Initialized Vite + React frontend
- Set up folder structure: pages, components, utils


## 2026-04-17
- Defined color palette, typography, and spacing tokens in index.css


## 2026-04-18
- Built Login page with email/password form
- Added form validation


## 2026-04-21
- Created Dashboard page layout
- Added sidebar navigation component


## 2026-04-22
- Built Patients page with sortable table
- Integrated API call for patient listing


## 2026-04-23
- Started matching algorithm for symptom-to-disease correlation


## 2026-04-24
- Added analytics endpoint returning patient stats
- Aggregation pipeline for disease frequency


## 2026-04-25
- Built Search page with symptom filter UI
- Connected to backend search endpoint


## 2026-04-28
- Built Diseases listing page with card grid
- Added disease detail modal


## 2026-04-29
- Fixed token expiry issue in auth interceptor
- Redirect to login on 401 responses


## 2026-04-30
- Moved auth helpers to utils/auth.js
- Cleaned up App.jsx imports


## 2026-05-02
- Created seed scripts for rare disease data
- Populated ORPHA disease list from CSV


## 2026-05-05
- Started PatientDetail page
- Added patient info header and tabs


## 2026-05-06
- Added clinical notes tab in PatientDetail
- Render notes with timestamps


## 2026-05-07
- Implemented PUT /patients/:id and DELETE /patients/:id
- Added authorization check


## 2026-05-08
- Designed system prompt for AI clinical assistant
- Defined input/output schema for LLM calls


## 2026-05-09
- Integrated Gemini API for AI assistant feature
- Added /ai/query backend route


## 2026-05-12
- Built AIAssistant chat UI
- Added message history and streaming response display


## 2026-05-13
- Implemented weighted symptom scoring for disease matching
- Normalized scores to 0-100%


## 2026-05-14
- Added Matching tab to PatientDetail page
- Rendered top matching diseases with confidence scores


## 2026-05-15
- Added glassmorphism card variants
- Implemented hover lift animations


## 2026-05-16
- Fixed pagination bug in search results
- Added total count header from API


## 2026-05-19
- Configured Flask-CORS for frontend dev server
- Restricted to allowed origins


## 2026-05-20
- Made sidebar collapsible on mobile
- Responsive grid breakpoints for patient cards


## 2026-05-21
- Updated requirements.txt with pinned versions
- Ran npm install and committed lockfile


## 2026-05-22
- Refined dark mode color palette
- Added subtle gradients to sidebar and cards


## 2026-05-23
- Added API_DOCS.md with endpoint descriptions
- Documented request/response schemas


## 2026-05-26
- Standardized error response format
- Added 404 and 500 error handlers


## 2026-05-27
- Added skeleton loaders for patient cards and tables
- Improved perceived performance


## 2026-05-28
- Added timeline component for patient medical history
- Sorted events chronologically


## 2026-05-29
- Added compound indexes on patients collection
- Reduced query latency for search


## 2026-05-30
- Cleaned up unused imports in auth.py
- Standardised response messages


## 2026-06-02
- Added bar chart for disease frequency analytics
- Integrated Chart.js components


## 2026-06-03
- Added age and gender breakdown charts
- Backend aggregation pipeline for demographics


## 2026-06-04
- Fixed markdown rendering in AI chat responses
- Added syntax highlighting for code blocks


## 2026-06-05
- Implemented rate limiting on /ai/query
- 20 requests per minute per user


## 2026-06-06
- Built toast notification component
- Integrated success/error toasts across all pages


## 2026-06-09
- Extracted PatientForm into shared component
- Used in both Create and Edit flows


## 2026-06-10
- Added GET /patients/export endpoint
- Returns CSV with patient fields


## 2026-06-11
- Added Export button to Patients page
- Triggers CSV download via blob URL


## 2026-06-12
- Updated README with full setup steps
- Added .env.example file


## 2026-06-13
- Wrote pytest test cases for auth endpoints
- Added test for patient CRUD


## 2026-06-16
- Added ObjectId validation in all route params
- Return 400 on invalid IDs


## 2026-06-17
- Added debounced search input in Patients page
- 300ms debounce prevents excess API calls


## 2026-06-18
- Added GET /diseases/:id endpoint
- Returns full disease profile with symptoms list


## 2026-06-19
- Built Disease detail page
- Shows prevalence, symptoms, and linked patients


## 2026-06-20
- Applied React.lazy for route-level code splitting
- Reduced initial bundle size


## 2026-06-23
- Added fade-in transition on page navigation
- CSS keyframe animations for route changes


## 2026-06-24
- Added GET /health endpoint
- Returns server status and DB connectivity


## 2026-06-25
- Ran ESLint and fixed all warnings
- Removed console.log statements
- PEP8 formatting on Python files


## 2026-06-26
- Generated Review 2 PPT from script
- Added updated screenshots and demo flow


<!-- extra: fix: typo in init config at 2026-04-01 10:17:00 -->

<!-- extra: style: add .editorconfig at 2026-04-01 11:34:00 -->
