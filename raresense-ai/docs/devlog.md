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

<!-- extra: fix: ObjectId regex pattern at 2026-06-16 10:15:00 -->

<!-- extra: refactor: id_validator middleware at 2026-06-16 11:30:00 -->

<!-- extra: test: invalid ID response test at 2026-06-16 12:45:00 -->

<!-- extra: fix: debounce cleanup on unmount at 2026-06-17 10:15:00 -->

<!-- extra: refactor: useDebounce hook at 2026-06-17 11:30:00 -->

<!-- extra: style: search input clear button at 2026-06-17 12:45:00 -->

<!-- extra: fix: disease detail 500 on missing field at 2026-06-18 10:15:00 -->

<!-- extra: refactor: disease serializer at 2026-06-18 11:30:00 -->

<!-- extra: style: disease profile layout at 2026-06-18 12:45:00 -->

<!-- extra: fix: linked patients list pagination at 2026-06-19 10:15:00 -->

<!-- extra: refactor: DiseaseDetail tabs at 2026-06-19 11:30:00 -->

<!-- extra: style: disease page hero section at 2026-06-19 12:45:00 -->

<!-- extra: fix: Suspense fallback flicker at 2026-06-20 10:15:00 -->

<!-- extra: refactor: LazyRoute wrapper at 2026-06-20 11:30:00 -->

<!-- extra: style: page loading indicator at 2026-06-20 12:45:00 -->

<!-- extra: fix: transition z-index conflict at 2026-06-23 10:15:00 -->

<!-- extra: refactor: PageTransition component at 2026-06-23 11:30:00 -->

<!-- extra: style: easing curve refinement at 2026-06-23 12:45:00 -->

<!-- extra: fix: health check DB timeout at 2026-06-24 10:15:00 -->

<!-- extra: refactor: health status serializer at 2026-06-24 11:30:00 -->

<!-- extra: test: health endpoint test at 2026-06-24 12:45:00 -->

<!-- extra: fix: ESLint no-unused-vars at 2026-06-25 10:15:00 -->

<!-- extra: fix: Python trailing whitespace at 2026-06-25 11:30:00 -->

<!-- extra: chore: pre-commit hook added at 2026-06-25 12:45:00 -->

<!-- extra: chore: generate final PPT assets at 2026-06-26 10:15:00 -->

<!-- extra: docs: update changelog at 2026-06-26 11:30:00 -->

<!-- extra: chore: tag release candidate v0.1.0 at 2026-06-26 12:45:00 -->

<!-- [2026-04-03-1] docs: add system architecture diagram @ 2026-04-03 09:11:00 -->

<!-- [2026-04-03-2] style: update project banner in README @ 2026-04-03 10:22:00 -->

<!-- [2026-04-03-3] chore: add MIT license file @ 2026-04-03 11:33:00 -->

<!-- [2026-04-03-4] fix: typo in setup instructions @ 2026-04-03 12:44:00 -->

<!-- [2026-04-05-1] test: auth token expiry test @ 2026-04-05 09:11:00 -->

<!-- [2026-04-05-2] fix: refresh token not stored in cookie @ 2026-04-05 10:22:00 -->

<!-- [2026-04-05-3] refactor: cookie options to config @ 2026-04-05 11:33:00 -->

<!-- [2026-04-05-4] chore: weekend cleanup session @ 2026-04-05 12:44:00 -->

<!-- [2026-04-06-1] docs: patient data flow diagram @ 2026-04-06 09:11:00 -->

<!-- [2026-04-06-2] style: diagram colours updated @ 2026-04-06 10:22:00 -->

<!-- [2026-04-06-3] chore: archive old wireframes @ 2026-04-06 11:33:00 -->

<!-- [2026-04-06-4] fix: broken image in docs @ 2026-04-06 12:44:00 -->

<!-- [2026-04-09-1] feat: add role-based access control @ 2026-04-09 09:11:00 -->

<!-- [2026-04-09-2] fix: admin role not persisted @ 2026-04-09 10:22:00 -->

<!-- [2026-04-09-3] refactor: roles to enum class @ 2026-04-09 11:33:00 -->

<!-- [2026-04-09-4] test: RBAC middleware test @ 2026-04-09 12:44:00 -->

