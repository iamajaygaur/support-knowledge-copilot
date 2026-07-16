# Demo & Study Guide (Questions + Answers)

Study sheet for the Support Knowledge Copilot. Answers are based on the sample docs in `docs/`.

Before live demos:

```bash
source .venv/bin/activate
python ingest.py --source docs/ --rebuild
streamlit run app.py
# or: python ask.py "What does AUTH-4291 mean?"
# or: make ui / make eval
```

Compare strategies: **hybrid** (best default), **dense**, **sparse**. The Streamlit sidebar can compare **hybrid vs dense** side by side.

---

## How to read each card

- **Question** — paste into the app
- **Expected answer** — what a good grounded response should say
- **Source docs** — where the facts live
- **Why it matters** — interview / demo angle

---

# 1. Simple factual lookups

### Q1. How do employees reset their password?

**Expected answer**

Employees reset passwords from the login page using **Forgot password**. A reset link is emailed to their verified work email and expires in **30 minutes**.

Support can also issue a **temporary password** from **Admin Console → Users → Security → Issue temporary password**. Temporary passwords expire in **24 hours** and must be changed on first login.

**Source docs:** `docs/faq/password-reset.md`

**Why it matters:** Basic citation demo — one clear FAQ source.

---

### Q2. How long is the billing grace period after a failed payment?

**Expected answer**

After a failed payment, the account gets a **7-day grace period**. On **day 8**, paid features are limited until payment succeeds.

**Source docs:** `docs/faq/billing-faq.md`

**Why it matters:** Simple number lookup (`7-day`).

---

### Q3. What is the rate limit for the standard API plan?

**Expected answer**

Standard plans are limited to **120 requests per minute**. Enterprise plans get **600 requests/minute**. Going over the limit returns HTTP **429** with error code **API-4290**.

**Source docs:** `docs/api/authentication.md`

**Why it matters:** API fact + related error code in one answer.

---

### Q4. What is the first-response SLA for an urgent ticket?

**Expected answer**

For **Urgent** priority, first response is due in **15 minutes**. Resolution target is **4 hours**.

**Source docs:** `docs/policies/support-sla.md`

**Why it matters:** Policy table lookup.

---

### Q5. Can support agents email MFA backup codes to users?

**Expected answer**

**No.** Support must **not** share backup codes over email. Backup codes may only be revealed on a **verified video call**.

**Source docs:** `docs/policies/mfa-policy.md`

**Why it matters:** Clear yes/no policy answer with a safety rule.

---

# 2. Error codes (hybrid retrieval shines)

### Q6. What does error AUTH-4291 mean and how do I fix it?

**Expected answer**

**AUTH-4291** means the user exceeded **5 MFA attempts** within **15 minutes**. MFA is soft-locked for **30 minutes**.

Fix options:

1. Wait for the lockout to expire, or
2. Admin clears it via **Admin Console → Users → Security → Clear MFA lockout**
3. User can try a **backup code** if available

**Source docs:** `docs/troubleshooting/auth-errors.md` (also related: April 2026 release notes)

**Why it matters:** Exact error-code match — BM25/hybrid usually beats dense-only.

---

### Q7. Error BILL-4020 appeared for a customer. What does it mean?

**Expected answer**

**BILL-4020** means the customer’s **card was declined** (failed payment). The account then enters the **7-day grace period**.

**Source docs:** `docs/faq/billing-faq.md`

**Why it matters:** Keyword/error-code retrieval.

---

### Q8. How do I resolve SYNC-2201 connector timeouts?

**Expected answer**

**SYNC-2201** means the external connector did not respond within **60 seconds**.

Steps:

1. Retry from **Integrations → Sync Jobs**
2. If it keeps timing out, reduce batch size to **100 records**

**Source docs:** `docs/troubleshooting/sync-failures.md`

**Why it matters:** Troubleshooting procedure with an error code.

---

### Q9. What does API-4290 mean?

**Expected answer**

**API-4290** means the client **exceeded the API rate limit**. Standard plans allow **120 req/min**; enterprise allows **600 req/min**. The HTTP status is **429**.

**Source docs:** `docs/api/authentication.md`

**Why it matters:** Same family as Q3, but asked via error code.

