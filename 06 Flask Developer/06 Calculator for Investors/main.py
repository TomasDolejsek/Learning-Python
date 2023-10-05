from sqlalchemy import Column, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv

Base = declarative_base()


class Companies(Base):
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

    def process_item(self, item):
        pass


class MainMenu(Menu):
    def __init__(self):
        super().__init__("MAIN MENU", ("Exit", "CRUD operations", "Show top ten companies by criteria"))

    def process_item(self, item):
        if item == 0:
            print("Have a nice day!")
            exit()
        return item


class CrudMenu(Menu):
    def __init__(self):
        super().__init__("CRUD MENU", ("Back", "Create a company", "Read a company", "Update a company",
                                       "Delete a company", "List all companies"))

    def process_item(self, item):
        if item == 0:
            return 0
        else:
            print("Not implemented!\n")
            return 0


class TopTenMenu(Menu):
    def __init__(self):
        super().__init__("TOP TEN MENU", ("Back", "List by ND/EBITDA", "List by ROE", "List by ROA"))

    def process_item(self, item):
        if item == 0:
            return 0
        else:
            print("Not implemented!\n")
            return 0


class InvestCalc:
    def __init__(self):
        self.DATA_FILES = ('Data/companies.csv', 'Data/financial.csv')
        self.create_database()
        # self.start()

    def create_database(self):
        engine = create_engine('sqlite:///investor.db', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        for n, file in enumerate(self.DATA_FILES):
            with open(file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                reader.__next__()  # skip the first line with a table header
                for row in reader:
                    for i, data in enumerate(row):  # replacing empty values with None
                        if not data:
                            row[i] = None
                    if n == 0:
                        item = Companies(ticker=row[0], name=row[1], sector=row[2])
                    else:
                        item = Financial(ticker=row[0], ebitda=row[1], sales=row[2], net_profit=row[3],
                                         market_price=row[4], net_debt=row[5], assets=row[6], equity=row[7],
                                         cash_equivalents=row[8], liabilities=row[9])
                    session.add(item)

        session.commit()
        session.close()
        print("\nDatabase created successfully!")

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
    InvestCalc()