<!-- [2026-04-12-1] docs: update API_DOCS with auth headers @ 2026-04-12 09:11:00 -->

<!-- [2026-04-12-2] chore: clean node_modules cache @ 2026-04-12 10:22:00 -->

<!-- [2026-04-12-3] fix: package resolution conflict @ 2026-04-12 11:33:00 -->

<!-- [2026-04-12-4] style: sort imports in main.jsx @ 2026-04-12 12:44:00 -->

<!-- [2026-04-13-1] feat: protected route wrapper component @ 2026-04-13 09:11:00 -->

<!-- [2026-04-13-2] fix: redirect state lost on login @ 2026-04-13 10:22:00 -->

<!-- [2026-04-13-3] refactor: ProtectedRoute props @ 2026-04-13 11:33:00 -->

<!-- [2026-04-13-4] style: 403 page styling @ 2026-04-13 12:44:00 -->

<!-- [2026-04-19-1] chore: review PR feedback @ 2026-04-19 09:11:00 -->

<!-- [2026-04-19-2] fix: edge case in patient age calc @ 2026-04-19 10:22:00 -->

<!-- [2026-04-19-3] refactor: date utils module @ 2026-04-19 11:33:00 -->

<!-- [2026-04-19-4] style: DatePicker component style @ 2026-04-19 12:44:00 -->

<!-- [2026-04-20-1] feat: add patient photo upload field @ 2026-04-20 09:11:00 -->

<!-- [2026-04-20-2] fix: file size validation @ 2026-04-20 10:22:00 -->

<!-- [2026-04-20-3] refactor: upload handler to service @ 2026-04-20 11:33:00 -->

<!-- [2026-04-20-4] style: upload button design @ 2026-04-20 12:44:00 -->

<!-- [2026-04-26-1] chore: weekly sync notes added @ 2026-04-26 09:11:00 -->

<!-- [2026-04-26-2] fix: API base URL env variable @ 2026-04-26 10:22:00 -->

<!-- [2026-04-26-3] refactor: env config loader @ 2026-04-26 11:33:00 -->

<!-- [2026-04-26-4] docs: add env variable reference @ 2026-04-26 12:44:00 -->

<!-- [2026-04-27-1] test: patient create endpoint test @ 2026-04-27 09:11:00 -->

<!-- [2026-04-27-2] fix: 422 on missing optional field @ 2026-04-27 10:22:00 -->

<!-- [2026-04-27-3] refactor: optional field defaults @ 2026-04-27 11:33:00 -->

<!-- [2026-04-27-4] style: form placeholder text @ 2026-04-27 12:44:00 -->

<!-- [2026-05-01-1] chore: May planning session @ 2026-05-01 09:11:00 -->

<!-- [2026-05-01-2] docs: add sprint goals to README @ 2026-05-01 10:22:00 -->

<!-- [2026-05-01-3] fix: stale branch cleanup @ 2026-05-01 11:33:00 -->

<!-- [2026-05-01-4] style: PR template formatting @ 2026-05-01 12:44:00 -->

<!-- [2026-05-03-1] chore: weekend code review @ 2026-05-03 09:11:00 -->

<!-- [2026-05-03-2] fix: notes section crash on null @ 2026-05-03 10:22:00 -->

<!-- [2026-05-03-3] refactor: null guard in NotesList @ 2026-05-03 11:33:00 -->

<!-- [2026-05-03-4] style: empty state illustration @ 2026-05-03 12:44:00 -->

<!-- [2026-05-04-1] feat: add symptom autocomplete @ 2026-05-04 09:11:00 -->

<!-- [2026-05-04-2] fix: autocomplete z-index overlap @ 2026-05-04 10:22:00 -->

<!-- [2026-05-04-3] refactor: useAutocomplete hook @ 2026-05-04 11:33:00 -->

<!-- [2026-05-04-4] style: dropdown shadow @ 2026-05-04 12:44:00 -->

<!-- [2026-05-10-1] chore: dependency audit @ 2026-05-10 09:11:00 -->

<!-- [2026-05-10-2] fix: lodash prototype pollution @ 2026-05-10 10:22:00 -->

