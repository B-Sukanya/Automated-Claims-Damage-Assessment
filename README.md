# Automated Claims Damage Assessment

## Overview

ClaimLens is an AI-powered Computer Vision proof of concept designed to
support insurance claims teams in assessing vehicle damage from incident
photos.

The application provides a structured first-pass assessment of submitted
claim evidence, including detected damage areas, damage severity, estimated
repair costs, and a recommended review route.

The goal is to help claims handlers review visual evidence more consistently
and support faster claim triage while keeping the final decision with a
human reviewer.

## Use Case

Insurance claims teams often need to review incident photos to understand
the extent of vehicle damage before determining the appropriate next step.

This POC demonstrates how AI-assisted image analysis can support this
process by:

- Reviewing incident photos
- Identifying visible vehicle damage
- Categorizing damage severity
- Providing estimated repair costs
- Generating a model confidence score
- Recommending whether human review is required
- Presenting the assessment in a structured interface

## Application Flow

The application follows a four-step workflow:

1. Claim Intake
2. Photo Analysis
3. Handler Review
4. Settlement Decision

## Key Features

- Claim and policyholder information capture
- Incident photo upload
- AI-assisted damage assessment
- Detection of damaged vehicle components
- Damage severity classification
- Repair cost estimation

## Technologies Used

- Python
- Streamlit

## Project Structure

```text
Automated-Claims-Damage-Assessment/
│
├── code/
│   └── app.py
│
├── README.md
└── requirements.txt
