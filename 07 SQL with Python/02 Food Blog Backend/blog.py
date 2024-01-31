from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func
import argparse
from os.path import exists

Base = declarative_base()


# Association table for meals, recipes
class Serve(Base):
    __tablename__ = 'serve'
    serve_id = Column(Integer, primary_key=True)
    meal_id = Column('meal_id', Integer, ForeignKey('meals.meal_id'), nullable=False)
    recipe_id = Column('recipe_id', Integer, ForeignKey('recipes.recipe_id'), nullable=False)


# Association table for measures, recipes, ingredients
class Quantity(Base):
    __tablename__ = 'quantity'
    quantity_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), nullable=False)
    measure_id = Column(Integer, ForeignKey('measures.measure_id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), nullable=False)


class Measure(Base):
    __tablename__ = 'measures'
    measure_id = Column(Integer, primary_key=True)
    measure_name = Column(String, unique=True)

    recipes = relationship("Recipe", secondary='quantity', back_populates='measures')


class Ingredient(Base):
    __tablename__ = 'ingredients'
    ingredient_id = Column(Integer, primary_key=True)
    ingredient_name = Column(String, nullable=False, unique=True)

    recipes = relationship("Recipe", secondary='quantity', back_populates='ingredients',
                           overlaps='recipes')


class Meal(Base):
    __tablename__ = 'meals'
    meal_id = Column(Integer, primary_key=True)
    meal_name = Column(String, nullable=False, unique=True)

    recipes = relationship("Recipe", secondary='serve', back_populates='meals')


class Recipe(Base):
    __tablename__ = 'recipes'
    recipe_id = Column(Integer, primary_key=True)
    recipe_name = Column(String, nullable=False)
    recipe_description = Column(String)

    meals = relationship('Meal', secondary='serve', back_populates='recipes')
    measures = relationship("Measure", secondary='quantity', back_populates='recipes',
                            overlaps='recipes')
    ingredients = relationship("Ingredient", secondary='quantity', back_populates='recipes',
                               overlaps='recipes, measures')


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
        for measure in self.data['measures']:
            self.session.add(Measure(measure_name=measure))
        for ingredient in self.data['ingredients']:
            self.session.add(Ingredient(ingredient_name=ingredient))
        for meal in self.data['meals']:
            self.session.add(Meal(meal_name=meal))
        self.session.commit()

    def add_to_db(self, asset):
        self.session.add(asset)
        self.session.commit()

    def get_meals(self):
        query = self.session.query(Meal)
        return [x for x in query]

    def get_measures(self):
        query = self.session.query(Measure)
        return [x for x in query]

    def get_ingredients(self):
        query = self.session.query(Ingredient)
        return [x for x in query]

    def get_recipes(self, wi, wm):
        if wi and wm:
            query = self.session.query(Recipe).join(Recipe.ingredients).join(Recipe.meals)
            filter_query = (
                query.filter(Ingredient.ingredient_name.in_(wi))
                .filter(Meal.meal_name.in_(wm))
                .group_by(Recipe.recipe_id)
                .having(func.count(Ingredient.ingredient_id) == len(wi))
            )
        elif not wm:
            query = self.session.query(Recipe).join(Recipe.ingredients)
            filter_query = (
                query.filter(Ingredient.ingredient_name.in_(wi))
                .group_by(Recipe.recipe_id)
                .having(func.count(Ingredient.ingredient_id) == len(wi))
            )
        elif not wi:
            query = self.session.query(Recipe).join(Recipe.meals)
            filter_query = query.filter(Meal.meal_name.in_(wm))

        return [x.recipe_name for x in filter_query.all()]

    def get_ingredient_data(self, ing):
        split_ing = ing.split()
        if len(split_ing) == 3:
            quantity, measure, ingredient = split_ing
        elif len(split_ing) == 2:
            quantity, ingredient = split_ing
            measure = None
        else:
            return False

        try:
            quantity = int(quantity)
        except ValueError:
            print("Quantity must be a number!")
            return False

        if not measure:
            measure_id = 8  # empty measure id
        else:
            known_measures = self.get_measures()
            same = 0
            for m in known_measures:
                if m.measure_name.startswith(measure):
                    same += 1
                    measure_id = m.measure_id
            if same > 1:
                print("The measure is not conclusive!")
                return False
            if same == 0:
                print("No such measure!")
                return False

        known_ingredients = self.get_ingredients()
        same = 0
        for i in known_ingredients:
            if ingredient in i.ingredient_name:
                same += 1
                ingredient_id = i.ingredient_id
        if same > 1:
            print("The ingredient is not conclusive!")
            return False
        if same == 0:
            print("No such ingredient!")
            return False

        return quantity, measure_id, ingredient_id

    def close(self):
        self.session.close()
        self.engine.dispose()


class UserInterface:
    def __init__(self, wanted_ings, wanted_meals):
        if not (wanted_ings or wanted_meals):
            self.add_new_items()
        else:
            self.search_recipes(wanted_ings, wanted_meals)

    @staticmethod
    def search_recipes(wanted_ings, wanted_meals):
        wi = wanted_ings.split(',') if wanted_ings else None
        wm = wanted_meals.split(',') if wanted_meals else None
        result = db.get_recipes(wi, wm)
        if result:
            print(f"Recipes selected for you: {', '.join(map(str,result))}")
        else:
            print("There are no such recipes in the database.")
        db.close()

    @staticmethod
    def add_new_items():
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
            recipe = Recipe(recipe_name=name, recipe_description=desc)
            db.add_to_db(recipe)

            for s in served:
                serve = Serve(meal_id=int(s), recipe_id=recipe.recipe_id)
                db.add_to_db(serve)

            while True:
                ing = input("Input quantity of ingredient <press ENTER to stop>: ")
                if not ing:
                    break
                results = db.get_ingredient_data(ing)
                if not results:
                    continue
                quantity = Quantity(quantity=results[0], recipe_id=recipe.recipe_id,
                                    measure_id=results[1], ingredient_id=results[2])
                db.add_to_db(quantity)
        db.close()


class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('db_name')
        parser.add_argument('--ingredients')
        parser.add_argument('--meals')
        self.args = parser.parse_args()


if __name__ == '__main__':
    cl = CommandLine()
    db = DatabaseProcessor(cl.args.db_name)
    UserInterface(cl.args.ingredients, cl.args.meals)
