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

