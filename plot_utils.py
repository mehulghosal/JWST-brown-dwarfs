import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

# setting global variables
plt.rc("figure", autolayout=True)


# most useful function here -- plotting and all customizations in a one line function call
# requires x and y data values: have to be the same size 1d array
# returns figure and axis objects; optional to keep them in scope for plot_existing
def plot ( x , y , xlabel='' , xlim=() , ylim=() , ylabel=() , markerstyle='.' , markersize=1 , 
		   size=(6,6) , dpi=100 , show=False , logx=False , logy=False , alpha=1 , title='', 
		   color='black' , linewidth=0 , linestyle='-' , label='' , leg=False , zorder=1 ) : 

	
	fig, ax = plt.subplots( figsize=size , dpi=dpi )
	ax.plot ( x , y , markerstyle , markersize=markersize , linestyle=linestyle , 
		linewidth=linewidth , color=color , alpha=alpha , label=label , zorder=zorder )
	if leg: ax.legend()
	ax.set_title  ( title  )
	ax.set_xlabel ( xlabel )
	ax.set_ylabel ( ylabel )
	if xlim: ax.set_xlim   ( xlim   )
	if ylim: ax.set_ylim   ( ylim   )


	if logx : ax.set_xscale ( 'log' )
	if logy : ax.set_yscale ( 'log' )

	if show: fig.show( )
	return fig, ax

def errorbar ( x , y , yerr=None, xlabel='' , xlim=() , ylim=() , ylabel=() , markerstyle='.' , markersize=1 , 
		   size=(6,6) , dpi=100 , show=False , logx=False , logy=False , alpha=1 , title='', 
		   color='black' , linewidth=0 , linestyle='-' , label='' , leg=False , zorder=1 , ecolor='black', elinewidth=None, capsize=2, ) : 

	
	fig, ax = plt.subplots( figsize=size , dpi=dpi )
	if yerr is None:
		ax.plot ( x , y , markerstyle , markersize=markersize , linestyle=linestyle , linewidth=linewidth , color=color , alpha=alpha , label=label , zorder=zorder )
	else:
		plt.errorbar ( x , y , yerr=yerr,  markersize=markersize , linestyle=linestyle , linewidth=linewidth , color=color , alpha=alpha , label=label , zorder=zorder , elinewidth=elinewidth , capsize=capsize )
	if leg: ax.legend()
	ax.set_title  ( title  )
	ax.set_xlabel ( xlabel )
	ax.set_ylabel ( ylabel )
	if xlim: ax.set_xlim   ( xlim   )
	if ylim: ax.set_ylim   ( ylim   )


	if logx : ax.set_xscale ( 'log' )
	if logy : ax.set_yscale ( 'log' )

	if show: fig.show( )
	return fig, ax

# requires fig and axis objects, returned by plot() and x and y data
# returns same figure and axis objects
def plot_existing ( fig , ax , x , y , show=False , markerstyle='.' , markersize=1 , alpha=1 ,
					linewidth=0 , linestyle='-' , color='black' , label='' , leg=False , zorder=2 ,
					markerfacecolor='black' , markeredgecolor='black' ):
	
	ax.plot ( x , y , markerstyle , markersize=markersize , linestyle=linestyle , 
		linewidth=linewidth , color=color , alpha=alpha , label=label , zorder=2, 
		markerfacecolor=markerfacecolor , markeredgecolor=markeredgecolor )
	if leg : ax.legend()

	if show: fig.show()
	return fig, ax

# show figure
def show ( fig , leg_loc=(0,0)): 
	fig.legend(bbox_to_anchor=leg_loc)
	plt.tight_layout()
	fig.show()
	
# show all figures
def show ( leg_loc=(0,0) ): 
	# plt.legend(bbox_to_anchor=leg_loc)
	plt.tight_layout()
	plt.show()

# this one is scary -- 2d plot with colorscale for another axis of information
def hist2d ( x , y , title='' , xlabel='' , ylabel='number' , binsx=100 , binsy=100 , xlim=() , dopdf=False ,
	 	   logx=False , logy=False , size=(6,6), dpi=100 , show=False , ylim=() , norm=False , 
	 	   cmap='hot' , alpha=1 , label='' , ret_hist=True , cbar_label='' ) :

	fig, ax = plt.subplots ( figsize=size , dpi=dpi )
	h,xbin,ybin,img = ax.hist2d ( x , y , bins=[binsx,binsy] , cmap=cmap , range=[ xlim , ylim ] )
	divider = make_axes_locatable(ax)
	cax = divider.append_axes('right', size='5%', pad=0.05)
	cbar = fig.colorbar ( img , cax=cax )
	if xlim : ax.set_xlim  ( xlim )
	if ylim : ax.set_ylim  ( ylim )
	if logx : ax.set_xscale( 'log' )
	if logy : ax.set_yscale( 'log' )
	if cbar_label: 
		cbar.ax.get_yaxis().labelpad = 15
		cbar.ax.set_ylabel(cbar_label, rotation=270)
	ax.set_xlabel ( xlabel )
	ax.set_ylabel ( ylabel )
	ax.set_title  ( title  )

	if show: fig.show ( )
	ret = fig, ax
	if ret_hist: ret = fig,ax,h,xbin,ybin,img

	return ret

