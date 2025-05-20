# Frontend TODOs for ByLand.ai (Chainlit)

## Project Setup
- [x] Remove React/Vite files and config (migrated to Chainlit-only frontend)
- [x] Set up Chainlit project in this directory
- [x] Configure Python environment and dependencies (chainlit, requests, etc.)
- [x] Add .env for backend API URL and secrets

## Core Features
- [ ] Implement onboarding conversational UI (connect to backend `/hiker_profiles/chat/{user_id}`)
- [ ] Add user authentication (optional, if supported by Chainlit)
- [ ] Add profile management UI (CRUD for hiker profiles, optional)
- [ ] Add error handling and loading states
- [ ] Add admin/analytics dashboard (optional)
- [ ] Ensure responsive/mobile-friendly design (if possible)
- [ ] Add Chainlit UI customizations (theme, branding, etc.)
- [ ] Add onboarding start/reset commands
- [ ] Add profile view/edit commands
- [ ] Add admin/analytics commands (optional)

## API Integration
- [ ] Add API service layer (Python requests or httpx)
- [ ] Add API error handling and retry logic
- [ ] Generate OpenAPI client from backend schema (optional)

## Testing
- [ ] Add unit tests for Chainlit flows
- [ ] Add integration tests for onboarding and profile flows

## DevOps
- [ ] Add CI/CD pipeline for Chainlit frontend
- [ ] Add deployment scripts (Docker, etc.)

## Documentation
- [ ] Write setup instructions for Chainlit frontend
- [ ] Add contribution guidelines
- [ ] Document API usage and flows

---

> Add more TODOs as features and requirements evolve.