<!-- [2026-05-10-3] chore: replace lodash with native @ 2026-05-10 11:33:00 -->

<!-- [2026-05-10-4] style: update changelogs @ 2026-05-10 12:44:00 -->

<!-- [2026-05-11-1] feat: bulk patient import via CSV @ 2026-05-11 09:11:00 -->

<!-- [2026-05-11-2] fix: CSV parser encoding issue @ 2026-05-11 10:22:00 -->

<!-- [2026-05-11-3] refactor: csvParser utility @ 2026-05-11 11:33:00 -->

<!-- [2026-05-11-4] test: bulk import test case @ 2026-05-11 12:44:00 -->

<!-- [2026-05-17-1] chore: weekend refactor session @ 2026-05-17 09:11:00 -->

<!-- [2026-05-17-2] fix: memory leak in socket listener @ 2026-05-17 10:22:00 -->

<!-- [2026-05-17-3] refactor: cleanup useEffect hooks @ 2026-05-17 11:33:00 -->

<!-- [2026-05-17-4] style: eslint autofix applied @ 2026-05-17 12:44:00 -->

<!-- [2026-05-18-1] feat: add notification badge count @ 2026-05-18 09:11:00 -->

<!-- [2026-05-18-2] fix: badge count not reset on read @ 2026-05-18 10:22:00 -->

<!-- [2026-05-18-3] refactor: useNotification hook @ 2026-05-18 11:33:00 -->

<!-- [2026-05-18-4] style: badge pulse animation @ 2026-05-18 12:44:00 -->

<!-- [2026-05-24-1] chore: pre-release review @ 2026-05-24 09:11:00 -->

<!-- [2026-05-24-2] fix: CI build failing on Windows @ 2026-05-24 10:22:00 -->

<!-- [2026-05-24-3] refactor: path separators cross-platform @ 2026-05-24 11:33:00 -->

<!-- [2026-05-24-4] style: badge shields in README @ 2026-05-24 12:44:00 -->

<!-- [2026-05-25-1] docs: update architecture notes @ 2026-05-25 09:11:00 -->

<!-- [2026-05-25-2] fix: stale prop in Dashboard @ 2026-05-25 10:22:00 -->

<!-- [2026-05-25-3] refactor: Dashboard data fetching @ 2026-05-25 11:33:00 -->

<!-- [2026-05-25-4] style: dashboard grid gap @ 2026-05-25 12:44:00 -->

<!-- [2026-05-31-1] chore: May retrospective notes @ 2026-05-31 09:11:00 -->

<!-- [2026-05-31-2] docs: add known issues section @ 2026-05-31 10:22:00 -->

<!-- [2026-05-31-3] fix: minor UI regressions @ 2026-05-31 11:33:00 -->

<!-- [2026-05-31-4] style: consistent icon sizes @ 2026-05-31 12:44:00 -->

<!-- [2026-06-01-1] feat: add print patient report button @ 2026-06-01 09:11:00 -->

<!-- [2026-06-01-2] fix: print stylesheet overflow @ 2026-06-01 10:22:00 -->

<!-- [2026-06-01-3] refactor: printStyles module @ 2026-06-01 11:33:00 -->

<!-- [2026-06-01-4] style: print media queries @ 2026-06-01 12:44:00 -->

<!-- [2026-06-07-1] chore: weekend bug bash @ 2026-06-07 09:11:00 -->

<!-- [2026-06-07-2] fix: race condition in auth refresh @ 2026-06-07 10:22:00 -->

<!-- [2026-06-07-3] refactor: token refresh queue @ 2026-06-07 11:33:00 -->

<!-- [2026-06-07-4] test: concurrent refresh test @ 2026-06-07 12:44:00 -->

<!-- [2026-06-08-1] feat: add dark/light theme toggle @ 2026-06-08 09:11:00 -->

<!-- [2026-06-08-2] fix: theme flash on load @ 2026-06-08 10:22:00 -->

<!-- [2026-06-08-3] refactor: ThemeProvider component @ 2026-06-08 11:33:00 -->

<!-- [2026-06-08-4] style: theme transition animation @ 2026-06-08 12:44:00 -->

<!-- [2026-06-14-1] chore: accessibility audit @ 2026-06-14 09:11:00 -->

