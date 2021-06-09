#import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date


def bar_chart(df, root_path):

   df.plot(
      kind='bar',
      figsize=(10,6),
      x='Datum',
      y='Anzahl Artikel',
      alpha=0.65,
      
      ylabel='Anzahl Artikel',
      xlabel='Zeitraum in Monaten',
      title=f'Alle Beiträge über Justin Trudeau die zwischen 2018-01-01 und {date.today().strftime("%Y-%m-%d")},\n von The Guardian veröffentlicht wurden.')

   ax = plt.subplot(111)

   ax.yaxis.set_major_locator(plt.MaxNLocator(6)) 
   ax.yaxis.get_major_locator().set_params(integer=True) #use jsut integers on the y axis.
   
   ### beautify graph ###

   # remove ugly frames     
   ax.spines["top"].set_visible(False) 
   ax.spines["right"].set_visible(False)    

   plt.legend(frameon=False, labelcolor='grey') #remove Frame of legend
   plt.gcf().subplots_adjust(bottom=0.2) # make sure all axis lables are visible

   ax.yaxis.label.set_color('grey') 
   ax.xaxis.label.set_color('grey')
   
   #plt.show()
   plt.savefig(f'{root_path}/data/export/{date.today().strftime("%Y-%m-%d")}_graph.png')

   
