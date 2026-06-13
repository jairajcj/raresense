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

<!-- extra: docs: add project overview to README at 2026-04-01 12:51:00 -->

<!-- extra: chore: add .gitignore entries at 2026-04-02 10:17:00 -->

<!-- extra: refactor: rename db config vars at 2026-04-02 11:34:00 -->

<!-- extra: test: verify MongoDB connection at 2026-04-02 12:51:00 -->

<!-- extra: fix: env variable loading order at 2026-04-04 10:17:00 -->

<!-- extra: chore: update .env.example at 2026-04-04 11:34:00 -->

<!-- extra: style: format config.py with black at 2026-04-04 12:51:00 -->

<!-- extra: fix: JWT secret key validation at 2026-04-07 10:17:00 -->

<!-- extra: refactor: move token utils to helpers at 2026-04-07 11:34:00 -->

<!-- extra: test: add auth unit test stub at 2026-04-07 12:51:00 -->

<!-- extra: fix: bcrypt import path at 2026-04-08 10:17:00 -->

<!-- extra: chore: pin bcrypt version in requirements at 2026-04-08 11:34:00 -->

<!-- extra: style: clean up auth route comments at 2026-04-08 12:51:00 -->

<!-- extra: fix: patient list returns 500 on empty DB at 2026-04-10 10:17:00 -->

<!-- extra: refactor: extract pagination helper at 2026-04-10 11:34:00 -->

<!-- extra: style: format patients.py at 2026-04-10 12:51:00 -->

<!-- extra: fix: missing field error message at 2026-04-11 10:17:00 -->

<!-- extra: refactor: validation logic into utils at 2026-04-11 11:34:00 -->

<!-- extra: style: consistent error response format at 2026-04-11 12:51:00 -->

<!-- extra: fix: disease route import error at 2026-04-14 10:17:00 -->

<!-- extra: chore: add ORPHA codes enum at 2026-04-14 11:34:00 -->

<!-- extra: refactor: disease model field names at 2026-04-14 12:51:00 -->

<!-- extra: fix: search index not created on startup at 2026-04-15 10:17:00 -->

<!-- extra: refactor: search query builder at 2026-04-15 11:34:00 -->

<!-- extra: style: clean search.py formatting at 2026-04-15 12:51:00 -->

<!-- extra: chore: vite config tweaks at 2026-04-16 10:17:00 -->

<!-- extra: fix: hot reload path alias at 2026-04-16 11:34:00 -->

<!-- extra: style: prettier config added at 2026-04-16 12:51:00 -->

<!-- extra: style: CSS variable naming convention at 2026-04-17 10:17:00 -->

<!-- extra: fix: font import order at 2026-04-17 11:34:00 -->

<!-- extra: refactor: move base styles to _reset.css at 2026-04-17 12:51:00 -->

<!-- extra: fix: login form validation state at 2026-04-18 10:17:00 -->

<!-- extra: refactor: LoginForm extracted to component at 2026-04-18 11:34:00 -->

<!-- extra: style: Login page spacing fixes at 2026-04-18 12:51:00 -->

<!-- extra: fix: sidebar active link highlight at 2026-04-21 10:17:00 -->

<!-- extra: refactor: nav items to config array at 2026-04-21 11:34:00 -->

<!-- extra: style: sidebar hover animation at 2026-04-21 12:51:00 -->

<!-- extra: fix: patient table column widths at 2026-04-22 10:17:00 -->

<!-- extra: refactor: table to DataTable component at 2026-04-22 11:34:00 -->

<!-- extra: style: zebra striping on table rows at 2026-04-22 12:51:00 -->

<!-- extra: fix: matching algo divide-by-zero edge case at 2026-04-23 10:17:00 -->

<!-- extra: refactor: scoring function signature at 2026-04-23 11:34:00 -->

<!-- extra: test: matching unit test cases at 2026-04-23 12:51:00 -->

<!-- extra: fix: analytics aggregation pipeline null check at 2026-04-24 10:17:00 -->

<!-- extra: refactor: pipeline stages to constants at 2026-04-24 11:34:00 -->

<!-- extra: style: analytics.py formatting at 2026-04-24 12:51:00 -->

<!-- extra: fix: search filter UI state reset at 2026-04-25 10:17:00 -->

<!-- extra: refactor: filter state to useReducer at 2026-04-25 11:34:00 -->

<!-- extra: style: filter panel spacing at 2026-04-25 12:51:00 -->

<!-- extra: fix: disease card missing alt text at 2026-04-28 10:17:00 -->

