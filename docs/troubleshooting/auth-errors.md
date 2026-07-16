---
source_name: Authentication Error Codes
title: Authentication Error Codes
last_updated: 2026-04-10
access_level: internal
---

# Authentication Error Codes

## AUTH-4291 — Too many MFA attempts

**AUTH-4291** is returned when a user exceeds **5 MFA attempts** within 15 minutes. The account is soft-locked for MFA for **30 minutes**.

### Resolution

1. Wait for the lockout window to expire, or
2. An admin can clear the lock from **Admin Console → Users → Security → Clear MFA lockout**.
3. Advise the user to use a backup code if available.

## AUTH-4010 — Invalid API token

The API token is missing, expired, or revoked. Generate a new token under **Developer Settings → API Tokens**. Tokens created before **2025-01-01** are no longer accepted.

## AUTH-4400 — SSO assertion failed

The SAML assertion could not be validated. Check clock skew, certificate expiry, and whether the `NameID` format matches the configured value (`emailAddress`).
