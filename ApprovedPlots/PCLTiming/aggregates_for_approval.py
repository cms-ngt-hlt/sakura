import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime

# Database path
db_path = "MergedPCLStats_2024.db"

# Workflows to include
selected_workflows = {
    "BeamSpotObjectHP_ByLumi",
    "EcalPedestals_pcl",
    "SiPixelAliHG_pcl",
    "SiPixelQualityFromDbRcd_prompt",
    "SiStripBadStrip_pcl"
}

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to get CMS_RUN data
cms_run_query = """
    SELECT number, start, end FROM CMS_RUN
"""
cms_run_df = pd.read_sql_query(cms_run_query, conn)

# Query to get WORKFLOW_FILE data
workflow_file_query = """
    SELECT run, workflow, created, uploaded FROM WORKFLOW_FILE
"""
workflow_file_df = pd.read_sql_query(workflow_file_query, conn)

# Close database connection
conn.close()

# Convert date columns to datetime format
cms_run_df["start"] = pd.to_datetime(cms_run_df["start"], errors='coerce')
cms_run_df["end"] = pd.to_datetime(cms_run_df["end"], errors='coerce')
workflow_file_df["created"] = pd.to_datetime(workflow_file_df["created"], errors='coerce')
workflow_file_df["uploaded"] = pd.to_datetime(workflow_file_df["uploaded"], errors='coerce')

# Filter only the selected workflows
workflow_file_df = workflow_file_df[workflow_file_df["workflow"].isin(selected_workflows)]

# Merge the dataframes on run number
merged_df = workflow_file_df.merge(cms_run_df, left_on="run", right_on="number", how="inner")

# Calculate time differences
diff_df = merged_df.dropna().copy()
diff_df["diff_job_run_from_end"] = (diff_df["created"] - diff_df["end"]).dt.total_seconds() / 3600
diff_df["diff_job_run_from_start"] = (diff_df["created"] - diff_df["start"]).dt.total_seconds() / 3600
diff_df["diff_upload_from_end"] = (diff_df["uploaded"] - diff_df["end"]).dt.total_seconds() / 3600
diff_df["diff_upload_from_start"] = (diff_df["uploaded"] - diff_df["start"]).dt.total_seconds() / 3600
diff_df["diff_upload_from_created"] = (diff_df["uploaded"] - diff_df["created"]).dt.total_seconds() / 3600

# Time difference configurations
time_diff_configs = [
    ("diff_job_run_from_end", np.arange(0, 48.5, 0.5)),
    ("diff_job_run_from_start", np.arange(0, 60.5, 0.5)),
    ("diff_upload_from_end", np.arange(0, 48.5, 0.5)),
    ("diff_upload_from_start", np.arange(0, 60.5, 0.5)),
    ("diff_upload_from_created", np.arange(0, 12.5, 0.25)),
]

# Axis label mapping for each time difference
time_diff_labels = {
    "diff_job_run_from_end":    r"$\Delta T_{\mathrm{job\ creation - run\ end}}\ \mathrm{[hours]}$",
    "diff_job_run_from_start":  r"$\Delta T_{\mathrm{job\ creation - run\ start}}\ \mathrm{[hours]}$",
    "diff_upload_from_end":     r"$\Delta T_{\mathrm{upload - run\ end}}\ \mathrm{[hours]}$",
    "diff_upload_from_start":   r"$\Delta T_{\mathrm{upload - run\ start}}\ \mathrm{[hours]}$",
    "diff_upload_from_created": r"$\Delta T_{\mathrm{upload - job\ creation}}\ \mathrm{[hours]}$"
}

# Generate and save aggregate plots
for time_diff_col, bins in time_diff_configs:
    output_dir = time_diff_col
    os.makedirs(output_dir, exist_ok=True)

    # Compute statistics
    mean_diff = diff_df[time_diff_col].mean()
    rms_diff = np.sqrt(((diff_df[time_diff_col] - mean_diff) ** 2).mean())
    total_entries = len(diff_df[time_diff_col].dropna())

    # --- CMS Style Configuration ---
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "font.size": 14,
        "font.family": "sans-serif",
        "figure.figsize": (6, 6),      # square format
        "savefig.dpi": 300,
        "axes.labelsize": 16,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "legend.fontsize": 13
    })
    
    # --- Create the figure ---
    fig, ax = plt.subplots()

    # Histogram
    ax.hist(diff_df[time_diff_col], bins=bins, edgecolor="black", color="#5790fc", alpha=0.75)

    # Labels
    ax.set_xlabel(time_diff_labels[time_diff_col])
    ax.set_ylabel("Number of workflows")

    # Vertical lines for mean ± RMS (add labels for legend)
    ax.axvline(mean_diff, color="red", linestyle="dashed", linewidth=1.5, label=f"Mean = {mean_diff:.2f} h")
    ax.axvline(mean_diff + rms_diff, color="green", linestyle="dotted", linewidth=1.5, label=f"RMS = {rms_diff:.2f} h")
    ax.axvline(mean_diff - rms_diff, color="green", linestyle="dotted", linewidth=1.5)
    
    # CMS label (upper left)
    ax.text(
        0.635, 0.955, "CMS",
        transform=ax.transAxes,
        fontsize=18, fontweight="bold",
        va="top", ha="left"
    )
    
    # "Preliminary" label (upper right)
    ax.text(
        0.98, 0.95, "Preliminary",
        transform=ax.transAxes,
        fontsize=16, style="italic",
        va="top", ha="right"
    )
    
    # Legend on the right, below "Preliminary"
    ax.legend(
        frameon=False,
        bbox_to_anchor=(0.98, 0.80),
        bbox_transform=ax.transAxes,
        loc="upper right"
    )
    
    # Additional info (bottom right)
    #ax.text(
    #    0.98, 0.02, f"Workflows: {len(selected_workflows)}",
    #    transform=ax.transAxes,
    #    fontsize=11, color="gray",
    #    va="bottom", ha="right"
    #)

    plt.tight_layout()

    # Save (avoid clipping right-side labels)
    plot_path = os.path.join(output_dir, f"aggregate_{time_diff_col}_CMSStyle.png")
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()

    # Plot
    # plt.figure(figsize=(10, 5))
    # plt.hist(diff_df[time_diff_col], bins=bins, edgecolor='black', alpha=0.7)
    # plt.xlabel("Time Difference (hours)")
    # plt.ylabel("Frequency")
    # plt.title(f"Aggregate {time_diff_col.replace('_', ' ').capitalize()} for Selected Workflows")
    # plt.grid(True)

    # # Add lines for mean and RMS
    # plt.axvline(mean_diff, color='r', linestyle='dashed', linewidth=1, label=f'Mean: {mean_diff:.2f}h')
    # plt.axvline(mean_diff + rms_diff, color='g', linestyle='dashed', linewidth=1, label=f'RMS: {rms_diff:.2f}h')
    # plt.axvline(mean_diff - rms_diff, color='g', linestyle='dashed', linewidth=1)
    # plt.legend()

    # # Save plot
    # plot_path = os.path.join(output_dir, f"aggregate_{time_diff_col}.png")
    # plt.savefig(plot_path)
    # plt.close()

    # Print statistics
    print(f"Plot saved in {plot_path}")
    print(f"{time_diff_col}: Mean = {mean_diff:.2f} hours, RMS = {rms_diff:.2f} hours, Total Entries = {total_entries}")

