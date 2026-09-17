#!/usr/bin/env python3
"""
Minimal PyROOT replacement for NGT_Studies_2025G.ipynb.

Fills TnP pass/fail histograms from Reference/Target ntuples and writes
efficiency ratio plots as ROOT macros (.C) and PNGs.

Usage (CMSSW or any ROOT+Python):
  python3 plot_NGT_Studies_2025G_pyroot.py
  python3 plot_NGT_Studies_2025G_pyroot.py -o /path/to/outdir
"""

from __future__ import annotations

import argparse
import os
from array import array
from ctypes import c_double

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetErrorX(0.5)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetEndErrorSize(0)
ROOT.gStyle.SetMarkerStyle(20)
ROOT.gStyle.SetTextFont(42)
ROOT.gStyle.SetLabelFont(42, "XYZ")
ROOT.gStyle.SetTitleFont(42, "XYZ")
ROOT.gStyle.SetLegendFont(42)

# ---------------------------------------------------------------------------
# Inputs / outputs
# ---------------------------------------------------------------------------
TREE = "tnpEleTrig/fitter_tree"
NTUPLES = {
    "Reference": "/afs/cern.ch/work/s/ssaumya/public/ForNGT/Ntuples/tnpNtuple_Reference_Set3.root",
    "Target": "/afs/cern.ch/work/s/ssaumya/public/ForNGT/Ntuples/tnpNtuple_Target_Set3.root",
}
DEFAULT_OUT = "/eos/user/m/mzarucki/www/2026/NGT/SAKURA/NERD/efficiencies//Set3"

HLT_PATHS = {
    "Ele30": "passHLTEle30WPTightGsfTrackIsoFilter",
    "Ele32": "passHLTEle32WPTightGsfTrackIsoFilter",
    "Ele115": "passHLTEle115CaloIdVTGsfTrkIdTGsfDphiFilter",
    "Ele135": "passHLTEle135CaloIdVTGsfTrkIdTGsfDphiFilter",
    "Ele23Ele12Leg1": "passHLTEle23Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg1Filter",
    "Ele23Ele12Leg2": "passHLTEle23Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg2Filter",
    "DoubleEle33SeededLeg": "passHLTEle33CaloIdLMWPMS2Filter",
    "DoubleEle33UnseededLeg": "passHLTDiEle33CaloIdLMWPMS2UnseededFilter",
}

PLATEAU_CUTS = {
    "Ele30": 35,
    "Ele32": 35,
    "Ele115": 120,
    "Ele135": 140,
    "Ele23Ele12Leg1": 25,
    "Ele23Ele12Leg2": 15,
    "DoubleEle33SeededLeg": 35,
    "DoubleEle33UnseededLeg": 35,
}

PT_BINS_LOW = [
    5, 10, 12, 14, 16, 18, 20, 23, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50, 60, 80, 100, 150, 250, 400,
]
PT_BINS_HIGH = [
    5, 10, 15, 20, 22, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50, 60, 80, 100,
    105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 200, 250, 300, 350, 400,
]
ETA_BINS = [
    -2.5, -2.4, -2.3, -2.2, -2.1, -2.0, -1.9, -1.8, -1.7, -1.566, -1.4442,
    -1.3, -1.2, -1.1, -1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1,
    0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3,
    1.4442, 1.566, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5,
]
PHI_BINS = [
    -3.32, -2.97, -2.62, -2.27, -1.92, -1.57, -1.22, -0.87, -0.52, -0.18,
    0.18, 0.52, 0.87, 1.22, 1.57, 1.92, 2.27, 2.62, 2.97, 3.32,
]

ETA_REGIONS_PT = {
    "barrel": (0.0, 1.4442),
    "endcap_loweta": (1.566, 2.0),
    "endcap_higheta": (2.0, 2.5),
}

