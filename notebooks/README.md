# Lexicographic Constraint Optimization (LCO)
### **Reproducible Notebooks, Datasets, and Simulation Framework**

This repository contains the complete computational environment for executing **Lexicographic Constraint Optimization (LCO)** simulations, demonstrations, and Monte-Carlo studies.  
It accompanies the LCO research papers authored by **Antonios Valamontes, Kapodistrian Academy of Science**.

All notebooks are runnable directly in **Google Colab** and require no local installation.

---

# 🔗 Quick Launch — Open in Google Colab

| Notebook | Colab Link |
|---------|------------|
| **LCO_Static_2Tier_Demo.ipynb** | [Open in Colab](https://colab.research.google.com/)|
| **LCO_Colab_Procedures.ipynb** | [Open in Colab](https://colab.research.google.com/)|
| **LCO_Colab_Simulations.ipynb** | [Open in Colab](https://colab.research.google.com/)|

---

# 📘 Notebook Descriptions (FULL EXPLANATIONS RESTORED)

## **1. `LCO_Static_2Tier_Demo.ipynb`**  
### *Purpose:*  
This notebook demonstrates the **core mathematical mechanism** of lexicographic floors using a minimal synthetic instance (10 rooms × 5 days).

### *What it shows:*  
- Tier **L2**: maximize expected revenue  
- Tier **L3**: minimize expected overbooking slack  
- Automatic computation of revenue optimum \( Z_2^\* \)  
- Injection of the revenue floor into Tier L3  
- Re-solving with strict lexicographic precedence  
- Extraction of KPIs (Rev, Slack, Assignment)

### *Use case:*  
This notebook is the **baseline correctness and pedagogical example**.  
It is recommended for anyone learning LCO for the first time or verifying the fundamental lexicographic mechanism.

---

## **2. `LCO_Colab_Procedures.ipynb`**  
### *Purpose:*  
A **procedural, step-by-step** notebook that mirrors the exact method described in the formal research paper “Procedures for Executing Lexicographic Constraint Optimization in Google Colab.”

### *What it includes:*  
- Full Pyomo model construction (sets, parameters, binaries)  
- Assignment, exclusivity, and continuity constraints  
- Slack-based overbooking constraints  
- Tier L2 ➝ Tier L3 lexicographic solve  
- KPI export to tables  
- Visualizations (optional)  
- Section-by-section correspondence with the TEX paper

### *Use case:*  
This notebook is intended as the **official procedural companion** to the LCO methodology paper.  
It is also used for reviewers, collaborators, and reproducibility audits.

---

## **3. `LCO_Colab_Simulations.ipynb`**  
### *Purpose:*  
A complete, heavy-duty notebook performing **multi-scenario, rolling-horizon, and multi-property simulations**.

### *What it performs:*  

#### ✔ **Monte-Carlo Simulations**
- Random demand realizations  
- Noise injected into show rates  
- Random booking arrivals  
- Scenario-by-scenario LCO solution  
- Distributional KPI outputs (Violin plots, Histograms)

#### ✔ **Rolling-Horizon Dynamic LCO**
- 14-day forward decision window  
- Dynamic state evolution \( x_{t+1} = \Phi(x_t, u_t, \xi_t) \)  
- Feasibility gate for Tier L1  
- Persistent floors for revenue and risk tiers  
- CMDP-consistent lexicographic evaluation

#### ✔ **Multi-Hotel Chain Simulation**
Using `LCO_multi_hotel_chain.csv`:
- Separate MILP per property  
- Cloud-like coordinator  
- Floors aggregation across properties  
- Chain-level KPIs & comparisons  

#### ✔ **Outputs Produced**
- KPI distributions  
- Property-level and chain-level statistics  
- Comparative plots (Scalar vs LCO)  
- Exportable CSV summaries  

### *Use case:*  
This is the **primary notebook for research results**, experiments, figures, and all simulation-related content in the LCO studies.  
It is the exact notebook used in your CMDP/LCO manuscript simulations.

---

# 📁 Datasets Included

| File | Description |
|------|-------------|
| `synthetic_booking_scenarios.csv` | Baseline 12-booking dataset |
| `LCO_50_bookings.csv` | Standard medium-sized test set |
| `LCO_500_stochastic_bookings.csv` | Full Monte-Carlo scale dataset |
| `LCO_multi_hotel_chain.csv` | Multi-property chain dataset |

---

# 🔧 Installation

### ✔ Use Colab (recommended)
No installation required.

```python
!pip install pyomo highspy
!apt-get install -y coinor-cbc

LCO-Notebooks/
│
├── notebooks/
│   ├── LCO_Static_2Tier_Demo.ipynb
│   ├── LCO_Colab_Procedures.ipynb
│   ├── LCO_Colab_Simulations.ipynb
│
├── data/
│   ├── synthetic_booking_scenarios.csv
│   ├── LCO_50_bookings.csv
│   ├── LCO_500_stochastic_bookings.csv
│   ├── LCO_multi_hotel_chain.csv
│
├── requirements.txt
├── LICENSE
└── README.md

