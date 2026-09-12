from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

def load_clean(T):
    df = pd.read_csv(DATA / f"bulk_{T}K_timeseries.csv")
    if len(df) > 1 and np.isclose(df.loc[0, "MSD_A2"], df.loc[1, "MSD_A2"]):
        df = df.drop(index=1).reset_index(drop=True)
        df["time_ps"] = np.arange(len(df)) * 0.01
    return df

dfs = {T: load_clean(T) for T in [300, 480, 673]}

plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
    "savefig.dpi": 350,
})

# MSD
fig, ax = plt.subplots(figsize=(8.6, 5.4))
for T, df in dfs.items():
    ax.plot(df["time_ps"], df["MSD_A2"], linewidth=2.2, label=f"{T} K")
ax.set_xlabel("Production time (ps)")
ax.set_ylabel(r"H mean-squared displacement ($\AA^2$)")
ax.set_title("CHGNet Mg–H quick run: hydrogen displacement")
ax.text(0.02, 0.96, "Real CHGNet output • 0.50 ps diagnostic run", transform=ax.transAxes, va="top")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(FIG / "REAL_quick_H_MSD.png", bbox_inches="tight")
plt.close(fig)

# Temperature
fig, ax = plt.subplots(figsize=(8.6, 5.4))
for T, df in dfs.items():
    ax.plot(df["time_ps"], df["temperature_K"], linewidth=1.4, alpha=0.65, label=f"{T} K instantaneous")
    roll = df["temperature_K"].rolling(window=7, center=True, min_periods=1).mean()
    ax.plot(df["time_ps"], roll, linewidth=2.3, label=f"{T} K rolling mean")
ax.set_xlabel("Production time (ps)")
ax.set_ylabel("Temperature (K)")
ax.set_title("CHGNet Mg–H quick run: thermostat response")
ax.legend(frameon=False, ncol=2)
fig.tight_layout()
fig.savefig(FIG / "REAL_quick_temperature.png", bbox_inches="tight")
plt.close(fig)

# Potential energy
fig, ax = plt.subplots(figsize=(8.6, 5.4))
for T, df in dfs.items():
    e = df["potential_energy_eV"]
    ax.plot(df["time_ps"], e - e.mean(), linewidth=1.9, label=f"{T} K")
ax.axhline(0, linewidth=1.0)
ax.set_xlabel("Production time (ps)")
ax.set_ylabel("Potential energy relative to run mean (eV)")
ax.set_title("CHGNet Mg–H quick run: energetic stability")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(FIG / "REAL_quick_potential_energy.png", bbox_inches="tight")
plt.close(fig)

# Diagnostic diffusion fit
rows = []
for T, df in dfs.items():
    t = df["time_ps"].to_numpy()
    msd = df["MSD_A2"].to_numpy()
    i0, i1 = max(1, int(0.40 * len(df))), max(5, int(0.90 * len(df)))
    slope, intercept = np.polyfit(t[i0:i1], msd[i0:i1], 1)
    pred = slope * t[i0:i1] + intercept
    ss_res = np.sum((msd[i0:i1] - pred) ** 2)
    ss_tot = np.sum((msd[i0:i1] - np.mean(msd[i0:i1])) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    D = max(slope / 6 * 1e-4, 0.0)
    rows.append((T, D, r2))

summary = pd.DataFrame(rows, columns=["temperature_K", "D_cm2_s", "fit_r2"])
fig, ax = plt.subplots(figsize=(7.2, 5.0))
ax.plot(summary["temperature_K"], summary["D_cm2_s"], marker="o", linewidth=2)
ax.set_yscale("log")
ax.set_xlabel("Temperature (K)")
ax.set_ylabel(r"Apparent $D$ (cm$^2$ s$^{-1}$)")
ax.set_title("Diagnostic-only diffusion estimate")
ax.text(0.02, 0.96, "Do not report scientifically: 0.50 ps is too short", transform=ax.transAxes, va="top")
fig.tight_layout()
fig.savefig(FIG / "REAL_quick_diagnostic_D.png", bbox_inches="tight")
plt.close(fig)

print(summary)
print(f"Figures written to: {FIG}")