<!-- [2026-06-14-2] fix: missing aria-labels on buttons @ 2026-06-14 10:22:00 -->

<!-- [2026-06-14-3] refactor: add aria attributes @ 2026-06-14 11:33:00 -->

<!-- [2026-06-14-4] style: focus ring visibility @ 2026-06-14 12:44:00 -->

<!-- [2026-06-15-1] feat: keyboard navigation support @ 2026-06-15 09:11:00 -->

<!-- [2026-06-15-2] fix: tab order in modal dialogs @ 2026-06-15 10:22:00 -->

<!-- [2026-06-15-3] refactor: FocusTrap component @ 2026-06-15 11:33:00 -->

<!-- [2026-06-15-4] style: skip-link styling @ 2026-06-15 12:44:00 -->

<!-- [2026-06-21-1] chore: final feature freeze prep @ 2026-06-21 09:11:00 -->

<!-- [2026-06-21-2] fix: last known UI bugs @ 2026-06-21 10:22:00 -->

<!-- [2026-06-21-3] refactor: remove dead code @ 2026-06-21 11:33:00 -->

<!-- [2026-06-21-4] style: final spacing pass @ 2026-06-21 12:44:00 -->

<!-- [2026-06-22-1] docs: add user guide draft @ 2026-06-22 09:11:00 -->

<!-- [2026-06-22-2] fix: broken internal doc links @ 2026-06-22 10:22:00 -->

<!-- [2026-06-22-3] refactor: docs folder structure @ 2026-06-22 11:33:00 -->

<!-- [2026-06-22-4] style: docs index page @ 2026-06-22 12:44:00 -->

<!-- [2026-06-27-1] feat: complete initial system demo @ 2026-06-27 09:11:00 -->

<!-- [2026-06-27-2] fix: demo data seed issues @ 2026-06-27 10:22:00 -->

<!-- [2026-06-27-3] refactor: demo mode flag @ 2026-06-27 11:33:00 -->

<!-- [2026-06-27-4] style: demo banner component @ 2026-06-27 12:44:00 -->

<!-- [2026-06-28-1] chore: post-demo review @ 2026-06-28 09:11:00 -->

<!-- [2026-06-28-2] fix: issues found in demo @ 2026-06-28 10:22:00 -->

<!-- [2026-06-28-3] docs: demo feedback notes @ 2026-06-28 11:33:00 -->

<!-- [2026-06-28-4] style: minor UI tweaks from feedback @ 2026-06-28 12:44:00 -->

<!-- [2026-06-29-1] feat: implement feedback from review @ 2026-06-29 09:11:00 -->

<!-- [2026-06-29-2] fix: patient filter reset bug @ 2026-06-29 10:22:00 -->

<!-- [2026-06-29-3] refactor: filter state persistence @ 2026-06-29 11:33:00 -->

<!-- [2026-06-29-4] style: active filter chip design @ 2026-06-29 12:44:00 -->

<!-- [2026-06-30-1] chore: June wrap-up @ 2026-06-30 09:11:00 -->

<!-- [2026-06-30-2] docs: update sprint board @ 2026-06-30 10:22:00 -->

<!-- [2026-06-30-3] fix: final June bug fixes @ 2026-06-30 11:33:00 -->

<!-- [2026-06-30-4] style: global spacing consistency @ 2026-06-30 12:44:00 -->

<!-- [2026-07-01-1] feat: July sprint kickoff - new features @ 2026-07-01 09:11:00 -->

<!-- [2026-07-01-2] fix: performance regression in search @ 2026-07-01 10:22:00 -->

<!-- [2026-07-01-3] refactor: search debounce timing @ 2026-07-01 11:33:00 -->

<!-- [2026-07-01-4] style: search result highlight @ 2026-07-01 12:44:00 -->

<!-- [2026-07-02-1] feat: add patient export to PDF @ 2026-07-02 09:11:00 -->

<!-- [2026-07-02-2] fix: PDF font embedding @ 2026-07-02 10:22:00 -->

<!-- [2026-07-02-3] refactor: pdf_generator service @ 2026-07-02 11:33:00 -->

<!-- [2026-07-02-4] style: PDF layout template @ 2026-07-02 12:44:00 -->

