import pandas as pd

def sanity_check(df, field, check):
    if len(df[df[field] == check]) > 0:
        print("There is an issue with this data")
    else:
        print("This data passes the check")

def rounder(num, denom):
    return(round((num/denom)*100,2))

def get_stats(df, spon_names):
    all_spons = []
    for s in spon_names:
        spon_df = df[df.normalized_name == s]
        stats = {}
        stats['sponsor_name'] = s
        stats['total_registered'] = len(spon_df)
        stats['due'] = spon_df.results_expected.sum()
        stats['due_reported'] = len(spon_df[(spon_df.results_expected == 1) & (spon_df.has_results == 1)])

        if stats['due'] == 0:
            stats['due_reported_prct'] = 0
        else:
            stats['due_reported_prct'] = rounder(stats['due_reported'],stats['due'])

        filt1 = spon_df.comp_date_while_ongoing == 1
        filt2 = spon_df.all_completed_no_comp_date == 1
        filt3 = spon_df.contains_non_eu == 1
        filt4 = spon_df.trial_status == 4
        filt5 = spon_df.exempt == 1
        stats['inconsistent_data'] = len(spon_df[((filt1 | filt2 | filt3 | filt4) & ~filt5)])

        if stats['inconsistent_data'] == 0:
            stats['inconsistent_data_prct'] = 0
            stats['comp_ongoing'] = stats['comp_ongoing_prct'] = 0
            stats['missing_comp'] = stats['missing_comp_prct'] = 0
            stats['contains_non_eu'] = stats['contains_non_eu_prct'] = 0
            stats['missing_status'] = stats['missing_status_prct'] = 0
            stats['inconsistent_w_results'] = stats['inconsistent_w_results_prct'] = 0
        else:
            stats['inconsistent_data_prct'] = rounder(stats['inconsistent_data'], stats['total_registered'])
            stats['comp_ongoing'] = len(spon_df[filt1 & ~filt5])
            stats['comp_ongoing_prct'] = rounder(stats['comp_ongoing'], stats['inconsistent_data'])
            stats['missing_comp'] = len(spon_df[filt2 & ~filt5])
            stats['missing_comp_prct'] = rounder(stats['missing_comp'], stats['inconsistent_data'])
            stats['contains_non_eu'] = len(spon_df[filt3 & ~filt5])
            stats['contains_non_eu_prct'] = rounder(stats['contains_non_eu'], stats['inconsistent_data'])
            stats['missing_status'] = len(spon_df[filt4 & ~filt3 & ~filt5])
            stats['missing_status_prct'] = rounder(stats['missing_status'], stats['inconsistent_data'])
            stats['inconsistent_w_results'] = len(spon_df[(filt1 | filt2 | filt3 | filt4) & ~filt5 & spon_df.has_results==1])
            stats['inconsistent_w_results_prct'] = rounder(stats['inconsistent_w_results'], stats['inconsistent_data'])
    
        all_spons.append(stats)
    
    return all_spons