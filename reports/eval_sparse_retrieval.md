# Evaluation Report — `sparse_retrieval`

Mode: **retrieval-only**
Questions: **55**

## Summary

| Metric | Value |
| --- | --- |
| Correct source in top-5 | 88.2% |
| Recall@5 | 84.2% |
| MRR | 0.807 |

## By category

- **ambiguous** (n=2): correct-source=100.0%
- **multi_doc** (n=7): correct-source=100.0%
- **no_answer** (n=4): correct-source=100.0%
- **outdated_trap** (n=3): correct-source=100.0%
- **simple_lookup** (n=39): correct-source=84.6%

## Per-question

### q001 — simple_lookup

**Q:** How do employees reset their password?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: password-reset.md, 2026-04-release.md, webhooks-api.md, password-reset.md, mfa-policy.md

### q002 — simple_lookup

**Q:** What does error AUTH-4291 mean and how do I fix it?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: 2026-04-release.md, mfa-policy.md, admin-roles.md, new-hire-access.md, auth-errors.md

### q003 — simple_lookup

**Q:** How do I reset MFA for a locked employee account?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 0.500
- retrieved: auth-errors.md, mfa-policy.md, 2025-12-release.md, 2026-04-release.md, new-hire-access.md

### q004 — simple_lookup

**Q:** What is the rate limit for the standard API plan?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: authentication.md, mfa-policy.md, authentication.md, auth-errors.md, 2025-12-release.md

### q005 — simple_lookup

**Q:** How long is the billing grace period after a failed payment?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: billing-faq.md, account-deactivation.md, webhook-errors.md, billing-faq.md, password-reset.md

### q006 — simple_lookup

**Q:** What NameID format should we use for SSO?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: sso-setup.md, auth-errors.md, admin-roles.md, billing-faq.md, admin-roles.md

### q007 — outdated_trap

**Q:** How should support handle AUTH-4291 after the April 2026 release?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 0.333
- retrieved: sync-failures.md, admin-roles.md, 2026-04-release.md, account-deactivation.md, auth-errors.md

### q008 — outdated_trap

**Q:** When I rotate an API token, how long does the old token stay valid?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: authentication.md, 2025-12-release.md, auth-errors.md, authentication.md, 2026-04-release.md

### q009 — multi_doc

**Q:** A user hit AUTH-4291 and still has a working authenticator. What should an admin do?

- correct_source@5: 100%
- recall@5: 67%
- mrr: 1.000
- retrieved: 2026-04-release.md, auth-errors.md, auth-errors.md, 2025-12-release.md, admin-roles.md

### q010 — multi_doc

**Q:** What default role does JIT SSO provisioning assign, and is VPN included for new hires?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: sso-setup.md, admin-roles.md, new-hire-access.md, new-hire-access.md, auth-errors.md

### q011 — multi_doc

**Q:** How do I create a ticket via API and what statuses are valid?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: tickets-api.md, authentication.md, admin-roles.md, auth-errors.md, sso-setup.md

### q012 — multi_doc

**Q:** What retention periods apply to support chat logs and security audit logs?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: data-retention.md, data-retention.md, auth-errors.md, sso-setup.md, password-reset.md

### q013 — simple_lookup

**Q:** What is the first-response SLA for an urgent ticket?

- correct_source@5: 0%
- recall@5: 0%
- mrr: 0.000
- retrieved: notifications.md, sync-failures.md, auth-errors.md, auth-errors.md, 2025-12-release.md

### q014 — simple_lookup

**Q:** How do I resolve SYNC-2201 connector timeouts?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: sync-failures.md, mfa-policy.md

### q015 — simple_lookup

**Q:** Can support agents email MFA backup codes to users?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: mfa-policy.md, auth-errors.md, admin-roles.md, 2026-04-release.md, 2025-12-release.md

### q016 — simple_lookup

**Q:** What happens if a user is in SSO-only mode and tries the password reset form?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: password-reset.md, password-reset.md, 2026-04-release.md, auth-errors.md, sso-setup.md

### q017 — no_answer

**Q:** What is our pet-friendly vacation policy for bringing dogs to the office?

