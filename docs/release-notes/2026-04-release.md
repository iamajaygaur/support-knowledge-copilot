---
source_name: April 2026 Release Notes
title: April 2026 Release Notes
last_updated: 2026-04-30
access_level: public
---

# April 2026 Release Notes

## MFA lockout controls

Admins can now clear MFA lockouts without a full MFA reset. This is the preferred fix for **AUTH-4291** when the user still has a working authenticator.

## API token overlap window

Token rotation now includes a **1-hour** overlap window. Older documentation that mentioned immediate invalidation is outdated.

## Deprecated

Legacy password reset SMS codes are removed. Email reset links remain supported.