# normal 1d histogram; only requires x data values
# returns fig and axis objects
def hist ( x , title='' , xlabel='' , ylabel='number' , bins=100 , xlim=() , dopdf=False ,
	 	   logx=False , logy=False , size=(6,6), dpi=100 , show=False , ylim=() , norm=False , 
	 	   color='black' , ret_hist=False , cumulative=False, label='' ) :

	nPerBin, binEdges, patches = 0 , 0 , 0
	nparray = np.ndarray.flatten( x )

	if( norm ):
		# nTotal = np.sum( nparray )
		nTotal = len(nparray)
	else:
		nTotal = 1
	
	fig , ax = plt.subplots ( figsize=size , dpi=dpi )
	
	if xlim : 
		ax.set_xlim ( xlim )
		if logx : 
			xmin , xmax = xlim[0] , xlim[1]
			logbins = 10 ** np.linspace( np.log10(xmin), np.log10(xmax) )
			nPerBin, binEdges, patches = ax.hist( nparray/nTotal, bins=logbins, density=dopdf, histtype='step', range=xlim , color=color , cumulative=cumulative )
		else:
			nPerBin, binEdges, patches = ax.hist( nparray/nTotal, bins=bins,   density=dopdf, histtype='step', range=xlim  , color=color , cumulative=cumulative, label=label)
	else:
		nPerBin, binEdges, patches = ax.hist( nparray/nTotal, bins, density=dopdf, histtype='step' , color=color, cumulative=cumulative, label=label )
	binCenters = (shift(binEdges,-1)[:-1]+binEdges[:-1])/2  #should use np.roll NOT shift! here and elsewhere
	
	ax.set_xlabel ( xlabel )
	ax.set_ylabel ( ylabel )
	ax.set_title  ( title  )
	if ylim : ax.set_ylim   ( ylim   )
	if logx : ax.set_xscale ( 'log' )
	if logy : ax.set_yscale ( 'log' )
	# if not label == '' : ax.legend()
	if show : fig.show( )

	ret = fig, ax
	if ret_hist: ret = fig, ax , nPerBin , binEdges , patches

	return ret

def hist_existing ( fig , ax , x, show=False , label='', color='black', bins=100, ret_hist=False , cumulative=False , leg=False , histtype='step',): 
	nPerBin, binEdges, patches = ax.hist ( x , label=label , color=color, bins=bins, cumulative=cumulative , histtype=histtype,  )
	if leg: ax.legend()
	if show : fig.show()
	ret = fig, ax
	if ret_hist: ret = fig, ax, nPerBin, binEdges, patches
	return ret

#-----------------------------------------------------------------------------------
# plots  npn vs npx as if the data is a histogram instead of histogramming the array
# assumes that npx is the bin edges returned by np.hist
def plotAsHistogram( npBinEdges, npValues, title='', xrange=(), xlabel="", xticks=(), yrange=(), ylabel='value', logx=False, logy=False, doShow=False,
                    bShowErrorBars=False, bPoissonErrors=False, bUseYErrorVectors=False, yErrorNeg=[], yErrorPos=[],
                    plotFunc=True, xfunc=(), yfunc=(), figsize=(8,8), dpi=200 ):
    
    pyplot.figure( figsize=figsize, dpi=dpi )
    
    if ( xrange ): pyplot.xlim( xrange )
    if ( yrange ): pyplot.ylim( yrange )
        
    npValuesNoNaN = np.nan_to_num( npValues )
    
    pyplot.hist( npBinEdges[:-1], npBinEdges, weights=npValuesNoNaN, histtype="step" )
    
    if ( logy ): pyplot.yscale( "log" )
        
    if ( logx ): pyplot.xscale( "log" )
    
    binCenters = (shift(npBinEdges,-1)[:-1]+npBinEdges[:-1])/2
        
    if( bShowErrorBars ):
        if( bPoissonErrors ):  yError = np.sqrt( npValues );  yErrorPos = yError;  yErrorNeg = yError         
        pyplot.errorbar( binCenters, npValues, yerr=[ yErrorNeg, yErrorPos ], fmt='none' )

    pyplot.xlabel( xlabel )
    pyplot.ylabel( ylabel )

    if( plotFunc ):  pyplot.plot( xfunc, yfunc, 'g-' )
    
    if( xticks ):  pyplot.xticks( xticks[0], xticks[1] )

    if( title != '' ):  pyplot.title( title )
    
    if ( doShow ):  pyplot.show()
    
# ignore this one for now!!
def plot_fraction ( fig , ax , nPerBin , nPerBin_all , bins_all , xlim , yscale='linear' , ymax=1 , legloc='upper right' , leg=True , bx=.85 , by=.85) :

	ax_2 = ax.twinx()
	ax_2.set_yticks ( np.linspace (0,10,11)/10 )
	ax_2.set_yticklabels ( np.linspace (0,10,11)/10 )
	ax_2.set_ylim (1e-5 , ymax)
	ax_2.set_yscale(yscale)
	ax_2.set_xlim (xlim)
	ax_2.set_ylabel ('fraction of population detected')
	fig.subplots_adjust(right=0.85)

	#  np.linspace(a_xlim[0], a_xlim[1], len(nPerBin)) 
	plot_existing ( fig , ax_2 , [np.mean(bins_all[i:i+2]) for i in range(len(bins_all)-1)] , nPerBin/nPerBin_all , linestyle='solid' , linewidth=5 , markersize=6 , label='Fraction detected' , leg=False , color='blue' , zorder=10)
	# plot_existing ( fig , ax_2 , bins_all , nPerBin/nPerBin_all , linestyle='solid' , linewidth=5 , markersize=6 , label='Fraction detected' , leg=False , color='blue' , zorder=10)

	# fig.legend(loc='upper right')
	if leg : fig.legend(loc=legloc, bbox_to_anchor=(bx , by))
	return fig, ax_2