import pandas as pd


def clean_data(path):
    df = pd.read_csv(path)
    df['b_day'] = pd.to_datetime(df['b_day'], format='%m/%d/%y')
    df['draft_year'] = pd.to_datetime(df['draft_year'], format='%Y')
    df['team'].fillna('No Team', inplace=True)
    df['height'] = pd.Series([x.split('/')[1] for x in df['height'].astype('string')]).astype('float')
    df['weight'] = pd.Series([x.split('/')[1][:-4] for x in df['weight'].astype('string')]).astype('float')
    df['salary'] = pd.Series([x.replace('$', '') for x in df['salary'].astype('string')]).astype('float')
    df.loc[df.country != 'USA', 'country'] = 'Not-USA'
    df.loc[df.draft_round == 'Undrafted', 'draft_round'] = '0'
    return df


def feature_data(df):
    df['version'] = pd.Series([x.replace('NBA2k', '') for x in df['version'].astype('string')])
    df['version'] = pd.to_datetime((df['version']), format='%y')
    divisor = 60 * 60 * 24 * 365  # seconds in a year
    df['age'] = ((df['version'] - df['b_day']).dt.total_seconds() / divisor + 1).astype('int')
    df['experience'] = ((df['version'] - df['draft_year']).dt.total_seconds() / divisor).astype('int')
    df['bmi'] = (df['weight'] / (df['height'] ** 2)).astype('float')
    df.drop(['version', 'b_day', 'draft_year', 'weight', 'height'], axis=1, inplace=True)
    for column in df.columns:
        if df[column].dtype == object and df[column].nunique() > 50:
            df.drop(column, axis=1, inplace=True)
    return df


if __name__ == '__main__':
    DATA_PATH = '../Data/nba2k-full.csv'

    # stage 1
    df_cleaned = clean_data(DATA_PATH)
    # print(df_cleaned[['b_day', 'team', 'height', 'weight', 'country', 'draft_round', 'draft_year', 'salary']].head())

    # stage 2
    df_featured = feature_data(df_cleaned)
    print(df_featured[['age', 'experience', 'bmi']].head())
