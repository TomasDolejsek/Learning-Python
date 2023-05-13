import openpyxl
import os


class ToolDatabase:
    def __init__(self):
        self.data = dict()

    def save_tools_data(self, output_name):
        if not self.data:
            print('No tools found...')
            return
        if not os.path.exists('Results'):
            os.mkdir('Results')
        output_name = 'Results\\' + output_name + '.xlsx'
        header = ['Tool ID', 'FG Machine', 'Project', 'Form', 'Align/Rough-in',
                  'Cavities Made', 'Cavities Range', 'Time Range']
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(header)
        for tool in self.data.values():
            tool_data = (tool['id'], tool['fgmachine'], tool['project'], tool['form'], tool['prod_type'],
                         tool['cavities_made'], tool['cavities_range'], tool['time_range'])
            sheet.append(tool_data)
        # formatting output table
        cdim = [0 for x in range(8)]
        for i in range(1, sheet.max_row + 1):
            for j in range(1, sheet.max_column + 1):
                cell = sheet.cell(row=i, column=j)
                cell.alignment = openpyxl.styles.Alignment(horizontal='center')
                if i == 1:
                    cell.font = openpyxl.styles.Font(bold=True, size=12)
                else:
                    cell.font = openpyxl.styles.Font(size=12)
                if cdim[j-1] < len(str(cell.value)) + 4:
                    cdim[j-1] = len(str(cell.value)) + 4
                sheet.column_dimensions[openpyxl.utils.get_column_letter(j)].width = cdim[j-1]
        wb.save(output_name)
        print(f"\n{len(self.data)} tool{'s have' if len(self.data) > 1 else ' has'} been found.")
        print(f"Searching results have been saved to {output_name}\n")
        wb.close()

