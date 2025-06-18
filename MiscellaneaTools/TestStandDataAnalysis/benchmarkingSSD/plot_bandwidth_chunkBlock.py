import os
import json
import re
import ROOT
from array import array

ROOT.gStyle.SetOptStat(0)

base_dir = "/eos/user/m/mzarucki/NGT/SAKURA/demonstrator/SSDbenchmarks/fio_logs/realistic"
output_dir_base = "/eos/user/m/mzarucki/www/2025/NGT/SAKURA/SSDbenchmarks/bandwidth/realistic"
plot_dir_3d = os.path.join(output_dir_base, "ssds_raid0_xfs_3D")
os.makedirs(plot_dir_3d, exist_ok=True)

bs_order = ["64k", "128k", "256k", "512k", "1M", "2M"]
cs_order = ["64k", "128k", "256k", "512k", "1M", "2M"]
bs_index = {v: i for i, v in enumerate(bs_order)}
cs_index = {v: i for i, v in enumerate(cs_order)}

def extract_labels(path):
    match_cs = re.search(r'cs(\d+[kM])', path)
    match_bs = re.search(r'bs(\d+[kM])', path)
    return match_cs.group(1) if match_cs else None, match_bs.group(1) if match_bs else None

data_by_config = {}

for cs_dir in os.listdir(base_dir):
    if not cs_dir.startswith("ssds_raid0_cs"):
        continue
    cs_path = os.path.join(base_dir, cs_dir)
    for bs_dir in os.listdir(cs_path):
        full_path = os.path.join(cs_path, bs_dir)
        if not os.path.isdir(full_path):
            continue
        for fname in os.listdir(full_path):
            if not fname.endswith(".json"):
                continue
            filepath = os.path.join(full_path, fname)
            cs_label, bs_label = extract_labels(filepath)
            if cs_label not in cs_index or bs_label not in bs_index:
                continue
            with open(filepath) as f:
                try:
                    data = json.load(f)
                except Exception:
                    continue
            for job in data.get("jobs", []):
                m = re.search(r"readwrite-iodepth-(\d+)-numjobs-(\d+)", job.get("jobname", ""))
                if not m:
                    continue
                qd = int(m.group(1))
                nj = int(m.group(2))
                bw_read = job.get("read", {}).get("bw", 0) / 1024.0**2
                bw_write = job.get("write", {}).get("bw", 0) / 1024.0**2
                key = (qd, nj)
                if key not in data_by_config:
                    data_by_config[key] = []
                data_by_config[key].append((bs_label, cs_label, bw_read, bw_write))

canvs = {}

