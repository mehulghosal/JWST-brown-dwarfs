import os
from os.path import isdir, isfile, join
import plot_utils as plt
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.patches as patches

def bin_spectrum ( wl , fl , factor=5 , fl_err=None ) :
	fl_binned = np.array([ np.sum( fl[ii:ii+factor] )/factor for ii in range( 0 , len(wl)-factor , factor)  ])
	wl_binned = np.array([ wl[ii]     for ii in range(0 , len(wl)-factor , factor ) ])

	ret = (wl_binned , fl_binned )
	if fl_err is not None:
		err_binned = np.array([ (np.sum( fl[ii:ii+factor] ** 2 )/(factor**2)) **.5 for ii in range( 0 , len(wl)-factor , factor)  ])
		ret = (wl_binned , fl_binned , err_binned)
	return ret


def steff_boltzmann ( wl , Teff ) : 
	h = 6.63e-34
	c = 3e8
	kb = 1.38e-23
	# R = 2 * h * c**2 * wl**-5 * (np.exp( h*c / (kb*wl*Teff) )-1) **-1
	R = 8 * np.pi * h * c * (wl**-5) *( (np.exp(h*c/(wl*kb*Teff)) - 1) **-1)
	return R * 10**-7 * 100**2 * 10**8
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
	fig_app , ax_app = plt.errorbar( wavelength_microns , apparent_flux , size=(8,6) , yerr= apparent_flux_error, title='WISEU_J050305.68-564834.0', xlabel=r'wavelength[$\mu$]' , ylabel='Apparent flux[Jy]' , xlim=[3.6,5.] , ylim=[0, 1.1 * np.max(apparent_flux[wavelength_microns>3.6])] , label="flux" , markerstyle='.' , color='black' , markersize=2 , linewidth=2 , ecolor='black' , alpha=.2,  )
	# ax_app.grid()

	# plotting binned flux 
	bins = 20
	wl_binned , fl_binned , err_binned = bin_spectrum ( wavelength_microns , apparent_flux , factor=bins , fl_err=apparent_flux_error )
	ax_app.errorbar ( wl_binned , fl_binned , err_binned , label=f'binned by {bins}' , marker='.' , markerfacecolor='blue' , markersize=2, linewidth=2 , color='blue' , capsize=1 , elinewidth=1 , zorder=1 )

	# wavelength_microns = wl_binned
	# apparent_flux = fl_binned

	# FOR CO2 INDEX
	continuum_wl_CO2 = 4.13
	CO2_cont_width   = .05
	# ABSORPOTION FEATURE DETAILS
	CO2_center = 4.26
	CO2_width  = .055

	# SLICING WAVELENGTHS TO REGION OF INTEREST: isolating the continuum wavelengths
	where_continuum = np.where( (wavelength_microns < continuum_wl_CO2 + CO2_cont_width) & (wavelength_microns > continuum_wl_CO2 - CO2_cont_width) )
	# USING THAT SLICE OF WAVELENGTHS, WE CAN SLICE INTO FLUX TO CALCULATE THE AVERAGE FLUX OF THE CONTINUUM SPECTRUM
	app_flux_continuum = np.average ( apparent_flux[where_continuum] )

	# SLICING WAVELENGTHS TO REGION OF INTEREST: ISOLATING CO2 ABSORPTION FEATURE
	where_CO2 = np.where( (wavelength_microns < CO2_center + CO2_width) & (wavelength_microns > CO2_center - CO2_width) )
	# USING THE ABOVE SLICE OF WAVELENGTHS, WE CAN SLICE INTO FLUX TO CALCULATE THE AVERAGE FLUX OF THE ABSORPTION FEATURE
	app_flux_CO2 = np.average ( apparent_flux[where_CO2] )

	# REDFINE CONTINUUM SPECTRA FOR CO
	continuum_wl_CO = 4.4
	CO_cont_width   = .05
	# ABSORBTION FEATURE DETAILS
	CO_center = 4.67
	CO_width  = .11

	# SLICING WAVELENGTHS TO REGION OF INTEREST: isolating the continuum wavelengths
	where_continuumCO = np.where( (wavelength_microns < continuum_wl_CO + CO_cont_width) & (wavelength_microns > continuum_wl_CO - CO_cont_width) )
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

	CO_color='cyan'
	CO2_color='red'

	# PLOTTING CONTINUUM FLUX AVERAGES
	plt.plot_existing( fig_app , ax_app , continuum_wl_CO2 , app_flux_continuum    , label=f'CO2 Continuum={continuum_wl_CO2}'+r'$\mu$'+f'\nwl width={CO2_cont_width}'+r'$\mu$' , markerfacecolor=CO2_color   , markersize=20 , markerstyle='*' )
	plt.plot_existing( fig_app , ax_app , continuum_wl_CO  , app_flux_continuumCO  , label=f'CO Continuum={continuum_wl_CO}'+r'$\mu$'+f'\nwl width={CO_cont_width}'+r'$\mu$' , markerfacecolor=CO_color , markersize=20 , markerstyle='*' )

	# PLOTTING ABSORPTION FEATURE FLUX AVERAGES
	plt.plot_existing( fig_app , ax_app , CO2_center  , app_flux_CO2  , label=f'CO2 INDEX={CO2_index:.2f}' , markerfacecolor=CO2_color   , markersize=20 )
	plt.plot_existing( fig_app , ax_app , CO_center   , app_flux_CO   , label=f'CO  INDEX={CO_index :.2f}'  , markerfacecolor=CO_color , markersize=20 )

	rect1 = patches.Rectangle((continuum_wl_CO2 -CO2_cont_width, 0), CO2_cont_width*2, 1e-16, linewidth=1, facecolor='lightgray' , alpha=.5 , edgecolor='black',)
	rect2 = patches.Rectangle((continuum_wl_CO  -CO_cont_width, 0), CO_cont_width*2, 1e-16, linewidth=1, facecolor='lightgray' , alpha=.5,  edgecolor='black',)
	rect3 = patches.Rectangle((CO2_center       -CO2_width, 0), CO2_width*2, 1e-16, linewidth=1, edgecolor=CO2_color, facecolor='lightgray' , alpha=.5 , label=f'CO2 center={CO2_center}'+r'$\mu$'+f'\nwl width={CO2_width}'+r'$\mu$')
	rect4 = patches.Rectangle((CO_center        -CO_width , 0), CO_width *2, 1e-16, linewidth=1, edgecolor=CO_color , facecolor='lightgray' , alpha=.5 , label=f'CO center={CO_center}'+r'$\mu$'+f'\nwl width={CO_width}'+r'$\mu$')
	ax_app.add_patch(rect1)
	ax_app.add_patch(rect2)
	ax_app.add_patch(rect3)
	ax_app.add_patch(rect4)


	# SB_flux = steff_boltzmann ( wavelength_microns , 400 )
	# plt.plot_existing ( fig_app , ax_app , wavelength_microns , SB_flux , label='blackbody' , linewidth=4 ,  )
	# print ( steff_boltzmann ( 4, 800 ) )

	ax_app.legend()

	# if True: break
	plot.savefig ( directory_name.split('/')[1]+'.png'  )


plt.show()
