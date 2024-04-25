#%% PREPROCESSING
# libs and defs
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter, defaultdict
import ast
from tqdm import tqdm
import heapq

# create list of years based on input start and end years
def year_list(start_year:int, end_year:int):
    return [year for year in range(start_year, end_year + 1)]

# look for target inst/country/region
def contains_target(s, targets):
    return not s.isdisjoint(targets)

# category count by conference
def count_by_conf(data:pd.DataFrame):
    return data['Conference'].value_counts()

# category count by year
def count_by_year(data:pd.DataFrame):
    return data['Year'].value_counts()

# number of matching publications
def count_total_publ(data:pd.DataFrame):
    return len(data)

# display set of all inst/country/region
def show_options(label:str,data:pd.DataFrame):
    data[label] = data[label].apply(ast.literal_eval)
    return set().union(*data[label])

# save file
def save_to_csv(data:pd.DataFrame,file_name:str):
    data.to_csv(file_name, index=False)

# filter functions
def filter_by_year(data:pd.DataFrame,target:list):
    data = data[data['Year'].isin(target)]
    return data

def filter_by_conf(data:pd.DataFrame,target:list):
    data = data[data['Conference'].isin(target)]
    return data

def filter_by_inst(data:pd.DataFrame,target:list):
    data = data[data['Affiliations'].apply(contains_target, args=(target,))]
    return data

def filter_by_country(data:pd.DataFrame,target:list):
    data = data[data['Countries'].apply(contains_target, args=(target,))]
    return data

def filter_by_region(data:pd.DataFrame,target:list):
    data = data[data['Region'].apply(contains_target, args=(target,))]
    return data

# apply filter functions based on input parameters
def search(data:pd.DataFrame,
           lookup_years:list,
           lookup_conf:list,
           lookup_country:list,
           lookup_region:list,
           lookup_inst:list):
    
    # filter by year
    if lookup_years:
        data = filter_by_year(data,lookup_years)

    # filter by conference
    if lookup_conf:
        data = filter_by_conf(data,lookup_conf)

    # 3 choose 1
    if lookup_country:
        data = filter_by_country(data,lookup_country)
    elif lookup_region:
        data = filter_by_region(data,lookup_region)
    elif lookup_inst:
        data = filter_by_inst(data,lookup_inst)

    return data

# determine top N institutions from the filtered dataset
def get_topN(top_n:int,data:pd.DataFrame):
    publ_counts = Counter()

    for row in data['Affiliations']:
        publ_counts.update(row)

    return heapq.nlargest(top_n, publ_counts, key=publ_counts.get)

# get ranking of particular institution
def get_ranking(data:pd.DataFrame,inst:str):
    df = data.explode('Affiliations')
    val_counts = df['Affiliations'].value_counts()
    return val_counts.index.get_loc(inst)+1

# visualization
def inst_data(data:pd.Series,title:str,label:str):


    graph = data.plot(kind='bar')

    plt.title(title)
    plt.xlabel(label)
    plt.ylabel('Count')

    for p in graph.patches:
        graph.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()-1),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    plt.show()


#%% DATA
# read and format csv data
publications = pd.read_csv('DBLP_publications_2024-01-22.csv')
publications['Affiliations'] = publications['Affiliations'].apply(ast.literal_eval)
publications['Countries'] = publications['Countries'].apply(ast.literal_eval)
publications['Region'] = publications['Region'].apply(ast.literal_eval)
#%% MBZUAI data
# parameters
lookup_years = year_list(2023,2023)
lookup_conf = ['aaai','acl','cvpr','eccv','emnlp','iccv','iclr','icml','icra','ijcai','iros','naacl','nips','rss']
lookup_country = []
lookup_region = []
lookup_inst = ['MBZUAI']

mbzuai_result = search(publications,lookup_years,lookup_conf,lookup_country,lookup_region,lookup_inst)
#search_result.to_csv('test.csv', index=False) 

conf_result = count_by_conf(mbzuai_result)
year_result = count_by_year(mbzuai_result).sort_index()
inst_data(conf_result,'MBZUAI Publications 2021-2023','Conference')
inst_data(year_result,'MBZUAI Publications 2021-2023','Year')
#%%
conf_result
#%%
conference_counts = mbzuai_result.groupby(['Year', 'Conference']).size().reset_index(name='count')
conference_counts_sorted = conference_counts.sort_values(by='Conference')
conference_counts_sorted
# %% Compare mbzuai with global top 10
# parameters
lookup_years = year_list(2021,2023)
lookup_conf = ['aaai','acl','cvpr','eccv','emnlp','iccv','iclr','icml','icra','ijcai','iros','naacl','nips','rss']
lookup_country = []
lookup_region = []
lookup_inst = []

target_inst = 'MBZUAI'
world_top = get_topN(10,search(publications,lookup_years,lookup_conf,lookup_country,lookup_region,lookup_inst))

world_top.append(target_inst)
global_result = search(publications,lookup_years,lookup_conf,lookup_country,lookup_region,world_top)

counts = defaultdict(Counter)

for _, row in global_result.iterrows():
    year = row['Year']
    for value in world_top:
        if value in row['Affiliations']:
            counts[year][value] += 1

filtered_counts = {year: {value: counts[year][value] for value in world_top} for year in counts}
filtered_counts = dict(sorted(filtered_counts.items()))

df = pd.DataFrame.from_dict(filtered_counts)

ax = df.plot(kind='bar')

plt.title('Publications by Top 10 Institutions')
plt.xlabel('Institution')
plt.ylabel('Count')
plt.show()
#%% get ranking of particular institution
lookup_years = year_list(2021,2023)
lookup_conf = ['aaai','acl','cvpr','eccv','emnlp','iccv','iclr','icml','icra','ijcai','iros','naacl','nips','rss']
lookup_country = ['il']
lookup_region = []
lookup_inst = []

target_inst = 'Tel Aviv University'

data = search(publications,lookup_years,lookup_conf,lookup_country,lookup_region,lookup_inst)
get_ranking(data,target_inst)


#%% global top 10
world_top = get_topN(10,search(publications,lookup_years,lookup_conf,lookup_country,lookup_region,lookup_inst))


global_result = search(publications,lookup_years,lookup_conf,lookup_country,lookup_region,world_top)

counts = defaultdict(Counter)

for _, row in global_result.iterrows():
    year = row['Year']
    for value in world_top:
        if value in row['Affiliations']:
            counts[year][value] += 1

filtered_counts = {year: {value: counts[year][value] for value in world_top} for year in counts}
dict(sorted(filtered_counts.items()))

# %%
