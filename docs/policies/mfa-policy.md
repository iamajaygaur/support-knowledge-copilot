---
source_name: MFA Policy
title: MFA Policy
last_updated: 2026-05-01
access_level: internal
---

# MFA Policy

## Reset procedure for locked accounts

When an employee is locked out of MFA, support must verify identity using the **HR employee ID** and a manager confirmation in Slack `#identity-verify`.

After verification:

1. Open **Admin Console → Users → Security**.
2. Select **Reset MFA**.
3. Choose **Invalidate all MFA methods**.
4. Send the user the enrollment link. Enrollment must be completed within **2 hours**.

Support agents must not share backup codes over email. Backup codes may only be revealed in a verified video call.

## Exceptions

Contractors on the `vendor-lite` plan use email OTP only and do not have authenticator-app MFA.
