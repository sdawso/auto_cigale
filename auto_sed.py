import os
from astropy.io import fits
import subprocess

def run_command(command):
    print(f"Running: {command}")
    completed = subprocess.run(command, shell=True)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed: {command}")

# def load_all_results_pandas(root_dir):
#     all_dfs = []
#     for dirpath, _, filenames in os.walk(root_dir):
#         for filename in filenames:
#             if filename == "results.fits":
#                 filepath = os.path.join(dirpath, filename)
#                 try:
#                     table = Table.read(filepath)
#                     df = table.to_pandas()
#                     df["source_dir"] = dirpath  # Optional: track origin
#                     all_dfs.append(df)
#                 except Exception as e:
#                     print(f"Failed to load {filepath}: {e}")
#
#     if all_dfs:
#         combined_df = pd.concat(all_dfs, ignore_index=True)
#         print('sheesh')
#         return combined_df
#     else:
#         print('crud')
#         return pd.DataFrame()
#         # Empty if nothing found

def load_all_results_astropy(root_dir):
    results = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file == "results.fits":
                filepath = os.path.join(dirpath, file)
                try:
                    hdul = fits.open(filepath)
                    results.append(hdul)
                except Exception as e:
                    print(f"Failed to open {filepath}: {e}")
    return results
