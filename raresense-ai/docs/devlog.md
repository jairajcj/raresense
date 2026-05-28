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