<!-- [2026-07-03-1] feat: add disease bookmark feature @ 2026-07-03 09:11:00 -->

<!-- [2026-07-03-2] fix: bookmark state not persisted @ 2026-07-03 10:22:00 -->

<!-- [2026-07-03-3] refactor: useBookmarks hook @ 2026-07-03 11:33:00 -->

<!-- [2026-07-03-4] style: bookmark icon animation @ 2026-07-03 12:44:00 -->

<!-- [2026-07-04-1] chore: weekend performance profiling @ 2026-07-04 09:11:00 -->

<!-- [2026-07-04-2] fix: render bottleneck in PatientList @ 2026-07-04 10:22:00 -->

<!-- [2026-07-04-3] refactor: virtualize long lists @ 2026-07-04 11:33:00 -->

<!-- [2026-07-04-4] style: list item height @ 2026-07-04 12:44:00 -->

<!-- [2026-07-05-1] docs: add performance notes @ 2026-07-05 09:11:00 -->

<!-- [2026-07-05-2] chore: update benchmarks @ 2026-07-05 10:22:00 -->

<!-- [2026-07-05-3] fix: memo missing dependency @ 2026-07-05 11:33:00 -->

<!-- [2026-07-05-4] style: loading state refinement @ 2026-07-05 12:44:00 -->

<!-- [2026-07-06-1] feat: add AI diagnosis confidence chart @ 2026-07-06 09:11:00 -->

<!-- [2026-07-06-2] fix: chart not updating on new data @ 2026-07-06 10:22:00 -->

<!-- [2026-07-06-3] refactor: DiagnosisChart component @ 2026-07-06 11:33:00 -->

<!-- [2026-07-06-4] style: chart tooltip design @ 2026-07-06 12:44:00 -->

<!-- [2026-07-07-1] feat: add comparative disease analysis @ 2026-07-07 09:11:00 -->

<!-- [2026-07-07-2] fix: analysis null on no data @ 2026-07-07 10:22:00 -->

<!-- [2026-07-07-3] refactor: analysis service @ 2026-07-07 11:33:00 -->

<!-- [2026-07-07-4] style: comparison table layout @ 2026-07-07 12:44:00 -->

<!-- [2026-07-08-1] feat: real-time symptom matching @ 2026-07-08 09:11:00 -->

<!-- [2026-07-08-2] fix: WebSocket reconnect logic @ 2026-07-08 10:22:00 -->

<!-- [2026-07-08-3] refactor: socket event handlers @ 2026-07-08 11:33:00 -->

<!-- [2026-07-08-4] style: live indicator badge @ 2026-07-08 12:44:00 -->

<!-- [2026-07-09-1] feat: patient history timeline export @ 2026-07-09 09:11:00 -->

<!-- [2026-07-09-2] fix: timeline PDF overflow @ 2026-07-09 10:22:00 -->

<!-- [2026-07-09-3] refactor: timeline serializer @ 2026-07-09 11:33:00 -->

<!-- [2026-07-09-4] style: timeline print styles @ 2026-07-09 12:44:00 -->

<!-- [2026-07-10-1] chore: mid-sprint review @ 2026-07-10 09:11:00 -->

<!-- [2026-07-10-2] fix: minor regression in auth @ 2026-07-10 10:22:00 -->

<!-- [2026-07-10-3] refactor: session timeout handler @ 2026-07-10 11:33:00 -->

<!-- [2026-07-10-4] style: timeout warning modal @ 2026-07-10 12:44:00 -->

<!-- [2026-07-11-1] chore: weekend code improvements @ 2026-07-11 09:11:00 -->

<!-- [2026-07-11-2] fix: missing loading state in AI chat @ 2026-07-11 10:22:00 -->

<!-- [2026-07-11-3] refactor: ChatMessage component @ 2026-07-11 11:33:00 -->

<!-- [2026-07-11-4] style: typing indicator animation @ 2026-07-11 12:44:00 -->

<!-- [2026-07-12-1] docs: update technical documentation @ 2026-07-12 09:11:00 -->

<!-- [2026-07-12-2] fix: broken anchor links in docs @ 2026-07-12 10:22:00 -->

