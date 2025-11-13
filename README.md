# Lexicographic Constraint Optimization (LCO) — Colab Simulations

This repository contains a reproducible Google Colab notebook implementing the static
two-tier **Lexicographic Constraint Optimization (LCO)** demo:

- Tier **L2**: maximize expected revenue
- Tier **L3**: minimize expected overbooking slack under a fixed revenue floor

The model mirrors the synthetic 10-rooms × 5-days instance used in the main
LCO hotel-management paper.

## Contents

- `LCO_Colab_Simulations.ipynb` — runnable Colab notebook implementing the full L2→L3 workflow.

## How to Use in Google Colab

1. Upload the notebook to your GitHub repository.
2. Open in Google Colab using one of the following methods:
   - From GitHub directly in Colab (`Open in Colab`).
   - Or download the file and upload it manually to Colab.

Once in Colab:

1. Run the installation cell to install Pyomo and solvers:
   ```python
   !pip install pyomo highspy
   !apt-get install -y coinor-cbc
   ```
2. Run all remaining cells in order.
3. The notebook will print:
   - The Tier L2 revenue optimum `Z2*`,
   - The Tier L3 overbooking slack sum,
   - A table of accepted bookings and room assignments,
   - A compact KPI summary.

## Reproducibility

All data are synthetic and defined inside the notebook; no external files are required.
Any Colab runtime with network access (for `pip` and `apt-get`) can reproduce the results.

## Citation

If you use this notebook in academic or technical work, please cite:

> Antonios Valamontes, *Procedures for Executing Lexicographic Constraint Optimization (LCO) Simulations Using Google Colab*, Kapodistrian Academy of Science.

