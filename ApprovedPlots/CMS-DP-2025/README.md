# CMS DPS in 2025
## Overivew
This directory should include an overview of the 2025 DP notes and recipes on how the approved plots were obtained.

Here a list of our DPS notes:
- [CMS-DP-2025/082](https://cds.cern.ch/record/2951246)
- [CMS-DP-2025/087](https://cds.cern.ch/record/2951246)


## Plots for which recipes exist
### Time Variation of Calibrations on Z-Peak fit 
![time variations of physics performance on varying conditions demonstrated on Z peak fit](./082/dCal_dt-ECAL/screenshot_stability_comparison_sigma_over_mu.png)

This plot is included in [CMS-DP-2025/082](https://twiki.cern.ch/twiki/bin/view/CMSPublic/DP2025082) and the recipes are in `./dCal_dt-ECAL`.

### Absolute timing for the Prompt Calibration Loop
![Absolute PCL timing from Run start](./087/PCLTiming/aggregate_diff_upload_from_start_CMSStyle.png)

![Absolute PCL timing from Run end](./087/PCLTiming/aggregate_diff_upload_from_end_CMSStyle.png)

These plots are included in [CMS-DP-2025/087](https://cds.cern.ch/record/2951246) and recipes are in `./PCLTiming`

### Difference in reconstruction timing for different reconstruction options

![Per event time of full offline reconstruction as used in the PCL](./087/ProfilingReco/fullRecoTimingForPCL.png)
![Per event time of offline reconstruction employing simplified tracking](./087/ProfilingReco/twoItersTimeForPCL.png)

![Difference in reconstruction timing for different reconstruction options](./087/ProfilingReco/plot.png)


### Scaling of inverse average throughput with respect to Pile Up
![Latency of reconstruction vs PU](./087/ScalingPU/latency_plot.png)

These plots are included in [CMS-DP-2025/087](https://cds.cern.ch/record/2951246) and recipes are in `./ScalingPU`