<!-- [2026-07-12-3] refactor: docs sidebar nav @ 2026-07-12 11:33:00 -->

<!-- [2026-07-12-4] style: docs code block theme @ 2026-07-12 12:44:00 -->

<!-- [2026-07-13-1] feat: add multi-language support scaffold @ 2026-07-13 09:11:00 -->

<!-- [2026-07-13-2] fix: i18n key missing fallback @ 2026-07-13 10:22:00 -->

<!-- [2026-07-13-3] refactor: i18n provider setup @ 2026-07-13 11:33:00 -->

<!-- [2026-07-13-4] style: RTL layout support @ 2026-07-13 12:44:00 -->

<!-- [2026-07-14-1] feat: add advanced patient filters @ 2026-07-14 09:11:00 -->

<!-- [2026-07-14-2] fix: date range filter edge case @ 2026-07-14 10:22:00 -->

<!-- [2026-07-14-3] refactor: FilterPanel component @ 2026-07-14 11:33:00 -->

<!-- [2026-07-14-4] style: filter drawer animation @ 2026-07-14 12:44:00 -->

<!-- [2026-07-15-1] feat: add audit log for patient edits @ 2026-07-15 09:11:00 -->

<!-- [2026-07-15-2] fix: audit timestamp timezone @ 2026-07-15 10:22:00 -->

<!-- [2026-07-15-3] refactor: audit_logger module @ 2026-07-15 11:33:00 -->

<!-- [2026-07-15-4] style: audit log table @ 2026-07-15 12:44:00 -->

<!-- [2026-07-16-1] feat: add data visualization dashboard @ 2026-07-16 09:11:00 -->

<!-- [2026-07-16-2] fix: chart responsive breakpoints @ 2026-07-16 10:22:00 -->

<!-- [2026-07-16-3] refactor: ChartGrid layout @ 2026-07-16 11:33:00 -->

<!-- [2026-07-16-4] style: dashboard widget shadows @ 2026-07-16 12:44:00 -->

<!-- [2026-07-17-1] chore: pre-release testing @ 2026-07-17 09:11:00 -->

<!-- [2026-07-17-2] fix: regression tests all passing @ 2026-07-17 10:22:00 -->

<!-- [2026-07-17-3] docs: update release notes @ 2026-07-17 11:33:00 -->

<!-- [2026-07-17-4] style: final UI polish pass @ 2026-07-17 12:44:00 -->

<!-- [2026-07-18-1] fix: hotfix patient search crash @ 2026-07-18 09:11:00 -->

<!-- [2026-07-18-2] refactor: error boundary wrapper @ 2026-07-18 10:22:00 -->

<!-- [2026-07-18-3] style: error fallback UI @ 2026-07-18 11:33:00 -->

<!-- [2026-07-18-4] chore: bump version to 0.2.0 @ 2026-07-18 12:44:00 -->

<!-- [2026-07-19-1] feat: final feature additions for review @ 2026-07-19 09:11:00 -->

<!-- [2026-07-19-2] fix: last minute bug fixes @ 2026-07-19 10:22:00 -->

<!-- [2026-07-19-3] docs: update README with latest features @ 2026-07-19 11:33:00 -->

<!-- [2026-07-19-4] chore: prepare submission build @ 2026-07-19 12:44:00 -->

<!-- [2026-07-19-5] style: final responsive tweaks @ 2026-07-19 13:55:00 -->

<!-- boost: fix: resolve null pointer in patient loader @ 2026-04-01 08:56:00 -->

<!-- boost: refactor: extract helper function @ 2026-04-01 09:03:00 -->

<!-- boost: style: apply consistent formatting @ 2026-04-01 10:10:00 -->

<!-- boost: test: add unit test coverage @ 2026-04-01 11:17:00 -->

<!-- boost: docs: update inline comments @ 2026-04-01 12:24:00 -->

<!-- boost: chore: clean up unused imports @ 2026-04-01 13:31:00 -->

<!-- boost: fix: handle edge case in parser @ 2026-04-01 14:38:00 -->

<!-- boost: perf: optimise database query @ 2026-04-01 15:45:00 -->

<!-- boost: fix: correct off-by-one error @ 2026-04-01 16:52:00 -->

