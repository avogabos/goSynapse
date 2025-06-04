# Architecture Overview

The original repository contained a Go client library under `client/` with the
following files:

- `auth.go` – authentication helpers
- `axon.go` – axon file operations
- `base.go` – `SynapseClient` type
- `cortex.go` – cortex query helpers
- `parse.go` – JSON parsing helpers
- `types.go` – data structures

Dependencies included the Go standard library only. No tests were provided.

The Python rewrite exposes the same functionality under `gosynapse` using a
single `SynapseClient` class. Data structures are implemented with dataclasses
and HTTP interactions are performed with the `requests` library.
