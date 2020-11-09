##Todo 
# >Process images in Imaage J (make note of paramters), generate csv files for anaysis.
# >Analyse csv files...
#   > what are the main headers of interst?
#   > Generate histograms of particle size distributions (are there any clear catagories?)
#   > std dev and means, etc

import pandas as pd
import numpy as np
import sys 

#set 1 calibrated to 140 px/1mm

#Creates a label of descriptive statistics on graph.
def write_pandas_stats_description_on_graph(graph_obj, pandas_obj, x, y, gap):
    
    #typecast pandas_obj to string, then generate a list from entries to organize them.
    display_text = str(pandas_obj.describe()["radii"]).split("\n")[:-1]    
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
            tmp[1] = str("{0:.2f}".format(float(tmp[1])))
        
        
        #seperating lables from data to make it easier to organize the text.
        data_info.append(tmp[0])
        stat_data.append(tmp[1])
        
    #adding dispersity value: std-dev/mean
    #https://www.materials-talks.com/blog/2017/10/23/polydispersity-what-does-it-mean-for-dls-and-chromatography/
    data_info.append("dispersity %")
    stat_data.append(str("{0:.2f}".format(pandas_obj.std()["radii"]*100/pandas_obj.mean()["radii"])))
    print(pandas_obj.mean()["radii"])

    
    #rejoining the labels/ text into their own string blocks that can be
    # easily organize relative to each other.
    data_info = "\n".join(data_info)
    stat_data = "\n".join(stat_data)
    
    graph_obj.text(x,y, data_info)
    graph_obj.text(x+gap,y, stat_data)

def main():
    
    #get the csv file of interest
    df = pd.read_csv("..\\09_11_2020\\set_1\\summary.csv")
    
    #filtering unreasonably small particles (basically dust)
    df_area = df.query("Area>0.05")
    
    # converting from area to average radius.
    df_radii = pd.DataFrame(columns=["radii"])
    df_radii["radii"] = np.sqrt(df_area["Area"]/np.pi)
    
    #plotting data
    ax = df_radii["radii"].plot.hist(bins=20)
    ax.set_xlabel("Avg radii (mm)")
    ax.set_ylabel("Frequency")
    ax.set_title("Set 1\n(140 px/1mm)")
    
    #Writing analytics on graph
    write_pandas_stats_description_on_graph(ax, df_radii, 0.24, 9.5, 0.05)


if __name__ == "__main__":
    main()
    
    