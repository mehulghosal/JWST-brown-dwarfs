import os
from os.path import isdir, isfile, join
import plot_utils as plt
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.patches as patches

from scipy.optimize import curve_fit

def line ( x , m , b ):
	return m * x + b

directory = './'	
dir_names = [directory+f+'/' for f in os.listdir(directory) if isdir(join(directory,f))] 

# print(dir_names)

for directory_name in dir_names: 
	print(directory_name)

	if 'pycache' in directory_name or 'git' in directory_name : continue

	apparent_file_name = directory_name.split('/')[1] + '_apparent_SED.txt'

	file_path = directory_name + apparent_file_name

	print( file_path )

	# READING IN DATA FILE: apparent_file is now a 2d table: 28658 rows, 3 columns
	# apparent_file = np.loadtxt ( '2MASS_J04151954-0935066/2MASS_J04151954-0935066_apparent_SED.txt' , skiprows=3)
	apparent_file = np.loadtxt ( file_path , skiprows=3)

	# ISOLATING THREE COLUMNS INTO SEPARATE VARIABLES
	wavelength_microns  = apparent_file [:,0]
	apparent_flux 		= apparent_file [:,1]
	apparent_flux_error = apparent_file [:,2]

	# PLOTTING FLUX vs WAVELENGTH
	fig_app , ax_app = plt.errorbar( wavelength_microns , apparent_flux , yerr= apparent_flux_error, title=directory_name.split('/')[1] , xlabel='wavelength [micron]' , ylabel='Apparent flux' , xlim=[3.6,5.] , ylim=[0, np.max(apparent_flux[wavelength_microns>3.6]) * 1.1] , label="flux density" , markerstyle='.' , color='blue' , markersize=2 , linewidth=1 , ecolor='black' )

	# FOR CO2 INDEX
	continuum_wl_CO2 = 4.15
	wl_width         = .05/2
	# ABSORPOTION FEATURE DETAILS
	CO2_center = 4.29
	CO2_width  = .05/2

	# SLICING WAVELENGTHS TO REGION OF INTEREST: isolating the continuum wavelengths
	where_continuum = np.where( (wavelength_microns < continuum_wl_CO2 + wl_width) & (wavelength_microns > continuum_wl_CO2 - wl_width) )
	app_flux_continuum = np.average ( apparent_flux[where_continuum] )

	where_CO2 = np.where( (wavelength_microns < CO2_center + CO2_width) & (wavelength_microns > CO2_center - CO2_width) )
	app_flux_CO2 = np.average ( apparent_flux[where_CO2] )

	# REDFINE CONTINUUM SPECTRA FOR CO
	continuum_wl_CO = 4.4
	wl_width     = .05/2
	# ABSORBTION FEATURE DETAILS
	CO_center = 4.56
	CO_width  = .05/2

	# SLICING WAVELENGTHS TO REGION OF INTEREST: isolating the continuum wavelengths
	where_continuumCO = np.where( (wavelength_microns < continuum_wl_CO + wl_width) & (wavelength_microns > continuum_wl_CO - wl_width) )
	# USING THAT SLICE OF WAVELENGTHS, WE CAN SLICE INTO FLUX TO CALCULATE THE AVERAGE FLUX OF THE CONTINUUM SPECTRUM
	app_flux_continuumCO = np.average ( apparent_flux[where_continuumCO] )

	# AGAIN SLICING, THIS TIME FOR THE CO
	where_CO = np.where ( (wavelength_microns < CO_center + CO_width) & (wavelength_microns > CO_center - CO_width) )
	app_flux_CO = np.average ( apparent_flux[where_CO] )

	CO2_index = app_flux_continuum   / app_flux_CO2
	CO_index  = app_flux_continuumCO / app_flux_CO

	print ( f'CO2 index: {CO2_index:.2f}' )
	# CO2 index: 1.48
	print ( f'CO  index: {CO_index:.2f}' )
	# CO  index: 2.08

	# PLOTTING CONTINUUM FLUX AVERAGES
	plt.plot_existing( fig_app , ax_app , continuum_wl_CO2 , app_flux_continuum    , label=f'Center={continuum_wl_CO2}' , markerfacecolor='red'   , markersize=20 , markerstyle='*' )
	plt.plot_existing( fig_app , ax_app , continuum_wl_CO  , app_flux_continuumCO  , label=f'Center={continuum_wl_CO }' , markerfacecolor='green' , markersize=20 , markerstyle='*' )

	# PLOTTING ABSORPTION FEATURE FLUX AVERAGES
	plt.plot_existing( fig_app , ax_app , CO2_center  , app_flux_CO2  , label=f'CO2 INDEX={CO2_index:.2f}' , markerfacecolor='red'    , markersize=20 )
	plt.plot_existing( fig_app , ax_app , CO_center   , app_flux_CO   , label=f'CO  INDEX={CO_index :.2f}'  , markerfacecolor='green' , markersize=20 )

	rect1 = patches.Rectangle((continuum_wl_CO2 -wl_width, 0), wl_width*2, 1e-16, linewidth=1, edgecolor='black', facecolor='red'    , alpha=.5 , label=f'window={wl_width}' )
	rect2 = patches.Rectangle((continuum_wl_CO  -wl_width, 0), wl_width*2, 1e-16, linewidth=1, edgecolor='black', facecolor='green'  , alpha=.5 , label=f'window={wl_width}' )
	rect3 = patches.Rectangle((CO2_center       -wl_width, 0), wl_width*2, 1e-16, linewidth=1, edgecolor='black', facecolor='orange' , alpha=.5 , label=f'Center={CO2_center } \nwindow={wl_width}' )
	rect4 = patches.Rectangle((CO_center        -wl_width, 0), wl_width*2, 1e-16, linewidth=1, edgecolor='black', facecolor='cyan'   , alpha=.5 , label=f'Center={CO_center  } \nwindow={wl_width}' )
	ax_app.add_patch(rect1)
	ax_app.add_patch(rect2)
	ax_app.add_patch(rect3)
	ax_app.add_patch(rect4)

	ax_app.legend(loc='upper left')

	# if True: break
	plot.savefig ( directory_name.split('/')[1]+'.png'  )


plt.show()
