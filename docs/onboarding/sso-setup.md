---
source_name: SSO Setup Guide
title: SSO Setup Guide
last_updated: 2026-04-02
access_level: internal
---

# SSO Setup Guide

## Supported providers

We support Okta, Azure AD, and Google Workspace via SAML 2.0.

## Configuration steps

1. In the product, open **Settings → Security → SSO**.
2. Download the service provider metadata.
3. Create a SAML app in the identity provider.
4. Upload the IdP certificate and SSO URL.
5. Set `NameID` format to `emailAddress`.
6. Enable **SSO-only** only after a successful test login.

## Just-in-time provisioning

JIT provisioning is enabled by default. Users are created on first successful SSO login with the default role `member`.
