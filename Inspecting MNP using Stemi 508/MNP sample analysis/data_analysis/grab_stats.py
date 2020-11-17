##Todo 
# >Process images in Imaage J (make note of paramters), generate csv files for anaysis.
# >Analyse csv files...
#   > what are the main headers of interst?
#   > Generate histograms of particle size distributions (are there any clear catagories?)
#   > std dev and means, etc

## Reference:
#   > https://matplotlib.org/3.1.3/gallery/statistics/hist.html
   

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import numpy as np
import sys 

#set 1 calibrated to 140 px/mm
#set 2 calibrated to 1101.67 px/mm
#set 3A calibrated to 438.67 px/mm
#set 3B calibrated to 875.00 px/mm

#Creates a label of descriptive statistics on graph.
def write_pandas_stats_description_on_graph(graph_obj, pandas_obj, x, y, gap):
    
    #typecast pandas_obj to string, then generate a list from entries to organize them.
    display_text = str(pandas_obj.describe()["diam"]).split("\n")[:-1]    
    data_info = [] #holds labels
    stat_data = [] #holds data
    
    #formatting the analytics text to make it neater
    for i in range(len(display_text)):
        
        tmp = display_text[i].split()
        
        #the "count" value should be an integer, but looks like a float
        # when the pandas object is typecast into a string (fixing that here)
        if(tmp[0] == "count"):
            tmp[-1] = str(int(float(tmp[-1])))
        else:
            tmp[1] = str("{0:.4f}".format(float(tmp[1])))
        
        
        #seperating lables from data to make it easier to organize the text.
        data_info.append(tmp[0])
        stat_data.append(tmp[1])
        
    #adding dispersity value: std-dev/mean
    #https://www.materials-talks.com/blog/2017/10/23/polydispersity-what-does-it-mean-for-dls-and-chromatography/
    data_info.append("dispersity %")
    stat_data.append(str("{0:.2f}".format(pandas_obj.std()["diam"]*100/pandas_obj.mean()["diam"])))
    print(pandas_obj.mean()["diam"])

    
    #rejoining the labels/ text into their own string blocks that can be
    # easily organize relative to each other.
    data_info = "\n".join(data_info)
    stat_data = "\n".join(stat_data)
    
    graph_obj.text(x,y, data_info)
    graph_obj.text(x+gap,y, stat_data)


def generate_graph(path, filter_dims, set_bins, is_log=True, title = "some_title", x_label = "Avg diameter (um)", y_label = "Frequency"):
    
#Preparing dataframe#

    # generating a dataframe from the csv file.
    df_area = pd.read_csv(path)
    
    #converting the area to an average diameter
    df_diam = pd.DataFrame(columns=["diam"])
    df_diam["diam"] = np.sqrt(df_area["Area"]/np.pi)*2*(10**3) #NOTE: setting units to um (originally mm)
    
    #filtering particles sizes that are beyond the ROI
    for dim in filter_dims:
        df_diam = df_diam.query("diam"+dim)

#plotting data#
    
    # instantiating plot object
    fig, ax = plt.subplots(tight_layout=True)
    N, bins, patches = ax.hist(bins=set_bins, x=df_diam["diam"])

    # normalizing data (https://matplotlib.org/3.1.3/gallery/statistics/hist.html)
    fracs = N/N.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    # set color of each bar according to its height.
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)
    
    # creat labels 
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    
    if is_log:
        ax.set_xscale('log')
        
    
#Writing analytics on graph#

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    txt_y_origin = 0
    txt_x_stp    = 0
    txt_x_origin = 0

    if is_log:
        txt_y_origin = (y_max-y_min)/2.1
        txt_x_stp    = x_max-x_max/1.75
        txt_x_origin = x_max - txt_x_stp*1.9 
        txt_x_stp    = x_max-x_max/1.5
    else:
        txt_y_origin = (y_max-y_min)/2.1
        txt_x_stp    = (x_max-x_min)/5
        txt_x_origin = x_max - 1.7*txt_x_stp     
    
    write_pandas_stats_description_on_graph(ax, df_diam, txt_x_origin, txt_y_origin, txt_x_stp)
    

    
    
def main():
    

    path_set_1  = "..\\09_11_2020\\set_1\\summary.csv"
    title_1     ="Set 1\n(140 px/mm)"
    
    path_set_2  = "C:\\Users\\alfre\\Desktop\\Inspecting MNP from Quentin with Stemi 508\\MNP sample analysis\\09_11_2020\\set_2\\summary.csv"
    title_2     = "Set 2\n(1102 px/mm)"
    
    path_set_3A  = "C:\\Users\\alfre\\Desktop\\Inspecting MNP from Quentin with Stemi 508\\MNP sample analysis\\09_11_2020\\set_3\\2_0x_bodyZoom\\summary.csv"
    title_3A     = "Set 3A\n(439 px/mm)"
    
    path_set_3B  = "C:\\Users\\alfre\\Desktop\\Inspecting MNP from Quentin with Stemi 508\\MNP sample analysis\\09_11_2020\\set_3\\4_0x_bodyZoom\\summary.csv"
    title_3B     = "Set 3B\n(875.00 px/mm)"
    
    fltr_dim = [">0"]
    
    generate_graph(path=path_set_1, title=title_1, filter_dims=fltr_dim, set_bins=200, is_log=False)
    generate_graph(path=path_set_2, title=title_2, filter_dims=fltr_dim, set_bins=200, is_log=False)
    generate_graph(path=path_set_3A, title=title_3A, filter_dims=fltr_dim, set_bins=200, is_log=False)
    generate_graph(path=path_set_3B, title=title_3B, filter_dims=fltr_dim, set_bins=200, is_log=False)
    
if __name__ == "__main__":
    main()
    
    