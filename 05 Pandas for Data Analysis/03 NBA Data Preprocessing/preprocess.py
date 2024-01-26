import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder


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


def multicol_data(df, target='salary'):
    # 1. create a correlation matrix of all numeric features except target ('salary' by default)
    pearson = df.select_dtypes('number').drop(target, axis=1).corr()

    # 2. find all features where correlation coefficient is higher than 0.5 (or lower than -0.5)
    high_corrs = []
    for column in pearson.columns:
        for i in range(pearson.shape[0]):
            if 0.5 < abs(pearson[column][i]) < 1.0:
                high_corrs.append(column)

    # 3. find correlation coefficients of found high_corrs with the target variable
    columns = [*high_corrs, target]
    target_corrs = df[columns].corr()[target].drop(target)

    # 4. drop the feature with the lowest correlation coefficient
    drop_feature = target_corrs.idxmin()
    df.drop(drop_feature, axis=1, inplace=True)
    return df

def transform_data(df, target='salary'):
    # 1. find numeric features and drop target variable ('salary' by default)
    numerical_df = df.select_dtypes('number').drop(target, axis=1)

    # 2. scale numerical features
    scaler = StandardScaler()
    scaler.fit(numerical_df)
    numerical = pd.DataFrame(scaler.transform(numerical_df), columns=numerical_df.columns.to_list())

    # 3. find categorical features
    categorical_df = df.select_dtypes('object')

    # 4. encode categorical features using OneHotEncoder
    encoder = OneHotEncoder()
    encoder.fit(categorical_df)
    columns = [y for x in encoder.categories_ for y in x]
    categorical = pd.DataFrame(data=encoder.transform(categorical_df).toarray(), columns=columns)

    # 5. concatenate them together
    result_df = pd.concat([numerical, categorical], axis=1)

    # 6. return result_df and the target series
    return result_df, df[target]


if __name__ == '__main__':
    DATA_PATH = 'Data/nba2k-full.csv'

    # stage 1
    df_cleaned = clean_data(DATA_PATH)
    # print(df_cleaned[['b_day', 'team', 'height', 'weight', 'country', 'draft_round', 'draft_year', 'salary']].head())

    # stage 2
    df_featured = feature_data(df_cleaned)
    # print(df_featured[['age', 'experience', 'bmi']].head())

    # stage 3
    df_multicolled = multicol_data(df_featured)
    #print(list(df_multicol.select_dtypes('number').drop(columns='salary')))

    # stage 4
    X, y = transform_data(df_multicolled)
    answer = {'shape': [X.shape, y.shape],
              'features': list(X.columns)}
    print(answer)