<!-- extra: refactor: DiseaseCard props interface at 2026-04-28 11:34:00 -->

<!-- extra: style: card hover elevation effect at 2026-04-28 12:51:00 -->

<!-- extra: fix: redirect loop on token refresh at 2026-04-29 10:17:00 -->

<!-- extra: refactor: axios interceptor cleanup at 2026-04-29 11:34:00 -->

<!-- extra: style: loading spinner alignment at 2026-04-29 12:51:00 -->

<!-- extra: fix: auth util export names at 2026-04-30 10:17:00 -->

<!-- extra: refactor: consolidate token storage at 2026-04-30 11:34:00 -->

<!-- extra: style: eslint warnings resolved at 2026-04-30 12:51:00 -->

<!-- extra: fix: seed script duplicate key error at 2026-05-02 11:13:00 -->

<!-- extra: refactor: seed runner as CLI at 2026-05-02 12:26:00 -->

<!-- extra: style: seed_data.py formatting at 2026-05-02 13:39:00 -->

<!-- extra: fix: PatientDetail 404 on bad ID at 2026-05-05 11:13:00 -->

<!-- extra: refactor: patient header component at 2026-05-05 12:26:00 -->

<!-- extra: style: detail page layout spacing at 2026-05-05 13:39:00 -->

<!-- extra: fix: notes sort order bug at 2026-05-06 11:13:00 -->

<!-- extra: refactor: NoteItem component at 2026-05-06 12:26:00 -->

<!-- extra: style: notes timestamp formatting at 2026-05-06 13:39:00 -->

<!-- extra: fix: PUT endpoint missing auth check at 2026-05-07 11:13:00 -->

<!-- extra: refactor: route auth decorator at 2026-05-07 12:26:00 -->

<!-- extra: test: update/delete endpoint tests at 2026-05-07 13:39:00 -->

<!-- extra: fix: prompt template escaping at 2026-05-08 11:13:00 -->

<!-- extra: refactor: prompt builder function at 2026-05-08 12:26:00 -->

<!-- extra: style: AI prompt documentation at 2026-05-08 13:39:00 -->

<!-- extra: fix: Gemini API key validation at 2026-05-09 11:13:00 -->

<!-- extra: refactor: AI service error handling at 2026-05-09 12:26:00 -->

<!-- extra: style: ai_service.py formatting at 2026-05-09 13:39:00 -->

<!-- extra: fix: chat scroll to bottom on new msg at 2026-05-12 11:13:00 -->

<!-- extra: refactor: MessageBubble component at 2026-05-12 12:26:00 -->

<!-- extra: style: chat bubble border radius at 2026-05-12 13:39:00 -->

<!-- extra: fix: score normalisation edge case at 2026-05-13 11:13:00 -->

<!-- extra: refactor: score weighting config at 2026-05-13 12:26:00 -->

<!-- extra: test: scoring unit tests at 2026-05-13 13:39:00 -->

<!-- extra: fix: matching tab empty state UI at 2026-05-14 11:13:00 -->

<!-- extra: refactor: MatchCard component at 2026-05-14 12:26:00 -->

<!-- extra: style: confidence bar animation at 2026-05-14 13:39:00 -->

<!-- extra: fix: glass card blur on Firefox at 2026-05-15 11:13:00 -->

<!-- extra: refactor: card variant props at 2026-05-15 12:26:00 -->

<!-- extra: style: animation timing functions at 2026-05-15 13:39:00 -->

<!-- extra: fix: page count off-by-one at 2026-05-16 11:13:00 -->

<!-- extra: refactor: usePagination hook at 2026-05-16 12:26:00 -->

<!-- extra: style: pagination button styles at 2026-05-16 13:39:00 -->

<!-- extra: fix: CORS preflight OPTIONS missing at 2026-05-19 11:13:00 -->

<!-- extra: refactor: CORS config to separate module at 2026-05-19 12:26:00 -->

<!-- extra: style: app.py cleanup at 2026-05-19 13:39:00 -->

<!-- extra: fix: sidebar collapse animation stutter at 2026-05-20 11:13:00 -->

<!-- extra: refactor: useBreakpoint hook at 2026-05-20 12:26:00 -->

<!-- extra: style: mobile nav overlay at 2026-05-20 13:39:00 -->

<!-- extra: chore: update all npm packages at 2026-05-21 11:13:00 -->

<!-- extra: chore: update Python dependencies at 2026-05-21 12:26:00 -->

<!-- extra: fix: lockfile conflicts resolved at 2026-05-21 13:39:00 -->