# Selection matching ElectronTagNProbeFromNTuples defaults (notebook)
BASE_SELECTION = (
    "tag_Ele_pt > 35 && "
    "abs(tag_Ele_eta) < 2.5 && "
    "(abs(tag_Ele_eta) < 1.4442 || abs(tag_Ele_eta) > 1.566) && "
    "abs(el_eta) < 2.5 && "
    "tag_Ele_q * el_q == -1 && "
    "passingCutBasedTight122XV1 == 1 && "
    "abs(pair_mass - 91.1876) < 30 && "
    "el_pt > 5"
)

RLABEL = "2025G (13.6 TeV)"
COLOR_REF = ROOT.kBlack
COLOR_TGT = ROOT.TColor.GetColor(255, 51, 204)  # notebook #ff33cc


def _edges(bins):
    return array("d", bins)


def _trigger_title_lines(name: str):
    """Multi-line trigger label matching the notebook / mplhep legend."""
    short = (
        name.replace("Leg1", "")
        .replace("Leg2", "")
        .replace("SeededLeg", "")
        .replace("UnseededLeg", "")
    )
    if name in ("Ele32", "Ele30"):
        return [f"HLT_{short}_WPTight_Gsf"]
    if name in ("Ele115", "Ele135"):
        return [f"HLT_{short}_CaloIdVT_GsfTrkIdT"]
    if name == "DoubleEle33SeededLeg":
        return [f"HLT_{short}_CaloIdL_MW", "Seeded leg"]
    if name == "DoubleEle33UnseededLeg":
        return [f"HLT_{short}_CaloIdL_MW", "Unseeded leg"]
    # Ele23: Leg1/Leg2 on the same line as the HLT name (matches notebook snapshot)
    if name == "Ele23Ele12Leg1":
        return [f"HLT_{short}_CaloIdL_TrackIdL_IsoVL Leg1"]
    if name == "Ele23Ele12Leg2":
        return [f"HLT_{short}_CaloIdL_TrackIdL_IsoVL Leg2"]
    return [f"HLT_{short}"]


def _style_graph(g, color, marker_size=1.0):
    g.SetMarkerStyle(20)
    g.SetMarkerSize(marker_size)
    g.SetMarkerColor(color)
    g.SetLineColor(color)
    g.SetLineWidth(1)
    g.SetTitle("")


def fill_dataset(label: str, path: str) -> dict:
    """Fill pass/fail histograms for one ntuple.

    Returns
    -------
    dict: trigger -> region_key -> (h_pass, h_fail)
    """
    print(f"Filling {label} from {path}")
    df0 = ROOT.RDataFrame(TREE, path).Filter(BASE_SELECTION)

    # Keep bin arrays alive until RDF finishes (Histo1D takes a raw pointer)
    edge_store = []

    def bins_arr(bins):
        a = _edges(bins)
        edge_store.append(a)
        return a

    eta_arr = bins_arr(ETA_BINS)
    phi_arr = bins_arr(PHI_BINS)

    delayed = {}
    for trig, filt in HLT_PATHS.items():
        pt_bins = PT_BINS_HIGH if trig in ("Ele115", "Ele135") else PT_BINS_LOW
        pt_arr = bins_arr(pt_bins)
        plateau = PLATEAU_CUTS[trig]
        df = df0.Define(f"pass_{trig}", f"{filt} == 1")
        df_pass = df.Filter(f"pass_{trig}")
        df_fail = df.Filter(f"!pass_{trig}")
        df_plat = df.Filter(f"el_pt > {plateau}")
        df_plat_pass = df_plat.Filter(f"pass_{trig}")
        df_plat_fail = df_plat.Filter(f"!pass_{trig}")

        store = {}
        for region, (emin, emax) in ETA_REGIONS_PT.items():
            eta_cut = f"abs(el_eta) >= {emin} && abs(el_eta) < {emax}"
            hp = df_pass.Filter(eta_cut).Histo1D(
                (f"{label}_{trig}_pt_{region}_pass", "", len(pt_bins) - 1, pt_arr), "el_pt"
            )
            hf = df_fail.Filter(eta_cut).Histo1D(
                (f"{label}_{trig}_pt_{region}_fail", "", len(pt_bins) - 1, pt_arr), "el_pt"
            )
            store[f"pt_{region}"] = (hp, hf)

        store["eta"] = (
            df_plat_pass.Histo1D((f"{label}_{trig}_eta_pass", "", len(ETA_BINS) - 1, eta_arr), "el_eta"),
            df_plat_fail.Histo1D((f"{label}_{trig}_eta_fail", "", len(ETA_BINS) - 1, eta_arr), "el_eta"),
        )
        store["phi"] = (
            df_plat_pass.Histo1D((f"{label}_{trig}_phi_pass", "", len(PHI_BINS) - 1, phi_arr), "el_phi"),
            df_plat_fail.Histo1D((f"{label}_{trig}_phi_fail", "", len(PHI_BINS) - 1, phi_arr), "el_phi"),
        )
        delayed[trig] = store

    materialized = {}
    for trig, store in delayed.items():
        materialized[trig] = {}
        for key, (hp, hf) in store.items():
            hpass = hp.GetValue().Clone()
            hfail = hf.GetValue().Clone()
            hpass.SetDirectory(0)
            hfail.SetDirectory(0)
            materialized[trig][key] = (hpass, hfail)
        hp = materialized[trig]["pt_barrel"][0].Clone(f"{label}_{trig}_pt_combined_pass")
        hf = materialized[trig]["pt_barrel"][1].Clone(f"{label}_{trig}_pt_combined_fail")
        for r in ("pt_endcap_loweta", "pt_endcap_higheta"):
            hp.Add(materialized[trig][r][0])
            hf.Add(materialized[trig][r][1])
        materialized[trig]["pt_combined"] = (hp, hf)
    return materialized


