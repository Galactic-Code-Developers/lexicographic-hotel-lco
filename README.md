# Lexicographic Constraint Optimization in Hotel Management  
_A Static and Dynamic Tiered Optimization Framework with Colab Procedures_

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Pyomo](https://img.shields.io/badge/optimize-Pyomo-orange.svg)](http://www.pyomo.org/)
[![Colab](https://img.shields.io/badge/run%20in-Colab-yellow.svg)](<COLAB_NOTEBOOK_URL>)

This repository contains the reference implementation and reproducible
simulation workflow for **Lexicographic Constraint Optimization (LCO)**
applied to hotel management.  
The codebase supports:

- **Static 2-tier LCO**:
  - Tier \(\mathcal{L}_2\): revenue maximization
  - Tier \(\mathcal{L}_3\): expected overbooking slack minimization
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
├── tex/
│   ├── Lexicographic_Constraint_Optimization_in_Hotel_Management_v1_4_8.tex
│   └── LCO_Colab_Procedures.tex     # Standalone "how to run in Colab" paper
│
└── data/
    └── synthetic_booking_scenarios.csv  # Optional synthetic datasets
