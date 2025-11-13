# Lexicographic Constraint Optimization (LCO) — Notebook Repository

This repository contains the complete computational framework for running **Lexicographic Constraint Optimization (LCO)** experiments, including static tiered optimization, dynamic revenue-floor enforcement, and reproducible workflows in Google Colab and local Python environments.

The notebooks implement the exact procedures used in the accompanying LCO research papers by **Antonios Valamontes, Kapodistrian Academy of Science**.

---

## 📘 Notebooks

| Notebook | Description |
|----------|-------------|
| **`LCO_Static_2Tier_Demo.ipynb`** | Minimal, fully reproducible demonstration of a 2-tier lexicographic model using Pyomo. Tier L2 maximizes revenue; Tier L3 minimizes overbooking slack with a locked revenue floor. |
| **`LCO_Colab_Procedures.ipynb`** | Full Colab-ready workflow for synthetic dataset generation, Pyomo modeling, rolling-horizon extensions, and reproducible simulations. |

---

## 📁 Datasets

All datasets are synthetic and fully reproducible.

| CSV File | Description |
|----------|-------------|
| **`synthetic_booking_scenarios.csv`** | Baseline 12-booking dataset used in the LCO paper. |
| **`LCO_50_bookings.csv`** | Medium-size scenario for validation and comparison testing. |
| **`LCO_500_stochastic_bookings.csv`** | Large, stochastic simulation dataset for stress testing performance. |
| **`LCO_multi_hotel_chain.csv`** | Multi-property synthetic dataset for multi-hotel chain experiments. |

---

## 🔧 Installation & Requirements

### Option A — Run in Google Colab (Recommended)

No installation required.  
Run inside Colab:

```python
!pip install pyomo highspy
!apt-get install -y coinor-cbc