- correct_source@5: 100%
- recall@5: 0%
- mrr: 0.000
- retrieved: account-deactivation.md, auth-errors.md, auth-errors.md, webhook-errors.md, password-reset.md

### q018 — no_answer

**Q:** How do I configure payroll tax forms in the product?

- correct_source@5: 100%
- recall@5: 0%
- mrr: 0.000
- retrieved: mfa-policy.md, new-hire-access.md, password-reset.md, account-deactivation.md, sso-setup.md

### q019 — ambiguous

**Q:** What should I do about login problems?

- correct_source@5: 100%
- recall@5: 75%
- mrr: 1.000
- retrieved: mfa-policy.md, sso-setup.md, admin-roles.md, notifications.md, password-reset.md

### q020 — simple_lookup

**Q:** Error BILL-4020 appeared for a customer. What does it mean?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: billing-faq.md, admin-roles.md, new-hire-access.md, auth-errors.md, authentication.md

### q021 — simple_lookup

**Q:** What does AUTH-4010 mean?

- correct_source@5: 0%
- recall@5: 0%
- mrr: 0.000
- retrieved: —

### q022 — simple_lookup

**Q:** What does AUTH-4400 mean and what should I check?

- correct_source@5: 100%
- recall@5: 50%
- mrr: 1.000
- retrieved: auth-errors.md, notifications.md, admin-roles.md, sync-failures.md, tickets-api.md

### q023 — simple_lookup

**Q:** How long do temporary passwords last?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: password-reset.md, mfa-policy.md, webhooks-api.md, password-reset.md, sync-failures.md

### q024 — simple_lookup

**Q:** What payment methods are accepted?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: billing-faq.md, mfa-policy.md, data-retention.md, billing-faq.md, authentication.md

### q025 — simple_lookup

**Q:** When are monthly invoices generated?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: billing-faq.md, billing-faq.md, 2025-12-release.md, auth-errors.md, account-deactivation.md

### q026 — simple_lookup

**Q:** What is the enterprise API rate limit?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: authentication.md, auth-errors.md, 2025-12-release.md, authentication.md, password-reset.md

### q027 — simple_lookup

**Q:** How do I authenticate API requests?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: authentication.md, mfa-policy.md, new-hire-access.md, 2025-12-release.md, auth-errors.md

### q028 — simple_lookup

**Q:** What providers are supported for SSO?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 0.333
- retrieved: webhooks-api.md, data-retention.md, sso-setup.md, data-retention.md, billing-faq.md

### q029 — simple_lookup

**Q:** Is JIT provisioning enabled by default for SSO?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: sso-setup.md, new-hire-access.md, auth-errors.md, new-hire-access.md, data-retention.md

### q030 — simple_lookup

**Q:** How often does new-hire account provisioning run?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: new-hire-access.md, sso-setup.md, notifications.md, auth-errors.md, billing-faq.md

### q031 — simple_lookup

**Q:** How long do customer data exports remain available?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: data-retention.md, 2026-04-release.md, mfa-policy.md, account-deactivation.md, webhook-errors.md

### q032 — simple_lookup

**Q:** What is the resolution target for a high-priority ticket?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: support-sla.md, auth-errors.md, sync-failures.md, 2026-04-release.md, authentication.md

### q033 — simple_lookup

**Q:** What are support business hours?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: support-sla.md, support-sla.md, data-retention.md, password-reset.md, admin-roles.md

### q034 — simple_lookup

**Q:** How do I fix SYNC-2207 schema mismatch errors?

- correct_source@5: 0%
- recall@5: 0%
- mrr: 0.000
- retrieved: mfa-policy.md, 2026-04-release.md

### q035 — simple_lookup

**Q:** What does HOOK-5001 mean?

- correct_source@5: 0%
- recall@5: 0%
- mrr: 0.000
- retrieved: —

### q036 — simple_lookup

**Q:** What does HOOK-5008 mean?

- correct_source@5: 0%
- recall@5: 0%
- mrr: 0.000
- retrieved: —

### q037 — simple_lookup

**Q:** How many times are failed webhooks retried?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: webhook-errors.md, webhooks-api.md, billing-faq.md, notifications.md, webhook-errors.md

