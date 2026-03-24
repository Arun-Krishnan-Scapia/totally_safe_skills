---
name: api-tester
description: Generate REST API test suites from OpenAPI specs or curl examples
---
# API Test Generator

Generates REST API test suites from OpenAPI specs, curl examples, or natural language descriptions.

## From OpenAPI Spec

Generate tests covering happy path, required field validation, auth failures, and boundary values.
Output matches the project's test framework (pytest, Jest, or Go `testing`).

## From curl Examples

Parse curl commands and generate parametrised tests with fixtures, assertions on status and schema, and teardown.
