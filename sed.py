import plot_utils as plt
import numpy as np

# READING IN DATA FILE: apparent_file is now a 2d table: 28658 rows, 3 columns
apparent_file = np.loadtxt ( '2MASS_J04151954-0935066/2MASS_J04151954-0935066_apparent_SED.txt' , skiprows=3)

# ISOLATING THREE COLUMNS INTO SEPARATE VARIABLES
wavelength_microns  = apparent_file [:,0]
apparent_flux 		= apparent_file [:,1]
apparent_flux_error = apparent_file [:,2]

# PLOTTING FLUX vs WAVELENGTH
fig_app , ax_app = plt.errorbar( wavelength_microns , apparent_flux , yerr= apparent_flux_error, title='2MASS_J04151954-0935066', xlabel='wavelength [micron]' , ylabel='Apparent flux' , xlim=[3.6,5.] , ylim=[0, 1e-16] , label="flux density" , markerstyle='.' , color='blue' , markersize=2 , linewidth=1 , ecolor='black' )

# FOR CO2 INDEX
continuum_wl_CO2 = 4.15
wl_width         = .05
# ABSORPOTION FEATURE DETAILS
CO2_center = 4.3
CO2_width  = .05

# SLICING WAVELENGTHS TO REGION OF INTEREST: isolating the continuum wavelengths
where_continuum = np.where( (wavelength_microns < continuum_wl_CO2 + wl_width) & (wavelength_microns > continuum_wl_CO2 - wl_width) )
# USING THAT SLICE OF WAVELENGTHS, WE CAN SLICE INTO FLUX TO CALCULATE THE AVERAGE FLUX OF THE CONTINUUM SPECTRUM
app_flux_continuum = np.average ( apparent_flux[where_continuum] )

# SLICING WAVELENGTHS TO REGION OF INTEREST: ISOLATING CO2 ABSORPTION FEATURE
where_CO2 = np.where( (wavelength_microns < CO2_center + CO2_width) & (wavelength_microns > CO2_center - CO2_width) )
# USING THE ABOVE SLICE OF WAVELENGTHS, WE CAN SLICE INTO FLUX TO CALCULATE THE AVERAGE FLUX OF THE ABSORPTION FEATURE
app_flux_CO2 = np.average ( apparent_flux[where_CO2] )

# REDFINE CONTINUUM SPECTRA FOR CO
continuum_wl_CO = 4.4
wl_width     = .05
# ABSORBTION FEATURE DETAILS
CO_center = 4.56
CO_width  = .05

# SLICING WAVELENGTHS TO REGION OF INTEREST: isolating the continuum wavelengths
where_continuumCO = np.where( (wavelength_microns < continuum_wl_CO + wl_width) & (wavelength_microns > continuum_wl_CO - wl_width) )
# USING THAT SLICE OF WAVELENGTHS, WE CAN SLICE INTO FLUX TO CALCULATE THE AVERAGE FLUX OF THE CONTINUUM SPECTRUM
app_flux_continuumCO = np.average ( apparent_flux[where_continuumCO] )

# AGAIN SLICING, THIS TIME FOR THE CO, SEE COMMENTS ON LINE 27 AND 29
where_CO = np.where ( (wavelength_microns < CO_center + CO_width) & (wavelength_microns > CO_center - CO_width) )
app_flux_CO = np.average ( apparent_flux[where_CO] )

CO2_index = app_flux_continuum   / app_flux_CO2
CO_index  = app_flux_continuumCO / app_flux_CO

print ( f'CO2 index: {CO2_index:.2f}' )
# CO2 index: 1.48
print ( f'CO  index: {CO_index:.2f}' )
# CO  index: 2.08

# PLOTTING CONTINUUM FLUX AVERAGES
plt.plot_existing( fig_app , ax_app , continuum_wl_CO2 , app_flux_continuum    , label=f'Continuum for CO2' , markerfacecolor='red'   , markersize=20 , markerstyle='*' )
plt.plot_existing( fig_app , ax_app , continuum_wl_CO  , app_flux_continuumCO  , label=f'Continuum used CO' , markerfacecolor='green' , markersize=20 , markerstyle='*' )

# PLOTTING ABSORPTION FEATURE FLUX AVERAGES
plt.plot_existing( fig_app , ax_app , CO2_center  , app_flux_CO2  , label=f'CO2 INDEX={CO2_index:.2f}' , markerfacecolor='red'   , markersize=20 )
plt.plot_existing( fig_app , ax_app , CO_center   , app_flux_CO   , label=f'CO  INDEX={CO_index :.2f}'  , markerfacecolor='green' , markersize=20 , leg=True )

plt.show()
