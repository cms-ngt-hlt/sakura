import json
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep


plt.style.use(hep.style.CMS)

with open('/eos/user/j/jprendi/www/PUScaling/data.json', 'r') as file:
    data = json.load(file)

data1 = data['No modification step2']
PCL_PU = [item['pu'] for item in data1]
PCL_Latency = [1.0 / item['average_throughput'] for item in data1]

data2 = data['trackingIters01 step2']
mod_PU = [item['pu'] for item in data2]
mod_Latency = [1.0 / item['average_throughput'] for item in data2]

pcl_coeffs = np.polyfit(PCL_PU, PCL_Latency, 2)
mod_coeffs = np.polyfit(mod_PU, mod_Latency, 2)
pcl_fit = np.poly1d(pcl_coeffs)
mod_fit = np.poly1d(mod_coeffs)
pcl_label_fit = (f'interpolation: y = {pcl_coeffs[0]:.4f}x² {pcl_coeffs[1]:+.4f}x {pcl_coeffs[2]:+.4f}')
mod_label_fit = (f'interpolation: y = {mod_coeffs[0]:.4f}x² {mod_coeffs[1]:+.4f}x {mod_coeffs[2]:+.4f}')

x_smooth = np.linspace(min(PCL_PU), max(PCL_PU), 200)

labels = {'No modification step2':'full offline reconstruction','trackingIters01 step2':'first two tracking iterations'}
hep.cms.label("Preliminary", data=True, year="2024-2025", com=13.6)

plt.plot(PCL_PU, PCL_Latency, 'o--', label=labels['No modification step2'], markersize=10, color='#5790fc')
#plt.plot(x_smooth, pcl_fit(x_smooth), color='#648FFF', linestyle='--', alpha=0.8)#, label=pcl_label_fit)

plt.plot(mod_PU, mod_Latency, '*--', label=labels['trackingIters01 step2'], markersize=20, color='#f89c20')
#plt.plot(x_smooth, mod_fit(x_smooth), color='#FE6100', linestyle='--', alpha=0.8)#, label=mod_label_fit)

plt.xlabel("PU")
plt.ylabel("Inverse Average Throughput (s/ev)")

plt.legend(loc='upper left')
plt.grid(True, alpha=0.6, linestyle='--') 
plt.savefig('latency_plot.png')
#plt.show()