def efficiency(hpass: ROOT.TH1, hfail: ROOT.TH1, name: str) -> ROOT.TGraphAsymmErrors:
    hall = hpass.Clone(f"{name}_all")
    hall.Add(hfail)
    hall.SetDirectory(0)
    if not ROOT.TEfficiency.CheckConsistency(hpass, hall):
        # fall back to empty graph
        return ROOT.TGraphAsymmErrors()
    teff = ROOT.TEfficiency(hpass, hall)
    g = teff.CreateGraph()
    g.SetName(name)
    return g


def divide_graphs(g_num: ROOT.TGraphAsymmErrors, g_den: ROOT.TGraphAsymmErrors) -> ROOT.TGraphAsymmErrors:
    """Target / Reference with simple relative-error propagation."""
    gr = ROOT.TGraphAsymmErrors()
    n = min(g_num.GetN(), g_den.GetN())
    x1, y1, x2, y2 = c_double(), c_double(), c_double(), c_double()
    ip = 0
    for i in range(n):
        g_num.GetPoint(i, x1, y1)
        g_den.GetPoint(i, x2, y2)
        num, den = y1.value, y2.value
        if den == 0:
            continue
        ratio = num / den
        # relative errors (asymm averaged into approx symmetric for ratio panel)
        en = 0.5 * (g_num.GetErrorYlow(i) + g_num.GetErrorYhigh(i))
        ed = 0.5 * (g_den.GetErrorYlow(i) + g_den.GetErrorYhigh(i))
        er = ratio * ((en / num) ** 2 + (ed / den) ** 2) ** 0.5 if num != 0 else 0.0
        exl = g_num.GetErrorXlow(i)
        exh = g_num.GetErrorXhigh(i)
        gr.SetPoint(ip, x1.value, ratio)
        gr.SetPointError(ip, exl, exh, er, er)
        ip += 1
    return gr


