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
        print("\nDatabase created successfully!")

    def create_company(self):
        data = dict()
        print("Enter ticker (in the format 'MOON'):")
        data['ticker'] = input()
        print("Enter company (in the format 'Moon Corp'):")
        data['name'] = input()
        print("Enter industries (in the format 'Technology'):")
        data['sector'] = input()

        self.session.add(Company(ticker=data['ticker'], name=data['name'], sector=data['sector']))

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

        self.session.add(Financial(ticker=data['ticker'], ebitda=data['ebitda'], sales=data['sales'],
                                   net_profit=data['net_profit'], market_price=data['market_price'],
                                   net_debt=data['net_debt'], assets=data['assets'], equity=data['equity'],
                                   cash_equivalents=data['cash_equivalents'], liabilities=data['liabilities']))

        self.session.commit()
        print("Company created successfully!")

    def read_company(self):
        query = self.session.query(Company)
        print("Enter company name:")
        comp_name = input()
        comp_filter = query.filter(Company.name == comp_name)
        if not comp_filter.first():
            print("Company not found!\n")
            return
        print(f"{i} {row.name}")


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
        return 0


class TopTenMenu(Menu):
    def __init__(self):
        super().__init__("TOP TEN MENU", ("Back", "List by ND/EBITDA", "List by ROE", "List by ROA"))

    @staticmethod
    def process_item(item):
        if item == 0:
            return 0
        else:
            print("Not implemented!\n")
            return 0


class InvestCalc:
    def __init__(self):
        self.start()

    @staticmethod
    def start():
        menu = MainMenu()
        while True:
            menu.display()
            pick = menu.pick_from_menu()
            if pick == -1:
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
