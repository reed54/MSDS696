'''o
 Colorad Election Abstract processing functions.
'''
# Count Plot of Republican versus Democrat Counties
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import pickle

def get_maj_counties(dfi): 
    df = dfi.copy(deep = True)
    
    df['Reppct'] = df['Republican'] / (df['Republican'] + df['Democrat']) * 100
    df['Dempct'] = df['Democrat'] / (df['Republican'] + df['Democrat']) * 100
    df['Majority'] = 'Republican'
    df.loc[df['Dempct'] > 50, 'Majority'] = 'Democrat'
    #print(df)
    dem_county = []
    rep_county = []
    for c, i in zip(df.County, range(len(df.County))):
        if df['Reppct'][i] >= 50:
            rep_county.append(c)
        else:
            dem_county.append(c)

    #print(f'Democrat Counties:\n {len(dem_county)}\n {dem_county}\n\n')
    #print(f'Republican Counties:\n {len(rep_county)}\n{rep_county}\n\n')


    dem_votes = df['Democrat'].sum()
    rep_votes = df['Republican'].sum()
    dem_pct  = dem_votes / (df['Republican'] + df['Democrat']) * 100
    rep_pct = rep_votes / (df['Republican'] + df['Democrat']) * 100

    #print(f'    Democrat Votes:  {dem_votes:.0f} {dem_pct:.2f}%')
    #print(f'  Republican Votes:  {rep_votes:.0f} {rep_pct:.2f}%')
    
    num_counties = {'Republican Majority': len(rep_county),'Democrat Majority': len(dem_county)}
    
    cat_order = ['Democrat', 'Republican']
    print(num_counties)
    df['Majority'] = 'Republican'
    df.loc[df['Dempct'] > 50, 'Majority'] = 'Democrat'
    sns.catplot(x = 'Majority', kind = "count", order = cat_order, data = df, palette = {"Republican": 'Red', "Democrat": 'Blue'})
    plt.title("Number of Counties with Majority Democrat or Republican")
    plt.show()
    return(df)


def dem_vs_rep_scatter(dfi):
    df = dfi.copy(deep = True)
    #print(df)
    max_votes = int(max(df['Republican'].max(), df['Democrat'].max()))
    min_votes = int(min(df['Republican'].min(), df['Democrat'].min()))

    X_plot = range(max_votes,min_votes, -1)
    Y_plot = range(max_votes, min_votes, -1)
    cat_order = ["Democrat", "Republican"]
    plot = sns.relplot(x = 'Republican', y = 'Democrat', data = df, 
                       hue = 'Majority', kind = "scatter",
                       palette = {"Republican": 'Red', "Democrat": 'Blue'})
    plot.set(xscale='log', yscale='log')  
    plot = plt.plot(X_plot, Y_plot, color='k')
    plt.title("County Votes for Democrat versus Republican")
    plt.show()
    return


def get_top_counties(dfi, n = 12):
    '''
    Sort counties by total votes in descending order.  
    Return top n counties in data frame.
    '''
    data = dfi.copy(deep = True)
    data['Total'] = data['Democrat'] + data['Republican']
    data = data.sort_values('Total',  ascending = False)
    num = n * 2
    drec = []
    for c in range(data.shape[0]):
        cnty = data.iloc[c,:]['County']
        rec = {'County': cnty, 'Party': 'Democrat', 'Votes': data.iloc[c,:]['Democrat']}
        drec.append(rec)
        rec = {'County': cnty, 'Party': 'Republican', 'Votes': data.iloc[c,:]['Republican']}
        drec.append(rec)
    d = pd.DataFrame.from_dict(drec)
    print(d.shape)
    dtop = d.head(num)

    plot = sns.barplot(x = 'County', y = 'Votes', data = dtop, hue = 'Party', palette = {"Republican": 'Red', "Democrat": 'Blue'})
    plot.set_xticklabels(plot.get_xticklabels(), rotation=45)
    plt.title("Total Votes by Top " + str(n) + " Counties")
    plt.show()
    return
    

    
