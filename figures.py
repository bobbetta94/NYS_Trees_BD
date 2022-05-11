import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% Reading in data

forest_new = pd.read_csv('forest_data.csv')

forest_grouped = forest_new.groupby('county')['STAND_BASA', 'DIG_ACRES'].sum()

pop_all = pd.read_csv('population.csv')

# %% Bar Plots for Forest Cover of Most and Least Densely Populated Counties

plt.rcParams['figure.dpi'] = 300 

county_graph = forest_grouped.merge(pop_all, how = 'inner', on = 'county', validate = 'm:1')
county_graph = county_graph.drop(columns = 'Unnamed: 0')

county_graph.to_csv('forest_counties.csv')

# most densely populated counties
dense_counties = county_graph.nlargest(n=5, columns = ['DENSITY'], keep = 'all')

fig, ax1 = plt.subplots()
sns.barplot(data= dense_counties, x='county', y='DIG_ACRES', hue = 'county', ax=ax1)
ax1.set_title("Dig Acres for 5 Most Densely Populated Counties (Excluding NYC)")
ax1.set_xlabel("County")
ax1.set_ylabel("Acres")
ax1.set_ylim([0, 90000])
fig.tight_layout()
fig.savefig('acres_dense_counties.png')

# most sparsely (least dense) populated counties
sparse_counties = county_graph.nsmallest(n=5, columns = ['DENSITY'], keep = 'all')

fig2, ax2 = plt.subplots()
sns.barplot(data= sparse_counties, x='county', y='DIG_ACRES', hue = 'county', ax=ax2)
ax2.set_title("Dig Acres for 5 Least Densely Populated Counties (Excluding NYC)")
ax2.set_xlabel("County")
ax2.set_ylabel("Acres")
ax2.set_ylim([0, 90000])
fig2.tight_layout()
fig2.savefig('acres_sparse_counties.png')

# dig acres for 5 poorest counties
poor_counties = county_graph.nlargest(n = 5, columns = ['Poverty_Rate'], keep = 'all')

fig3, ax3 = plt.subplots()
sns.barplot(data= poor_counties, x='county', y='DIG_ACRES', hue = 'county', ax=ax3)
ax3.set_title("Dig Acres for 5 Poorest Counties (Excluding NYC)")
ax3.set_xlabel("County")
ax3.set_ylabel("Acres")
ax3.set_ylim([0, 90000])
fig3.tight_layout()
fig3.savefig('acres_poor_counties.png')

# dig acres for 5 richest counties
rich_counties = county_graph.nsmallest(n = 5, columns = ['Poverty_Rate'], keep = 'all')

fig4, ax4 = plt.subplots()
sns.barplot(data= rich_counties, x='county', y='DIG_ACRES', hue = 'county', ax=ax4)
ax4.set_title("Dig Acres for 5 Richest Counties (Excluding NYC)")
ax4.set_xlabel("County")
ax4.set_ylabel("Acres")
ax4.set_ylim([0, 90000])
fig4.tight_layout()
fig4.savefig('acres_rich_counties.png')


