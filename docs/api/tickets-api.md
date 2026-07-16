---
source_name: Tickets API
title: Tickets API
last_updated: 2026-03-28
access_level: public
---

# Tickets API

## Create a ticket

`POST /v1/tickets`

Required fields: `subject`, `body`, `priority` (`low|medium|high|urgent`).

## Get a ticket

`GET /v1/tickets/{ticket_id}`

Returns ticket metadata, requester, assignee, and status.

## Status values

Valid statuses are `open`, `pending`, `solved`, and `closed`. Transitioning from `closed` back to `open` requires scope `write:tickets:reopen`.