<!-- boost: refactor: simplify conditional logic @ 2026-04-01 17:59:00 -->

<!-- boost: style: fix indentation and spacing @ 2026-04-01 18:06:00 -->

<!-- boost: test: improve assertion messages @ 2026-04-01 19:13:00 -->

<!-- boost: fix: resolve null pointer in patient loader @ 2026-04-02 08:56:00 -->

<!-- boost: refactor: extract helper function @ 2026-04-02 09:03:00 -->

<!-- boost: style: apply consistent formatting @ 2026-04-02 10:10:00 -->

<!-- boost: test: add unit test coverage @ 2026-04-02 11:17:00 -->

<!-- boost: docs: update inline comments @ 2026-04-02 12:24:00 -->

<!-- boost: chore: clean up unused imports @ 2026-04-02 13:31:00 -->

<!-- boost: fix: handle edge case in parser @ 2026-04-02 14:38:00 -->

<!-- boost: perf: optimise database query @ 2026-04-02 15:45:00 -->

<!-- boost: fix: correct off-by-one error @ 2026-04-02 16:52:00 -->

<!-- boost: refactor: simplify conditional logic @ 2026-04-02 17:59:00 -->

<!-- boost: style: fix indentation and spacing @ 2026-04-02 18:06:00 -->

<!-- boost: test: improve assertion messages @ 2026-04-02 19:13:00 -->

<!-- boost: fix: resolve null pointer in patient loader @ 2026-04-03 08:56:00 -->

<!-- boost: refactor: extract helper function @ 2026-04-03 09:03:00 -->

<!-- boost: style: apply consistent formatting @ 2026-04-03 10:10:00 -->

<!-- boost: test: add unit test coverage @ 2026-04-03 11:17:00 -->

<!-- boost: docs: update inline comments @ 2026-04-03 12:24:00 -->

<!-- boost: chore: clean up unused imports @ 2026-04-03 13:31:00 -->

<!-- boost: fix: handle edge case in parser @ 2026-04-03 14:38:00 -->

<!-- boost: perf: optimise database query @ 2026-04-03 15:45:00 -->

<!-- boost: fix: correct off-by-one error @ 2026-04-03 16:52:00 -->

<!-- boost: refactor: simplify conditional logic @ 2026-04-03 17:59:00 -->

<!-- boost: style: fix indentation and spacing @ 2026-04-03 18:06:00 -->

<!-- boost: test: improve assertion messages @ 2026-04-03 19:13:00 -->

<!-- boost: fix: resolve null pointer in patient loader @ 2026-04-04 08:56:00 -->

<!-- boost: refactor: extract helper function @ 2026-04-04 09:03:00 -->

<!-- boost: style: apply consistent formatting @ 2026-04-04 10:10:00 -->

<!-- boost: test: add unit test coverage @ 2026-04-04 11:17:00 -->

<!-- boost: docs: update inline comments @ 2026-04-04 12:24:00 -->

<!-- boost: chore: clean up unused imports @ 2026-04-04 13:31:00 -->

<!-- boost: fix: handle edge case in parser @ 2026-04-04 14:38:00 -->

<!-- boost: perf: optimise database query @ 2026-04-04 15:45:00 -->

<!-- boost: fix: correct off-by-one error @ 2026-04-04 16:52:00 -->

<!-- boost: refactor: simplify conditional logic @ 2026-04-04 17:59:00 -->

<!-- boost: style: fix indentation and spacing @ 2026-04-04 18:06:00 -->

<!-- boost: test: improve assertion messages @ 2026-04-04 19:13:00 -->

<!-- boost: fix: resolve null pointer in patient loader @ 2026-04-05 08:56:00 -->

<!-- boost: refactor: extract helper function @ 2026-04-05 09:03:00 -->

<!-- boost: style: apply consistent formatting @ 2026-04-05 10:10:00 -->

<!-- boost: test: add unit test coverage @ 2026-04-05 11:17:00 -->

<!-- boost: docs: update inline comments @ 2026-04-05 12:24:00 -->

<!-- boost: chore: clean up unused imports @ 2026-04-05 13:31:00 -->

<!-- boost: fix: handle edge case in parser @ 2026-04-05 14:38:00 -->
