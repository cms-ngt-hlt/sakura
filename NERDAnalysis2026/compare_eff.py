import ROOT
import os
import argparse

ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

parser = argparse.ArgumentParser(description="Overlay efficiency graphs from two aggregated ROOT files.")
parser.add_argument('--f1', required=True, help='First input ROOT file (e.g., aggregated_NGT.root)')
parser.add_argument('--l1', required=True, help='Legend label for first file (e.g., "NGT")')
parser.add_argument('--f2', required=True, help='Second input ROOT file (e.g., aggregated_HTS.root)')
parser.add_argument('--l2', required=True, help='Legend label for second file (e.g., "HTS TestStand")')
parser.add_argument('--outdir', default='plots_comparison', help='Directory to save overlaid plots')
args = parser.parse_args()

def main():
    os.makedirs(args.outdir, exist_ok=True)

    file1 = ROOT.TFile.Open(args.f1)
    file2 = ROOT.TFile.Open(args.f2)

    if not file1 or file1.IsZombie() or not file2 or file2.IsZombie():
        raise SystemExit("Error: Could not open one or both input ROOT files.")

    # Get a list of all graph names from the first file
    keys = file1.GetListOfKeys()
    graph_names = [k.GetName() for k in keys if k.ReadObj().InheritsFrom("TGraphAsymmErrors")]

    if not graph_names:
        print(f"No TGraphAsymmErrors found in {args.f1}.")
        return

    for gname in graph_names:
        g1 = file1.Get(gname)
        g2 = file2.Get(gname)

        if not g1 or not g2:
            continue # Skip if the graph doesn't exist in both files

        c = ROOT.TCanvas(f"c_{gname}", "", 800, 600)
        c.SetRightMargin(0.05)
        c.SetLeftMargin(0.12)
        c.SetBottomMargin(0.12)
        c.SetGridy()

        # Styling for File 1 (e.g., NGT)
        g1.SetLineColor(ROOT.kBlue + 1)
        g1.SetMarkerColor(ROOT.kBlue + 1)
        g1.SetMarkerStyle(20)
        g1.SetLineWidth(2)

        # Styling for File 2 (e.g., HTS)
        g2.SetLineColor(ROOT.kRed + 1)
        g2.SetMarkerColor(ROOT.kRed + 1)
        g2.SetMarkerStyle(21)
        g2.SetLineWidth(2)

        # Determine Y-axis range
        y_min = 1.0
        for g in [g1, g2]:
            for i in range(g.GetN()):
                y = g.GetY()[i]
                if 0 < y < y_min:
                    y_min = y
        
        g1.SetMaximum(1.05)
        g1.SetMinimum(y_min * 0.9)
        
        # Clean up the graph title to look nice
        clean_title = gname.replace("g_", "Efficiency: ").replace("_", " ")
        g1.SetTitle(clean_title)
        g1.GetYaxis().SetTitle("Efficiency")
        g1.GetXaxis().SetTitle("Variable") # You can extract the variable from gname if needed

        # Draw
        g1.Draw("AP")
        g2.Draw("P SAME")

        # Legend
        leg = ROOT.TLegend(0.65, 0.2, 0.9, 0.35)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.AddEntry(g1, args.l1, "lp")
        leg.AddEntry(g2, args.l2, "lp")
        leg.Draw()

        # Save
        out_path = os.path.join(args.outdir, f"compare_{gname}.png")
        c.SaveAs(out_path)
        c.SaveAs(out_path.replace(".png", ".pdf"))

    print(f"Comparison plots saved to {args.outdir}/")

if __name__ == "__main__":
    main()
