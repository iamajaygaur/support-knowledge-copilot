# Evaluation Report — `hybrid`

Mode: **full (answer + citations)**
Questions: **12**

## Summary

| Metric | Value |
| --- | --- |
| Correct source in top-5 | 100.0% |
| Recall@5 | 100.0% |
| MRR | 0.958 |
| Citation support rate | 91.7% |
| Refusal accuracy | 100.0% |
| Avg confidence | 0.624 |

## By category

- **multi_doc** (n=4): correct-source=100.0%, citation-support=75.0%, refusal=100.0%
- **outdated_trap** (n=2): correct-source=100.0%, citation-support=100.0%, refusal=100.0%
- **simple_lookup** (n=6): correct-source=100.0%, citation-support=100.0%, refusal=100.0%

## Per-question

### q001 — simple_lookup

**Q:** How do employees reset their password?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.661
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: password-reset.md, password-reset.md, 2026-04-release.md, password-reset.md, mfa-policy.md

<details><summary>Answer</summary>

Employees can reset their password by selecting **Forgot password** on the login page, which sends a reset link to their verified work email that expires in 30 minutes [password-reset-000-d9118a913f]. Legacy SMS reset codes are no longer supported [2026-04-release-002-8533c4ecab]. 

If the employee has an SSO-only account, they must reset their credentials through their identity provider rather than the product password form [password-reset-002-bc7761df38].

Alternatively, support agents can assist by issuing a temporary password from the Admin Console under **Users → Security → Issue temporary password**. This temporary password expires after 24 hours and requires the employee to change it upon their first login [password-reset-001-f207053e35].

</details>

### q002 — simple_lookup

**Q:** What does error AUTH-4291 mean and how do I fix it?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.661
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: 2026-04-release.md, auth-errors.md, authentication.md, billing-faq.md, mfa-policy.md

<details><summary>Answer</summary>

Error **AUTH-4291** means that a user has exceeded 5 MFA attempts within 15 minutes, resulting in the account being soft-locked for MFA for 30 minutes [auth-errors-000-841ff75cfc].

To fix this:
* Admins can clear the MFA lockout without performing a full MFA reset. This is the preferred fix if the user still has a working authenticator [2026-04-release-000-2373536d32].

</details>

### q003 — simple_lookup

**Q:** How do I reset MFA for a locked employee account?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.661
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: mfa-policy.md, 2025-12-release.md, auth-errors.md, 2026-04-release.md, auth-errors.md

<details><summary>Answer</summary>

To reset MFA for a locked employee account, follow these steps:

1. **Verify Identity**: Verify the employee's identity using their **HR employee ID** and a manager confirmation in the Slack channel `#identity-verify` [mfa-policy-000-d706899942].
2. **Access Security Settings**: Open **Admin Console → Users → Security** [mfa-policy-000-d706899942].
3. **Initiate Reset**: Select **Reset MFA** [mfa-policy-000-d706899942].
4. **Invalidate Methods**: Choose **Invalidate all MFA methods** [mfa-policy-000-d706899942].
5. **Send Enrollment Link**: Send the user the enrollment link. The user must complete enrollment within **2 hours** [mfa-policy-000-d706899942].

*Alternative (for AUTH-4291 lockouts)*: If the user is locked out due to exceeding 5 attempts but still has a working authenticator, you can clear the lockout without a full reset by navigating to **Admin Console → Users → Security → Clear MFA lockout** [2026-04-release-000-2373536d32, auth-errors-001-bda04c0881].

*Security Note*: Do not share backup codes over email. They may only be revealed in a verified video call [mfa-policy-000-d706899942].

</details>

### q004 — simple_lookup

**Q:** What is the rate limit for the standard API plan?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.661
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: authentication.md, auth-errors.md, mfa-policy.md, billing-faq.md, webhook-errors.md

<details><summary>Answer</summary>

The rate limit for the standard API plan is **120 requests/minute** [authentication-001-038c099794].

</details>

### q005 — simple_lookup

**Q:** How long is the billing grace period after a failed payment?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.610
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: billing-faq.md, account-deactivation.md, billing-faq.md, webhook-errors.md, auth-errors.md

