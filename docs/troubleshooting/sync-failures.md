---
source_name: Sync Failure Guide
title: Sync Failure Guide
last_updated: 2026-01-20
access_level: internal
---

# Sync Failure Guide

## SYNC-2201 — Connector timeout

The external connector did not respond within **60 seconds**. Retry the job from **Integrations → Sync Jobs**. If timeouts persist, reduce batch size to **100 records**.

## SYNC-2207 — Schema mismatch

A required field was removed upstream. Open the field mapping editor and either map a replacement field or mark the field optional.

## Partial syncs

Partial syncs leave a warning badge on the integration card. Support should not mark the ticket resolved until the last successful sync timestamp is newer than the incident start time.
