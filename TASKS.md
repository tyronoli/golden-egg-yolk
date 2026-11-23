# TASKS: Golden Egg Yolk Cooperatives Management System

Work is done **one task at a time**. The scope, rules, stack, security requirements and data model live in `CLAUDE.md` (or `project-knowledge.md` in a claude.ai Project). This file only says *what to do next* and *when it is done*. If a task conflicts with that file, stop and ask.

## How to use this file

**Run a task:** say `Do T-013` (or "do the next task"). Claude reads the task, checks its dependencies are fully ticked, does only that task, then reports.

**Each task follows this loop:**
1. Confirm every task listed under `depends` is fully ticked `[x]`. If not, say which are missing and stop.
2. Restate the task in 2-3 lines and list any open question that blocks it. Ask before assuming business rules (rates, fees, formulas). Make them configurable instead.
3. Implement in small steps. Each checkbox under the task is one commit-sized step.
4. Write tests for the step and run them (Claude Code), or give the commands and expected output (claude.ai Project).
5. Commit, ticking the boxes that commit covers (see "Commit and checkbox rules").
6. When all sub-boxes are ticked and the Definition of Done is met, tick the task's own box. Add follow-up work as new tasks at the end of the phase or in the Backlog.
7. **Finish with git:** run the commands in "Git: finishing a task" (commit, push the task branch, open a pull request), then report what was pushed.

**Starter prompts**
- `Do T-0XX following TASKS.md and CLAUDE.md.`
- `Do the next unchecked step of T-0XX, then commit.`
- `What is the next task? Check dependencies and tell me if anything blocks it.`
- `Show progress: how many boxes are ticked per phase?`
- `Split T-0XX into smaller steps.` / `Add a task for <idea> after T-0XX.`
- `Review T-0XX against its checkboxes and the Definition of Done.`

**In a claude.ai Project (no file access):** Claude gives you the updated checklist block after each session. Paste it back into this file and re-upload it.

## Commit and checkbox rules

- **Every commit ticks the boxes it covers, in the same commit.** Change `- [ ]` to `- [x]` for each step the commit completes, so the code and this file always match.
- Tick a box **only if** the step is finished and its tests pass. Half-done work stays unticked. Add an indented note under it (`  - note: what is left`).
- Put the task ID in the commit message: `T-013: add scoped throttles for login and OTP`. A commit that covers several tasks lists them: `T-010, T-014: ...`.
- One commit should cover one step, or a few related steps. Do not mix unrelated tasks in one commit.
- The task's own box (the bold line) is ticked in the commit that finishes its last sub-box.
- If a step is blocked, leave it unticked and add `  - BLOCKED: <reason / who must answer>`.
- Never tick a box for work that is not in the repository or not passing tests.
- Never commit `.env`, database dumps, uploaded member files or secrets.

## Git: finishing a task

One branch per task, named `task/T-XXX-short-name`. Commit as you go (one commit per step, boxes ticked in the same commit). When the task is finished, push the branch and open a pull request. Replace `T-013` and the names with the real task.

**1. Start the task** (once, before any work)
```bash
git switch main
git pull origin main
git switch -c task/T-013-rate-limiting
```

**2. After each step** (repeat; tick the matching boxes in `TASKS.md` first)
```bash
git status                       # review: no .env, dumps, uploads or secrets
git add <changed files> TASKS.md # prefer named files; use `git add -A` only after reviewing status
git commit -m "T-013: add scoped throttles for login and OTP"
```

**3. Finish the task** (all sub-boxes ticked, tests and lint pass, Definition of Done met)
```bash
# run the checks first (backend and frontend)
pytest
npm run lint && npm run build

git status                       # working tree should be clean
git push -u origin task/T-013-rate-limiting
gh pr create --base main --title "T-013: Rate limiting and lockout" \
  --body "Completes T-013. See the ticked boxes in TASKS.md. Tests: pytest passing."
```

**4. After the pull request is merged**
```bash
git switch main
git pull origin main
git branch -d task/T-013-rate-limiting
```

**Git rules**
- Run the tests and lint **before** pushing. Do not push a failing task.
- Never push straight to `main` and never use `git push --force`. If a push is rejected, stop and report it.
- Never commit `.env`, database dumps, uploaded member files or secrets. If `git status` shows one, stop and fix `.gitignore` first.
- If a task is only partly done, still commit and push the branch with the unticked boxes left as they are, and say so in the pull request. Do not open it as finished.
- No `gh` CLI or no remote yet? Push the branch, then open the pull request on the Git host's website.
- Solo and want no pull requests? Replace step 3's `gh pr create` and step 4 with: `git switch main && git merge --no-ff task/T-013-rate-limiting && git push origin main`.
- **Claude Code** runs these commands itself and reports the result. **A claude.ai Project** cannot run git, so Claude gives you the exact block above, filled in with the task ID, branch name and commit message, for you to run.

