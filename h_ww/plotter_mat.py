import uproot
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np

# Input directory containing ROOT files
inputDir = "./output/"
files = {
    "wzp6_ee_nunuH_HWW_ecm240": f"{inputDir}wzp6_ee_nunuH_HWW_ecm240.root",
    "p8_ee_ZZ_ecm240": f"{inputDir}p8_ee_ZZ_ecm240.root",
    "p8_ee_WW_ecm240": f"{inputDir}p8_ee_WW_ecm240.root"
}

# Histogram definitions
hists = {
    "leptons_p_dist": {"output": "leptons_p_dist", "logy": True, "xmin": 9, "xmax": 124, "ymin": 1e-2, "xtitle": "Leptons momentum (GeV/c)", "ytitle": "Events"},
    "MissingET_dist": {"output": "MissingET_dist", "logy": True, "xmin": 0, "xmax": 128, "ymin": 1e-2, "ymax": 1e8, "xtitle": "Missing energy (GeV)", "ytitle": "Events"},
    "photon_energy": {"output": "photon_energy", "logy": True, "xmin": 0, "xmax": 60, "ymin": 1e-2, "xtitle": "Photon Energy (GeV)", "ytitle": "Events"},
    "invariant_mass": {"output": "invariant_mass", "logy": True, "xmin": 0, "xmax": 200, "ymin": 1e1, "ymax": 1e8, "xtitle": "Invariant mass (GeV)", "ytitle": "Events"},
    "hadronicEnergy": {"output": "hadronicEnergy", "logy": True, "xmin": 0, "xmax": 250, "ymin": 1e1, "ymax": 1e8, "xtitle": "Hadronic Energy (GeV)", "ytitle": "Events"},
    "electrons_soft_p_dist": {"output": "electrons_soft_p_dist", "logy": True, "xmin": 9, "xmax": 124, "ymin": 1e-2, "xtitle": "Soft electrons momentum (GeV/c)", "ytitle": "Events"},
    "muons_soft_p_dist": {"output": "muons_soft_p_dist", "logy": True, "xmin": 9, "xmax": 124, "ymin": 1e-2, "ymax": 1e8, "xtitle": "Soft muons momentum (GeV/c)", "ytitle": "Events"},
    "photon_num": {"output": "photon_num", "logy": True, "xmin": 0, "xmax": 30, "ymin": 1e-2, "xtitle": "Photon number", "ytitle": "Events"},
    "missingMass": {"output": "missing_Mass", "logy": True, "xmin": 0, "xmax": 240, "ymin": 1e1, "ymax": 1e8, "xtitle": "Missing mass (GeV)", "ytitle": "Events"},
    "n_jets": {"output": "n_jets", "logy": True, "xmin": 0, "xmax": 18, "ymin": 1e-2, "xtitle": "Number of Jets", "ytitle": "Events"},
    "cutFlow": {
    "output": "cutFlow",
    "logy": True,
    "xmin": 1,
    "xmax": 9,
    "ymin": 1e2,
    "ymax": 1e9,
    "xtitle": "Selection Steps",  # Keep xtitle a single string
    "xlabels": [  # Add labels separately
        "All events", 
        "#==2 lep", 
        "OS for combos", 
        "missingMass>130", 
        "30<missingET<70", 
        "#μ_p e_p<38", 
        "had_energy<20",
        "#γ_n<3 && #γ_E<7", 
        "n_jets<=2"
    ],
    "ytitle": "Events"
}

}

# Custom legend labels
legend_labels = {
    "wzp6_ee_nunuH_HWW_ecm240": r"$e^+e^-\to\nu\nu H, H\to WW$",
    "p8_ee_ZZ_ecm240": r"$e^+e^-\to ZZ$",
    "p8_ee_WW_ecm240": r"$e^+e^-\to WW$"
}

# Plot histograms
for hist_name, hist_info in hists.items():
    plt.figure()
    ax = plt.gca()
    hep.style.use("CMS")  # Use CMS-like style

    for file_key, file_path in files.items():
        with uproot.open(file_path) as f:
            if hist_name in f:
                hist = f[hist_name]
                edges = hist.axis().edges()
                values = hist.values()
                hep.histplot(values, bins=edges, label=legend_labels[file_key], ax=ax)

    ax.set_xlabel(hist_info["xtitle"], fontsize=14)
    ax.set_ylabel(hist_info["ytitle"], fontsize=14)
    ax.set_xlim(hist_info["xmin"], hist_info["xmax"])
    if "ymax" in hist_info:
        ax.set_ylim(hist_info["ymin"], hist_info["ymax"])
    if hist_info["logy"]:
        ax.set_yscale("log")

    if hist_name == "cutFlow":
        ax.set_xticks(range(1, len(hist_info["xlabels"]) + 1))  # Set tick positions
        ax.set_xticklabels(hist_info["xlabels"], rotation=39, ha="right", fontsize=13)
    # Custom legend properties
    ax.legend(fontsize=15, loc="upper right", frameon=True)

    # Custom experiment label with energy scale and luminosity
    hep.label.exp_label(
        exp="FCC-ee", 
        ax=ax, 
        lumi=None, 
        data=False, 
        com=None, 
        label=r"$\sqrt{s} = 240.0$ GeV, $\mathcal{L} = 10.8$ ab$^{-1}$",
        fontsize=15  # Change this value to adjust the size
)

    # Save figure
    plt.savefig(f"{hist_info['output']}.png", bbox_inches="tight")
    plt.close()
