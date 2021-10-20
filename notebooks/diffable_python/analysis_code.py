# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   orig_nbformat: 4
# ---

# + trusted=true
import matplotlib.pyplot as plt
import pandas as pd
from lib.functions import *

# + trusted=true
import os
import sys
from pathlib import Path
cwd = os.getcwd()
parent = str(Path(cwd).parents[0])
sys.path.append(parent)
# -

# # Creating Figure 1

# + trusted=true
#This data is simple and small enough that we can enter it by hand

dates = ['Jan 2018', 'August 2018', 'Sept 2018', 'Nov 2018', 'Dec 2018', 'Jan 2019', 'Feb 2019', 
         'Mar 2019', 'Apr 2019', 'May 2019', 'Jun 2019', 'Jul 2019', 'Aug 2019', 'Sep 2019', 'Oct 2019', 
         'Nov 2019', 'Dec 2019', 'Jan 2020', 'Feb 2020', 'Mar 2020', 'Apr 2020', 'May 2020', 'Jun 2020', 
         'Jul 2020', 'Aug 2020', 'Sep 2020', 'Oct 2020', 'Nov 2020', 'Dec 2020', 'Jan 2021', 'Feb 2021', 
         'Mar 2021', 'Apr 2021', 'May 2021']

months = [0] + list(range(7,40))

reporting = [49.6, 51.1, 51.2, 51.4, 51.9, 52.8, 53.6, 54.1, 55.1, 56.4, 57.2, 58, 60.2, 61.2, 61.5, 61.8, 62.5, 
             63.2, 64, 64.9, 66, 66.2, 66.4, 66.6, 66.3, 66.8, 67.2, 67.9, 68.1, 68.8, 68.9, 69.6, 70.2, 70.2]

# + trusted=true
#sanity check
len(dates) == len(reporting)

# + trusted=true
tstamps = []
for d in dates:
    tstamps.append(pd.Timestamp(d))
    
r_dict = dict(zip(months, reporting))

# + trusted=true
fig, ax = plt.subplots(figsize = (18,8), dpi=300)

pd.Series(r_dict).plot(lw=4, marker='.', markersize=13, grid=True, ax=ax)

ax.set_yticks(range(0,90, 10))
ax.tick_params(axis='both', labelsize=17)

#Optional annotations
#ax.annotate('EU TrialsTracker\nLaunched', xy=('2018-09-12', 51), xytext=(pd.Timestamp('2018-09-12'),60), 
#            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

#ax.annotate('UK Parliment\nSends Letters', xy=('2019-01-24', 53), xytext=(pd.Timestamp('2019-02-01'),40), 
#            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

#ax.annotate('EC/EMA/HMA Joint Letter', xy=('2019-06-01', 57), xytext=(pd.Timestamp('2019-06-10'),70), 
#            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

plt.ylabel('Percent of Due Trials Reported', fontsize=20, labelpad=10)
plt.title('Trend in Results Reporting to the EU-CTR Over Time', pad=10, fontsize=24)
plt.xticks([0,5,10,15,20,25,30,35,40],
          ['Jan 2018', 'Jun 2018', 'Nov 2018', 'Apr 2019', 'Sep 2019', 'Feb 2020', 'Jul 2020', 'Dec 2020', 'May 2021'])

counter = 0
annotations = [0, 4, 9, 14, 19, 24, 29, 33]
for a, b in zip(r_dict.keys(), r_dict.values()):
    if counter in annotations:
        ax.annotate(b, (a-.425, b-4), fontsize=18)
        counter+=1
    else:
        counter+=1
        continue
    
    #if counter == 0:
    #    ax.annotate(b, (a-.4, b-3.2), fontsize=12)
    #    counter += 1
    #else:
    #    ax.annotate(b, (a-.4, b+2), fontsize=12)
    #    counter -= 1
        

plt.show()
#plt.savefig(parent + '/data/euctr_trends.tiff')
# + [markdown]
# # Making the May 2021 Datasets


# + trusted=true
#This is the raw data by trial for the EU TrialsTracker from May 2021 drawn directly from GitHub
df = pd.read_json('https://raw.githubusercontent.com/ebmdatalab/euctr-tracker-data/ae46ca2cfb8918962083b01482c3e8a0b39251f3/all_trials.json')

# + trusted=true
#Only the columns we need
cols = ['trial_id', 
        'results_expected', 
        'has_results', 
        'exempt', 
        'normalized_name', 
        'comp_date_while_ongoing', 
        'all_completed_no_comp_date', 
        'contains_non_eu', 
        'trial_status']

df2 = df[cols].reset_index(drop=True)
# -

# # Country Comparisons

# + trusted=true
#This is the list of sponsors for the country analysis
spons_by_country = pd.read_excel(parent + '/data/sponsors_lists.xlsx', sheet_name='nc_sponsors_country')
# + trusted=true
#This is the raw dataset for the sponsors by country
spon_country_final = spons_by_country.merge(pd.DataFrame(get_stats(df2, spons_by_country.sponsor_name.to_list())), on='sponsor_name')


# + trusted=true
#Test to make sure sponsor name joining worked.
sanity_check(spon_country_final, "total_registered", 0)

# + trusted=true
#How many are in the sample
print(f'There are {spon_country_final.total_registered.sum()} trials in this population.')
print(f'{spon_country_final.due.sum()} are due, and {spon_country_final.due_reported.sum()} are due and reported')

# + trusted=true
#Can check individual country grouping here by changing the string
spon_country_final[spon_country_final.country == 'France']
# -

# # Table 1

