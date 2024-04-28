# preprocessing
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm
import ast

# definitions

# parse xml
def parse(xml_file_path:str):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    return root

# load csv data
def load_csv(csv_file:str):
    data = pd.read_csv(csv_file)
    return data

# unpack parsed xml data into dataframe format for processing
def unpack(root):
    cols = ['Title','Conference','Year','Authors']
    df = pd.DataFrame(columns=cols)
    rows = []

    for p in root:

        author_list = []
        for author in p.findall('.//author'):
            author_list.append(author.text)

        row = {'Title': p.find('title').text, 
            'Conference': p.attrib['key'].split('/')[1], 
            'Year': int(p.find('year').text),
            'Authors': author_list,}
        rows.append(row)

    rows_df = pd.DataFrame(rows)
    df = pd.concat([df, rows_df], ignore_index=True)
    return df

# set data editor
def replace_set(s, country, region):
    if country in s:
        s.remove(country)
        s.add(region)
    return s

# find country of list of institutions   
def inst2countries(country_info:pd.DataFrame,inst_list:list):
    countries = []
    for inst in inst_list:
        country = country_info[country_info['institution'] == inst]['countryabbrv']
        if not country.empty:
            countries.append(country.iloc[0])
        else:
            countries.append('us')
    return set(countries)

# find multiple author affiliation
def names2insts(authors:list,csr:pd.DataFrame):
    affils = []
    for author in authors:
        try:
            inst = csr[csr['name'] == author]['affiliation']
            affils.append(inst.iloc[0])
        except:
            continue
    return set(affils)

# find region of list of institutions   
def country2region(country_info:pd.DataFrame,country_list:list):
    regs = []
    for c in country_list:
        reg = country_info[country_info['countryabbrv'] == c]['region']
        if not reg.empty:
            regs.append(reg.iloc[0])
        else:
            regs.append('us')
    return set(regs)

# save file
def save_to_csv(data,file_name:str):
    data.to_csv(file_name, index=False)  

# parsing
dblp_data = 'datasets/uniranking_data/dblp2.xml'
root = parse(dblp_data)

locations = load_csv('UniRanking\data\country-info.csv')
csr = load_csv('UniRanking\data\csrankings.csv')

publications = unpack(root)

# gather affiliation and country info from author data
inst_list = []
country_list = []
region_list = []

# map location data of institutions
for _, row in tqdm(publications.iterrows(), total=publications.shape[0]):
    authors = row['Authors']

    affils = names2insts(authors,csr)
    affils = set(nonempty for nonempty in affils if nonempty)
    inst_list.append(affils)

    countries = inst2countries(locations,affils)
    country_list.append(countries)

    region = country2region(locations,countries)
    region_list.append(region)

publications['Affiliations'] = inst_list
publications['Countries'] = country_list
publications['Region'] = region_list

result = publications[publications['Affiliations'].apply(lambda x: len(x) > 0)]

# combine us and canada into northamerica region
if any('us' in s for s in result['Region']):
    result['Region'] = result['Region'].apply(ast.literal_eval)
    result['Region'] = result['Region'].apply(lambda s: replace_set(s, 'us', 'northamerica'))
    result['Region'] = result['Region'].apply(lambda s: replace_set(s, 'canada', 'northamerica'))


# Create the filename with the current date
filename = "DBLP_publications.csv"
save_to_csv(result,filename)

# memory usage
total_memory_usage = result.memory_usage(deep=True).sum()
print("Total memory usage:", total_memory_usage/1000000, "MB")

