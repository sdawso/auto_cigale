from astropy.io import fits
from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

def extract_data(fits_path,
                 sfr_key = 'bayes.sfh.sfr', mstar_key = 'best.stellar.m_star', redshift_key = 'best.universe.redshift'):
    with fits.open(fits_path) as hdul:
        data = Table(hdul[1].data)

    sfr = data[sfr_key].data
    mstar = data[mstar_key].data
    redshift = data[redshift_key].data

    log_sfr = np.log10(np.clip(sfr, 1e-10, None))
    log_mstar = np.log10(np.clip(mstar, 1e-10, None))

    combined = np.vstack((redshift, log_mstar, log_sfr)).T
    combined = combined[np.isfinite(combined).all(axis=1)]
    return combined

def run_list_parse(fits_directory = None, base_directory = ".", results_name = "results.fits"):
    out = []

    if fits_directory is not None:
        for dirpath, _, filenames in os.walk(fits_directory):
            for filename in filenames:
                if filename == results_name:
                    fits_path = os.path.join(dirpath, filename)
                    run = extract_data(fits_path)
                    out.append(run)
    else:
        for dirpath, _, filenames in os.walk(base_directory):
            for filename in filenames:
                if filename == results_name:
                    fits_path = os.path.join(dirpath, filename)
                    run = extract_data(fits_path)
                    out.append(run)

    return out

# Generate corner plot, toggleable histograms and triangle scatter plots

def corner_plot(label_list = None, fits_directory = None,
                diagonal_histograms = True, triangle_scatter = True):

    # Default behavior - read every results.fits file in current directory
    # Optional:
    # - fits_directory: filepath string, overrides and points to fits results directory
    # - base_directory: specify default directory
    run_list = run_list_parse(fits_directory)

    output_dir = os.path.join(os.getcwd(), 'figures')
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'corner_plot({timestamp}).png'

    param_names = ["Redshift", "log M*", "log_sfr"]
    colors = ['blue', 'orange', 'green']

    # Optional - include list of labels (length must match number of fits files)
    labels = label_list if label_list is not None and len(label_list) == len(run_list) else colors
    runs = [r for r in run_list]
    n = len(param_names)

    fig, axes = plt.subplots(n, n, figsize=(4 * n, 4 * n))

    # Clear all axes first
    for i in range(n):
        for j in range(n):
            axes[i, j].axis('off')

    # Diagonal histograms
    if diagonal_histograms:
        for i in range(n):
            ax = axes[i, i]
            ax.axis('on')
            bins = 30
            for run, color in zip(runs, colors):
                ax.hist(run[:, i], bins=bins, color=color, alpha=0.4, density=True)
            ax.set_ylabel(param_names[i], fontsize=12)
            ax.set_xlabel(param_names[i], fontsize=12)
            ax.tick_params(axis='both', which='major', labelsize=10)

    if triangle_scatter:
        # Dictionary to store median ±1sigma info for scatter pairs
        summary_stats = {lab: {} for lab in labels}

        # Lower triangle scatter plots (no 1-1 line)
        for i in range(1, n):
            for j in range(i):
                ax = axes[i, j]
                ax.axis('on')

                for run, color, lab in zip(runs, colors, labels):
                    ax.scatter(run[:, j], run[:, i], s=10, alpha=0.5, color=color)

                    x = run[:, j]
                    y = run[:, i]

                    quartiles = np.percentile(x, [25, 50, 75])
                    bins_edges = [x.min() - 1e-10, quartiles[0], quartiles[1], quartiles[2], x.max() + 1e-10]

                    medians = []
                    sigmas_low = []
                    sigmas_high = []
                    for b in range(len(bins_edges) - 1):
                        mask = (x >= bins_edges[b]) & (x < bins_edges[b + 1])
                        if np.sum(mask) > 0:
                            y_bin = y[mask]
                            med = np.median(y_bin)
                            p16 = np.percentile(y_bin, 16)
                            p84 = np.percentile(y_bin, 84)
                            medians.append(med)
                            sigmas_low.append(med - p16)
                            sigmas_high.append(p84 - med)

                    # Average median and sigmas over bins for summary
                    if len(medians) > 0:
                        avg_med = np.mean(medians)
                        avg_sig_low = np.mean(sigmas_low)
                        avg_sig_high = np.mean(sigmas_high)
                        summary_stats[lab][f"{param_names[i]} vs {param_names[j]}"] = (avg_med, avg_sig_low, avg_sig_high)

                # Set axis limits
                all_x = np.hstack([run[:, j] for run in runs])
                all_y = np.hstack([run[:, i] for run in runs])
                low_x, high_x = all_x.min(), all_x.max()
                low_y, high_y = all_y.min(), all_y.max()

                padding_x = 0.05 * (high_x - low_x)
                padding_y = 0.05 * (high_y - low_y)
                ax.set_xlim(low_x - padding_x, high_x + padding_x)
                ax.set_ylim(low_y - padding_y, high_y + padding_y)

                # Labels and ticks
                if i == n - 1:
                    ax.set_xlabel(param_names[j], fontsize=12)
                else:
                    ax.set_xticks([])

                if j == 0:
                    ax.set_ylabel(param_names[i], fontsize=12)
                else:
                    ax.set_yticks([])

                ax.tick_params(axis='both', which='major', labelsize=10)

    plt.tight_layout()

    # Legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=8, label=lab)
               for color, lab in zip(colors, labels)]

    # Compose summary text
    summary_lines = []
    for lab in labels:
        summary_lines.append(f"--- {lab} ---")
        for pair, stats in summary_stats[lab].items():
            med, sig_low, sig_high = stats
            summary_lines.append(f"{pair}: median = {med:.2f} (+{sig_high:.2f}/-{sig_low:.2f})")
        summary_lines.append("")

    summary_text = "\n".join(summary_lines)

    # Place summary text above the legend (adjust coordinates as needed)
    fig.legend(handles=handles, loc='upper right', fontsize=12)
    fig.text(0.40, 0.90, summary_text, fontsize=10, va='top', ha='left', family='monospace')

    plt.savefig(os.path.join(output_dir, output_file))
    plt.show()