# + trusted=true
table_1 = spon_country_final[['country', 'total_registered', 'due', 'due_reported']].groupby('country').sum()
table_1['due_reported_prct'] = round((table_1['due_reported']/table_1['due'])*100,2)
table_1
# -

# # Table 2

# + trusted=true
table_2 = spon_country_final[['country', 'total_registered', 'inconsistent_data', 'comp_ongoing', 'missing_comp', 'contains_non_eu', 'missing_status', 'inconsistent_w_results']].groupby('country').sum()

# + trusted=true
table_2['inconsistent_data_prct'] = round((table_2['inconsistent_data']/table_2['total_registered']) * 100,2)
table_2['comp_ongoing_prct'] = round((table_2['comp_ongoing']/table_2['inconsistent_data'])*100,2)
table_2['missing_comp_prct'] = round((table_2['missing_comp']/table_2['inconsistent_data'])*100,2)
table_2['contains_non_eu_prct'] = round((table_2['contains_non_eu']/table_2['inconsistent_data'])*100,2)
table_2['missing_status_prct'] = round((table_2['missing_status']/table_2['inconsistent_data'])*100,2)
table_2['inconsistent_w_results_prct'] = round((table_2['inconsistent_w_results']/table_2['inconsistent_data'])*100,2)

# + trusted=true
table_2 = table_2[['total_registered', 'inconsistent_data', 'inconsistent_data_prct', 'comp_ongoing', 'comp_ongoing_prct', 'missing_comp', 'missing_comp_prct', 'contains_non_eu', 'contains_non_eu_prct', 'missing_status', 'missing_status_prct', 'inconsistent_w_results', 'inconsistent_w_results_prct']]

# + trusted=true
table_2

# + trusted=true
print(f'Total Inconsistencies: {table_2.inconsistent_data.sum()}')
print(f'Completed & Ongoing: {table_2.comp_ongoing.sum()}')
print(f'Missing Completion Date: {table_2.missing_comp.sum()}')
print(f'Non-EU Location: {table_2.contains_non_eu.sum()}')
print(f'Missing Status: {table_2.missing_status.sum()}')
print(f'Iconsistent with Results: {table_2.inconsistent_w_results.sum()}')
# -

# # Commercial Sponsors

# + trusted=true
#Loading in the commercial sponsor names

comm_spons = pd.read_excel(parent + '/data/sponsors_lists.xlsx', sheet_name='comm_sponsors')

# + trusted=true
comm_spons_final = comm_spons.merge(pd.DataFrame(get_stats(df2, comm_spons.sponsor_name.to_list())), on='sponsor_name')
# -

# # 2021 Major Sponsors Comparison Data 

# + trusted=true
#getting 2018 major spsonsors comparison data

compare_2021 = pd.read_excel(parent + '/data/sponsors_lists.xlsx', sheet_name='sponsor_compare')

# + trusted=true
compare_final = compare_2021.merge(pd.DataFrame(get_stats(df2, compare_2021.sponsor_name.to_list())), on='sponsor_name')

total_2021 = compare_final[['grouped_name', 'total_registered', 'due', 'due_reported']].groupby('grouped_name').sum().reset_index()

total_2021['reported_prct'] = round((total_2021.due_reported / total_2021.due) * 100, 2)

total_2021 = total_2021.merge(compare_final[['grouped_name', 'country']].groupby('grouped_name', as_index=False).max(), how='left', on='grouped_name')

# + trusted=true
total_2018 = pd.read_excel(parent + '/data/sponsors_lists.xlsx', sheet_name='2018_data')
# -

# # Data for Table 3

# + trusted=true
table_3 = total_2018.merge(total_2021, how='left', left_on='2021_name', right_on='grouped_name', suffixes = ['_2018', '_2021'])

# + trusted=true
#Limiting Reporting to the Median and below
table_3[table_3.reported_prct <= 43.33].head()

# + trusted=true
table_3[table_3.country_2021 == 'UK']
# -

# # Table 4

# + trusted=true
#2018 numbers

table4_2018 = total_2018[['country', 'due', 'due_reported']].groupby('country').agg({'due':['count', 'sum'], 'due_reported':['sum']})
table4_2018['reported_prct'] = round((table4_2018['due_reported']['sum'] / table4_2018['due']['sum']) * 100,2)

# + trusted=true
table4_2018

# + trusted=true
#2021 numbers
table4_2021 = total_2021[['country', 'due', 'due_reported']].groupby('country').agg({'due':['count', 'sum'], 'due_reported':['sum']})
table4_2021['reported_prct'] = round((table4_2021['due_reported']['sum'] / table4_2021['due']['sum']) * 100,2)

# + trusted=true
table4_2021
# -

# # Table 5 - High performers

# + trusted=true
#Highest Overall Reporting %
total_2021.sort_values(by='reported_prct', ascending=False).head(6)

# + trusted=true
#Highest absolute number of trials reported
total_2021.sort_values(by='due_reported', ascending=False).head(6)

# + trusted=true
#Biggest increase in reporting %
increase_df = table_3[['sponsor_name', 'due_reported_prct', 'reported_prct']].reset_index(drop=True)
increase_df['delta'] = (increase_df['due_reported_prct'] - increase_df['reported_prct']) * -1

# + trusted=true
increase_df.sort_values(by='delta', ascending=False).head(6)

# +
#Biggest increase in abolsute trials reported

# + trusted=true
increase_df_count = table_3[['sponsor_name', 'due_reported_2021', 'due_reported_2018']].reset_index(drop=True)
increase_df_count['delta'] = (increase_df_count['due_reported_2021'] - increase_df_count['due_reported_2018'])

# + trusted=true
increase_df_count.sort_values(by='delta', ascending=False).head(6)
# -








# +


