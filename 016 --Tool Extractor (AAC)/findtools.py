import openpyxl


class ToolDatabase:
    def __init__(self):
        self.data = dict()


class Tool:
    def __init__(self):
        self.id = ''
        self.cavities_made = 0
        self.prod_type = ''


class Extractor:
    def __init__(self):
        self.TOOLCOLUMN = 6
        self.INFOCOLUMN = 1
        self.tablename = 'FG115.xlsm'

    def search_all(self):
        cavities_made = 0
        prod_type = ''
        wb_obj = openpyxl.load_workbook(self.tablename)
        sheet_obj = wb_obj.active
        max_row = sheet_obj.max_row
        toolcell_obj = sheet_obj.cell(row=6, column=self.TOOLCOLUMN)
        current_tool = str(toolcell_obj.value)
        for i in range(7, max_row + 1):
            toolcell_obj = sheet_obj.cell(row=i, column=self.TOOLCOLUMN)
            infocell_obj = sheet_obj.cell(row=i, column=self.INFOCOLUMN)
            c_value = str(toolcell_obj.value)
            info = infocell_obj.value
            if c_value == 'None':
                continue
            if 'Cav' not in c_value:
                if c_value != current_tool:
                    tool = Tool()
                    tool.cavities_made = int(cavities_made)
                    tool.prod_type = prod_type
                    tools.data[current_tool] = tool
                    current_tool = c_value
                else:
                    if 'Align' in info:
                        prod_type = 'Align'
                    elif 'Rough-in' in info:
                        prod_type = 'Rough-in'
            elif 'Cav.' in c_value:
                cavities_made = c_value[:-14]
        for id, t in tools.data.items():
            print(f"Tool '{id}' made {t.cavities_made} {t.prod_type}"
                  f" cavit{'y' if t.cavities_made == 1 else 'ies'}.")

    def search_tool(self, id):
        found = False
        prod_type = ''
        wb_obj = openpyxl.load_workbook(self.tablename)
        sheet_obj = wb_obj.active
        max_row = sheet_obj.max_row
        found = False
        for i in range(6, max_row + 1):
            toolcell_obj = sheet_obj.cell(row=i, column=self.TOOLCOLUMN)
            c_value = str(toolcell_obj.value)
            if c_value.lower() == id.lower():
                infocell_obj = sheet_obj.cell(row=i, column=self.INFOCOLUMN)
                info = infocell_obj.value
                if 'Align' in info:
                    prod_type = 'Align'
                elif 'Rough-in' in info:
                    prod_type = 'Rough-in'
                if not found:
                    found = True
                continue
            if found:
                if 'Cav.' in c_value:
                    cav = c_value[:-14]
                    continue
                if c_value.lower() != id.lower():
                    tool = Tool()
                    tool.cavities_made = cav
                    tool.prod_type = prod_type
                    break
        if not found:
            print(f"\nNo entry for tool '{id}'.\n")
            return
        print(f"\nTool '{id.upper()}' made {tool.cavities_made} {tool.prod_type}"
              f" cavit{'y' if tool.cavities_made == 1 else 'ies'}.\n")


class UserInterface:
    def __init__(self):
        self.valid_commands = ('all', 'tool', 'exit')
        print('*** Tool Data Extractor *** (c) TDO 2023 ***')
        print(f"Valid commands = {self.valid_commands}.\n")
        self.start()

    def start(self):
        while True:
            user = input("Your command? ").lower().strip()
            if user in self.valid_commands:
                if user == self.valid_commands[0]:
                    extractor.search_all()
                    continue
                if user == self.valid_commands[1]:
                    self.search_tool_menu()
                    continue
                if user == self.valid_commands[-1]:
                    print("Bye!")
                    exit()
            else:
                print('Unknown Command.')
                print(f"Valid commands = {self.valid_commands}.\n")
                continue

    def search_tool_menu(self):
        while True:
            print("Type 'back' to return to main menu or 'exit' to exit the program.")
            id = input("Enter tool id: ").strip()
            if id == 'back':
                break
            if id == 'exit':
                print("Bye!")
                exit()
            else:
                extractor.search_tool(id)
                continue


if __name__ == '__main__':
    tools = ToolDatabase()
    extractor = Extractor()
    UserInterface()
