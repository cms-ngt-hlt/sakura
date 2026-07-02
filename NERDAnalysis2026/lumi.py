import ROOT
import os
import argparse
import csv

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
    "hltEle32WPTightGsfTrackIsoFilter"
]

def short_label(name):
    name = name.replace("hltEG32L1SingleEGOrEtFilter", "L1")
    name = name.replace("hltEle32WPTight", "")
    name = name.replace("Gsf", "")
    name = name.replace("Filter", "")
    return name

AVAILABLE_LABELS = ["total"] + [short_label(f) for f in filters[1:]]

# --- Argument Parsing ---
parser = argparse.ArgumentParser()
parser.add_argument('--dirA', default='plots_HTS', help='First plots directory')
parser.add_argument('--labelA', default='HLTTestStand', help='Legend label for dirA')
parser.add_argument('--dirB', default='plots_NGT', help='Second plots directory')
parser.add_argument('--labelB', default='NGTDemonstrator', help='Legend label for dirB')
parser.add_argument('--regions', nargs='+', default=['EB', 'EE', 'EBplus', 'EBminus', 'EEplus', 'EEminus'])
parser.add_argument('--which', nargs='+', default=['total'], help=f"Filter curve(s) to overlay. 'all', or any of: {AVAILABLE_LABELS}")
parser.add_argument('--outdir', default='plots_overlay_HTS_NGT')
parser.add_argument('--lumi-csv', default='lumi_data.csv', help='Path to brilcalc CSV file for lumi plots')
parser.add_argument('--quiet', '-q', action='store_true')
args = parser.parse_args()

# --- Helper Functions ---
def load_lumi_data(csv_path):
    """Parses brilcalc CSV and returns a dictionary mapping Run -> Cumulative Lumi."""
    run_lumi_map = {}
    cumulative_lumi = 0.0
    
    if not os.path.exists(csv_path):
        if not args.quiet:
            print(f"Warning: Lumi CSV '{csv_path}' not found. Lumi plots will be skipped.")
        return None
        
    with open(csv_path, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) < 6:
                continue
            
            run = int(parts[0].split(':')[0])
            recorded_lumi = float(parts[5])
            
            cumulative_lumi += recorded_lumi
            run_lumi_map[run] = cumulative_lumi
            
    return run_lumi_map

def convert_to_lumi_graph(g_run, run_lumi_map):
    """Clones a graph and replaces X-axis run numbers with cumulative luminosity."""
    g_lumi = g_run.Clone(g_run.GetName() + "_lumi")
    points_to_remove = []
    
    for i in range(g_lumi.GetN()):
        run = int(g_lumi.GetX()[i])
        if run in run_lumi_map:
            g_lumi.SetPoint(i, run_lumi_map[run], g_lumi.GetY()[i])
        else:
            points_to_remove.append(i)
            
    # Remove from back-to-front to avoid index shifting issues
    for i in reversed(points_to_remove):
        g_lumi.RemovePoint(i)
        
    return g_lumi

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

def overlay(region, which_label, gA, gB, x_title="Run", suffix=""):
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

    # Failsafe if graph is empty
    if x_min == float('inf'): x_min, x_max = 0, 1

    gA.SetTitle(f"{region}: {which_label} efficiency vs {x_title.split(' (')[0]}")
    gA.GetXaxis().SetTitle(x_title)
    gA.GetYaxis().SetTitle("Filter Efficiency")
    
    x_padding = (x_max - x_min) * 0.05
    if x_padding == 0: x_padding = 1.0 # Protect against single-point graphs
    
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
    lumi_map = load_lumi_data(args.lumi_csv)
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

            # 1. Plot Original (vs. Run)
            overlay(region, which, gA, gB, x_title="Run Number", suffix="_vs_Run")

            # 2. Plot Lumi Converted (vs. Cumulative Luminosity)
            if lumi_map:
                gA_lumi = convert_to_lumi_graph(gA, lumi_map)
                gB_lumi = convert_to_lumi_graph(gB, lumi_map)
                
                # We use ROOT's LaTeX syntax ^{} for the superscript in pb^-1
                overlay(region, which, gA_lumi, gB_lumi, 
                        x_title="Cumulative Recorded Luminosity (pb^{-1})", 
                        suffix="_vs_Lumi")
