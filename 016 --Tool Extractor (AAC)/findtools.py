import openpyxl
import os

class ToolDatabase:
    def __init__(self):
        self.data = dict()


class Tool:
    def __init__(self, id):
        self.id = id
        self.cavities_made = 0
        self.fgmachine = ''
        self.project = ''
        self.form = ''
        self.prod_type = ''


class Extractor:
    def __init__(self):
        self.TOOLCOLUMN = 6
        self.INFOCOLUMN = 1
        self.PATHBASE = "Z:\CZ_Production\Prod_RW\Tooling\T02 FG Machines\T02.00.202 "
        self.FGMACHINES = [*range(105, 116)]

    def get_runlog_names(self, dict):
        filelist = list()
        while True:
            scan = os.listdir(dict)
            dir = ''
            for filename in scan:
                filepath = dict + filename
                if os.path.isdir(filepath):
                    dir = filename
                if os.path.isfile(filepath) and not filename.startswith('~$'):
                    filelist.append(filepath)
            if not dir:
                break
            else:
                dict = dict + dir + '\\'
                continue
        return filelist

    def search_all_machines(self, tool_id):
        print("Not implemented yet.")
        pass

    def search_machine(self, machine_id, tool_id):
        runlog_dict = self.PATHBASE + machine_id.upper() + '\\Runlog\\'
        filelist = self.get_runlog_names(runlog_dict)
        print(f"\nSearching {machine_id.upper()}...")
        for tablename in filelist:
            print("Searching runlog:", tablename)
            if tool_id != 'all':
                self.search_tool(tablename, machine_id, tool_id)
            else:
                self.search_all_tools(tablename, machine_id)
        output_name = tool_id.upper() + '_on_' + machine_id.upper()
        self.save_result(output_name)
        print(f"Results have been saved to {output_name}\n")

    def search_all_tools(self, tablename, fgname):
        cavities_made = 0
        project = ''
        prod_type = ''
        form = ''
        wb_obj = openpyxl.load_workbook(tablename)
        sheet_obj = wb_obj.active
        max_row = sheet_obj.max_row
        toolcell_obj = sheet_obj.cell(row=6, column=self.TOOLCOLUMN)
        current_tool = str(toolcell_obj.value)
        for i in range(7, max_row + 1):
            toolcell_obj = sheet_obj.cell(row=i, column=self.TOOLCOLUMN)
            infocell_obj = sheet_obj.cell(row=i, column=self.INFOCOLUMN)
            c_value = str(toolcell_obj.value)
            info = infocell_obj.value
            if c_value == 'None' or info == 'None':
                continue
            if 'Cav' not in c_value:
                if c_value != current_tool:
                    tool = Tool(current_tool)
                    tool.cavities_made = int(cavities_made)
                    tool.fgmachine = fgname.upper()
                    tool.project = project
                    tool.form = form
                    tool.prod_type = prod_type
                    tools.data[current_tool] = tool
                    current_tool = c_value
                else:
                    if info:
                        if 'Align' in info or 'Rough-in' in info:
                            infolist = info.split()
                            project = ' '.join(infolist[0:4])
                            form = infolist[4]
                            prod_type = infolist[6]
            elif 'Cav.' in c_value:
                cavities_made = c_value[:-14]
        for id, t in tools.data.items():
            print(f"Tool '{t.id}' made {t.cavities_made} {t.prod_type}"
                  f" cavit{'y' if t.cavities_made == 1 else 'ies'}.")
            print(f"Project: {t.project} {t.form}\n")
        output_name = 'ALL' + '_on_' + fgname.upper()
        self.save_result(output_name)
        wb_obj.close()

    def search_tool(self, tablename, fgname, id):
        found = False
        project = ''
        form = ''
        prod_type = ''
        wb_obj = openpyxl.load_workbook(tablename)
        sheet_obj = wb_obj.active
        max_row = sheet_obj.max_row
        found = False
        for i in range(6, max_row + 1):
            toolcell_obj = sheet_obj.cell(row=i, column=self.TOOLCOLUMN)
            c_value = str(toolcell_obj.value)
            if c_value.lower() == id.lower():
                infocell_obj = sheet_obj.cell(row=i, column=self.INFOCOLUMN)
                info = infocell_obj.value
                if 'Align' in info or 'Rough-in' in info:
                    infolist = info.split()
                    project = ' '.join(infolist[0:4])
                    form = infolist[4]
                    prod_type = infolist[6]
                if not found:
                    found = True
                continue
            if found:
                if 'Cav.' in c_value:
                    cav = c_value[:-14]
                    continue
                if c_value.lower() != id.lower():
                    tool = Tool(id.upper())
                    tool.cavities_made = cav
                    tool.fgmachine = fgname.upper()
                    tool.project = project
                    tool.form = form
                    tool.prod_type = prod_type
                    tools.data[id.upper()] = tool
                    break
        if not found:
            return
        for id, t in tools.data.items():
            print(f"Tool '{t.id}' made {t.cavities_made} {t.prod_type}"
                  f" cavit{'y' if t.cavities_made == 1 else 'ies'}.")
            print(f"Project: {t.project} {t.form} on {t.fgmachine}\n")
        wb_obj.close()

    def save_result(self, output_name):
        r_filename = output_name + '.xlsx'
        header = ['Tool ID', 'Cavities Made', 'FG Machine', 'Align/Rough-in', 'Project', 'Form']
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(header)
        for id in tools.data.keys():
            tool_data = (tools.data[id].id, tools.data[id].cavities_made, tools.data[id].fgmachine,
                         tools.data[id].prod_type, tools.data[id].project, tools.data[id].form)
            sheet.append(tool_data)
        # formatting output table
        for i in range(1, sheet.max_row + 1):
            for j in range(1, sheet.max_column + 1):
                cell = sheet.cell(row=i, column=j)
                cell.alignment = openpyxl.styles.Alignment(horizontal='center')
                if i == 1:
                    cell.font = openpyxl.styles.Font(bold=True, size=13)
                else:
                    cell.font = openpyxl.styles.Font(size=13)
                sheet.column_dimensions[openpyxl.utils.get_column_letter(j)].width = 22
        wb.save(r_filename)
        wb.close()


class UserInterface:
    def __init__(self):
        self.valid_commands = ('exit')
        print('*** Tool Data Extractor *** (c) TDO 2023 ***')
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
                        extractor.search_all_machines(tool_id)
                        break
                    if not machine.startswith('fg'):
                        machine = 'fg' + machine
                    try:
                        if not (105 <= int(machine[2:]) <= 115):
                            raise ValueError
                    except ValueError:
                        print("Unknown FG Machine!\n")
                        continue
                    extractor.search_machine(machine, tool_id)
                    break


if __name__ == '__main__':
    tools = ToolDatabase()
    extractor = Extractor()
    UserInterface()
