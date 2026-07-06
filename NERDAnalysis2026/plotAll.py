import ROOT
import os
import argparse

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gErrorIgnoreLevel = ROOT.kError

parser = argparse.ArgumentParser()
parser.add_argument('--infile', default='out_barrelendcaps_NGT.root', help='Input ROOT file with the histograms')
parser.add_argument('--outdir', default='plots_filter_eff_NGT', help='Directory to save plots')
parser.add_argument('--label', default='NGTDemonstrator (from HLT DQM T&P)', help='Annotation label drawn on each plot')
parser.add_argument('--quiet', '-q', action='store_true', help='Suppress printout messages')
args = parser.parse_args()

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

colors = [
    ROOT.kRed + 1, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 7,
    ROOT.kViolet + 1, ROOT.kOrange + 3, ROOT.kMagenta + 2, ROOT.kAzure + 2,
    ROOT.kPink + 9, ROOT.kTeal + 2, ROOT.kSpring + 9, ROOT.kGray + 3
]

def short_label(name):
    name = name.replace("hltEG32L1SingleEGOrEtFilter", "L1")
    name = name.replace("hltEle32WPTight", "")
    name = name.replace("Gsf", "")
    name = name.replace("Filter", "")
    return name

def load_histograms(file, region):
    histos = {}
    for filt in filters:
        hname = f"histos{region}_countsvsrun_{filt}"
        h = file.Get(hname)
        if h:
            histos[filt] = h.Clone(f"{region}_{filt}")
            h.SetDirectory(0)
    return histos

def compute_efficiencies(histos, region_label):
    effs = []

    for i in range(1, len(filters)):
        num = histos.get(filters[i])
        denom = histos.get(filters[i - 1])
        if not num or not denom:
            continue

        g = ROOT.TGraphAsymmErrors()
        g.BayesDivide(num, denom)
        # Shift X points back by 0.5 to get correct run number
        for j in range(g.GetN()):
            x = g.GetX()[j]
            y = g.GetY()[j]
            ex_low = g.GetErrorXlow(j)
            ex_high = g.GetErrorXhigh(j)
            ey_low = g.GetErrorYlow(j)
            ey_high = g.GetErrorYhigh(j)
            g.SetPoint(j, x - 0.5, y)
            g.SetPointEXlow(j, ex_low)
            g.SetPointEXhigh(j, ex_high)
            g.SetPointEYlow(j, ey_low)
            g.SetPointEYhigh(j, ey_high)
        g.SetName(f"g_{region_label}_{i}")
        g.SetLineWidth(3)
        g.SetMarkerStyle(20)
        g.SetMarkerSize(1.0)
        g.SetMarkerColor(colors[i % len(colors)])
        g.SetLineColor(colors[i % len(colors)])

        label = short_label(filters[i])
        effs.append((label, g))

    # Total efficiency (last filter / first)
    num = histos.get(filters[-1])
    denom = histos.get(filters[0])
    if num and denom:
        g_total = ROOT.TGraphAsymmErrors()
        g_total.BayesDivide(num, denom)
        g_total.SetName(f"g_{region_label}_total")
        g_total.SetLineWidth(4)
        g_total.SetMarkerColor(ROOT.kBlack)
        g_total.SetLineColor(ROOT.kBlack)
        g_total.SetMarkerStyle(22)
        g_total.SetMarkerSize(1.2)
        g_total.SetTitle("Total")
        effs.append(("Total", g_total))

    return effs

def draw_overlay(effs, title, outname, outdir):
    c = ROOT.TCanvas("c", "", 1000, 700)
    c.SetRightMargin(0.2)

    pad = ROOT.TPad("pad", "", 0.0, 0.0, 0.85, 1.0)
    pad.SetBottomMargin(0.12)
    pad.Draw()
    pad.cd()
    c._pad = pad

    # Auto y-axis range
    y_min = 1.0
    y_max = 0.0
    latest_run = 0
    for _, g in effs:
        for i in range(g.GetN()):
            x = g.GetX()[i]
            y = g.GetY()[i]
            yerr = g.GetErrorYhigh(i)
            if y > 0 and y < y_min:
                y_min = y
            if y + yerr > y_max:
                y_max = y + yerr
            if x > latest_run:
                latest_run = int(x)
    # Draw each graph
    for i, (label, g) in enumerate(effs):
        g.GetXaxis().SetTitle("Run")
        g.GetYaxis().SetTitle("Filter Efficiency")
        g.GetXaxis().SetTitleOffset(1.2)
        g.GetYaxis().SetTitleOffset(1.3)
        g.GetXaxis().SetLabelSize(0.04)
        g.GetYaxis().SetLabelSize(0.04)
        g.SetMinimum(y_min * 0.94)
        g.SetMaximum(y_max * 1.05)
        if i == 0:
            g.SetTitle(f"{title}")  # Set title on first graph only
        draw_opt = "AP" if i == 0 else "P SAME"
        g.Draw(draw_opt)

    # Annotation
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextColor(ROOT.kBlack)
    latex.DrawLatex(0.15, 0.87, "{" + args.label + "}")
    latex.SetTextSize(0.032)
    latex.DrawLatex(0.10, 0.03, f"#it{{Updated till Run {latest_run}}}")

    # Legend
    c.cd()
    legend = ROOT.TLegend(0.76, 0.25, 0.99, 0.95)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)
    for label, g in effs:
        legend.AddEntry(g, label, "p")
    legend.Draw()

    os.makedirs(outdir, exist_ok=True)
    full_out = os.path.join(outdir, outname)
    c.SaveAs(full_out)
    c.SaveAs(full_out.replace(".png", ".pdf"))  # PDF
    c.SaveAs(full_out.replace(".png", ".root"))  # ROOT
    if not args.quiet:
        print(f"Saved: {full_out}")

# --- Main ---
if __name__ == "__main__":
    f = ROOT.TFile(args.infile)
    if f.IsZombie() or not f.IsOpen():
        raise SystemExit(f"Could not open input file: {args.infile}")

    for region in ["EB", "EE", "EBplus", "EBminus", "EEplus", "EEminus"]:
        hists = load_histograms(f, region)
        effs = compute_efficiencies(hists, region)
        draw_overlay(
            effs,
            f"{region}: Filter Efficiency vs Run",
            f"step_efficiency_{region}.png",
            args.outdir
        )
    f.Close()