<!-- extra: fix: gradient banding on dark bg at 2026-05-22 11:13:00 -->

<!-- extra: refactor: CSS custom property scopes at 2026-05-22 12:26:00 -->

<!-- extra: style: consistent border radius tokens at 2026-05-22 13:39:00 -->

<!-- extra: docs: add authentication flow diagram at 2026-05-23 11:13:00 -->

<!-- extra: docs: response schema examples at 2026-05-23 12:26:00 -->

<!-- extra: style: API_DOCS.md formatting at 2026-05-23 13:39:00 -->

<!-- extra: fix: unhandled promise in error handler at 2026-05-26 11:13:00 -->

<!-- extra: refactor: centralised error factory at 2026-05-26 12:26:00 -->

<!-- extra: test: error handler tests at 2026-05-26 13:39:00 -->

<!-- extra: fix: skeleton flicker on fast load at 2026-05-27 11:13:00 -->

<!-- extra: refactor: Skeleton component variants at 2026-05-27 12:26:00 -->

<!-- extra: style: skeleton shimmer animation at 2026-05-27 13:39:00 -->

<!-- extra: fix: timeline event ordering bug at 2026-05-28 11:13:00 -->

<!-- extra: refactor: TimelineEvent component at 2026-05-28 12:26:00 -->

<!-- extra: style: timeline connector line at 2026-05-28 13:39:00 -->

<!-- extra: fix: index not applied on restart at 2026-05-29 11:13:00 -->

<!-- extra: refactor: db init function at 2026-05-29 12:26:00 -->

<!-- extra: chore: add index creation logging at 2026-05-29 13:39:00 -->

<!-- extra: fix: unused variable in auth.py at 2026-05-30 11:13:00 -->

<!-- extra: refactor: response builder helper at 2026-05-30 12:26:00 -->

<!-- extra: style: consistent 200/201 status codes at 2026-05-30 13:39:00 -->

<!-- extra: fix: chart tooltip overflow at 2026-06-02 10:15:00 -->

<!-- extra: refactor: ChartCard component at 2026-06-02 11:30:00 -->

<!-- extra: style: chart color palette at 2026-06-02 12:45:00 -->

<!-- extra: fix: demographics null gender handling at 2026-06-03 10:15:00 -->

<!-- extra: refactor: demographics pipeline at 2026-06-03 11:30:00 -->

<!-- extra: style: pie chart label formatting at 2026-06-03 12:45:00 -->

<!-- extra: fix: code block language detection at 2026-06-04 10:15:00 -->

<!-- extra: refactor: MarkdownRenderer component at 2026-06-04 11:30:00 -->

<!-- extra: style: chat message padding at 2026-06-04 12:45:00 -->

<!-- extra: fix: rate limit header not sent at 2026-06-05 10:15:00 -->

<!-- extra: refactor: rate limiter decorator at 2026-06-05 11:30:00 -->

<!-- extra: test: rate limit endpoint test at 2026-06-05 12:45:00 -->

<!-- extra: fix: toast duplicate on retry at 2026-06-06 10:15:00 -->

<!-- extra: refactor: toast queue manager at 2026-06-06 11:30:00 -->

<!-- extra: style: toast slide-in animation at 2026-06-06 12:45:00 -->

<!-- extra: fix: form dirty state on cancel at 2026-06-09 10:15:00 -->

<!-- extra: refactor: useForm hook at 2026-06-09 11:30:00 -->

<!-- extra: style: form field focus ring at 2026-06-09 12:45:00 -->

<!-- extra: fix: CSV encoding for special chars at 2026-06-10 10:15:00 -->

<!-- extra: refactor: csv_exporter utility at 2026-06-10 11:30:00 -->

<!-- extra: test: CSV export test at 2026-06-10 12:45:00 -->

<!-- extra: fix: download blob memory leak at 2026-06-11 10:15:00 -->

<!-- extra: refactor: useDownload hook at 2026-06-11 11:30:00 -->

<!-- extra: style: export button loading state at 2026-06-11 12:45:00 -->

<!-- extra: docs: add .env.example file at 2026-06-12 10:15:00 -->

<!-- extra: docs: contributor guide at 2026-06-12 11:30:00 -->

<!-- extra: style: README badge links at 2026-06-12 12:45:00 -->

<!-- extra: test: add patient model test at 2026-06-13 10:15:00 -->

<!-- extra: test: search route test at 2026-06-13 11:30:00 -->

<!-- extra: fix: test DB teardown issue at 2026-06-13 12:45:00 -->