## Definition of Done (applies before a task's own box is ticked)

- All sub-boxes ticked, including its **Done when** check.
- Tests written and passing (backend: pytest; frontend: lint, type-check and component tests where relevant).
- Lint, formatting and type checks pass. No `any` in TypeScript.
- **Nothing business-specific hard-coded** (rates, fees, terms, limits, number formats come from configuration).
- Endpoints have explicit permission classes, input validation, pagination on lists and rate limiting where relevant. Member data is scoped to the logged-in member.
- Money uses `Decimal`; financial records are append-only; postings are balanced and atomic.
- Create, update, void and approve actions write to the audit trail.
- No secrets in code; new env vars added to `.env.example`.
- Loading, empty and error states handled in the UI. Works on phone and desktop widths.

---

## Phase 1: Project scaffold

- [ ] **T-001 Repo and Docker Compose** (depends: none)
  - [ ] `backend/` and `frontend/` folders, `.gitignore`, `.env.example`
  - [ ] Docker Compose with Postgres and Redis
  - [ ] Backend and frontend containers defined and start
  - [ ] Git repository initialized with `origin` remote and `main` branch (protect `main` on the Git host: require pull requests)
  - [ ] Done when: `docker compose up` starts all services; Postgres and Redis reachable

- [ ] **T-002 Django project** (depends: T-001)
  - [ ] Settings split (base/dev/prod), all values from environment variables
  - [ ] DRF and drf-spectacular installed; API under `/api/v1/`
  - [ ] `core` app with base model (`created_at`, `updated_at`, `created_by`)
  - [ ] ruff, black and pytest configured
  - [ ] Done when: `/api/v1/health/` works, OpenAPI schema renders, pytest runs

- [ ] **T-003 React + TypeScript app** (depends: T-001)
  - [ ] Vite + TypeScript (strict), eslint, prettier
  - [ ] Router, TanStack Query, typed API client
  - [ ] Theme tokens (green/gold palette from `CLAUDE.md`)
  - [ ] App shell: top bar, mobile bottom nav, desktop sidebar
  - [ ] Done when: app loads, shell is responsive, health endpoint call works

- [ ] **T-004 CI pipeline** (depends: T-002, T-003)
  - [ ] Lint, type-check and tests for backend and frontend
  - [ ] `pip-audit` and `npm audit` steps
  - [ ] Done when: CI runs green on a pull request

## Phase 2: Accounts and security

- [ ] **T-010 Users, roles and permissions** (depends: T-002)
  - [ ] Custom `User`, `Role`, `Permission` models (permissions stored in DB)
  - [ ] Seed default roles from `CLAUDE.md`
  - [ ] DRF permission classes and object-level helper
  - [ ] Tests: allow and deny per role
  - [ ] Done when: a view can require a named permission and tests prove it

- [ ] **T-011 Login, logout, change password** (depends: T-010)
  - [ ] Login/logout with httpOnly cookie session or JWT (no tokens in JS)
  - [ ] Argon2 hashing, password validators (min length 12)
  - [ ] Forced password change on first login and after admin reset
  - [ ] Idle timeout
  - [ ] Done when: login works end to end and password rules are enforced

- [ ] **T-012 OTP and password reset** (depends: T-011)
  - [ ] Email OTP and TOTP; short-lived, single-use, hashed codes
  - [ ] Staff roles require OTP; members optional
  - [ ] Forgot/reset password flow with expiring single-use links
  - [ ] Done when: OTP login and reset work, and reuse or expired codes are rejected

- [ ] **T-013 Rate limiting and lockout** (depends: T-011)
  - [ ] DRF throttle classes on Redis; scoped throttles for login, OTP, reset, public forms
  - [ ] Limit values read from config with seeded defaults
  - [ ] Account lockout with backoff; generic error messages (no username enumeration)
  - [ ] `429` with `Retry-After`; log throttled and locked events
  - [ ] Done when: tests prove the 6th login in a minute gets 429 and lockout triggers then expires

- [ ] **T-014 Audit trail and activity log** (depends: T-010)
  - [ ] Audit model and helper (who, what, when, IP, before/after)
  - [ ] Activity log (logins, failed logins, permission changes, exports)
  - [ ] Audit records immutable through the app
  - [ ] Done when: create/update/void on a sample model writes audit rows that cannot be edited via the API

