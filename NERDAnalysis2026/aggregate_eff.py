import ROOT
import os
import re
import argparse

ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

trigger_paths = {
    "Ele32_WPTight": [
        "hltEG32L1SingleEGOrEtFilter",
        "hltEle32WPTightClusterShapeFilter",
        "hltEle32WPTightHEFilter",
        "hltEle32WPTightEcalIsoFilter",
        "hltEle32WPTightHcalIsoFilter",
        "hltEle32WPTightPixelMatchFilter",
        "hltEle32WPTightPMS2Filter",
        "hltEle32WPTightGsfOneOEMinusOneOPFilter",
        "hltEle32WPTightGsfMissingHitsFilter",
        "hltEle32WPTightGsfDetaFilter",
        "hltEle32WPTightGsfDphiFilter",
        "hltEle32WPTightGsfTrackIsoFilter"
    ],
    "DiEle25_CaloIdL": [
        "hltDiEG25CaloIdLClusterShapeUnseededFilter",
        "hltDiEle25CaloIdLPixelMatchUnseededFilter",
        "hltDiEle25CaloIdLMWPMS2UnseededFilter"
    ]
}

# Create a flat list of all unique filters to extract from the ROOT files
all_filters = list(set([filt for path in trigger_paths.values() for filt in path]))

VARIABLES = ["eta", "ptEB", "ptEE", "phiEB", "phiEE"]

colors = [
    ROOT.kRed + 1, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 7,
    ROOT.kViolet + 1, ROOT.kOrange + 3, ROOT.kMagenta + 2, ROOT.kAzure + 2,
    ROOT.kPink + 9, ROOT.kTeal + 2, ROOT.kSpring + 9, ROOT.kGray + 3
]

parser = argparse.ArgumentParser()
parser.add_argument('--folder', default='dqm_files', help='Folder with input DQM root files')
parser.add_argument('--pattern', default=None,
                     help='Optional substring filter on filenames. Default: use every .root file.')
parser.add_argument('--no-fakes', action='store_true', help='Disable sideband fake subtraction')
parser.add_argument('--outfile', default='aggregated_efficiency.root')
parser.add_argument('--outdir', default='plots_aggregated_eff')
parser.add_argument('--label', default='Aggregated over all input runs')
parser.add_argument('--quiet', '-q', action='store_true')
args = parser.parse_args()

firstbin_mass, lastbin_mass = 21, 41   # 81-101 GeV
sideband_bins = [(0, 5), (55, 60)]

def extract_run_number(filename):
    m = re.search(r'R0*([0-9]{6})', filename)
    return int(m.group(1)) if m else None

def short_label(name):
    name = name.replace("hltEG32L1SingleEGOrEtFilter", "L1")
    name = name.replace("hltEle32WPTight", "")
    name = name.replace("Gsf", "")
    name = name.replace("Filter", "")
    return name

def get_th2(f, run, filt, var):
    folder = f"DQMData/Run {run}/HLT/Run summary/EGM/TrigObjTnP/"
    h = f.Get(folder + f"stdTag_{filt}_{var}")
    if h: return h
    return f.Get(folder + f"stdTagAndEle25MW_{filt}_{var}")

def project_signal_minus_sideband(h2, name_tag, forfakes=True):
    h_sig = h2.ProjectionX(name_tag + "_sig", firstbin_mass, lastbin_mass)
    h_sig.SetDirectory(0)
    if not forfakes: return h_sig

    h_side = None
    for lo, hi in sideband_bins:
        h_tmp = h2.ProjectionX(name_tag + f"_side_{lo}_{hi}", lo, hi)
        if h_side is None:
            h_side = h_tmp
            h_side.SetDirectory(0)
        else:
            h_side.Add(h_tmp)

    h_out = h_sig.Clone(name_tag + "_net")
    h_out.SetDirectory(0)
    h_out.Add(h_side, -1)
    for b in range(0, h_out.GetNbinsX() + 2):
        if h_out.GetBinContent(b) < 0:
            h_out.SetBinContent(b, 0)
            h_out.SetBinError(b, 0)
    return h_out

def clamp_to_denominator(num, denom):
    num_c = num.Clone(num.GetName() + "_clamped")
    n_clamped = 0
    for b in range(0, num_c.GetNbinsX() + 2):
        n, d = num_c.GetBinContent(b), denom.GetBinContent(b)
        if n > d:
            num_c.SetBinContent(b, d)
            num_c.SetBinError(b, denom.GetBinError(b))
            n_clamped += 1
    return num_c, n_clamped

def check_binning_match(h1, h2):
    if h1.GetNbinsX() != h2.GetNbinsX(): return False
    if abs(h1.GetXaxis().GetXmin() - h2.GetXaxis().GetXmin()) > 1e-5: return False
    if abs(h1.GetXaxis().GetXmax() - h2.GetXaxis().GetXmax()) > 1e-5: return False
    return True

# --- Step 1: aggregate raw 2D histograms across all files ---
aggregated = {var: {filt: None for filt in all_filters} for var in VARIABLES}
n_files_used = 0