<details><summary>Answer</summary>

After a failed payment, the account enters a 7-day grace period [billing-faq-002-8070e4d60d, account-deactivation-001-325ac7295f]. On day 8, paid features are limited [billing-faq-002-8070e4d60d].

</details>

### q006 — simple_lookup

**Q:** What NameID format should we use for SSO?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.661
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: sso-setup.md, auth-errors.md, admin-roles.md, sso-setup.md, mfa-policy.md

<details><summary>Answer</summary>

You should set the `NameID` format to `emailAddress` [sso-setup-000-7ca9cb7ca0] [auth-errors-003-3067eab467].

</details>

### q007 — outdated_trap

**Q:** How should support handle AUTH-4291 after the April 2026 release?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.609
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: 2026-04-release.md, auth-errors.md, admin-roles.md, mfa-policy.md, password-reset.md

<details><summary>Answer</summary>

Following the April 2026 release, the preferred fix for AUTH-4291 is for admins to clear the MFA lockout without performing a full MFA reset, provided the user still has a working authenticator [2026-04-release-000-2373536d32]. AUTH-4291 occurs when a user exceeds 5 MFA attempts within 15 minutes, resulting in a 30-minute soft-lock [auth-errors-000-841ff75cfc]. If a full MFA reset is required, support must verify the user's identity via HR employee ID and manager confirmation in Slack before proceeding with the reset procedure in the Admin Console [mfa-policy-000-d706899942].

</details>

### q008 — outdated_trap

**Q:** When I rotate an API token, how long does the old token stay valid?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.661
- no_answer: False
- recall@5: 100%
- mrr: 0.500
- retrieved: 2025-12-release.md, authentication.md, 2026-04-release.md, auth-errors.md, authentication.md

<details><summary>Answer</summary>

When you rotate an API token, the old token remains valid for a 1-hour overlap window [authentication-002-556b660e68], [2026-04-release-001-28728374f5].

</details>

### q009 — multi_doc

**Q:** A user hit AUTH-4291 and still has a working authenticator. What should an admin do?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.661
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: 2026-04-release.md, auth-errors.md, auth-errors.md, 2025-12-release.md, mfa-policy.md

<details><summary>Answer</summary>

Admins should clear the MFA lockout without performing a full MFA reset [2026-04-release-000-2373536d32]. This can be done by navigating to **Admin Console → Users → Security → Clear MFA lockout** [auth-errors-001-bda04c0881].

</details>

### q010 — multi_doc

**Q:** What default role does JIT SSO provisioning assign, and is VPN included for new hires?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.661
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: sso-setup.md, new-hire-access.md, new-hire-access.md, sso-setup.md, admin-roles.md

<details><summary>Answer</summary>

JIT SSO provisioning assigns the default role of `member` [sso-setup-001-f23963b19b]. VPN access is not included for new hires by default and must be requested separately with business justification [new-hire-access-002-ec5d4cf858].

</details>

### q011 — multi_doc

**Q:** How do I create a ticket via API and what statuses are valid?

- correct_source@5: 100%
- citation_support: 100%
- refusal_ok: 100%
- confidence: 0.579
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: tickets-api.md, admin-roles.md, auth-errors.md, tickets-api.md, authentication.md

<details><summary>Answer</summary>

To create a ticket via the API, you must authenticate your request using an `Authorization: Bearer <api_token>` header [authentication-000-2ad4b3a8b8]. Valid statuses for tickets are `open`, `pending`, `solved`, and `closed` [tickets-api-002-bbf87f583d].

</details>

### q012 — multi_doc

**Q:** What retention periods apply to support chat logs and security audit logs?

- correct_source@5: 100%
- citation_support: 0%
- refusal_ok: 100%
- confidence: 0.404
- no_answer: False
- recall@5: 100%
- mrr: 1.000
- retrieved: data-retention.md, data-retention.md, password-reset.md, mfa-policy.md, support-sla.md

<details><summary>Answer</summary>

* Support chat logs (transcripts) are retained for **24 months** [data-retention-000-f725558448].
* Security audit logs are retained for **36 months** [data-retention-001-9b1efa1ad3].

</details>