- [ ] **T-015 Frontend authentication** (depends: T-003, T-012)
  - [ ] Login, OTP, forgot/reset and change password screens
  - [ ] Route guards by permission
  - [ ] Session expiry handling
  - [ ] Done when: a user logs in with OTP, is routed correctly, and loses access after logout or timeout

## Phase 3: Configuration Center (build before dependent modules)

- [ ] **T-020 Versioned settings framework** (depends: T-014)
  - [ ] `ConfigSetting` and history models with effective dates
  - [ ] Server-side validation framework
  - [ ] Audit hook on every change
  - [ ] Fail closed when a setting is missing; cache with invalidation
  - [ ] Done when: changing a setting creates a new version, invalid values are rejected, every change is audited

- [ ] **T-021 Module registry and feature flags** (depends: T-010)
  - [ ] Registry model (key, name, enabled, required permission, icon, route)
  - [ ] Menu API for staff and for the member portal
  - [ ] Done when: toggling a flag hides a module from menus

- [ ] **T-022 Number sequences** (depends: T-020)
  - [ ] `NumberSequence` service, concurrency-safe
  - [ ] Format settings (member ID, OR no., certificate no., voucher no.)
  - [ ] Done when: parallel requests never create duplicate numbers and formats change without code edits

- [ ] **T-023 Configuration Center screens** (depends: T-020, T-015)
  - [ ] Admin API and generic settings editor
  - [ ] Roles & Permissions editor
  - [ ] Cooperative profile (name, address, registration numbers, logo)
  - [ ] Done when: an admin edits settings and role permissions in the UI and non-admins cannot

- [ ] **T-024 Settings export and import** (depends: T-020)
  - [ ] Export settings as JSON
  - [ ] Import with validation and audit
  - [ ] Done when: an export imports cleanly into another environment and bad files are rejected

## Phase 4: Membership

- [ ] **T-030 Member models** (depends: T-022)
  - [ ] `Member`, `MembershipApplication` models and migrations
  - [ ] Member types and required documents from config
  - [ ] Member ID generation and QR token
  - [ ] Done when: member ID follows the configured format

- [ ] **T-031 Application and approval workflow** (depends: T-030, T-012)
  - [ ] Submit → verification → approval flow
  - [ ] Approval creates the member and the portal user (invite / set-password email)
  - [ ] Separation of duties enforced
  - [ ] Done when: the full flow is tested with the Membership Officer role

- [ ] **T-032 Member records and documents** (depends: T-030)
  - [ ] Member list with search and filters; profile API
  - [ ] Secure document upload (type/size allow-list, private storage)
  - [ ] Authorized document download
  - [ ] Done when: uploads are validated and files are not publicly reachable

- [ ] **T-033 Membership screens** (depends: T-031, T-032, T-003)
  - [ ] Application form, member list, profile
  - [ ] Verification and approval screens
  - [ ] Done when: staff can take an application from submitted to approved in the UI

## Phase 5: Share capital

- [ ] **T-040 Share capital config and models** (depends: T-020, T-030)
  - [ ] Config: par value, minimum subscription, contribution rules, redemption rules
  - [ ] `ShareCapitalAccount` and `CapitalTransaction` models
  - [ ] Done when: rules come from config with no constants in code

- [ ] **T-041 Capital transactions** (depends: T-040)
  - [ ] Contributions and capital build-up
  - [ ] Redemption (if enabled by config)
  - [ ] Transaction history and member capital statement
  - [ ] Append-only with void/reverse
  - [ ] Done when: balances are correct under concurrent requests

- [ ] **T-042 Share capital screens** (depends: T-041)
  - [ ] Capital dashboard and new contribution form
  - [ ] History and statement views
  - [ ] Done when: a Cashier records a contribution and views the statement

## Phase 6: Accounting core

- [ ] **T-050 Chart of accounts and fiscal periods** (depends: T-020)
  - [ ] Account CRUD with validation
  - [ ] Fiscal periods open/close
  - [ ] Seed an example chart marked editable
  - [ ] Done when: admin manages accounts and periods

- [ ] **T-051 Double-entry posting service** (depends: T-050)
  - [ ] `JournalEntry` and `JournalLine` models
  - [ ] Balanced check in service and database; atomic posting
  - [ ] Reversing entries; closed-period lock
  - [ ] Done when: unbalanced entries are impossible and posting to a closed period is rejected

