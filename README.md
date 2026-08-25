# Lab 1: Requirements Engineering & UML Use-Case Modelling

**Problem Statement #03 — Campus Placement & Internship Pipeline**

## Overview

The campus placement cell manages hundreds of corporate drives with varying eligibility criteria. This lab elicits requirements for a platform that parses student resumes, applies multi-tier CGPA and backlog filters, manages multi-round interview queues, and processes offer letters — then models that behavior as a UML use-case diagram and a detailed use-case flow.

**Actors:** Student Applicant, Placement Officer, Company / Recruiter System

## Repository Contents

| File | Description |
| --- | --- |
| `Requirements_Table.docx` | 5 Functional Requirements (FR-001–FR-005) and 2 Non-Functional Requirements (NFR-001–NFR-002), each with Req ID, Type, Description, Priority, Acceptance Criteria, and Rationale. |
| `UseCase_Diagram.pdf` | UML use-case diagram showing all actors, 8 use cases, and `<<include>>` / `<<extend>>` relationships. |
| `UseCase_Flow.docx` | One-page use-case flow specification for UC-02 (Register for Placement Drive), including preconditions, postconditions, main success scenario, and an alternate flow. |

## Use-Case Diagram Summary

- **UC-01** Upload Resume
- **UC-02** Register for Placement Drive
- **UC-03** Parse Resume & Extract Skills
- **UC-04** Apply Eligibility Filter (CGPA/Backlog)
- **UC-05** Schedule Interview Round
- **UC-06** Record Interview Result
- **UC-07** Generate Offer Letter
- **UC-08** View Placement Status

**Relationships:**
- UC-02 `<<include>>` UC-03 — registration always triggers resume parsing.
- UC-02 `<<include>>` UC-04 — registration always triggers the eligibility check.
- UC-07 `<<extend>>` UC-06 — an offer letter is optionally generated when an interview result is marked "Selected."

## Tools Used

- Diagramming: draw.io / Lucidchart-style UML notation
- Documentation: Microsoft Word (.docx)

## Author

*Add your name and roll number here.*
