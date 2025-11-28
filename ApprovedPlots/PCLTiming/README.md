# Recipe to generate the plot

```bash
wget https://cernbox.cern.ch/files/spaces/eos/user/m/musich/NGT/3.4/MergedPCLStats_2024.db
python3 aggregates_for_approval.py
```

This will generate the following directory structure
```
diff_job_run_from_end/
└── aggregate_diff_job_run_from_end_CMSStyle.png

diff_job_run_from_start/
└── aggregate_diff_job_run_from_start_CMSStyle.png

diff_upload_from_created/
└── aggregate_diff_upload_from_created_CMSStyle.png

diff_upload_from_end/
└── aggregate_diff_upload_from_end_CMSStyle.png

diff_upload_from_start/
└── aggregate_diff_upload_from_start_CMSStyle.png
```

The plots approved are `aggregate_diff_upload_from_end_CMSStyle.png` and `aggregate_diff_upload_from_start_CMSStyle.png`