- [ ] **T-052 Post share capital to accounting** (depends: T-041, T-051)
  - [ ] Each contribution/redemption creates a linked balanced entry
  - [ ] Done when: tests show ledger matches capital balances

- [ ] **T-053 Ledger and statements** (depends: T-051)
  - [ ] General ledger and trial balance
  - [ ] Balance sheet, income statement, cash flow
  - [ ] Cash receipts
  - [ ] Done when: reports reconcile with journal totals in tests

- [ ] **T-054 Accounting screens** (depends: T-053)
  - [ ] Chart of accounts and journal entry screens
  - [ ] Ledger, trial balance and statements views
  - [ ] Done when: an Accountant posts a manual entry and views statements

## Phase 7: Loans

- [ ] **T-060 Loan products** (depends: T-020)
  - [ ] `LoanProduct` and `LoanProductVersion` models
  - [ ] Admin API: rate, basis, method, min/max amount and term, frequencies, required docs, co-makers
  - [ ] Activate, retire and versioning
  - [ ] Done when: an admin creates, versions, activates and retires products

- [ ] **T-061 Loan rules as data** (depends: T-060, T-050)
  - [ ] Fees and charges (fixed or percent, when charged)
  - [ ] Penalty rules (rate, grace, compounding)
  - [ ] Eligibility rule builder (field, operator, value, message)
  - [ ] Approval workflow config and GL account mapping
  - [ ] Done when: all stored as validated data with no hard-coded rule

- [ ] **T-062 Calculation engine** (depends: T-061)
  - [ ] Confirm supported interest methods with the cooperative first
  - [ ] Interest method strategy classes
  - [ ] Amortization schedule, fees and penalties
  - [ ] Eligibility evaluation
  - [ ] Unit tests for every method incl. rounding and edge cases
  - [ ] Done when: the engine is pure and the same inputs always give the same output

- [ ] **T-063 Admin loan simulator** (depends: T-062)
  - [ ] Preview schedule for a product, amount and term
  - [ ] Done when: the simulation uses the backend engine only

- [ ] **T-064 Loan application and eligibility** (depends: T-062, T-030)
  - [ ] `LoanApplication` model and API
  - [ ] Eligibility check against the chosen product version
  - [ ] Done when: ineligible applications show the configured messages

- [ ] **T-065 Loan approval workflow** (depends: T-064)
  - [ ] Configurable approval steps, roles and amount thresholds
  - [ ] Loan snapshots the product version at approval
  - [ ] Separation of duties enforced
  - [ ] Done when: later product edits do not change existing loans

- [ ] **T-066 Loan release** (depends: T-065, T-051)
  - [ ] Disbursement with fee deductions
  - [ ] Accounting posting
  - [ ] Schedule stored
  - [ ] Done when: release creates balanced journal entries

- [ ] **T-067 Loan screens** (depends: T-063, T-066)
  - [ ] Product admin screens
  - [ ] Application, evaluation, approval queue
  - [ ] Release, loan statement and schedule
  - [ ] Done when: a loan goes from application to release in the UI

## Phase 8: Collections

- [ ] **T-070 Loan payments** (depends: T-066, T-022)
  - [ ] Payment recording with configurable allocation order
  - [ ] Official receipt numbering
  - [ ] Loan balance update
  - [ ] Done when: allocation is correct in tests and receipt numbers are unique and sequential

- [ ] **T-071 Post payments to accounting** (depends: T-070, T-051)
  - [ ] Each payment posts a balanced entry
  - [ ] Done when: ledger matches loan balances in tests

- [ ] **T-072 Delinquency and due loans** (depends: T-070)
  - [ ] Due loans list
  - [ ] Penalty accrual and aging with configurable buckets (Celery jobs)
  - [ ] Jobs are idempotent
  - [ ] Done when: aging matches the configured buckets

- [ ] **T-073 Collections screens** (depends: T-070, T-072)
  - [ ] Collection dashboard and record payment
  - [ ] Payment history, due and delinquent lists
  - [ ] Done when: a Cashier records a payment and views the receipt

## Phase 9: Member portal

- [ ] **T-080 Member-scoped API** (depends: T-066, T-041)
  - [ ] Own profile, capital, loans, payments, documents endpoints derived from `request.user` only
  - [ ] IDOR tests
  - [ ] Done when: changing IDs never exposes another member's data

- [ ] **T-081 Portal screens** (depends: T-080, T-015)
  - [ ] Dashboard and my profile
  - [ ] My share capital
  - [ ] My loans (status, balance, schedule, next due)
  - [ ] Apply for a loan
  - [ ] Done when: a member sees loan status and applies on a phone-size screen

