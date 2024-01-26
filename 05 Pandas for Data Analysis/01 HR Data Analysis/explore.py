import pandas as pd


class DataAnalysator:
    def __init__(self):
        self.start()

    @staticmethod
    def count_bigger_5(series):
        return series.where(series > 5).count()

    def start(self):
        # stage 1
        a_data = pd.read_xml('../Data/A_office_data.xml')
        b_data = pd.read_xml('../Data/B_office_data.xml')
        hr_data = pd.read_xml('../Data/hr_data.xml')
        a_data.set_index('employee_office_id', inplace=True, drop=True)
        new_indexes = ['A' + str(x) for x in a_data.index.tolist()]
        a_data.index = new_indexes
        b_data.set_index('employee_office_id', inplace=True, drop=True)
        new_indexes = ['B' + str(x) for x in b_data.index.tolist()]
        b_data.index = new_indexes
        hr_data.set_index('employee_id', inplace=True, drop=True)

        # stage 2
        ab_data = pd.concat([a_data, b_data])
        ab_hr_data = ab_data.merge(hr_data, left_index=True, right_index=True, how='left', indicator=True)
        ab_hr_data = ab_hr_data[ab_hr_data._merge == 'both']
        ab_hr_data.drop(['_merge'], axis=1, inplace=True)
        ab_hr_data.sort_index(inplace=True)

        # stage 3
        hard_working = ab_hr_data.sort_values('average_monthly_hours', ascending=False)['Department']
        # print(hard_working.head(10).tolist())
        projects = sum(ab_hr_data['number_project'].where((ab_hr_data.Department == 'IT')
                                                    & (ab_hr_data.salary == 'low'), 0))
        # print(projects)
        employees = ['A4', 'B7064', 'A3033']
        employees_data = []
        for employee in employees:
            data = ab_hr_data.loc[(ab_hr_data.index == employee), ['last_evaluation', 'satisfaction_level']]
            employees_data.append(data.values.tolist()[0])
        # print(employees_data)

        # stage 4
        boss_table = ab_hr_data.groupby(['left']).agg({'number_project': ['median', self.count_bigger_5],
                                                       'time_spend_company': ['mean', 'median'],
                                                       'Work_accident': 'mean',
                                                       'last_evaluation': ['mean', 'std']})
        # print(boss_table.round(2).to_dict())

        # stage 5
        piv_tab1 = ab_hr_data.pivot_table(index='Department', columns=['left', 'salary'], values='average_monthly_hours',
                                          aggfunc='median')
        disp_tab1 = piv_tab1.loc[(piv_tab1[(0, 'high')].values < piv_tab1[(0, 'medium')].values) |
                                 (piv_tab1[(1, 'low')].values < piv_tab1[(1, 'high')].values)]
        print(disp_tab1.to_dict())
        piv_tab2 = ab_hr_data.pivot_table(index='time_spend_company', columns='promotion_last_5years',
                                          values=['satisfaction_level', 'last_evaluation'], aggfunc=['min', 'max', 'mean'])
        disp_tab2 = piv_tab2.loc[piv_tab2[('mean', 'last_evaluation', 0)] > piv_tab2[('mean', 'last_evaluation', 1)]]
        print(disp_tab2.to_dict())


if __name__ == '__main__':
    DataAnalysator()
