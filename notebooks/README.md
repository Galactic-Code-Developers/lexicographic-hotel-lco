# Lexicographic Constraint Optimization (LCO)
### **Reproducible Notebooks, Datasets, and Simulation Framework**

This repository contains the complete computational environment for executing **Lexicographic Constraint Optimization (LCO)** models and simulations.  
All notebooks replicate the procedures used in the formal LCO research papers by **Antonios Valamontes, Kapodistrian Academy of Science**.

---

## 🔗 Quick Launch — Open in Google Colab

| Notebook | Colab Link |
|---------|------------|
| **LCO_Static_2Tier_Demo.ipynb** | [Open in Colab](https://colab.research.google.com/) |
| **LCO_Colab_Procedures.ipynb** | [Open in Colab](https://colab.research.google.com/) |
| **LCO_Colab_Simulations.ipynb** | **[Open Full Simulation Notebook](https://colab.research.google.com/)** |

*(Replace URLs with your actual repo links after upload.)*

---

## 📘 Notebooks Included

### **1. `LCO_Static_2Tier_Demo.ipynb`**
A minimal, mathematically rigorous demonstration of static lexicographic optimization:
- Tier **L2**: maximize expected revenue  
- Tier **L3**: minimize expected overbooking slack  
- Automatic extraction of floors \(Z_2^\*\)  
- Verified solver outputs  

This notebook is the baseline correctness demonstration of lexicographic floors.

---

### **2. `LCO_Colab_Procedures.ipynb`**
A procedural, step-by-step implementation in Colab:

- Build Pyomo models (sets, binaries, constraints)  
- Implement acceptance, assignment, continuity  
- Add overbooking slack  
- Solve Tier L2  
- Lock floors  
- Solve Tier L3  
- Extract KPIs  
- Produce validation tables

This notebook mirrors the methodology described in the main LCO paper.

---

### **3. `LCO_Colab_Simulations.ipynb`**  
### *(New — Full Simulation Suite)*

This is the **complete simulation notebook** performing:

#### ✔ **Monte Carlo Experimentation**
- Demand uncertainty
- Show-rate noise injection
- Price fluctuation scenarios
- KPI distributions

#### ✔ **Rolling-Horizon Dynamic LCO (CMDP-Compatible)**
- 14-day decision window  
- Dynamic arrivals  
- Real-time feasibility gate  
- Revenue floor propagation

#### ✔ **Multi-Hotel Chain Simulation**
Using the dataset:
- `LCO_multi_hotel_chain.csv`

Includes:
- Property-level subproblems  
- Global floors aggregation  
- Chain-level KPI tracking  

#### ✔ **Visualization**
- Revenue distributions  
- Slack distributions  
- Heatmaps of assignments  
- Comparative scalar vs LCO performance  

This is the companion notebook to the **simulation study section** of the LCO CMDP paper.

---

## 📁 Datasets Included

All CSVs are fully synthetic and reproducible.

| File | Description |
|------|-------------|
| `synthetic_booking_scenarios.csv` | Baseline 12-booking dataset |
| `LCO_50_bookings.csv` | Mid-size validation dataset |
| `LCO_500_stochastic_bookings.csv` | Large stochastic stress-test dataset |
| `LCO_multi_hotel_chain.csv` | Multi-property dataset for chain-level simulation |

---

## 🔧 Installation

### ✔ Recommended: Use Google Colab (No Setup Required)

```python
!pip install pyomo highspy
!apt-get install -y coinor-cbc