def plot_ratio(
    g_ref,
    g_tgt,
    *,
    out_base: str,
    xlabel: str,
    legend_lines,
    logx: bool = False,
    xmin: float = 10.0,
    xmax: float = 400.0,
    ymin: float = 0.3,
    ymax: float = 1.1,
    rymin: float = 0.8,
    rymax: float = 1.2,
    legend_loc: str = "right",
    hide_x_edge_labels: bool = False,
):
    # ~3:1 pad ratio with a small gap between efficiency and ratio
    c = ROOT.TCanvas(os.path.basename(out_base), "", 650, 650)
    pad1 = ROOT.TPad("pad1", "", 0.0, 0.283, 1.0, 1.0)
    pad2 = ROOT.TPad("pad2", "", 0.0, 0.00, 1.0, 0.281)
    for pad in (pad1, pad2):
        pad.SetLeftMargin(0.14)
        pad.SetRightMargin(0.04)
        pad.SetTicks(1, 1)
    pad1.SetTopMargin(0.10)   # room for "2025G (13.6 TeV)" above the frame
    pad1.SetBottomMargin(0.025)
    pad2.SetTopMargin(0.04)
    pad2.SetBottomMargin(0.38)
    pad1.Draw()
    pad2.Draw()

    # ---- upper pad ----
    pad1.cd()
    if logx:
        pad1.SetLogx()

    _style_graph(g_ref, COLOR_REF, marker_size=1.05)
    _style_graph(g_tgt, COLOR_TGT, marker_size=1.05)

    g_ref.GetXaxis().SetLimits(xmin, xmax)
    g_ref.GetXaxis().SetLabelSize(0)
    g_ref.GetXaxis().SetTitleSize(0)
    g_ref.GetXaxis().SetTickLength(0.03)
    if logx:
        g_ref.GetXaxis().SetMoreLogLabels()
        g_ref.GetXaxis().SetNoExponent()
    ay = g_ref.GetYaxis()
    ay.SetTitle("L1T + HLT Efficiency")
    ay.SetTitleSize(0.055)
    ay.SetTitleOffset(1.05)
    ay.SetLabelSize(0.045)
    ay.SetLabelOffset(0.005)
    ay.SetRangeUser(ymin, ymax)
    ay.SetNdivisions(510)
    ay.SetTickLength(0.025)
    g_ref.Draw("AP")
    g_tgt.Draw("P SAME")
    ROOT.gPad.Update()

    def ndc_to_user(x_ndc, y_ndc):
        """Map pad NDC -> object user coords (linear x even when pad is log-x)."""
        x = ROOT.gPad.GetX1() + x_ndc * (ROOT.gPad.GetX2() - ROOT.gPad.GetX1())
        y = ROOT.gPad.GetY1() + y_ndc * (ROOT.gPad.GetY2() - ROOT.gPad.GetY1())
        if ROOT.gPad.GetLogx():
            x = 10 ** x
        if ROOT.gPad.GetLogy():
            y = 10 ** y
        return x, y

    # CMS label: inside frame (top-left); energy label: outside frame (top-right)
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(11)
    latex.SetTextFont(61)
    latex.SetTextSize(0.085)
    latex.DrawLatex(0.16, 0.82, "CMS")
    latex.SetTextFont(52)
    latex.SetTextSize(0.050)
    # ROOT PDF italic (font 52) clips long strings ("Preliminary" -> "Pre").
    # Per-glyph #kern keeps italic look but avoids the clip bug.
    latex.DrawLatex(
        0.295,
        0.82,
        "P" + "".join(f"#kern[0]{{{ch}}}" for ch in "reliminary"),
    )
    latex.SetTextFont(42)
    latex.SetTextSize(0.050)
    latex.SetTextAlign(31)
    latex.DrawLatex(0.96, 0.93, RLABEL)

    # Legend placement: right (pt) or center (eta/phi) — title AND entries share the same center
    if legend_loc == "center":
        title_x = 0.55
    else:
        title_x = 0.68  # pT: slightly right
    title_y0 = 0.40
    dy = 0.045
    keep_objs = []
    for i, line in enumerate(legend_lines):
        tl = ROOT.TLatex()
        tl.SetNDC()
        tl.SetTextAlign(22)  # horizontally centered on title_x
        tl.SetTextFont(42)
        tl.SetTextSize(0.036)
        tl.DrawLatex(title_x, title_y0 - i * dy, line)
        keep_objs.append(tl)

    def _draw_legend_entry(y_ndc, color, label):
        """Marker + horiz/vert error bars + label, centered on title_x."""
        ex = 0.045
        ey = 0.022
        gap = 0.020
        # Optical width of "HLT"/"NGT" (~3 caps at text size 0.038). Shift the
        # (bar|gap|label) join left by half that width so the full entry
        # bbox — not just the gap — sits under the centered title.
        label_w = 0.060
        x_mid = title_x - label_w / 2.0
        x_sym = x_mid - ex - gap / 2.0
        x_lab = x_mid + gap / 2.0

        x0, y0 = ndc_to_user(x_sym, y_ndc)
        xL, _ = ndc_to_user(x_sym - ex, y_ndc)
        xR, _ = ndc_to_user(x_sym + ex, y_ndc)
        _, yD = ndc_to_user(x_sym, y_ndc - ey)
        _, yU = ndc_to_user(x_sym, y_ndc + ey)
        hx = ROOT.TLine(xL, y0, xR, y0)
        hy = ROOT.TLine(x0, yD, x0, yU)
        for ln in (hx, hy):
            ln.SetLineColor(color)
            ln.SetLineWidth(2)
            ln.Draw()
            keep_objs.append(ln)
        mk = ROOT.TMarker(x0, y0, 20)
        mk.SetMarkerColor(color)
        mk.SetMarkerSize(1.2)
        mk.Draw()
        keep_objs.append(mk)
        lab = ROOT.TLatex()
        lab.SetNDC()
        lab.SetTextAlign(12)
        lab.SetTextFont(42)
        lab.SetTextSize(0.038)
        lab.DrawLatex(x_lab, y_ndc, label)
        keep_objs.append(lab)

    entry_y0 = title_y0 - len(legend_lines) * dy - 0.025
    _draw_legend_entry(entry_y0, COLOR_REF, "HLT")
    _draw_legend_entry(entry_y0 - 0.055, COLOR_TGT, "NGT")

    # ---- lower pad ----
    pad2.cd()
    if logx:
        pad2.SetLogx()

    g_ratio = divide_graphs(g_tgt, g_ref)
    _style_graph(g_ratio, ROOT.kBlack, marker_size=1.05)
    g_ratio.GetXaxis().SetLimits(xmin, xmax)
    g_ratio.GetXaxis().SetTitle(xlabel)
    g_ratio.GetXaxis().SetTitleSize(0.13)
    g_ratio.GetXaxis().SetTitleOffset(1.15)
    g_ratio.GetXaxis().SetLabelSize(0.11)
    g_ratio.GetXaxis().SetLabelOffset(0.02)
    g_ratio.GetXaxis().SetTickLength(0.07)
    if logx:
        g_ratio.GetXaxis().SetMoreLogLabels()
        g_ratio.GetXaxis().SetNoExponent()

    ay2 = g_ratio.GetYaxis()
    ay2.SetTitle("Ratio")
    ay2.SetTitleSize(0.13)
    ay2.SetTitleOffset(0.42)
    ay2.SetLabelSize(0.11)
    ay2.SetNdivisions(2, False)  # labels only at 0.9, 1.0, 1.1; no minor ticks
    ay2.SetRangeUser(rymin, rymax)
    ay2.SetTickLength(0.05)
    g_ratio.Draw("AP")

    if hide_x_edge_labels:
        # Labels at -2,-1,0,1,2 only; keep ticks at ±2.5 but hide half/edge numbers
        # 10 primary bins over [-2.5, 2.5] → labels every 0.5: hide edges + half-integers
        ax = g_ratio.GetXaxis()
        ax.SetNdivisions(10, False)
        for i in (1, 3, 5, 7, 9, -1):  # ±2.5, ±1.5, ±0.5
            ax.ChangeLabel(i, -1, 0)

    line = ROOT.TLine(xmin, 1.0, xmax, 1.0)
    line.SetLineStyle(2)
    line.SetLineWidth(1)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("SAME")

    c._keep = [pad1, pad2, g_ref, g_tgt, g_ratio, latex, line, *keep_objs]

    for ext in (".png", ".pdf", ".C"):
        out = out_base + ext
        c.SaveAs(out)
        print(f"  wrote {out}")

    rf = ROOT.TFile(out_base + ".root", "RECREATE")
    g_ref.Clone("efficiency_reference").Write()
    g_tgt.Clone("efficiency_target").Write()
    g_ratio.Clone("efficiency_ratio").Write()
    c.Write("canvas")
    rf.Close()
    print(f"  wrote {out_base}.root")


