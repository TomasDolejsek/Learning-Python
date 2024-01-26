import pandas as pd
import matplotlib.pyplot as plt


class DataProcessor:
    def __init__(self):
        self.file_names = ('Data/general.csv',
                           'Data/prenatal.csv',
                           'Data/sports.csv')
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
        general = hospital_df.loc[hospital_df.hospital == 'general']
        prenatal = hospital_df.loc[hospital_df.hospital == 'prenatal']
        sports = hospital_df.loc[hospital_df.hospital == 'sports']

        grouped = hospital_df.groupby('hospital')['hospital'].count()
        grouped = sorted(grouped.to_dict().items(), key=lambda x: -x[1])
        answers['1st'] = grouped[0][0]

        stomach = general.loc[hospital_df.diagnosis == 'stomach']
        answers['2nd'] = round(stomach.shape[0] / general.shape[0], 3)

        dislocation = sports.loc[hospital_df.diagnosis == 'dislocation']
        answers['3rd'] = round(dislocation.shape[0] / sports.shape[0], 3)

        answers['4th'] = general.age.median() - sports.age.median()

        blood = hospital_df.loc[hospital_df.blood_test == 't']
        grouped = blood.groupby('hospital')['blood_test'].count()
        grouped = sorted(grouped.to_dict().items(), key=lambda x: -x[1])
        answers['5th'] = f"{grouped[0][0]}, {grouped[0][1]} blood tests"
        # self.print_answers(answers)

        # stage 5
        answers.clear()

        data = hospital_df['age']
        bins = [0, 15, 35, 55, 70, 80]
        self.display_histogram(data, bins)
        answers['1st'] = '15-35'

        data = hospital_df.groupby('diagnosis')['diagnosis'].count()
        labels = data.index.to_list()
        self.display_piechart(data, labels)
        answers['2nd'] = 'pregnancy'

        general_data = general['height']
        prenatal_data = prenatal['height']
        sports_data = sports['height']
        data = [general_data, prenatal_data, sports_data]
        self.display_violin(data)
        answers['3rd'] = "It's because general and prenatal use meters as height measurement units, " \
                        "whereas sports uses feet. Also prenatal hospital has only female patients, " \
                        "therefore its average patient's height is lower than general's and sports'."

        self.print_answers(answers)

    @staticmethod
    def display_histogram(data, bins):
        counts, edges, bars = plt.hist(data, bins=bins, color='lightblue', edgecolor='white')
        plt.title("Patients by age")
        plt.xlabel("Patient's age")
        plt.ylabel("Number of patients")
        plt.bar_label(bars)
        plt.show()

    @staticmethod
    def display_piechart(data, labels):
        plt.pie(data, labels=labels, autopct='%.1f%%')
        plt.title("Most common diagnosis")
        plt.show()

    @staticmethod
    def display_violin(data):
        fig, axes = plt.subplots()
        plt.violinplot(data)
        axes.set_xticks((1, 2, 3))
        axes.set_xticklabels(('general', 'prenatal', 'sports'))
        axes.set_ylabel("Patient's height")
        axes.set_title("Patient's height by hospital")
        plt.show()

    @staticmethod
    def print_answers(answers):
        for key, value in answers.items():
            print(f"The answer to the {key} question: {value}")

    def load_data(self):
        pd_files = []
        for file in self.file_names:
            pd_files.append(pd.read_csv(file))
        return pd_files


if __name__ == '__main__':
    pd.set_option('display.max_columns', 8)
    DataProcessor()
