import ROOT
import os
import re
import argparse

ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

filters = [
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
    "hltEle32WPTightGsfTrackIsoFilter",
    "hltDiEG25CaloIdLClusterShapeUnseededFilter",
    "hltDiEle25CaloIdLMWPMS2UnseededFilter",
    "hltDiEle25CaloIdLPixelMatchUnseededFilter"
]

#VARIABLES = ["pt", "eta", "phi"]
VARIABLES = ["eta", "ptEB", "ptEE", "phiEB", "phiEE"]

colors = [
    ROOT.kRed + 1, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 7,
    ROOT.kViolet + 1, ROOT.kOrange + 3, ROOT.kMagenta + 2, ROOT.kAzure + 2,
    ROOT.kPink + 9, ROOT.kTeal + 2, ROOT.kSpring + 9, ROOT.kGray + 3
]

parser = argparse.ArgumentParser()
parser.add_argument('--folder', default='dqm_files', help='Folder with input DQM root files')
parser.add_argument('--pattern', default=None,
                     help='Optional substring filter on filenames, e.g. "NGT" or "HLTTestStand". '
                          'Default: use every .root file in --folder.')
parser.add_argument('--no-fakes', action='store_true', help='Disable sideband fake subtraction')
parser.add_argument('--outfile', default='aggregated_efficiency.root')
parser.add_argument('--outdir', default='plots_aggregated_eff')
parser.add_argument('--label', default='Aggregated over all input runs')
parser.add_argument('--quiet', '-q', action='store_true')
args = parser.parse_args()

# Mass window used for signal counting (same as the run-vs-efficiency script)
firstbin_mass, lastbin_mass = 21, 41   # 81-101 GeV
sideband_bins = [(0, 5), (55, 60)]      # only used if fake subtraction is enabled

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
    h =  f.Get(folder + f"stdTag_{filt}_{var}")
    if h:
        return h
    h = f.Get(folder + f"stdTagAndEle25MW_{filt}_{var}")
    return h


def project_signal_minus_sideband(h2, name_tag, forfakes=True):
    """Project a TH2(variable, mass) onto the variable axis, integrating the
    signal mass window and optionally subtracting sideband-estimated fakes
    bin-by-bin (mirrors the per-run fake subtraction in get_counts)."""
    h_sig = h2.ProjectionX(name_tag + "_sig", firstbin_mass, lastbin_mass)
    h_sig.SetDirectory(0)
    if not forfakes:
        return h_sig

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

# --- Step 1: aggregate raw 2D histograms across all files ---
aggregated = {var: {filt: None for filt in filters} for var in VARIABLES}
n_files_used = 0

for fname in sorted(os.listdir(args.folder)):
    if fname.startswith('.'):
        continue
    if not fname.endswith(".root"):
        continue
    if args.pattern and args.pattern not in fname:
        continue
    run = extract_run_number(fname)
    if run is None:
        if not args.quiet:
            print(f"Skipping {fname}: no run number found")
        continue

    f = ROOT.TFile.Open(os.path.join(args.folder, fname))
    if not f or f.IsZombie():
        if not args.quiet:
            print(f"Skipping {fname}: could not open file")
        continue

    used_this_file = False
    for var in VARIABLES:
        for filt in filters:
            h2 = get_th2(f, run, filt, var)
            if not h2:
                continue
            h2c = h2.Clone(f"{var}_{filt}_run{run}")
            h2c.SetDirectory(0)
            if aggregated[var][filt] is None:
                aggregated[var][filt] = h2c
            else:
                aggregated[var][filt].Add(h2c)
            used_this_file = True
    f.Close()

    if used_this_file:
        n_files_used += 1
        if not args.quiet:
            print(f"Added {fname} (run {run})")

if n_files_used == 0:
    raise SystemExit(f"No usable files found in {args.folder} (pattern={args.pattern})")
if not args.quiet:
    print(f"Aggregated {n_files_used} files")

# --- Step 2: project each aggregated TH2 onto its variable axis ---
projected = {var: {} for var in VARIABLES}
for var in VARIABLES:
    for filt in filters:
        h2 = aggregated[var][filt]
        if h2 is None:
            if not args.quiet:
                print(f"Warning: stdTag_{filt}_{var} not found in any input file")
            continue
        projected[var][filt] = project_signal_minus_sideband(h2, f"{var}_{filt}", forfakes=not args.no_fakes)

# --- Step 3: build efficiency graphs per variable ---
out = ROOT.TFile(args.outfile, "RECREATE")
graphs_by_var = {var: [] for var in VARIABLES}

for var in VARIABLES:
    hmap = projected[var]
    for i in range(1, len(filters)):
        num, denom = hmap.get(filters[i]), hmap.get(filters[i - 1])
        if num is None or denom is None:
            continue
        num_c, n_clamped = clamp_to_denominator(num, denom)

        if n_clamped and not args.quiet:
            print(f"[{var}] {short_label(filters[i])}: clamped {n_clamped} bin(s)")
        g = ROOT.TGraphAsymmErrors()
        g.BayesDivide(num_c, denom)
        g.SetName(f"g_{var}_{i}")
        g.SetLineWidth(3)
        g.SetMarkerStyle(20)
        g.SetMarkerColor(colors[i % len(colors)])
        g.SetLineColor(colors[i % len(colors)])
        g.Write()
        graphs_by_var[var].append((short_label(filters[i]), g))

    num, denom = hmap.get(filters[-1]), hmap.get(filters[0])
    if num is not None and denom is not None:
        num_c, n_clamped = clamp_to_denominator(num, denom)
        if n_clamped and not args.quiet:
            print(f"[{var}] Total: clamped {n_clamped} bin(s)")
        g_total = ROOT.TGraphAsymmErrors()
        g_total.BayesDivide(num_c, denom)
        g_total.SetName(f"g_{var}_total")
        g_total.SetLineWidth(4)
        g_total.SetMarkerColor(ROOT.kBlack)
        g_total.SetLineColor(ROOT.kBlack)
        g_total.SetMarkerStyle(22)
        g_total.Write()
        graphs_by_var[var].append(("Total", g_total))

out.Close()
if not args.quiet:
    print(f"Saved graphs to {args.outfile}")

# --- Step 4: overlay plots per variable ---
def draw_overlay(effs, var, outdir):
    c = ROOT.TCanvas(f"c_{var}", "", 1000, 700)
    c.SetRightMargin(0.2)
    pad = ROOT.TPad("pad", "", 0.0, 0.0, 0.85, 1.0)
    pad.SetBottomMargin(0.12)
    pad.Draw()
    pad.cd()
    c._pad = pad

    y_min, y_max = 1.0, 0.0
    for _, g in effs:
        for i in range(g.GetN()):
            y = g.GetY()[i]
            yerr = g.GetErrorYhigh(i)
            if y > 0 and y < y_min:
                y_min = y
            if y + yerr > y_max:
                y_max = y + yerr

    for i, (label, g) in enumerate(effs):
        g.GetXaxis().SetTitle(var)
        g.GetYaxis().SetTitle("Filter Efficiency")
        g.SetMinimum(y_min * 0.94)
        g.SetMaximum(y_max * 1.05)
        if i == 0:
            g.SetTitle(f"Filter efficiency vs {var}")
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
    full_out = os.path.join(outdir, f"agg_efficiency_vs_{var}.png")
    c.SaveAs(full_out)
    c.SaveAs(full_out.replace(".png", ".pdf"))
    if not args.quiet:
        print(f"Saved {full_out}")

for var in VARIABLES:
    if graphs_by_var[var]:
        draw_overlay(graphs_by_var[var], var, args.outdir)
