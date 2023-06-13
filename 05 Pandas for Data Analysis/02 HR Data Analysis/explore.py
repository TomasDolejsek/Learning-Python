import pandas as pd

class DataAnalysator:
    def __init__(self):
        self.start()

    def start(self):
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
        print(a_data.index.tolist())
        print(b_data.index.tolist())
        print(hr_data.index.tolist())


if __name__ == '__main__':
    DataAnalysator()