for (qd, nj), results in data_by_config.items():
    bs_labels = sorted({bs for bs, _, *_ in results}, key=lambda x: bs_index.get(x, 999))
    cs_labels = sorted({cs for _, cs, *_ in results}, key=lambda x: cs_index.get(x, 999))

    # 3D
    z_vals = {}
    x_vals, y_vals, z_vals['Read'], z_vals['Write'] = array('d'), array('d'), array('d'), array('d')
    label_map_x, label_map_y = {}, {}

    for bs, cs, bw_read, bw_write in results:
        xi, yi = bs_index[bs], cs_index[cs]
        x_vals.append(xi)
        y_vals.append(yi)
        z_vals['Read'].append(bw_read)
        z_vals['Write'].append(bw_write)
        label_map_x[xi] = bs
        label_map_y[yi] = cs

    for rw in ['Read', 'Write']:
        graph = ROOT.TGraph2D(len(x_vals), x_vals, y_vals, z_vals[rw])
        graph.SetNpx(len(bs_labels))
        graph.SetNpy(len(cs_labels))
        graph.SetTitle(f"Read & Write Bandwidths (Micron 9400 PRO, RAID0, XFS, QD{qd}, NJ{nj}) ; Block Size ; Chunk Size ; {rw} Bandwidth [GiB/s]")

        canvs['3D_qd%s_nj%s_%s'%(qd,nj,rw)] = ROOT.TCanvas(f"3D_qd%s_nj%s_%s"%(qd,nj,rw), f"3D {rw} Bandwidth QD={qd} NJ={nj}", 1200, 900)
        canvs['3D_qd%s_nj%s_%s'%(qd,nj,rw)].SetRightMargin(0.15)
        graph.Draw("LEGO2Z")

        hist = graph.GetHistogram()
        hist.GetZaxis().SetRangeUser(0, 6)
        for i, bs in label_map_x.items():
            hist.GetXaxis().SetBinLabel(i+1, bs)
            hist.GetXaxis().CenterTitle(1)
        for j, cs in label_map_y.items():
            hist.GetYaxis().SetBinLabel(j+1, cs)
            hist.GetYaxis().CenterTitle(1)

        canvs['3D_qd%s_nj%s_%s'%(qd,nj,rw)].SaveAs(os.path.join(plot_dir_3d, f"bandwidth3D_qd{qd}_nj{nj}_{rw}.png".lower()))

    # bar plots (slices) 
    for cs in cs_labels:
        plot_dir_cs = os.path.join(output_dir_base, f"ssds_raid0_cs{cs}_xfs")
        os.makedirs(plot_dir_cs, exist_ok=True)
        entries = [(bs, r, w) for bs, c, r, w in results if c == cs]
        entries.sort(key=lambda x: bs_index.get(x[0], 999))
        nbins = len(entries)

        hist_read = ROOT.TH1D(f"read_cs{cs}_qd{qd}_nj{nj}", "", nbins, 0, nbins)
        hist_write = ROOT.TH1D(f"write_cs{cs}_qd{qd}_nj{nj}", "", nbins, 0, nbins)
        for i, (bs, r, w) in enumerate(entries):
            hist_read.SetBinContent(i+1, r)
            hist_write.SetBinContent(i+1, w)
            hist_read.GetXaxis().SetBinLabel(i+1, bs)

        canvs['bar_qd%s_nj%s_cs%s'%(qd,nj,cs)] = ROOT.TCanvas()
        hist_read.SetMinimum(0)
        hist_read.SetMaximum(6)
        hist_write.SetMinimum(0)
        hist_write.SetMaximum(6)
        hist_read.SetBarWidth(0.4)
        hist_write.SetBarWidth(0.4)
        hist_read.SetBarOffset(0.0)
        hist_write.SetBarOffset(0.4)
        hist_read.SetFillColorAlpha(ROOT.kBlue, 0.7)
        hist_write.SetFillColorAlpha(ROOT.kRed, 0.7)
        hist_read.SetTitle(f"Read & Write Bandwidths (Micron 9400 PRO, RAID0, XFS, QD{qd}, NJ{nj}, CS{cs}) ; Block Size ; Bandwidth [GiB/s]")
        hist_read.LabelsOption("h")
        hist_read.Draw("bar")
        hist_write.Draw("bar same")
        canvs['bar_qd%s_nj%s_cs%s'%(qd,nj,cs)].SaveAs(os.path.join(plot_dir_cs, f"bandwidth_qd{qd}_nj{nj}_cs{cs}.png"))

    for bs in bs_labels:
        plot_dir_bs = os.path.join(output_dir_base, f"ssds_raid0_bs{bs}_xfs")
        os.makedirs(plot_dir_bs, exist_ok=True)
        entries = [(cs, r, w) for b, cs, r, w in results if b == bs]
        entries.sort(key=lambda x: cs_index.get(x[0], 999))
        nbins = len(entries)

        hist_read = ROOT.TH1D(f"read_bs{bs}_qd{qd}_nj{nj}", "", nbins, 0, nbins)
        hist_write = ROOT.TH1D(f"write_bs{bs}_qd{qd}_nj{nj}", "", nbins, 0, nbins)
        for i, (cs, r, w) in enumerate(entries):
            hist_read.SetBinContent(i+1, r)
            hist_write.SetBinContent(i+1, w)
            hist_read.GetXaxis().SetBinLabel(i+1, cs)

        canvs['bar_qd%s_nj%s_bs%s'%(qd,nj,bs)] = ROOT.TCanvas()
        hist_read.SetMinimum(0)
        hist_read.SetMaximum(6)
        hist_write.SetMinimum(0)
        hist_write.SetMaximum(6)
        hist_read.SetBarWidth(0.4)
        hist_write.SetBarWidth(0.4)
        hist_read.SetBarOffset(0.0)
        hist_write.SetBarOffset(0.4)
        hist_read.SetFillColorAlpha(ROOT.kBlue, 0.7)
        hist_write.SetFillColorAlpha(ROOT.kRed, 0.7)
        hist_read.SetTitle(f"Read & Write Bandwidths (Micron 9400 PRO, RAID0, XFS, QD{qd}, NJ{nj}, BS{bs}) ; Chunk Size ; Bandwidth [GiB/s]")
        hist_read.LabelsOption("h")
        hist_read.Draw("bar")
        hist_write.Draw("bar same")
        canvs['bar_qd%s_nj%s_bs%s'%(qd,nj,bs)].SaveAs(os.path.join(plot_dir_bs, f"bandwidth_qd{qd}_nj{nj}_bs{bs}.png"))
