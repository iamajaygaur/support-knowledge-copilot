---
source_name: Webhooks API
title: Webhooks API
last_updated: 2026-04-05
access_level: public
---

# Webhooks API

## Register an endpoint

`POST /v1/webhooks`

Required fields: `url`, `events` (array), `secret`.

Supported events include `ticket.created`, `ticket.updated`, and `sync.failed`.

## List endpoints

`GET /v1/webhooks`

Returns configured endpoints and their last delivery status.

## Replay a failed event

`POST /v1/webhooks/events/{event_id}/replay`

Only events in `dead` status can be replayed. Requires scope `write:webhooks`.