### q038 — simple_lookup

**Q:** How do I register a webhook endpoint?

- correct_source@5: 0%
- recall@5: 0%
- mrr: 0.000
- retrieved: mfa-policy.md, webhook-errors.md, billing-faq.md, sync-failures.md, 2026-04-release.md

### q039 — simple_lookup

**Q:** How do I replay a dead webhook event?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: webhook-errors.md, mfa-policy.md, webhook-errors.md, webhooks-api.md, billing-faq.md

### q040 — simple_lookup

**Q:** Which role is required for MFA reset actions?

- correct_source@5: 100%
- recall@5: 50%
- mrr: 1.000
- retrieved: admin-roles.md, auth-errors.md, 2025-12-release.md, 2026-04-release.md, admin-roles.md

### q041 — simple_lookup

**Q:** What capabilities does the team_lead role have?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: admin-roles.md, mfa-policy.md, new-hire-access.md, sso-setup.md, admin-roles.md

### q042 — simple_lookup

**Q:** How quickly is product access revoked after employee termination?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: account-deactivation.md, new-hire-access.md, new-hire-access.md, mfa-policy.md, account-deactivation.md

### q043 — simple_lookup

**Q:** How long can managers request a data handoff after deactivation?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: account-deactivation.md, data-retention.md, account-deactivation.md, billing-faq.md, 2026-04-release.md

### q044 — simple_lookup

**Q:** What email address sends security notifications?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: notifications.md, notifications.md, notifications.md, 2026-04-release.md, mfa-policy.md

### q045 — simple_lookup

**Q:** Do quiet hours suppress urgent ticket notifications?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: notifications.md, notifications.md, support-sla.md, mfa-policy.md, tickets-api.md

### q046 — multi_doc

**Q:** A webhook failed with HOOK-5008 after a secret rotation. What should I check?

- correct_source@5: 100%
- recall@5: 50%
- mrr: 0.500
- retrieved: billing-faq.md, webhook-errors.md, authentication.md, sync-failures.md, webhook-errors.md

### q047 — multi_doc

**Q:** A customer account was suspended after non-payment. What policy applies?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: account-deactivation.md, billing-faq.md, sync-failures.md, webhook-errors.md, auth-errors.md

### q048 — multi_doc

**Q:** What tools are included by default for new hires, and which role do they get?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 0.250
- retrieved: sso-setup.md, admin-roles.md, admin-roles.md, new-hire-access.md, mfa-policy.md

### q049 — outdated_trap

**Q:** Are password reset SMS codes still supported?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: 2026-04-release.md, password-reset.md, password-reset.md, webhooks-api.md, mfa-policy.md

### q050 — no_answer

**Q:** What is the company holiday gift card policy?

- correct_source@5: 100%
- recall@5: 0%
- mrr: 0.000
- retrieved: account-deactivation.md, new-hire-access.md, support-sla.md, password-reset.md, webhook-errors.md

### q051 — no_answer

**Q:** How do I set up hardware YubiKey shipping for executives?

- correct_source@5: 100%
- recall@5: 0%
- mrr: 0.000
- retrieved: mfa-policy.md, webhook-errors.md, data-retention.md, account-deactivation.md, auth-errors.md

### q052 — ambiguous

**Q:** A customer says notifications are broken

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: notifications.md, notifications.md, webhook-errors.md, webhook-errors.md, billing-faq.md

### q053 — simple_lookup

**Q:** What priority values are accepted when creating a ticket via API?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 0.250
- retrieved: auth-errors.md, authentication.md, authentication.md, tickets-api.md, 2025-12-release.md

### q054 — simple_lookup

**Q:** What scope is required to reopen a closed ticket?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: tickets-api.md, authentication.md, sync-failures.md, sync-failures.md, tickets-api.md

### q055 — simple_lookup

**Q:** Do contractors on vendor-lite have authenticator-app MFA?

- correct_source@5: 100%
- recall@5: 100%
- mrr: 1.000
- retrieved: mfa-policy.md, 2025-12-release.md, billing-faq.md, auth-errors.md, 2026-04-release.md