- [ ] **T-082 Profile change requests** (depends: T-080)
  - [ ] Member submits changes; staff approval queue
  - [ ] Approval applies and audits the change
  - [ ] Done when: member edits wait for approval

- [ ] **T-083 Notifications** (depends: T-072, T-020)
  - [ ] In-app notifications
  - [ ] Email/SMS through configured templates
  - [ ] Throttled sending
  - [ ] Done when: templates are editable in the Configuration Center

- [ ] **T-084 Portal Services area** (depends: T-021)
  - [ ] Area built from the module registry (empty in v1)
  - [ ] Done when: it shows enabled modules only

## Phase 10: Dashboard and reports

- [ ] **T-090 Main dashboard** (depends: T-053, T-072)
  - [ ] Dashboard API (summary cards, recent notifications, shortcuts)
  - [ ] Role-aware dashboard UI
  - [ ] Done when: figures reconcile with ledger and loan data

- [ ] **T-091 Reports** (depends: T-090)
  - [ ] Membership, share capital, loan portfolio with aging
  - [ ] Collection, delinquency, financial, management reports
  - [ ] Async generation, PDF/CSV export, rate-limited, exports audited
  - [ ] Done when: large reports do not block requests

## Phase 11: Dividends and patronage

- [ ] **T-100 Dividend and patronage engine** (depends: T-053, T-020)
  - [ ] Confirm formulas and fiscal year with the cooperative first
  - [ ] Config for rates/formula types, computation basis, reserves
  - [ ] Computation engine with unit tests from worked examples
  - [ ] Done when: results match the cooperative's worked examples

- [ ] **T-101 Dividend run** (depends: T-100)
  - [ ] Preview, approval, posting to accounting
  - [ ] Member dividend/patronage statement
  - [ ] Done when: a run is approved before posting and allocations sum to the total distributed

## Phase 12: Documents and administration

- [ ] **T-110 Documents and PDFs** (depends: T-070, T-041)
  - [ ] Editable templates
  - [ ] Certificates (membership, share, loan), agreements, official receipts
  - [ ] Clearance and certificate of good standing
  - [ ] Done when: PDFs generate from templates and user-supplied text is sanitized

- [ ] **T-111 Admin screens** (depends: T-023, T-014)
  - [ ] User management
  - [ ] Audit trail viewer and activity logs
  - [ ] Backup status and system security settings
  - [ ] Done when: an admin searches audit logs and cannot edit or delete them

## Phase 13: Hardening

- [ ] **T-120 Security review** (depends: all features)
  - [ ] Permissions on every endpoint; IDOR sweep
  - [ ] Secure headers/CSP, upload checks
  - [ ] Dependency and secrets scan
  - [ ] Done when: a written pass/fail checklist exists and all fixes are done

- [ ] **T-121 Backup, restore and load tests** (depends: all features)
  - [ ] Backup and restore drill on a fresh database
  - [ ] Rate-limit load test
  - [ ] Concurrency tests on payments and numbering
  - [ ] Done when: restore is proven and limits hold under load

## Phase 14: Hosting and go-live

- [ ] **T-130 Supabase database** (depends: T-120)
  - [ ] Region, backup plan, SSL, least-privilege DB roles
  - [ ] **Data API locked down / RLS on all tables**
  - [ ] Pooler settings for Django; migrations run
  - [ ] Done when: direct Data API access to app tables is denied

- [ ] **T-131 Backend host** (depends: T-130)
  - [ ] Choose host for Django, Celery, Redis
  - [ ] Env vars, HTTPS, same-site domain plan
  - [ ] Done when: API reachable over HTTPS with workers and scheduler running

- [ ] **T-132 Netlify frontend** (depends: T-131)
  - [ ] Build, SPA redirect, security headers in `netlify.toml`
  - [ ] API base URL env var, custom domain
  - [ ] Done when: login works across app and API domains with secure cookies

- [ ] **T-133 Go-live** (depends: T-132)
  - [ ] Seed real config (products, rates, fees); create first admin
  - [ ] Import members
  - [ ] Monitoring, error alerts, runbook
  - [ ] Done when: the cooperative signs off in a staging dry run

---

## Task notes and decisions log

Add a line per finished task: `T-0XX (date): files, decisions, leftovers.`

- (none yet)

## Backlog and v2 (do not start)

- v2: Agriculture module (farmer registration, farm records, production, procurement, inventory, sales/buyers, payments, logistics) plugged in through the module registry.
- Ideas go here until they become tasks.
