import os
import json
import re
import ROOT
from array import array

# Load the FIO JSON file


benchmark = "realistic/ssds_raid0_cs256k_xfs/bs1M"
benchmark_ = benchmark.replace("_", "-").replace("/", "_")
inputFile = "benchmark_micron9400pro_%s_empty.json"%benchmark_
logDir = "/eos/user/m/mzarucki/NGT/SAKURA/demonstrator/SSDbenchmarks/fio_logs/" + benchmark
plotDir = "/eos/user/m/mzarucki/www/2025/NGT/SAKURA/SSDbenchmarks/bandwidth/" + benchmark
if not os.path.exists(plotDir): os.makedirs(plotDir)

with open("%s/%s"%(logDir,inputFile)) as f:
    data = json.load(f)

# Extract job data
points = {'read':[], 'write':[]}
iodepths_set = set()
numjobs_set = set()
bandwidth = {'read':{}, 'write':{}}

for job in data["jobs"]:
    jobname = job["jobname"]
    match = re.search(r"readwrite-iodepth-(\d+)-numjobs-(\d+)", jobname)
    if not match:
        continue
    iodepth = int(match.group(1))
    numjob = int(match.group(2))
    iodepths_set.add(iodepth)
    numjobs_set.add(numjob)
    for rw in ['read', 'write']:
        bandwidth[rw]['kib'] = job.get(rw, {}).get("bw", 0)
        points[rw].append((iodepth, numjob, bandwidth[rw]['kib']))

iodepths = sorted(iodepths_set)
numjobs = sorted(numjobs_set)

hists = {}
canvs = {'lego':{}, 'graph':{}}

for rw in ['read', 'write']:
    hists[rw] = ROOT.TH2F("bandwidth_"+rw, "Read & Write Bandwidth (Micron 9400 PRO, RAID0, CS256k, XFS, 0%, BS1M); IO Depth ; Jobs", len(iodepths), 0, len(iodepths), len(numjobs), 0, len(numjobs))
    for iodepth, numjob, bw in points[rw]:
        xbin = iodepths.index(iodepth) + 1
        ybin = numjobs.index(numjob) + 1
        bandwidth[rw]['gib'] = bw / 1024.0**2
        hists[rw].SetBinContent(xbin, ybin, bandwidth[rw]['gib'])

    for i, val in enumerate(iodepths):
        hists[rw].GetXaxis().SetBinLabel(i + 1, str(val))
    for j, val in enumerate(numjobs):
        hists[rw].GetYaxis().SetBinLabel(j + 1, str(val))
        
    hists[rw].GetXaxis().CenterTitle()
    hists[rw].GetYaxis().CenterTitle()
    
    hists[rw].SetStats(False)
    hists[rw].GetZaxis().SetTitle("%s Bandwidth [GiB/s]"%rw.capitalize())
    hists[rw].SetMinimum(0)  # Z-axis from zero
    
    canvs['lego'][rw] = ROOT.TCanvas("canv_lego_%s"%rw, "Fio LEGO2Z Plot", 1000, 800)
    canvs['lego'][rw].SetRightMargin(0.15)
    hists[rw].Draw("LEGO2Z")
    canvs['lego'][rw].SaveAs("%s/%s"%(plotDir,"bandwidth3D_LEGO2Z_%s_%s.png"%(benchmark_, rw)))

x_vals, y_vals, z_vals = array('d'), array('d'), array('d')

graphs = {}

for rw in ['read', 'write']:
    for iodepth, numjob, bw in points[rw]:
        x_vals.append(float(iodepth))
        y_vals.append(float(numjob))
        z_vals.append(bw / 1024.0**2)

    graphs[rw] = ROOT.TGraph2D(len(x_vals), x_vals, y_vals, z_vals)
    graphs[rw].SetTitle("Read & Write Bandwidth; IO Depth ; Jobs ; %s Bandwidth [GiB/s]"%rw.capitalize())
    graphs[rw].SetMinimum(0)  # Z-axis from zero
    graphs[rw].SetNpx(30)  # smoother grid
    graphs[rw].SetNpy(30)
    
    canvs['graph'][rw] = ROOT.TCanvas("canv_graph_%s"%rw, "Fio TGraph2D", 1000, 800)
    canvs['graph'][rw].SetRightMargin(0.15)
    graphs[rw].Draw("surf1")
    canvs['graph'][rw].SaveAs("%s/%s"%(plotDir,"bandwidth3D_TGraph2D_%s_%s.png"%(benchmark_, rw)))
