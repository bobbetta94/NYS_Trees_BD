import pandas as pd
import geopandas as gpd
import requests

# %% Preparing Forest Data

# reading in forest data
forest = gpd.read_file('DECSLFStands.zip')

# useful variables:
    # STAND_BASA:
        # The cross-sectional area of all stems of a species or all stems in a stand measured at breast height and expressed in sq/ft
    # DIG_ACRES
        # Acreage of the stand as digitized
    # DIG_YEAR
        # Year of last adjustment to a State Forests stand boundaries
    # TREE_TYPE1
        # The 3 species of greatest prominence in the stand. Tree type 1 would occupy the greatest percentage of the stand basal Area, followed by Tree type 2 etc
    # CALC_FT
        # Primary forest cover type (sfid calculated)
        
# selects UNIT column to remove unit numbers and preserve county names
county = forest["UNIT"]
county = county.str.split()

# deletes last element in each list of the series
for c in county:
    if c is not None:
        del c[-1]

# changes format of county names to match that in other datasets to be used
county_joined = county.str.join(' ')
county_final = county_joined.str.title()
# county_final = county_title.str.replace(pat = '.', repl = '', regex = False)


# selects relevant columns to make a new dataframe
forest_new = forest[['STAND_BASA', 'DIG_ACRES', 'DIG_YEAR', 'TREE_TYPE1', 'CALC_FT']].copy()
forest_new['county'] = county_final
forest_new.to_csv('forest_data.csv')

# %% Preparing Census Population Data

# creates variables for information to be used in API request
var_list = ['COUNTY', 'DENSITY', 'GEO_ID', 'POP']
var_string = ','.join(var_list)
api = 'http://api.census.gov/data/2019/pep/population'
for_clause = 'county:*'
in_clause = 'state:36'
key_value = '42d5820661d7ac8b32aaecf97250cd92b2f8fd10'

pop = {'get':var_string, 'for':for_clause, 'in':in_clause, 'key':key_value}

response = requests.get(api, pop)

# checks if request succeeded
if response.status_code == 200:
    print('Request succeeded.')
else:
    print(response.status_code)
    print(response.text)
    assert False

# defines column names and data for the dataframe
row_list = response.json()
colnames = row_list[0]
datarows = row_list[1:]

# creates dataframe from data requested from API server
pop_data = pd.DataFrame(columns = colnames, data = datarows)
pop_data = pop_data.astype({'DENSITY':'float', 'POP':'int', 'county':'int'})
pop_data['GEO_ID'] = pop_data['GEO_ID'].str.slice(-5)

# %% Loading in county names and FIPS codes and joining with population data

# read int NYS county names and FIPS code data to merge onto Census API data
fips = pd.read_csv('nys_counties.csv', dtype=str)
fips = fips.astype({'code':'int'})

# merges pop_data and fips to get county names in API dataset
pop_fips = pop_data.merge(fips, how = 'inner', left_on = 'county', right_on = 'code', validate = 'm:1')

pop_fips = pop_fips.drop(columns = ['COUNTY', 'state', 'county_x', 'code'])
pop_fips['county'] = pop_fips['county_y']
pop_fips = pop_fips.drop(columns = 'county_y')

# reads in NYS county poverty rates data to merge with pop_fips 
poverty = pd.read_csv('nys_poverty.csv')
pop_all = pop_fips.merge(poverty, how = 'inner', on =  'county', validate = 'm:1')

pop_all.to_csv('population.csv')


# %% Joining Population Data and Forest Data
 
# forest_final = forest_new.merge(pop_all, how = 'inner', on = 'county', validate = 'm:1')
# forest_final = forest_final.astype({'STAND_BASA':'int', 'DIG_ACRES':'float', 'DENSITY':'float', 'POP':'int'})






