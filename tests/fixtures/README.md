<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Schema fixtures

`plugin-1.0.0.schema.json` is an unmodified copy of the
[Agent Plugins 1.0.0 manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json),
retrieved on 2026-10-07. Keep this versioned fixture local so unit tests remain
offline. When changing the manifest schema version, update this fixture and
validate the migration against the target clients.
