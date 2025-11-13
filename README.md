# Lexicographic Constraint Optimization in Hotel Management  
_A Static and Dynamic Tiered Optimization Framework with Colab Procedures_

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Docs: CC BY 4.0](https://img.shields.io/badge/Docs-CC--BY%204.0-orange.svg)
![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)
![Pyomo](https://img.shields.io/badge/Modeling-Pyomo-green)
![HiGHS](https://img.shields.io/badge/Solver-HiGHS-purple)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
[![Colab](https://img.shields.io/badge/run%20in-Colab-yellow.svg)](<COLAB_NOTEBOOK_URL>)

This repository contains the reference implementation and reproducible
simulation workflow for **Lexicographic Constraint Optimization (LCO)**
applied to hotel management.  
The codebase supports:

- **Static 2-tier LCO**:
  - Tier $\mathcal{L}_2$: revenue maximization
  - Tier $\mathcal{L}_3$: expected overbooking slack minimization
- A **lexicographic floor mechanism** enforcing strict precedence between tiers
- A complete **Google Colab procedure** documented in a standalone TeX paper
- A code structure that is compatible with future **CMDP / RL extensions**

The mathematical core matches the model in:

> Valamontes, A. (2025).  
> *Lexicographic Constraint Optimization in Hotel Management: Dynamic Online Control, RL Adaptation, and Multi-Property Integration.*  
> Kapodistrian Academy of Science.

---

## Repository Structure

```text
lexicographic-hotel-lco/
├── README.md                   # This file
├── LICENSE                     # MIT license
├── requirements.txt            # Dependencies for local runs
├── pyproject.toml              # Optional packaging metadata
├── .gitignore
│
├── src/
│   └── lco_hotel/
│       ├── __init__.py
│       ├── static_lco_model.py      # Pyomo-based static 2-tier model
│       └── dynamic_lco_model.py     # (optional) CMDP / RL extensions
│
├── notebooks/
│   ├── LCO_Colab_Procedures.ipynb   # Full step-by-step Colab workflow
│   └── LCO_Static_2Tier_Demo.ipynb  # Minimal 10×5 synthetic instance
│
├── pdf/
│   ├── Lexicographic_Constraint_Optimization_in_Hotel_Management_v1_6.pdf
│   └── LCO_Colab_Procedures.pdf     # Standalone "how to run in Colab" paper
│
└── data/
    └── synthetic_booking_scenarios.csv  # Optional synthetic datasets
