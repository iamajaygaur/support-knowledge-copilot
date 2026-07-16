---
source_name: API Authentication
title: API Authentication
last_updated: 2026-04-18
access_level: public
---

# API Authentication

## API tokens

Authenticate requests with the header:

```http
Authorization: Bearer <api_token>
```

Tokens are scoped. A token with scope `read:tickets` cannot mutate ticket state.

## Rate limits

Standard plans are limited to **120 requests/minute**. Enterprise plans are limited to **600 requests/minute**. Exceeding the limit returns HTTP **429** with error code **API-4290**.

## Rotating tokens

Rotate tokens from **Developer Settings → API Tokens → Rotate**. The previous token remains valid for a **1-hour** overlap window.
