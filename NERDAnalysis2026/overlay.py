import ROOT
import os
import argparse

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gErrorIgnoreLevel = ROOT.kError

# Same filter list/short_label as the original scripts, needed to map
# a human-readable filter name back to the graph index it was saved under.
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

parser = argparse.ArgumentParser()
parser.add_argument('--dirA', default='plots_HTS', help='First plots directory')
parser.add_argument('--labelA', default='HLTTestStand', help='Legend label for dirA')
parser.add_argument('--dirB', default='plots_NGT', help='Second plots directory')
parser.add_argument('--labelB', default='NGTDemonstrator', help='Legend label for dirB')
parser.add_argument('--regions', nargs='+',
                     default=['EB', 'EE', 'EBplus', 'EBminus', 'EEplus', 'EEminus'])
parser.add_argument('--which', nargs='+', default=['total'],
                     help=f"Filter curve(s) to overlay. 'all', or any of: {AVAILABLE_LABELS}")
parser.add_argument('--outdir', default='plots_overlay_HTS_NGT')
parser.add_argument('--quiet', '-q', action='store_true')
args = parser.parse_args()

def graph_name_for(region, which):
    if which.lower() == 'total':
        return f"g_{region}_total"
    for i in range(1, len(filters)):
        if short_label(filters[i]) == which:
            return f"g_{region}_{i}"
    return None

def find_primitive(pad, name):
    """Recursively search a canvas/pad and any nested sub-pads for an
    object by name, since graphs live inside a subpad, not the canvas itself."""
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
    g = obj.Clone(gname + "_clone")  # detach from file before closing it
    f.Close()
    return g

def overlay(region, which_label, gA, gB):
    gA.SetMarkerColor(ROOT.kRed + 1)
    gA.SetLineColor(ROOT.kRed + 1)
    gA.SetMarkerStyle(20)

    gB.SetMarkerColor(ROOT.kBlue + 1)
    gB.SetLineColor(ROOT.kBlue + 1)
    gB.SetMarkerStyle(21)

    c = ROOT.TCanvas("c_overlay", "", 1000, 700)
    c.SetRightMargin(0.05)

    y_min, y_max = 1.0, 0.0
    for g in (gA, gB):
        for i in range(g.GetN()):
            y = g.GetY()[i]
            yerr = g.GetErrorYhigh(i)
            if y > 0 and y < y_min:
                y_min = y
            if y + yerr > y_max:
                y_max = y + yerr

    gA.SetTitle(f"{region}: {which_label} efficiency vs Run")
    gA.GetXaxis().SetTitle("Run")
    gA.GetYaxis().SetTitle("Filter Efficiency")
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
    outname = os.path.join(args.outdir, f"overlay_{region}_{safe_label}.png")
    c.SaveAs(outname)
    c.SaveAs(outname.replace(".png", ".pdf"))
    if not args.quiet:
        print(f"Saved {outname}")

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
                print(f"  {region}/{which}: not found in one or both files "
                      f"(A={bool(gA)}, B={bool(gB)})")
            continue

        overlay(region, which, gA, gB)