---

# 3. Policies and procedures

### Q10. How do I reset MFA for a locked employee account?

**Expected answer**

1. Verify identity with **HR employee ID** and manager confirmation in Slack **`#identity-verify`**
2. Open **Admin Console → Users → Security**
3. Select **Reset MFA**
4. Choose **Invalidate all MFA methods**
5. Send the enrollment link — user must enroll within **2 hours**

Do **not** email backup codes.

**Source docs:** `docs/policies/mfa-policy.md`

**Why it matters:** Multi-step procedure with citations.

---

### Q11. What NameID format should we use for SSO?

**Expected answer**

Set the SAML **`NameID` format to `emailAddress`**.

**Source docs:** `docs/onboarding/sso-setup.md` (also mentioned in `auth-errors.md` for AUTH-4400)

**Why it matters:** Exact config value support agents must get right.

---

### Q12. What happens if a user is in SSO-only mode and tries the password reset form?

**Expected answer**

SSO-only accounts **cannot** reset credentials through the product password form. They must reset through their **identity provider** (Okta / Azure AD / Google Workspace).

**Source docs:** `docs/faq/password-reset.md`

**Why it matters:** Common support pitfall.

---

### Q13. What retention periods apply to support chat logs and security audit logs?

**Expected answer**

- Support chat transcripts: **24 months**, then auto-deleted
- Security audit logs: **36 months**

(Customer data exports are downloadable for **14 days**, if mentioned.)

**Source docs:** `docs/policies/data-retention.md`

**Why it matters:** Two facts from one policy doc.

---

# 4. Multi-document answers

### Q14. A user hit AUTH-4291 and still has a working authenticator. What should an admin do?

**Expected answer**

Prefer **Clear MFA lockout** (not a full MFA reset). April 2026 added lockout-clear controls, and that is the preferred fix for AUTH-4291 when the authenticator still works.

Path: **Admin Console → Users → Security → Clear MFA lockout**.

**Source docs:**

- `docs/release-notes/2026-04-release.md`
- `docs/troubleshooting/auth-errors.md`
- (older/wrong path) full reset in `docs/policies/mfa-policy.md` / Dec 2025 notes

**Why it matters:** Combines error code + newer release guidance.

---

### Q15. What default role does JIT SSO provisioning assign, and is VPN included for new hires?

**Expected answer**

- JIT SSO provisioning creates users with default role **`member`**
- VPN is **not** included by default for new hires; it must be requested separately with business justification

**Source docs:**

- `docs/onboarding/sso-setup.md`
- `docs/onboarding/new-hire-access.md`

**Why it matters:** True multi-doc synthesis.

---

### Q16. How do I create a ticket via API and what statuses are valid?

**Expected answer**

Create a ticket with:

`POST /v1/tickets`

Required fields: `subject`, `body`, `priority` (`low` | `medium` | `high` | `urgent`).

Valid statuses: **`open`**, **`pending`**, **`solved`**, **`closed`**.

Reopening a closed ticket needs scope `write:tickets:reopen`.

**Source docs:** `docs/api/tickets-api.md`

**Why it matters:** API reference style answer.

---

# 5. Outdated-document traps

These have conflicting old vs new docs. The **newer** answer is correct.

### Q17. How should support handle AUTH-4291 after the April 2026 release?

**Expected answer (correct / newer)**

Admins should **clear the MFA lockout** without a full MFA reset when the user still has a working authenticator. That is the preferred fix after April 2026.

**Outdated answer (wrong if used alone)**

December 2025 notes said support must do a **full MFA reset** and there was no lockout-clear action.

**Source docs:**

- Newer: `docs/release-notes/2026-04-release.md` (updated 2026-04-30)
- Older: `docs/release-notes/2025-12-release.md` (updated 2025-12-15)

**Why it matters:** Shows `last_updated` / preferring current guidance.

---

### Q18. When I rotate an API token, how long does the old token stay valid?

**Expected answer (correct / newer)**

The previous token stays valid for a **1-hour overlap window**.

**Outdated answer (wrong if used alone)**

December 2025 notes said rotation **immediately invalidates** the old token.

**Source docs:**

