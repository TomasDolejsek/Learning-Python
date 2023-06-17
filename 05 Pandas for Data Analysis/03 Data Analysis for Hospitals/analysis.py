import pandas as pd


class DataProcessor:
    def __init__(self):
        self.file_names = ('test/general.csv',
                           'test/prenatal.csv',
                           'test/sports.csv')
        self.start()

    def start(self):
        # stage 1
        general, prenatal, sports = self.load_data()

        # stage 2
        prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
        sports.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'}, inplace=True)
        hospital_df = pd.concat([general, prenatal, sports], ignore_index=True)
        hospital_df.drop('Unnamed: 0', inplace=True, axis=1)

        # stage 3
        hospital_df.dropna(thresh=1, inplace=True)
        hospital_df['gender'] = hospital_df['gender'].replace(['female', 'woman'], 'f')
        hospital_df['gender'] = hospital_df['gender'].replace(['male', 'man'], 'm')
        hospital_df['gender'].fillna('f', inplace=True)
        columns_to_replace = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound',
                              'mri', 'xray', 'children', 'months']
        hospital_df[columns_to_replace] = hospital_df[columns_to_replace].fillna(0)
        # print(hospital_df.shape)
        # print(pd.DataFrame.sample(hospital_df, n=20, random_state=30))

        # stage 4
        answers = dict()
        grouped = hospital_df.groupby('hospital')['hospital'].count()
        grouped = sorted(grouped.to_dict().items(), key=lambda x: -x[1])
        answers['1st'] = grouped[0][0]

        general = hospital_df.loc[hospital_df.hospital == 'general']
        stomach = general.loc[hospital_df.diagnosis == 'stomach']
        answers['2nd'] = round(stomach.shape[0] / general.shape[0], 3)

        sports = hospital_df.loc[hospital_df.hospital == 'sports']
        dislocation = sports.loc[hospital_df.diagnosis == 'dislocation']
        answers['3rd'] = round(dislocation.shape[0] / sports.shape[0], 3)

        answers['4th'] = general.age.median() - sports.age.median()

        blood = hospital_df.loc[hospital_df.blood_test == 't']
        grouped = blood.groupby('hospital')['blood_test'].count()
        grouped = sorted(grouped.to_dict().items(), key=lambda x: -x[1])
        answers['5th'] = f"{grouped[0][0]}, {grouped[0][1]} blood tests"

        self.print_answers(answers)

    @staticmethod
    def print_answers(answers):
        for key, value in answers.items():
            print(f"The answer to the {key} question is {value}")

    def load_data(self):
        pd_files = []
        for file in self.file_names:
            pd_files.append(pd.read_csv(file))
        return pd_files


if __name__ == '__main__':
    pd.set_option('display.max_columns', 8)
    DataProcessor()
