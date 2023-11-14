import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm


def correct_time(df):
    '''
        Change the date column to appropriate format and add as a column the year for the time analysis
    '''
    df['date'] = pd.to_datetime(df.date, unit='s')
    df['year'] = df['date'].dt.year
    return(df)
    
def zscore_merge(df1, df2):
    '''
        Calculation of the z-score for each beer (not for the mean score of the beer that is what we have in BA_beers or RB_beers) and
        addition of this column to the identified merged ratings
    '''    
    df1['z_score'] = df1.groupby('year')['rating'].transform(lambda x: (x-x.mean())/x.std())
    df2 = df2.merge(df1, how='inner').copy(deep=True)
    return(df2)
 
def linear_trend(group):
    y = group['diff_exp_mean'].to_numpy()
    X = group['ith_rating'].to_numpy()
    X = sm.add_constant(X)
    res_ols = sm.OLS(y, X).fit()
    return pd.Series({
        'Slope': res_ols.params[1],
        'Intercept': res_ols.params[0]
    })

def detrend(group, trend_data):
    slope = trend_data.loc[group['beer_id'].iloc[1]]['Slope']
    intercept = trend_data.loc[group['beer_id'].iloc[0]]['Intercept']
    return pd.Series(group['z_score'] + (slope * group['ith_rating'] + intercept))

def he_correction(df, min_number, plotting=False):
    '''
        Detrend of the herding effect in the z-score column of the df
    ''' 
    # Expanding mean as a function of ith rating z-score
    df = df.sort_values(by=['beer_id', 'date']) #Sort according to the beer_id and, after that, according to date
    df['exp_mean'] = df.groupby('beer_id')['z_score'].transform(lambda x: x.expanding().mean())
    
    # Create new column with difference between the z_score of the rating and the expanded mean up to that value 
    df['diff_exp_mean'] = df['z_score'] - df['exp_mean']
    #)[['exp_mean', 'z_score']].transform(lambda x: x['z_score'] - x['exp_mean'])
       
    # Create column with indexing of number of rating for that beer for regression
    df['ith_rating'] = df.groupby('beer_id').cumcount() + 1
    
    if plotting:
        # Plot with just the first beer for a better comprehension
        grouped_df = df.groupby('beer_id')[['diff_exp_mean', 'ith_rating']]
        first_group_ID = list(grouped_df.groups.keys())[0]
        first_group = grouped_df.get_group(first_group_ID)

        plt.plot(first_group['ith_rating'], first_group['diff_exp_mean'])
        plt.xlabel('ith rating')
        plt.ylabel('Diff betwen rating and ith rating expanding average')
    
    grouped_df = df.groupby('beer_id')
    trend_data = grouped_df.apply(linear_trend)
    new_col = grouped_df.apply(lambda group: detrend(group, trend_data))
    A = pd.DataFrame(new_col)
    values = A[0].to_numpy()
    df['detrend'] = values
    return(df)
 