- Newer: `docs/api/authentication.md` and `docs/release-notes/2026-04-release.md`
- Older: `docs/release-notes/2025-12-release.md`

**Why it matters:** Classic stale-doc interview story.

---

# 6. No-answer cases (should refuse)

The assistant should **not invent** an answer. Expect `no_answer`, low confidence, and closest sections.

### Q19. What is our pet-friendly vacation policy for bringing dogs to the office?

**Expected answer**

**Not in the docs.** The corpus has no pet or office-dog policy. A good response says it could not find this and may list closest unrelated sections.

**Source docs:** none

**Why it matters:** Refusal quality — no hallucination.

---

### Q20. How do I configure payroll tax forms in the product?

**Expected answer**

**Not in the docs.** There is no payroll / tax-form documentation in this corpus.

**Source docs:** none

**Why it matters:** Another clean no-answer demo.

---

### Q21. What is the refund policy for unused enterprise seats?

**Expected answer**

**Not in the docs** (or only weak/unrelated billing facts). Should refuse rather than invent refund rules. Billing docs cover invoices, payment methods, and grace periods — not seat refunds.

**Source docs:** none for refunds (`billing-faq.md` is related but insufficient)

**Why it matters:** Near-miss retrieval should still refuse.

---

# 7. Ambiguous questions

### Q22. What should I do about login problems?

**Expected answer (partial / branching)**

Login issues can have several causes. A good answer outlines possible paths **without pretending there is one fix**:

- Password reset (`Forgot password`, 30-minute link)
- MFA lockout (`AUTH-4291`, clear lockout / wait 30 minutes)
- SSO problems (`NameID` = `emailAddress`, assertion errors)
- SSO-only users must reset via the identity provider

It may ask for more detail (error code, SSO vs password, MFA prompt, etc.).

**Source docs:** password-reset, auth-errors, sso-setup, mfa-policy

**Why it matters:** Shows cautious, multi-path support guidance.

---

### Q23. A customer can’t access their account

**Expected answer (partial / branching)**

Same idea as Q22. Should **not** invent a single root cause. Reasonable branches:

- Failed payment / grace period ended (`BILL-4020`)
- Auth / MFA / SSO issues
- Ask for error code, plan status, and whether SSO is enabled

**Source docs:** billing-faq, auth-errors, password-reset, sso-setup

**Why it matters:** Ambiguity handling without hallucination.

---

# 8. Expanded corpus (webhooks, roles, deactivation, notifications)

### Q24. What does HOOK-5001 mean?

**Expected answer**

**HOOK-5001** means the customer webhook endpoint was **unreachable**. The URL must be publicly reachable and return HTTP **2xx** within **10 seconds**.

**Source docs:** `docs/troubleshooting/webhook-errors.md`

**Why it matters:** Another exact error-code lookup for hybrid retrieval.

---

### Q25. What does HOOK-5008 mean?

**Expected answer**

**HOOK-5008** means **invalid signature**. The customer should use the current signing secret from **Settings → Developers → Webhooks**. Secrets rotated in the last hour may still accept the previous secret during the overlap window.

**Source docs:** `docs/troubleshooting/webhook-errors.md`

**Why it matters:** Error code + secret-rotation nuance.

---

### Q26. How many times are failed webhooks retried?

**Expected answer**

Failed deliveries retry up to **5 times** with exponential backoff. After the final failure, the event is marked `dead` and must be replayed manually.

**Source docs:** `docs/troubleshooting/webhook-errors.md`

**Why it matters:** Operational detail for support.

---

### Q27. How do I register a webhook endpoint?

**Expected answer**

Use `POST /v1/webhooks` with required fields `url`, `events`, and `secret`. Supported events include `ticket.created`, `ticket.updated`, and `sync.failed`.

**Source docs:** `docs/api/webhooks-api.md`

**Why it matters:** API reference style answer.

---

### Q28. How do I replay a dead webhook event?

**Expected answer**

Use `POST /v1/webhooks/events/{event_id}/replay`. Only events in `dead` status can be replayed. Requires scope `write:webhooks`.

**Source docs:** `docs/api/webhooks-api.md`, `docs/troubleshooting/webhook-errors.md`

**Why it matters:** Multi-doc procedure (API + error guide).

---

