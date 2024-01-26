from sqlalchemy import Column, Float, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os.path import exists
from csv import reader

Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'

    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)


class Financial(Base):
    __tablename__ = 'financial'

    ticker = Column(String, primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


class DatabaseProcessor:
    def __init__(self):
        self.DATABASE_NAME = 'investor.db'
        self.DATA_FILES = ('test/companies.csv', 'test/financial.csv')
        engine = create_engine("sqlite:///" + self.DATABASE_NAME, echo=False)
        Session = sessionmaker(bind=engine, autoflush=False)
        self.session = Session()
        if not exists(self.DATABASE_NAME):
            Base.metadata.create_all(engine)
            self.create_database()

    def create_database(self):
        for n, file in enumerate(self.DATA_FILES):
            with open(file, newline='') as csvfile:
                read_iter = reader(csvfile, delimiter=',', quotechar='"')
                read_iter.__next__()  # skip the first line with a table header
                for row in read_iter:
                    for i, data in enumerate(row):  # replacing empty values with None
                        if not data:
                            row[i] = None
                    if n == 0:
                        item = Company(ticker=row[0], name=row[1], sector=row[2])
                    else:
                        item = Financial(ticker=row[0], ebitda=row[1], sales=row[2], net_profit=row[3],
                                         market_price=row[4], net_debt=row[5], assets=row[6], equity=row[7],
                                         cash_equivalents=row[8], liabilities=row[9])
                    self.session.add(item)
        self.session.commit()
        print("Database created successfully!\n")

    @staticmethod
    def get_financial_data(ticker):
        data = dict()
        data['ticker'] = ticker
        print("Enter ebitda (in the format '987654321'):")
        data['ebitda'] = float(input())
        print("Enter sales (in the format '987654321'):")
        data['sales'] = float(input())
        print("Enter net profit (in the format '987654321'):")
        data['net_profit'] = float(input())
        print("Enter market price (in the format '987654321'):")
        data['market_price'] = float(input())
        print("Enter net debt (in the format '987654321'):")
        data['net_debt'] = float(input())
        print("Enter assets (in the format '987654321'):")
        data['assets'] = float(input())
        print("Enter equity (in the format '987654321'):")
        data['equity'] = float(input())
        print("Enter cash equivalents (in the format '987654321'):")
        data['cash_equivalents'] = float(input())
        print("Enter liabilities (in the format '987654321'):")
        data['liabilities'] = float(input())
        return data

    def create_company(self):
        comp_data = dict()
        print("Enter ticker (in the format 'MOON'):")
        comp_data['ticker'] = input()
        print("Enter company (in the format 'Moon Corp'):")
        comp_data['name'] = input()
        print("Enter industries (in the format 'Technology'):")
        comp_data['sector'] = input()
        self.session.add(Company(ticker=comp_data['ticker'], name=comp_data['name'], sector=comp_data['sector']))

        fin_data = self.get_financial_data(comp_data['ticker'])
        self.session.add(Financial(ticker=fin_data['ticker'], ebitda=fin_data['ebitda'], sales=fin_data['sales'],
                                   net_profit=fin_data['net_profit'], market_price=fin_data['market_price'],
                                   net_debt=fin_data['net_debt'], assets=fin_data['assets'], equity=fin_data['equity'],
                                   cash_equivalents=fin_data['cash_equivalents'], liabilities=fin_data['liabilities']))
        self.session.commit()
        print("Company created successfully!\n")

    def get_company_ids(self):
        comp_query = self.session.query(Company)
        print("Enter company name:")
        comp_name = input()
        comp_filter = comp_query.filter(Company.name.ilike(f"%{comp_name}%"))
        if not comp_filter.first():
            print("Company not found!\n")
            return False
        ticker_list = []
        for i, row in enumerate(comp_filter):
            print(f"{i} {row.name}")
            ticker_list.append([row.ticker, row.name])
        print("Enter company number:")
        number = int(input())
        return ticker_list[number]

    def read_company(self):
        ticker_list = self.get_company_ids()
        if not ticker_list:
            return
        results = self.calculate_data(ticker_list[0])
        print(ticker_list[0], ticker_list[1])
        for data, value in results.items():
            print(f"{data} = ", end='')
            print(f"{round(value, 2)}") if value is not None else print(f"{value}")
        print()

    def update_company(self):
        ticker_list = self.get_company_ids()
        if not ticker_list:
            return
        fin_data = self.get_financial_data(ticker_list[0])
        fin_query = self.session.query(Financial)
        fin_filter = fin_query.filter(Financial.ticker == fin_data['ticker'])
        fin_filter.update({
            'ebitda': fin_data['ebitda'],
            'sales': fin_data['sales'],
            'net_profit': fin_data['net_profit'],
            'market_price': fin_data['market_price'],
            'net_debt': fin_data['net_debt'],
            'assets': fin_data['assets'],
            'equity': fin_data['equity'],
            'cash_equivalents': fin_data['cash_equivalents'],
            'liabilities': fin_data['liabilities']
            })
        self.session.commit()
        print("Company updated successfully!\n")

    def delete_company(self):
        ticker_list = self.get_company_ids()
        if not ticker_list:
            return
        comp_query = self.session.query(Company)
        fin_query = self.session.query(Financial)
        comp_query.filter(Company.ticker == ticker_list[0]).delete()
        fin_query.filter(Financial.ticker == ticker_list[0]).delete()
        self.session.commit()
        print("Company deleted successfully!\n")

    def list_companies(self):
        print("COMPANY LIST")
        comp_query = self.session.query(Company)
        for row in sorted(comp_query, key=lambda x: x.ticker):
            print(f"{row.ticker} {row.name} {row.sector}")
        print()

    def top_ten(self, list_by):
        criteria = ['ND/EBITDA', 'ROE', 'ROA']
        print(f"TICKER {criteria[list_by - 1]}")
        comp_query = self.session.query(Company)
        results = []
        for row in comp_query:
            results.append([row.ticker, *self.calculate_data(row.ticker).values()])
        for result in results:
            if result[list_by + 3] is None:
                results.remove(result)
        results.sort(key=lambda x: x[list_by + 3], reverse=True)
        for i in range(10):
            print(f"{results[i][0]} {round(results[i][list_by + 3], 2)}")
        print()

    @staticmethod
    def get_result(data1, data2):
        try:
            result = data1 / data2
        except TypeError:
            result = None
        return result

    def calculate_data(self, ticker):
        fin_query = self.session.query(Financial)
        data = fin_query.filter(Financial.ticker == ticker).first()
        results = dict()
        results['P/E'] = self.get_result(data.market_price, data.net_profit)
        results['P/S'] = self.get_result(data.market_price, data.sales)
        results['P/B'] = self.get_result(data.market_price, data.assets)
        results['ND/EBITDA'] = self.get_result(data.net_debt, data.ebitda)
        results['ROE'] = self.get_result(data.net_profit, data.equity)
        results['ROA'] = self.get_result(data.net_profit, data.assets)
        results['L/A'] = self.get_result(data.liabilities, data.assets)
        return results


class Menu:
    def __init__(self, name, menus):
        self.menu_name = name
        self.menu = menus

    @property
    def n_items(self):
        return len(self.menu)

    def display(self):
        print(self.menu_name)
        for i in range(self.n_items):
            print(f"{i} {self.menu[i]}")

    def pick_from_menu(self):
        print("\nEnter an option:")
        try:
            user = int(input())
            if not (0 <= user < self.n_items):
                raise ValueError
            return user
        except ValueError:
            print("Invalid option!\n")
            return -1


class MainMenu(Menu):
    def __init__(self):
        super().__init__("MAIN MENU", ("Exit", "CRUD operations", "Show top ten companies by criteria"))

    @staticmethod
    def process_item(item):
        if item == 0:
            print("Have a nice day!")
            exit()
        return item


class CrudMenu(Menu):
    def __init__(self):
        super().__init__("CRUD MENU", ("Back", "Create a company", "Read a company", "Update a company",
                                       "Delete a company", "List all companies"))

    @staticmethod
    def process_item(item):
        if item == 1:
            db.create_company()
        elif item == 2:
            db.read_company()
        elif item == 3:
            db.update_company()
        elif item == 4:
            db.delete_company()
        elif item == 5:
            db.list_companies()
        return 0


class TopTenMenu(Menu):
    def __init__(self):
        super().__init__("TOP TEN MENU", ("Back", "List by ND/EBITDA", "List by ROE", "List by ROA"))

    @staticmethod
    def process_item(item):
        if item in [1, 2, 3]:
            db.top_ten(item)
        return 0


class InvestCalc:
    def __init__(self):
        self.start()

    @staticmethod
    def start():
        print("Welcome to the Investor Program!\n")
        menu = MainMenu()
        while True:
            menu.display()
            pick = menu.pick_from_menu()
            if pick == -1:
                menu = MainMenu()
                continue
            next_menu = menu.process_item(pick)
            if next_menu == 0:
                menu = MainMenu()
                continue
            if next_menu == 1:
                menu = CrudMenu()
                continue
            if next_menu == 2:
                menu = TopTenMenu()
                continue


if __name__ == "__main__":
    db = DatabaseProcessor()
    InvestCalc()