for fname in sorted(os.listdir(args.folder)):
    if fname.startswith('.') or not fname.endswith(".root"): continue
    if args.pattern and args.pattern not in fname: continue
    
    run = extract_run_number(fname)
    if run is None: continue

    f = ROOT.TFile.Open(os.path.join(args.folder, fname))
    if not f or f.IsZombie(): continue

    used_this_file = False
    for var in VARIABLES:
        for filt in all_filters:
            h2 = get_th2(f, run, filt, var)
            if not h2: continue
            h2c = h2.Clone(f"{var}_{filt}_run{run}")
            h2c.SetDirectory(0)
            if aggregated[var][filt] is None:
                aggregated[var][filt] = h2c
            else:
                aggregated[var][filt].Add(h2c)
            used_this_file = True
    f.Close()
    if used_this_file: n_files_used += 1

if n_files_used == 0:
    raise SystemExit("No usable files found.")
if not args.quiet: print(f"Aggregated {n_files_used} files")

# --- Step 2: project each aggregated TH2 onto its variable axis ---
projected = {var: {} for var in VARIABLES}
for var in VARIABLES:
    for filt in all_filters:
        h2 = aggregated[var][filt]
        if h2 is not None:
            projected[var][filt] = project_signal_minus_sideband(h2, f"{var}_{filt}", forfakes=not args.no_fakes)

# --- Step 3: build efficiency graphs per path and per variable ---
out = ROOT.TFile(args.outfile, "RECREATE")

# Dictionary to store graphs for plotting: graphs[path][var] = [(label, TGraph), ...]
graphs = {path: {var: [] for var in VARIABLES} for path in trigger_paths.keys()}

for path_name, path_filters in trigger_paths.items():
    for var in VARIABLES:
        hmap = projected[var]
        
        # Sequential filters
        for i in range(1, len(path_filters)):
            num, denom = hmap.get(path_filters[i]), hmap.get(path_filters[i - 1])
            if num is None or denom is None: continue
                
            if not check_binning_match(num, denom):
                if not args.quiet: print(f"[{path_name} - {var}] Skipping {short_label(path_filters[i])} -> Binning mismatch!")
                continue

            num_c, n_clamped = clamp_to_denominator(num, denom)
            
            g = ROOT.TGraphAsymmErrors()
            g.BayesDivide(num_c, denom)
            
            clean_name = short_label(path_filters[i])
            g.SetName(f"eff_{path_name}_{var}_{clean_name}") 
            g.SetLineWidth(3)
            g.SetMarkerStyle(20)
            g.SetMarkerColor(colors[i % len(colors)])
            g.SetLineColor(colors[i % len(colors)])
            g.Write()
            graphs[path_name][var].append((clean_name, g))

        # Total Efficiency for the path
        num, denom = hmap.get(path_filters[-1]), hmap.get(path_filters[0])
        if num is not None and denom is not None:
            if not check_binning_match(num, denom):
                if not args.quiet: print(f"[{path_name} - {var}] Skipping Total Efficiency -> Binning mismatch!")
            else:
                num_c, n_clamped = clamp_to_denominator(num, denom)
                g_total = ROOT.TGraphAsymmErrors()
                g_total.BayesDivide(num_c, denom)
                
                g_total.SetName(f"eff_{path_name}_{var}_Total") 
                g_total.SetLineWidth(4)
                g_total.SetMarkerColor(ROOT.kBlack)
                g_total.SetLineColor(ROOT.kBlack)
                g_total.SetMarkerStyle(22)
                g_total.Write()
                graphs[path_name][var].append(("Total", g_total))

out.Close()

# --- Step 4: overlay plots per path and per variable ---
def draw_overlay(effs, var, path_name, outdir):
    c = ROOT.TCanvas(f"c_{path_name}_{var}", "", 1000, 700)
    c.SetRightMargin(0.2)
    pad = ROOT.TPad("pad", "", 0.0, 0.0, 0.85, 1.0)
    pad.SetBottomMargin(0.12)
    pad.Draw()
    pad.cd()
    
    y_min, y_max = 1.0, 0.0
    for _, g in effs:
        for i in range(g.GetN()):
            y, yerr = g.GetY()[i], g.GetErrorYhigh(i)
            if 0 < y < y_min: y_min = y
            if y + yerr > y_max: y_max = y + yerr

    for i, (label, g) in enumerate(effs):
        g.GetXaxis().SetTitle(var)
        g.GetYaxis().SetTitle("Filter Efficiency")
        g.SetMinimum(max(0, y_min * 0.94))
        g.SetMaximum(min(1.1, y_max * 1.05))
        if i == 0:
            g.SetTitle(f"{path_name} efficiency vs {var}")
        g.Draw("AP" if i == 0 else "P SAME")

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.DrawLatex(0.15, 0.87, "{" + args.label + "}")

    c.cd()
    legend = ROOT.TLegend(0.76, 0.25, 0.99, 0.95)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)
    for label, g in effs:
        legend.AddEntry(g, label, "p")
    legend.Draw()

    os.makedirs(outdir, exist_ok=True)
    full_out = os.path.join(outdir, f"agg_eff_{path_name}_vs_{var}.png")
    c.SaveAs(full_out)
    c.SaveAs(full_out.replace(".png", ".pdf"))

# Draw plots for each path separately
for path_name in trigger_paths.keys():
    for var in VARIABLES:
        if graphs[path_name][var]:
            draw_overlay(graphs[path_name][var], var, path_name, args.outdir)