def region_legend_lines(trig, region):
    """Return legend header lines: trigger (+ optional leg) + kinematic cut."""
    lines = list(_trigger_title_lines(trig))
    if region == "eta" or region == "phi":
        lines.append("0.00 < |#eta| < 2.50")
        lines.append(f"Probe electron p_{{T}} > {PLATEAU_CUTS[trig]} GeV")
        return lines
    root_tags = {
        "pt_barrel": "0.00 < |#eta| < 1.44",
        "pt_endcap_loweta": "1.57 < |#eta| < 2.00",
        "pt_endcap_higheta": "2.00 < |#eta| < 2.50",
        "pt_combined": "0.00 < |#eta| < 1.44 or 1.57 < |#eta| < 2.50",
    }
    lines.append(root_tags[region])
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-o", "--outdir", default=DEFAULT_OUT, help="Output directory for .C / .png / .root")
    parser.add_argument("--ref", default=NTUPLES["Reference"], help="Reference ntuple path")
    parser.add_argument("--tgt", default=NTUPLES["Target"], help="Target ntuple path")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    NTUPLES["Reference"] = args.ref
    NTUPLES["Target"] = args.tgt

    hists = {
        "Reference": fill_dataset("Reference", args.ref),
        "Target": fill_dataset("Target", args.tgt),
    }

    plot_cfgs = [
        ("pt_barrel", "Offline electron p_{T} [GeV]", "barrel_pt", True, 10, 400),
        ("pt_endcap_loweta", "Offline electron p_{T} [GeV]", "endcap_loweta_pt", True, 10, 400),
        ("pt_endcap_higheta", "Offline electron p_{T} [GeV]", "endcap_higheta_pt", True, 10, 400),
        ("pt_combined", "Offline electron p_{T} [GeV]", "combined_pt", True, 10, 400),
        ("eta", "Offline electron #eta", "eta", False, -2.5, 2.5),
        ("phi", "Offline electron #phi", "phi", False, -3.32, 3.32),
    ]

    for trig in HLT_PATHS:
        logx_ok = trig not in ("Ele115", "Ele135")
        for key, xlabel, tag, want_logx, xmin, xmax in plot_cfgs:
            use_logx = want_logx and logx_ok
            if want_logx and not logx_ok:
                use_logx = False

            hp_r, hf_r = hists["Reference"][trig][key]
            hp_t, hf_t = hists["Target"][trig][key]
            g_ref = efficiency(hp_r, hf_r, f"{trig}_{key}_ref")
            g_tgt = efficiency(hp_t, hf_t, f"{trig}_{key}_tgt")

            out_base = os.path.join(
                args.outdir,
                f"{trig}_Reference_vs_Target_HLT_eff_{tag}",
            )
            plot_ratio(
                g_ref,
                g_tgt,
                out_base=out_base,
                xlabel=xlabel,
                legend_lines=region_legend_lines(trig, key),
                logx=use_logx,
                xmin=xmin,
                xmax=xmax,
                legend_loc="center" if key in ("eta", "phi") else "right",
                hide_x_edge_labels=(key == "eta"),
            )

    print("Done.")


if __name__ == "__main__":
    main()