class Extractor:

    def __init__(self):
        self.INFO_COLUMN = 1
        self.DATE_COLUMN = 3
        self.TOOL_COLUMN = 6
        #self.PATH_BASE = "Z:\CZ_Production\Prod_RW\Tooling\T02 FG Machines\T02.00.202 "
        self.PATH_BASE = "C:\\Tom\\Texts\\Python\\016 --Tool Extractor (AAC)\\"
        self.FG_MACHINES = [*range(105, 116)]
        self.counter = 0

    def get_runlog_names(self, folder):
        filelist = list()
        while True:
            scan = os.listdir(folder)
            dir = ''
            for filename in scan:
                filepath = folder + filename
                if os.path.isdir(filepath):
                    dir = filename
                if os.path.isfile(filepath) and not filename.startswith('~$'):
                    filelist.append(filepath)
            if not dir:
                break
            else:
                folder = folder + dir + '\\'
                continue
        return filelist

    def search_all_machines(self, tool_id):
        print("Not implemented yet.")
        pass

    def search_machine(self, machine_id, tool_id):
        runlog_folder = self.PATH_BASE + machine_id + '\\Runlog\\'
        runlog_list = self.get_runlog_names(runlog_folder)
        print(f"\nSearching {machine_id}...")
        for runlog_name in runlog_list:
            print("Searching runlog:", runlog_name)
            if tool_id != 'ALL':
                self.search_tool(runlog_name, machine_id, tool_id)
            else:
                self.search_all_tools(runlog_name, machine_id)
        output_name = tool_id + '_on_' + machine_id
        tools.save_tools_data(output_name)

    def search_all_tools(self, runlog_name, fgname):
        tool_dict = dict()
        wb_obj = openpyxl.load_workbook(runlog_name)
        sheet_obj = wb_obj.active
        rown = 5
        max_row = sheet_obj.max_row
        last_tool = ''
        while rown <= max_row:
            rown += 1
            c_value = str(sheet_obj.cell(row=rown, column=self.TOOL_COLUMN).value)
            if self.is_tool(c_value) and c_value != last_tool:
                self.counter += 1
                rown, tool_dict = self.get_tool_data(c_value, rown, sheet_obj)
                if tool_dict:
                    if tool_dict['id'] == 'reference':
                        self.counter -= 1
                        continue
                    tool_dict['fgmachine'] = fgname
                    tools.data[self.counter] = tool_dict
                last_tool = c_value
        wb_obj.close()

    def search_tool(self, runlog_name, fgname, id):
        tool_dict = dict()
        wb_obj = openpyxl.load_workbook(runlog_name)
        sheet_obj = wb_obj.active
        rown = 5
        max_row = sheet_obj.max_row
        while rown < max_row + 1:
            rown += 1
            c_value = str(sheet_obj.cell(row=rown, column=self.TOOL_COLUMN).value)
            if c_value == id:
                self.counter += 1
                rown, tool_dict = self.get_tool_data(c_value, rown, sheet_obj)
                if tool_dict:
                    if tool_dict['id'] == 'reference':
                        self.counter -= 1
                        continue
                    tool_dict['fgmachine'] = fgname
                    tools.data[self.counter] = tool_dict
        wb_obj.close()

    def get_tool_data(self, tool_id, start_row, sheet_obj):
        """
        1) Continue searching the runlog until next tool is found (or EOF).
        2) Gather all data about current tool
        3) Save gathered data to a tool dictionary
        :param tool_id: id of searched tool
        :param start_row: the number of a row where the data about current tool starts
        :param sheet_obj: sheet_object
        :return: end_row: the number of a row where the data about current tool ends
        """
        tooldata = dict()
        project = ''
        form = ''
        prod_type = ''
        cav = 0
        first_cavity = ''
        last_cavity = ''
        made = 0
        ministud = False
        reftool = False
        started = ''
        ended = ''
        rown = start_row - 1
        max_row = sheet_obj.max_row
        while rown <= max_row:
            rown += 1
            c_info = sheet_obj.cell(row=rown, column=self.INFO_COLUMN).value
            c_date = sheet_obj.cell(row=rown, column=self.DATE_COLUMN).value
            c_tool = str(sheet_obj.cell(row=rown, column=self.TOOL_COLUMN).value)
            if c_info and ('Ministud' in c_info or 'Idle' in c_info):
                ministud = True
            if c_info and ('reference' in c_info):
                reftool = True
            if c_info and ('Align' in c_info or 'Rough-in' in c_info):
                if 'Run-in' not in c_info:
                    infolist = c_info.split()
                    project = ' '.join(infolist[0:4])
                    form = infolist[4]
                    if not first_cavity:
                        first_cavity = infolist[5]
                    last_cavity = infolist[5]
                    prod_type = infolist[6]
                    if not started:
                        started = str(c_date)[:10]
                    ended = str(c_date)[:10]
            if c_tool and 'Cav.' in c_tool:
                cav = c_tool[:-14]
                if not ministud:
                    made += 1
                ministud = False
            if (self.is_tool(c_tool) and c_tool != tool_id) or rown == max_row:
                tooldata['id'] = tool_id
                tooldata['project'] = project
                tooldata['form'] = form
                tooldata['prod_type'] = prod_type
                tooldata['cavities_made'] = cav if int(cav) > 0 else str(made)
                tooldata['cavities_range'] = ' - '.join((first_cavity, last_cavity))
                tooldata['time_range'] = ' -> '.join((started, ended))
                if reftool:
                    tooldata['id'] = 'reference'
                break
        return rown - 1, tooldata

    def is_tool(self, tool_id):
        tool_id = str(tool_id)
        if tool_id.isnumeric() or tool_id.startswith('ML'):
            return True
        else:
            return False

class UserInterface:
    def __init__(self):
        self.valid_commands = ('exit')
        print('*** Runglog Tool Data Extractor *** (c) TDO 2023, for AAC Optics CZ ***')
        self.start()

    def start(self):
        while True:
            print(f"Type 'exit' to quit the program.")
            tool_id = input("Enter tool id (type 'all' to get list of all tools): ").lower().strip()
            if tool_id == 'exit':
                print("Bye!")
                exit()
            else:
                while True:
                    machine = input("FG Machine [FG105 - FG115] (type 'all' to search all machines): ").lower().strip()
                    if machine == 'exit':
                        print("Bye!")
                        exit()
                    if machine == 'all':
                        Extractor().search_all_machines(tool_id.upper())
                        break
                    if not machine.startswith('fg'):
                        machine = 'fg' + machine
                    try:
                        if not (105 <= int(machine[2:]) <= 115):
                            raise ValueError
                    except ValueError:
                        print("Unknown FG Machine!\n")
                        continue
                    Extractor().search_machine(machine.upper(), tool_id.upper())
                    break


if __name__ == '__main__':
    extractor = Extractor()
    tools = ToolDatabase()
    UserInterface()