### Q29. Which role is required for MFA reset actions?

**Expected answer**

MFA reset requires the **`admin`** role. Support agents should normally use `team_lead` unless they need user-security actions.

**Source docs:** `docs/onboarding/admin-roles.md`, `docs/policies/mfa-policy.md`

**Why it matters:** Role/permission guidance.

---

### Q30. What capabilities does the team_lead role have?

**Expected answer**

`team_lead` can **assign tickets** and **view team analytics**. It cannot manage users/SSO/API tokens (`admin`) or billing/destructive actions (`owner`).

**Source docs:** `docs/onboarding/admin-roles.md`

**Why it matters:** Role matrix lookup.

---

### Q31. How quickly is product access revoked after employee termination?

**Expected answer**

When HR marks an employee terminated in Workday, product access is revoked within **1 hour**. Shared credentials must be rotated the same day.

**Source docs:** `docs/policies/account-deactivation.md`

**Why it matters:** Offboarding policy fact.

---

### Q32. How long can managers request a data handoff after deactivation?

**Expected answer**

Managers may request a **30-day** data handoff package through Support.

**Source docs:** `docs/policies/account-deactivation.md`

**Why it matters:** Post-deactivation support process.

---

### Q33. What email address sends security notifications?

**Expected answer**

Account and security emails are sent from **`noreply@example.com`**.

**Source docs:** `docs/faq/notifications.md`

**Why it matters:** Simple FAQ fact.

---

### Q34. Do quiet hours suppress urgent ticket notifications?

**Expected answer**

**No.** Quiet hours suppress non-urgent notifications between **22:00 and 07:00**, but **urgent** priority tickets always notify immediately.

**Source docs:** `docs/faq/notifications.md`

**Why it matters:** Exception-to-the-rule answer.

---

### Q35. Are password reset SMS codes still supported?

**Expected answer (correct / newer)**

**No.** Legacy password reset SMS codes were **removed** in the April 2026 release. Email reset links remain supported.

**Source docs:** `docs/release-notes/2026-04-release.md`, `docs/faq/password-reset.md`

**Why it matters:** Another outdated-feature trap.

---

### Q36. What is the company holiday gift card policy?

**Expected answer**

**Not in the docs.** Refuse; do not invent HR perks policy.

**Source docs:** none

**Why it matters:** Extra no-answer case for eval.

---

### Q37. How do I set up hardware YubiKey shipping for executives?

**Expected answer**

**Not in the docs.** Refuse; no hardware-token shipping process is documented.

**Source docs:** none

**Why it matters:** Extra no-answer case for eval.

---

### Q38. A customer says notifications are broken

**Expected answer (partial / branching)**

Ask whether the issue is **email**, **Slack**, or **quiet hours**:

- Email comes from `noreply@example.com` (check spam/allowlist)
- Slack alerts are configured under **Settings → Notifications → Slack**
- Quiet hours suppress non-urgent alerts **22:00–07:00**, but urgent still notifies

**Source docs:** `docs/faq/notifications.md`

**Why it matters:** Ambiguous intake question.

---

### Q39. What priority values are accepted when creating a ticket via API?

**Expected answer**

`low`, `medium`, `high`, and `urgent`.

**Source docs:** `docs/api/tickets-api.md`

**Why it matters:** Exact enum lookup.

---

### Q40. What scope is required to reopen a closed ticket?

**Expected answer**

`write:tickets:reopen`

**Source docs:** `docs/api/tickets-api.md`

**Why it matters:** Scope/permission detail.

---

### Q41. Do contractors on vendor-lite have authenticator-app MFA?

**Expected answer**

**No.** Contractors on the `vendor-lite` plan use **email OTP only** and do not have authenticator-app MFA.

**Source docs:** `docs/policies/mfa-policy.md`

**Why it matters:** Exception case in MFA policy.

---

### Q42. What does AUTH-4010 mean?

**Expected answer**

**AUTH-4010** means the API token is missing, expired, or revoked. Generate a new token under **Developer Settings → API Tokens**. Tokens created before **2025-01-01** are no longer accepted.

**Source docs:** `docs/troubleshooting/auth-errors.md`

**Why it matters:** Error-code lookup.

---

