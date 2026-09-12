# CHGNet Mg–H Molecular Dynamics: Diffusion + Surface Release

A reproducible **machine-learning interatomic potential (MLIP)** portfolio project for hydrogen transport in magnesium using **CHGNet + ASE molecular dynamics**.

The project separates two physical questions:

1. **Bulk H diffusion in hcp Mg** — H mean-squared displacement (MSD), apparent diffusion analysis, temperature traces, and Arrhenius-ready processing.
2. **Hydrogen surface release from Mg(0001)** — H height above the Mg surface, Mg–H separation, and persistent atomic-H escape into the vacuum region.

## Real CHGNet quick-run data

The repository includes real Kaggle CHGNet output for **300, 480, and 673 K** from a **0.50 ps diagnostic production run**.

| Set T (K) | Mean T (K) | Final H MSD (Å²) | Diagnostic apparent D (cm²/s) | Fit R² |
|---:|---:|---:|---:|---:|
| 300 | 291.29 | 9.04 | 3.63×10⁻⁴ | 0.746 |
| 480 | 495.62 | 10.80 | 4.73×10⁻⁴ | 0.828 |
| 673 | 681.48 | 28.43 | 7.37×10⁻⁴ | 0.732 |

**These D values are diagnostic only and must not be interpreted as converged diffusion coefficients.** A 0.50 ps trajectory is too short to establish a stable diffusive regime, and the large MSD can contain transient relaxation and ballistic contributions.

## Scientific status

- Real CHGNet trajectory output: **yes**
- Zero-shot pretrained model: **CHGNet 0.3.0 MPtrj**
- DFT-validated diffusion coefficients: **no**
- Converged production diffusion study: **not yet**
- Surface release equals thermodynamic H₂ desorption: **no**

The goal is to demonstrate an honest, reproducible **MLIP research-engineering workflow** rather than overclaim scientific accuracy.

## Numerical choices

- CHGNet package: `0.4.2`
- pretrained checkpoint: `0.3.0` (MPtrj)
- ensemble: fixed-cell NVT
- thermostat: ASE Langevin
- H-containing timestep: **0.5 fs**
- bulk temperatures: **300, 480, 673 K**
- periodic-boundary unwrapping before MSD analysis
- Einstein diagnostic relation: `MSD = 6 D t`

## Repository layout

```text
code/
  chgnet_mgh_combined.py

data/
  bulk_300K_timeseries.csv
  bulk_480K_timeseries.csv
  bulk_673K_timeseries.csv
  quick_run_diagnostic_summary.csv

figures/
  REAL_quick_H_MSD.png
  REAL_quick_temperature.png
  REAL_quick_potential_energy.png
  REAL_quick_diagnostic_D.png

RESULTS_NOTE.md
```

## Next step

Use longer equilibration and production trajectories, then confirm a stable linear MSD regime before fitting diffusion coefficients or an Arrhenius activation energy.

## Citation

CHGNet: Deng, B. et al. *Nature Machine Intelligence* **5**, 1031–1041 (2023). DOI: **10.1038/s42256-023-00716-3**.

Mg–H diffusion benchmark: *Hydrogen diffusion in magnesium using machine learning potentials: a comparative study*, *npj Computational Materials* (2025). DOI: **10.1038/s41524-025-01555-z**.

## License

MIT.
