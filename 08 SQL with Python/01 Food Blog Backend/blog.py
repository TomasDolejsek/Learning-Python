from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import argparse
from os.path import exists

Base = declarative_base()


class Measure(Base):
    __tablename__ = 'measures'

    measure_id = Column(Integer, primary_key=True)
    measure_name = Column(String, unique=True)


class Ingredient(Base):
    __tablename__ = 'ingredients'

    ingredient_id = Column(Integer, primary_key=True)
    ingredient_name = Column(String, nullable=False, unique=True)


class Meal(Base):
    __tablename__ = 'meals'

    meal_id = Column(Integer, primary_key=True)
    meal_name = Column(String, nullable=False, unique=True)


class Recipe(Base):
    __tablename__ = 'recipes'

    recipe_id = Column(Integer, primary_key=True)
    recipe_name = Column(String, nullable=False)
    recipe_description = Column(String)


class Serve(Base):
    __tablename__ = 'serve'

    serve_id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey(Meal.meal_id), nullable=False)
    recipe_id = Column(Integer, ForeignKey(Recipe.recipe_id), nullable=False)


class DatabaseProcessor:
    def __init__(self, name):
        self.engine = create_engine("sqlite:///" + name, echo=False)
        self.session = sessionmaker(bind=self.engine)()
        self.data = {"measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", ""),
                     "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
                     "meals": ("breakfast", "brunch", "lunch", "supper")}
        if not exists(name):
            Base.metadata.create_all(self.engine)
            self.populate_db()

    def populate_db(self):
        for i, measure in enumerate(self.data['measures']):
            self.session.add(Measure(measure_id=i, measure_name=measure))
        for i, ingredient in enumerate(self.data['ingredients']):
            self.session.add(Ingredient(ingredient_id=i, ingredient_name=ingredient))
        for i, meal in enumerate(self.data['meals']):
            self.session.add(Meal(meal_id=i, meal_name=meal))
        self.session.commit()

    def add_to_db(self, asset):
        self.session.add(asset)
        self.session.commit()

    def get_meals(self):
        query = self.session.query(Meal)
        return [x for x in query]

    def close(self):
        self.session.close()
        self.engine.dispose()


class UserInterface:
    def __init__(self):
        self.start()

    @staticmethod
    def start():
        recipe_id = 0
        serve_id = 0
        meals = db.get_meals()
        while True:
            print("Pass the empty recipe name to exit.")
            name = input("Recipe name: ")
            if not name:
                break
            desc = input("Recipe description: ")
            for meal_id, meal in zip([x.meal_id for x in meals], [x.meal_name for x in meals]):
                print(f"{meal_id}) {meal}", end=' ')
            served = input("\nWhen the dish can be served: ").split()
            recipe = Recipe(recipe_id=recipe_id, recipe_name=name, recipe_description=desc)
            db.add_to_db(recipe)
            for s in served:
                serve = Serve(serve_id=serve_id, meal_id=int(s), recipe_id=recipe_id)
                db.add_to_db(serve)
                serve_id += 1
            recipe_id += 1
        db.close()


class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('db_name')
        self.args = parser.parse_args()


if __name__ == '__main__':
    db_name = CommandLine().args.db_name
    db = DatabaseProcessor(db_name)
    UserInterface()
