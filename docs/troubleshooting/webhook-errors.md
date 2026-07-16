---
source_name: Webhook Error Codes
title: Webhook Error Codes
last_updated: 2026-04-05
access_level: internal
---

# Webhook Error Codes

## HOOK-5001 — Endpoint unreachable

The customer webhook URL did not accept connections. Verify the URL is publicly reachable and returns HTTP **2xx** within **10 seconds**.

## HOOK-5008 — Invalid signature

The receiver rejected the request signature. Confirm the customer is using the current signing secret from **Settings → Developers → Webhooks**. Secrets rotated in the last hour may still use the previous secret during the overlap window.

## Retry policy

Failed deliveries retry up to **5 times** with exponential backoff. After the final failure, the event is marked `dead` and must be replayed manually.
