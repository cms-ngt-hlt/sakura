import ROOT
import os
import argparse
import math

# --- ROOT Configuration ---
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gErrorIgnoreLevel = ROOT.kError

# --- Filter Definitions ---
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

def short_label(name):
    name = name.replace("hltEG32L1SingleEGOrEtFilter", "L1")
    name = name.replace("hltEle32WPTight", "")
    name = name.replace("Gsf", "")
    name = name.replace("Filter", "")
    return name

AVAILABLE_LABELS = ["total"] + [short_label(f) for f in filters[1:]]

# --- Argument Parsing ---
parser = argparse.ArgumentParser(
    description="Overlay HLT filter efficiencies vs. cumulative luminosity, "
                 "with points aggregated PER FILL (inverse-variance weighted "
                 "average of the per-run efficiencies) instead of per run."
)
parser.add_argument('--dirA', default='plots_HTS', help='First plots directory')
parser.add_argument('--labelA', default='HLTTestStand', help='Legend label for dirA')
parser.add_argument('--dirB', default='plots_NGT', help='Second plots directory')
parser.add_argument('--labelB', default='NGTDemonstrator', help='Legend label for dirB')
parser.add_argument('--regions', nargs='+', default=['EB', 'EE', 'EBplus', 'EBminus', 'EEplus', 'EEminus'])
parser.add_argument('--which', nargs='+', default=['total'], help=f"Filter curve(s) to overlay. 'all', or any of: {AVAILABLE_LABELS}")
parser.add_argument('--outdir', default='plots_overlay_HTS_NGT_perFill')
parser.add_argument('--lumi-csv', default='lumi_data.csv', help='Path to brilcalc per-LS CSV file (must contain run:fill in column 0)')
parser.add_argument('--quiet', '-q', action='store_true')
args = parser.parse_args()

