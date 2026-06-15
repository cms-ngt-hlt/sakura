import uproot
import os
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import crystalball
from scipy.stats import chisquare
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import mplhep as hep
plt.style.use(hep.style.CMS)

class LCTS:
    def __init__(self, conditions):
        self.conditions = conditions
        self.get_directories = sorted(os.listdir('upload_' + self.conditions + '/'))
        self.means = []
        self.stdvs = []
        self.rnms = []
        self.fit_mus = []
        self.fit_mu_errors = []
        self.fit_sigmas = []
        self.fit_sigma_errors = []
        self.load_and_fit_files()

    def crystal_ball_pdf(self, x, beta, m, loc, scale, amplitude):
        """
        Crystal Ball probability density function.
        We add 'amplitude' to scale the PDF to match histogram counts.
        """
        return amplitude * crystalball.pdf(x, beta, m, loc=loc, scale=scale)
    


    def load_and_fit_files(self):
        #print(type(self.get_directories))
        for item in self.get_directories:#[2:3]:
            if not item.endswith(".root"):
                continue  # Skip non-ROOT files if any
            file_path = 'upload_' + self.conditions + '/' + item
            
            try:
                with uproot.open(file_path) as file:
                    monitoring_keys = [key for key in file.keys() if "di-Electron_Mass" in key]
                    if not monitoring_keys:
                        print(f"Warning: 'di-Electron_Mass' not found in {item}. Skipping.")
                        continue
                    
                    hist = file[monitoring_keys[0][:-2]]

                    bin_edges = hist.axis().edges()
                    #print(bin_edges)
                    bin_widhts = bin_edges[1:]-bin_edges[:-1]
                    #print(bin_widhts)
                    bin_centers = hist.axis().centers() 
                    #print(bin_centers) 
                    counts = hist.values()               

                    # Filter out zero counts to avoid issues with fitting
                    mask = counts > 0
                    bin_centers_filtered = bin_centers[mask]
                    counts_filtered = counts[mask]

                    if len(counts_filtered) < 5: # Need enough data points for a fit
                        print(f"Warning: Not enough non-zero bins in {item} for fitting. Skipping.")
                        mean = np.average(bin_centers, weights=counts)
                        variance = np.average((bin_centers - mean) ** 2, weights=counts)
                        std_dev = np.sqrt(variance)
                        self.means.append(mean)
                        self.stdvs.append(std_dev)
                        self.rnms.append(int(item[18:-5]))
                        self.fit_mus.append(np.nan)
                        self.fit_mu_errors.append(np.nan)
                        self.fit_sigmas.append(np.nan)
                        self.fit_sigma_errors.append(np.nan)
                        continue

                    # Initial guess for parameters: [beta, m, loc, scale, amplitude]
                    initial_loc = np.average(bin_centers_filtered, weights=counts_filtered)
                    initial_scale = np.sqrt(np.average((bin_centers_filtered - initial_loc) ** 2, weights=counts_filtered))
                    initial_amplitude = np.sum([counts_filtered[i]*bin_widhts[i] for i in range(len(counts_filtered))])

                    initial_beta = 1.0
                    initial_m = 2.0

                    p0 = [initial_beta, initial_m, initial_loc, initial_scale, initial_amplitude]

                    bounds = ([0.1, 0.1, initial_loc * 0.5, initial_scale * 0.1, initial_amplitude * 0.1],
                              [10.0, 100.0, initial_loc * 1.5, initial_scale * 10.0, initial_amplitude * 2.0])

                    try:
                        popt, pcov = curve_fit(self.crystal_ball_pdf, bin_centers_filtered, counts_filtered, p0=p0, bounds=bounds, maxfev=5000, sigma=np.sqrt(counts_filtered))
                        
                        beta_fit, m_fit, mu_fit, sigma_fit, amplitude_fit = popt
                        perr = np.sqrt(np.diag(pcov))
                        mu_error = perr[2]
                        sigma_error = perr[3]

                        self.fit_mus.append(mu_fit)
                        self.fit_mu_errors.append(mu_error)
                        self.fit_sigmas.append(sigma_fit)
                        self.fit_sigma_errors.append(sigma_error)

                        mean = np.average(bin_centers, weights=counts)
                        variance = np.average((bin_centers - mean) ** 2, weights=counts)
                        std_dev = np.sqrt(variance)

                        self.means.append(mean)
                        self.stdvs.append(std_dev)
                        self.rnms.append(int(item[18:-5]))

                        ndof = len(bin_centers_filtered) - len(popt)
                        x = np.linspace(min(bin_centers), max(bin_centers), 1000)


                        # Calculate expected counts from PDF (scale PDF by bin widths)
                        expected = self.crystal_ball_pdf(bin_centers_filtered, beta=beta_fit, m=m_fit,
                                                        loc=mu_fit, scale=sigma_fit, amplitude=amplitude_fit) #* bin_widhts
                        
                        sigma_data = np.sqrt(counts_filtered)
                        chi_squared = np.sum(((counts_filtered - expected) / sigma_data)**2)
                        reduced_chi2 = chi_squared/ndof
                        #print(chi_squared)
              
                    except RuntimeError as e:
                        print(f"Error fitting Crystal Ball to {item}: {e}. Falling back to simple mean/std.")
                        mean = np.average(bin_centers, weights=counts)
                        variance = np.average((bin_centers - mean) ** 2, weights=counts)
                        std_dev = np.sqrt(variance)
                        self.means.append(mean)
                        self.stdvs.append(std_dev)
                        self.rnms.append(int(item[18:-5]))
                        self.fit_mus.append(np.nan)
                        self.fit_mu_errors.append(np.nan)
                        self.fit_sigmas.append(np.nan)
                        self.fit_sigma_errors.append(np.nan)

            except Exception as e:
                print(f"Could not open or process file {item}: {e}. Skipping.")
                mean = np.nan
                std_dev = np.nan
                self.means.append(mean)
                self.stdvs.append(std_dev)
                self.rnms.append(int(item[18:-5]))
                self.fit_mus.append(np.nan)
                self.fit_mu_errors.append(np.nan)
                self.fit_sigmas.append(np.nan)
                self.fit_sigma_errors.append(np.nan)


        


    def plot_mu_vs_rnm(self):
        """
        Plots the fitted mu values with their errors as a function of run number.
        """
        # Ensure data is sorted by run number for a sensible plot
        # This assumes rnms, fit_mus, and fit_mu_errors are already aligned.
        # If not, you might want to zip them, sort, and then unpack.
        
        # Filter out NaN values if some fits failed
        valid_indices = ~np.isnan(self.fit_mus)
        rnms_to_plot = np.array(self.rnms)[valid_indices]
        mus_to_plot = np.array(self.fit_mus)[valid_indices]
        mu_errors_to_plot = np.array(self.fit_mu_errors)[valid_indices]

        # Sort based on run number
        sort_order = np.argsort(rnms_to_plot)
        rnms_to_plot = rnms_to_plot[sort_order]
        mus_to_plot = mus_to_plot[sort_order]
        mu_errors_to_plot = mu_errors_to_plot[sort_order]


        plt.figure(figsize=(10, 6)) # Adjust figure size as needed
        plt.errorbar(rnms_to_plot, mus_to_plot, yerr=mu_errors_to_plot, fmt='o', capsize=4, label='Fitted $\\mu$')
        
        plt.xlabel('Run Number (rnm)')
        plt.ylabel('Fitted Di-Electron Mass $\\mu$ (GeV/$c^2$)') # Example unit
        plt.title('Fitted Di-Electron Mass Peak vs. Run Number')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout() # Adjust layout to prevent labels from overlapping
        plt.savefig('mu_vs_rnm_plot.png') # Save the plot
        plt.show()

    def plot_sigma_vs_rnm(self):
        """
        Plots the fitted sigma values with their errors as a function of run number.
        """
        valid_indices = ~np.isnan(self.fit_sigmas)
        rnms_to_plot = np.array(self.rnms)[valid_indices]
        sigmas_to_plot = np.array(self.fit_sigmas)[valid_indices]
        sigma_errors_to_plot = np.array(self.fit_sigma_errors)[valid_indices]

        sort_order = np.argsort(rnms_to_plot)
        rnms_to_plot = rnms_to_plot[sort_order]
        sigmas_to_plot = sigmas_to_plot[sort_order]
        sigma_errors_to_plot = sigma_errors_to_plot[sort_order]

        plt.figure(figsize=(10, 6))
        plt.errorbar(rnms_to_plot, sigmas_to_plot, yerr=sigma_errors_to_plot, fmt='o', capsize=4, label='Fitted $\\sigma$')
        
        plt.xlabel('Run Number (rnm)')
        plt.ylabel('Fitted Di-Electron Mass Width $\\sigma$ (GeV/$c^2$)') # Example unit
        plt.title('Fitted Di-Electron Mass Width vs. Run Number')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.savefig('sigma_vs_rnm_plot.png')
        plt.show()



    def create_stability_plot(self, coloru, titleu):
        run_numbers = self.rnms
        mu = self.fit_mus
        mu_err = self.fit_mu_errors
        sigma = self.fit_sigmas
        sigma_err = self.fit_sigma_errors

        roboto_dir = "/Users/jessicaprendi/LC386/Roboto"
        if os.path.exists(roboto_dir):
            for filename in os.listdir(roboto_dir):
                if filename.endswith(".ttf"):
                    fm.fontManager.addfont(os.path.join(roboto_dir, filename))
        else:
            print(f"Warning: Font directory not found at {roboto_dir}. Using default fonts.")

        my_dark_style = sns.axes_style("darkgrid")
        #my_dark_style['axes.grid'] = True
        my_dark_style['grid.linestyle'] = '--'
        my_dark_style['font.family'] = 'sans-serif'
        my_dark_style['font.sans-serif'] = ['Roboto', 'DejaVu Sans', 'Arial', 'sans-serif']
        my_dark_style['axes.edgecolor'] = "#EAEAF2"
        my_dark_style['font.size'] = 20
        sns.set_theme(style=my_dark_style)
 
 

        fig, (ax1, ax2) = plt.subplots(
            2, 1,
            figsize=(14, 8),
            sharex=True, # Both plots will share the same x-axis ticks
            gridspec_kw={'height_ratios': [1.5, 1]} # Makes ax1 taller
        )
        fig.suptitle(titleu, fontsize=20, weight='bold')


        ax1.errorbar(
            run_numbers, mu, yerr=mu_err,
            fmt='o',          # 'o' for circular markers
            color=coloru,  # A nice blue-purple color
            ecolor=coloru, # Lighter color for error bars
            elinewidth=1.5,
            capsize=4,        # Size of the error bar caps
            label='Fitted $\\mu$',
        )

        ax1.set_ylabel('Fitted $\\mu$', weight='bold')
        #ax1.legend(loc='lower center')

        ax2.errorbar(
            run_numbers, sigma, yerr=sigma_err,
            fmt='s',          # 's' for square markers
            color=coloru,  # A nice green color
            ecolor=coloru,
            elinewidth=1.5,
            capsize=4,
            #label='Fitted $\\sigma$',
        )
        
        ax2.set_xlabel('Run Number', weight='bold')
        ax2.set_ylabel('Fitted $\\sigma$') # Use \n for a newline
        ax2.legend(loc='upper center')

        #plt.tight_layout(rect=[0, 0, 1, ])
        plt.show()

  