### Q43. What does AUTH-4400 mean and what should I check?

**Expected answer**

**AUTH-4400** means the SAML assertion failed validation. Check clock skew, certificate expiry, and that `NameID` format is `emailAddress`.

**Source docs:** `docs/troubleshooting/auth-errors.md`, `docs/onboarding/sso-setup.md`

**Why it matters:** Error code + SSO config.

---

# 9. Quick answer cheat sheet

| # | Question (short) | Key answer |
| --- | --- | --- |
| 1 | Password reset | Forgot password; link expires in **30 min** |
| 2 | Billing grace period | **7 days** |
| 3 | Standard API rate limit | **120 req/min** |
| 4 | Urgent first response | **15 minutes** |
| 5 | Email MFA backup codes? | **No** — video call only |
| 6 | AUTH-4291 | 5 MFA fails / 15 min → lock **30 min**; clear lockout |
| 7 | BILL-4020 | Declined card |
| 8 | SYNC-2201 | 60s timeout; batch size **100** |
| 9 | API-4290 | Rate limit exceeded |
| 10 | Reset MFA | Verify ID → Reset MFA → enroll in **2 hours** |
| 11 | SSO NameID | `emailAddress` |
| 12 | SSO-only password reset | Use identity provider, not product form |
| 13 | Retention | Chat **24 mo**, audit **36 mo** |
| 14 | AUTH-4291 + working authenticator | **Clear lockout**, not full reset |
| 15 | JIT role + VPN | Role `member`; VPN **not** default |
| 16 | Create ticket API | `POST /v1/tickets`; statuses open/pending/solved/closed |
| 17 | AUTH-4291 after Apr 2026 | Prefer clear lockout (new) |
| 18 | Token rotation overlap | **1 hour** (new), not immediate kill |
| 19 | Pet vacation policy | **No answer** |
| 20 | Payroll tax forms | **No answer** |
| 21 | Seat refund policy | **No answer** |
| 22 | Login problems | Branching / ask for details |
| 23 | Can’t access account | Branching / ask for details |
| 24 | HOOK-5001 | Endpoint unreachable; needs 2xx in 10s |
| 25 | HOOK-5008 | Invalid signature / signing secret |
| 26 | Webhook retries | **5** times, then `dead` |
| 27 | Register webhook | `POST /v1/webhooks` |
| 28 | Replay dead webhook | `POST /v1/webhooks/events/{id}/replay` |
| 29 | MFA reset role | **`admin`** |
| 30 | team_lead | Assign tickets + team analytics |
| 31 | Offboarding revoke | Within **1 hour** |
| 32 | Data handoff window | **30 days** |
| 33 | Security email from | `noreply@example.com` |
| 34 | Quiet hours vs urgent | Urgent **always** notifies |
| 35 | SMS password reset | **Removed** (Apr 2026) |
| 36 | Gift card policy | **No answer** |
| 37 | YubiKey shipping | **No answer** |
| 38 | Notifications broken | Branch email / Slack / quiet hours |
| 39 | Ticket priorities | low/medium/high/urgent |
| 40 | Reopen closed ticket scope | `write:tickets:reopen` |
| 41 | vendor-lite MFA | Email OTP only |
| 42 | AUTH-4010 | Invalid/missing/revoked API token |
| 43 | AUTH-4400 | SAML assertion failed |

---

# 10. 2–3 minute live walkthrough

1. **Ingest:** `python ingest.py --source docs/ --rebuild`
2. **Good cited answer:** Q6 (`AUTH-4291`)
3. **Newer-doc preference:** Q17 or Q18
4. **No-answer:** Q19 (pets)
5. **Dashboard:** show retrieved chunks, citation verdicts, confidence; optionally enable **Compare hybrid vs dense**

---

# 11. Eval commands (for portfolio numbers)

```bash
python eval.py --strategy dense --no-rerank
python eval.py --strategy hybrid
```

Reports:

- `reports/eval_dense.md`
- `reports/eval_hybrid.md`

Case-study line to fill after running eval:

> Hybrid retrieval improved correct-source retrieval from **X%** to **Y%** on an **N**-question eval set. Citation support rate was **Z%**, with refusal accuracy **R%** on no-answer items.