# --- Helper Functions ---
def load_lumi_and_fill_data(csv_path):
    """
    Parses a brilcalc per-LS CSV file and returns:
      - run_lumi_map: Run -> cumulative recorded luminosity (/fb) at the END of that run
      - run_fill_map: Run -> Fill number

    Expects column 0 to be formatted as 'run:fill' (standard brilcalc per-LS output)
    and column 5 to be the recorded luminosity in /pb.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Lumi CSV '{csv_path}' not found. A luminosity CSV (with run:fill info) "
            f"is required for per-fill plots."
        )

    run_lumi_map = {}
    run_fill_map = {}
    cumulative_lumi = 0.0

    with open(csv_path, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) < 6:
                continue

            run_fill = parts[0].split(':')
            run = int(run_fill[0])
            if len(run_fill) < 2:
                raise ValueError(
                    f"Could not find a fill number in column 0 ('{parts[0]}') of '{csv_path}'. "
                    f"Expected the brilcalc 'run:fill' format."
                )
            fill = int(run_fill[1])

            recorded_lumi_pb = float(parts[5])
            recorded_lumi = recorded_lumi_pb / 1000.0  # /pb -> /fb

            cumulative_lumi += recorded_lumi
            run_lumi_map[run] = cumulative_lumi
            run_fill_map[run] = fill

    return run_lumi_map, run_fill_map

def build_fill_groups(run_fill_map):
    """
    Groups runs into fills, preserving run-number order. Returns an ordered
    list of (fill_number, [runs...]) tuples. Runs are assumed to be grouped
    contiguously by fill when sorted by run number (true for LHC fills).
    """
    runs_sorted = sorted(run_fill_map.keys())
    groups = []
    current_fill = None
    current_runs = []

    for run in runs_sorted:
        fill = run_fill_map[run]
        if fill != current_fill:
            if current_runs:
                groups.append((current_fill, current_runs))
            current_fill = fill
            current_runs = [run]
        else:
            current_runs.append(run)

    if current_runs:
        groups.append((current_fill, current_runs))

    return groups

def build_centered_fill_lumi_map(fill_groups, run_lumi_map):
    """
    Same centering idea as the per-run version, but applied at the fill
    level: fill F is placed at the midpoint between its own end-of-fill
    cumulative luminosity and the following fill's end-of-fill cumulative
    luminosity. The last fill is extrapolated using the previous spacing.
    Returns Fill -> centered cumulative lumi (/fb).
    """
    fill_end_lumi = [(fill, run_lumi_map[runs[-1]]) for fill, runs in fill_groups]
    centered = {}

    for i, (fill, L1) in enumerate(fill_end_lumi):
        if i + 1 < len(fill_end_lumi):
            L2 = fill_end_lumi[i + 1][1]
        else:
            if i > 0:
                prev_L = fill_end_lumi[i - 1][1]
                L2 = L1 + (L1 - prev_L)
            else:
                L2 = L1
        centered[fill] = (L1 + L2) / 2.0

    return centered

def extract_run_values(g_run):
    """Reads a per-run TGraphAsymmErrors and returns Run -> (y, errlow, errhigh)."""
    values = {}
    for i in range(g_run.GetN()):
        run = int(g_run.GetX()[i])
        y = g_run.GetY()[i]
        errlow = g_run.GetErrorYlow(i)
        errhigh = g_run.GetErrorYhigh(i)
        values[run] = (y, errlow, errhigh)
    return values

def combine_fill_points(run_values, runs_in_fill, min_sigma=1e-6):
    """
    Inverse-variance weighted combination of the per-run efficiency values
    belonging to one fill. Uses the average of the low/high error as a
    symmetric proxy sigma_i for weighting, since the underlying pass/total
    counts aren't available here -- only the already-computed per-run
    efficiency and its error. Returns (y_combined, err_combined), or None
    if no runs in this fill have a valid point in run_values.

    NOTE: this is an approximation. If per-run pass/total counts are
    available upstream, summing counts and recomputing a Clopper-Pearson
    interval would be statistically more rigorous than combining errors.
    """
    present = [run_values[r] for r in runs_in_fill if r in run_values]
    if not present:
        return None

    if len(present) == 1:
        y, errlow, errhigh = present[0]
        return y, (errlow, errhigh)

    weights = []
    weighted_y_sum = 0.0
    weight_sum = 0.0
    for y, errlow, errhigh in present:
        sigma = max((errlow + errhigh) / 2.0, min_sigma)
        w = 1.0 / (sigma * sigma)
        weights.append(w)
        weighted_y_sum += w * y
        weight_sum += w

    y_combined = weighted_y_sum / weight_sum
    err_combined = math.sqrt(1.0 / weight_sum)
    return y_combined, (err_combined, err_combined)

def build_per_fill_graph(g_run, fill_groups, run_lumi_map, centered_fill_lumi_map, name_suffix="_perFill"):
    """
    Builds a new TGraphAsymmErrors with one point per fill: x = centered
    cumulative luminosity (/fb) for that fill, y = inverse-variance
    weighted average efficiency across the runs of that fill present in
    g_run, with symmetric combined errors.
    """
    run_values = extract_run_values(g_run)

    xs, ys, exl, exh, eyl, eyh = [], [], [], [], [], []
    for fill, runs_in_fill in fill_groups:
        combined = combine_fill_points(run_values, runs_in_fill)
        if combined is None:
            continue
        y, (errlow, errhigh) = combined
        xs.append(centered_fill_lumi_map[fill])
        ys.append(y)
        exl.append(0.0)
        exh.append(0.0)
        eyl.append(errlow)
        eyh.append(errhigh)

    n = len(xs)
    g_fill = ROOT.TGraphAsymmErrors(n)
    g_fill.SetName(g_run.GetName() + name_suffix)
    for i in range(n):
        g_fill.SetPoint(i, xs[i], ys[i])
        g_fill.SetPointEXlow(i, exl[i])
        g_fill.SetPointEXhigh(i, exh[i])
        g_fill.SetPointEYlow(i, eyl[i])
        g_fill.SetPointEYhigh(i, eyh[i])

    return g_fill

def graph_name_for(region, which):
    if which.lower() == 'total':
        return f"g_{region}_total"
    for i in range(1, len(filters)):
        if short_label(filters[i]) == which:
            return f"g_{region}_{i}"
    return None

def find_primitive(pad, name):
    obj = pad.FindObject(name)
    if obj and obj.GetName() == name:
        return obj
    for prim in pad.GetListOfPrimitives():
        if isinstance(prim, ROOT.TVirtualPad):
            found = find_primitive(prim, name)
            if found:
                return found
    return None

def get_graph(rootfile_path, gname):
    f = ROOT.TFile.Open(rootfile_path)
    if not f or f.IsZombie():
        return None
    c = f.Get("c")
    if not c:
        f.Close()
        return None
    obj = find_primitive(c, gname)
    if not obj:
        f.Close()
        return None
    g = obj.Clone(gname + "_clone")
    f.Close()
    return g

def overlay(region, which_label, gA, gB, x_title="Cumulative Recorded Luminosity (fb^{-1})", suffix=""):
    gA.SetMarkerColor(ROOT.kRed + 1)
    gA.SetLineColor(ROOT.kRed + 1)
    gA.SetMarkerStyle(20)

    gB.SetMarkerColor(ROOT.kBlue + 1)
    gB.SetLineColor(ROOT.kBlue + 1)
    gB.SetMarkerStyle(21)

    c = ROOT.TCanvas(f"c_overlay_{region}_{which_label}{suffix}", "", 1000, 700)
    c.SetRightMargin(0.05)

    y_min, y_max = 1.0, 0.0
    x_min, x_max = float('inf'), float('-inf')

    for g in (gA, gB):
        if g.GetN() == 0: continue
        for i in range(g.GetN()):
            x = g.GetX()[i]
            y = g.GetY()[i]
            yerr = g.GetErrorYhigh(i)

            if y > 0 and y < y_min: y_min = y
            if y + yerr > y_max: y_max = y + yerr
            if x < x_min: x_min = x
            if x > x_max: x_max = x

    if x_min == float('inf'): x_min, x_max = 0, 1

    gA.SetTitle(f"{region}: {which_label} efficiency vs {x_title.split(' (')[0]} (per-fill average)")
    gA.GetXaxis().SetTitle(x_title)
    gA.GetYaxis().SetTitle("Filter Efficiency")

    x_padding = (x_max - x_min) * 0.05
    if x_padding == 0: x_padding = 1.0

    gA.GetXaxis().SetLimits(x_min - x_padding, x_max + x_padding)
    gA.GetYaxis().SetRangeUser(y_min * 0.94, y_max * 1.05)

    gA.Draw("AP")
    gB.Draw("P SAME")

    legend = ROOT.TLegend(0.65, 0.15, 0.92, 0.30)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.AddEntry(gA, args.labelA, "p")
    legend.AddEntry(gB, args.labelB, "p")
    legend.Draw()

    os.makedirs(args.outdir, exist_ok=True)
    safe_label = which_label.replace(" ", "_")
    outname = os.path.join(args.outdir, f"overlay_{region}_{safe_label}{suffix}.png")

    c.SaveAs(outname)
    c.SaveAs(outname.replace(".png", ".pdf"))
    if not args.quiet:
        print(f"Saved {outname}")


# --- Main Execution ---
if __name__ == "__main__":
    run_lumi_map, run_fill_map = load_lumi_and_fill_data(args.lumi_csv)
    fill_groups = build_fill_groups(run_fill_map)
    centered_fill_lumi_map = build_centered_fill_lumi_map(fill_groups, run_lumi_map)

    if not args.quiet:
        print(f"Loaded {len(run_lumi_map)} runs grouped into {len(fill_groups)} fills.")

    which_list = AVAILABLE_LABELS if args.which == ['all'] else args.which

    for region in args.regions:
        fileA = os.path.join(args.dirA, f"step_efficiency_{region}.root")
        fileB = os.path.join(args.dirB, f"step_efficiency_{region}.root")

        if not (os.path.exists(fileA) and os.path.exists(fileB)):
            if not args.quiet:
                print(f"Skipping {region}: missing file(s)")
            continue

        for which in which_list:
            gname = graph_name_for(region, which)
            if gname is None:
                print(f"Unknown filter label '{which}'. Available: {AVAILABLE_LABELS}")
                continue

            gA = get_graph(fileA, gname)
            gB = get_graph(fileB, gname)

            if not gA or not gB:
                if not args.quiet:
                    print(f"  {region}/{which}: not found in one or both files")
                continue

            gA_fill = build_per_fill_graph(gA, fill_groups, run_lumi_map, centered_fill_lumi_map)
            gB_fill = build_per_fill_graph(gB, fill_groups, run_lumi_map, centered_fill_lumi_map)

            overlay(region, which, gA_fill, gB_fill, suffix="_vs_Lumi_perFill")