def save_majority_report(dfi, year):
    '''
    Add County FIPS code to data frame and saves majority  report in ../data/processed/abstracts
    '''
    df = dfi.copy(deep = True)
    countyLookup =         {'Adams': '001',      'Alamosa': '003',     'Arapahoe': '005',    'Archuleta': '007', 
                            'Baca': '009',       'Bent': '011',        'Boulder': '013',     'Broomfield': '014',  
                            'Chaffee': '015',    'Cheyenne': '017',    'Clear Creek': '019', 'Conejos': '021',  
                            'Costilla': '023',   'Crowley': '025',     'Custer': '027',      'Delta': '029',    
                            'Denver': '031',     'Dolores': '033',     'Douglas': '035',     'Eagle': '037',       
                            'El Paso': '041',    'Elbert': '039',      'Fremont': '043',     'Garfield': '045',   
                            'Gilpin': '047',     'Grand': '049',       'Gunnison': '051',    'Hinsdale': '053',  
                            'Huerfano': '055',   'Jackson': '057',     'Jefferson': '059',   'Kiowa': '061',  
                            'Kit Carson': '063', 'La Plata': '067',    'Lake': '065',        'Larimer': '069',    
                            'Las Animas': '071', 'Lincoln': '073',     'Logan': '075',       'Mesa': '077',      
                            'Mineral': '079',    'Moffat': '081',      'Montezuma': '083',   'Montrose': '085',    
                            'Morgan': '087',     'Otero': '089',       'Ouray': '091',       'Park': '093',       
                            'Phillips': '095',   'Pitkin': '097',      'Prowers': '099',     'Pueblo': '101',  
                            'Rio Blanco': '103', 'Rio Grande': '105',  'Routt': '107',       'Saguache': '109',    
                            'San Juan': '111',   'San Miguel': '113',  'Sedgwick': '115',    'Summit': '117',    
                            'Teller': '119',     'Washington': '121',  'Weld': '123',        'Yuma': '125'} 
    cnty_lst = [countyLookup[c] for c in df['County']]
    df["CNTY_FIPS"] = cnty_lst
    data_path = '../data/processed/abstracts/'
    fn = data_path + 'co_' + str(year) + "_majority.p"
    pickle.dump(df, open(fn, "wb"))

    return(df)

def gen_colorado_red_blue_map(dfi, title, f_name):


    sns.set_style('whitegrid')
    data_df = dfi.copy(deep = True)
    
    # This is the baseline map for all of our choropleth maps - Colorado counties.
    fp =  '../data/shape/Colorado_County_Boundaries.shp'
    map_df = gpd.read_file(fp)

    # change the data types of the key index fields to integer so that it matches our census data index
    map_df = map_df.astype({"CNTY_FIPS": int, "US_FIPS": int})
    map_df.reset_index(drop=True,inplace=True)
    
    data_df = data_df.rename(columns={"state_id": "STATEFP", "county_id": "CNTY_FIPS"})
    data_df['CNTY_FIPS'] = data_df['CNTY_FIPS'].astype(int)

    merged = map_df.set_index(['CNTY_FIPS']).join(data_df.set_index(['CNTY_FIPS']))
    merged = merged.drop(index = 14)
    dem_cntys = [merged.iloc[i]['County'] for i in range(merged.shape[0]) if merged.iloc[i]['Majority'] == 'Democrat']
    rep_cntys = [merged.iloc[i]['County'] for i in range(merged.shape[0]) if merged.iloc[i]['Majority'] == 'Republican']

    if len(dem_cntys) <= len(rep_cntys):
        print(f'Democratic majority counties: {dem_cntys}')
    else:
        print(f'Republican majority counties: {rep_cntys}')

    # Plotting the election results
    # Create an array with the colors you want to use
    colors = ["#EFDECD","#031cfc"]
    # Set your custom color palette
    customPalette = sns.set_palette(sns.color_palette(colors))

    fig, ax = plt.subplots(1,figsize=(10, 6))
    ax.axis('off')
    ax.set_title(title, fontdict={'fontsize': '25', 'fontweight' : '3'})
    merged.plot(column='Majority', linewidth=0.7,ax=ax,cmap = 'BuPu', edgecolor='0.8', legend=True)
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((1, 0.7, 0.2, 0.2))
    plt.show()
    #fig.savefig(“map_export.png”, dpi=300)
   
    
    return