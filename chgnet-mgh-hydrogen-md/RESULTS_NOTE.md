# Quick-run results note

These results are from a **real CHGNet Kaggle run** using bulk Mg–H trajectories at 300, 480 and 673 K.

## What is trustworthy

- the CHGNet calculations executed successfully;
- the temperature-dependent increase in H displacement is visible;
- the 673 K trajectory shows substantially larger H MSD than the 300 K trajectory;
- the raw time series and potential-energy traces are preserved in this repository.

## What is not yet trustworthy as a scientific claim

The production trajectory is only **0.50 ps** after removing the duplicated first saved frame. That duration is too short to establish a stationary diffusive regime. Therefore the apparent diffusion coefficients are retained only as **diagnostic values**, not as converged transport coefficients.

The diagnostic fits are:

- 300 K: D ≈ 3.63e-4 cm²/s, R² ≈ 0.746
- 480 K: D ≈ 4.73e-4 cm²/s, R² ≈ 0.828
- 673 K: D ≈ 7.37e-4 cm²/s, R² ≈ 0.732

The relatively modest fit R² and the very short trajectory mean that transient structural relaxation, ballistic motion and finite-time fluctuations can strongly affect these values.

## Bookkeeping correction

The original quick-run output contained a duplicated initial production frame. The diagnostic plots in `figures/` remove this duplicate and reconstruct the production time axis at 0.01 ps spacing.

## Next run

For a defensible diffusion analysis, use substantially longer equilibration and production trajectories and verify an approximately linear MSD regime before fitting D or an Arrhenius activation energy.
