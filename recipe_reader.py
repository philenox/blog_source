import pandas as pd
import sqlite3
import pprint as pp
import os
import re
import download_google_drive

def create_db(db_path):
    # Delete the database file if it exists
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the Recipes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Recipes (
        recipe_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL
    );
    """)

    # Create the Tags table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tags (
        tag_id INTEGER PRIMARY KEY,
        tag_name TEXT UNIQUE NOT NULL
    );
    """)

    # Create the Ingredients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ingredients (
        ingredient_id INTEGER PRIMARY KEY,
        ingredient_name TEXT UNIQUE NOT NULL
    );
    """)

    # Create the RecipeIngredients table for many-to-many relationship between recipes and ingredients
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS RecipeIngredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        ingredient_id INTEGER,
        amount REAL,
        preparation TEXT,
        FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id),
        FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
    );
    """)

    # Create the RecipeTags table for many-to-many relationship between recipes and tags
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS RecipeTags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        tag_id INTEGER,
        FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id),
        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
    );
    """)

    # Create the Instructions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Instructions (
        instruction_id INTEGER PRIMARY KEY,
        recipe_id INTEGER,
        step_number INTEGER,
        instruction_text TEXT NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
    );
    """)

    # Create the Notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Notes (
        note_id INTEGER PRIMARY KEY,
        recipe_id INTEGER,
        note_text TEXT NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
    );
    """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    
# function for reading in recipe record.xlsx
def read_recipes_to_db(file_path, db_path, mode):
    # initialize the database
    if mode == 'w':
        create_db(db_path)
    elif mode == 'a':
        pass
    else:
        raise ValueError("Mode must be 'w' or 'a'")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read the Excel file, each sheet is a recipe, column follows the following format:
    # Column 1: Recipe Title
    # Column 2: Tags
    # Column 3: Ingredient Amounts
    # Column 4: Ingredient Name
    # Column 5: Preparation (optional)
    # Column 4: Instructions
    # Column 5: Notes (optional)

    xls = pd.ExcelFile(file_path)
    
    # Iterate through each sheet (recipe) in the Excel file
    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame, the first row is the header
        df = pd.read_excel(xls, sheet_name, header=0)
        
        # get the recipe title, ingredients, tags, and instructions
        
        try:
            recipe_title = df["Title"][0]
            # create a slug for the recipe based on title
            slug = re.sub(r'\W+', '', recipe_title.lower())
            ingredients = df["Ingredients"]
            tags = df["Tags"]
            instructions = df["Instructions"]
            amounts = df["Amounts"]
        except KeyError as e:
            print(f"Error reading sheet {sheet_name}. Skipping...")
            continue

        # check if the recipe has a preparation column, if so read, it, otherwise, set it to None
        try:
            preparation = df["Preparation"]
        except KeyError:
            preparation = [None] * len(ingredients)

        # check if the recipe has a notes column, if so read, it, otherwise, set it to None
        try:
            notes = df["Notes"]
        except KeyError:
            notes = [None] * len(instructions)

        # add the recipe to the Recipes table
        try:
            cursor.execute("INSERT INTO Recipes (title, slug) VALUES (?, ?)", (recipe_title, slug))
        except sqlite3.IntegrityError:
            print(f"Recipe {recipe_title} already exists in the database. Skipping.")
            continue    
        # get the recipe_id of the recipe that was just added
        cursor.execute("SELECT recipe_id FROM Recipes WHERE title = ?", (recipe_title,))
        recipe_id = cursor.fetchone()[0]

        # add ingredient to the Ingredients table, linking them to the recipe in the RecipeIngredients table
        for ingredient, amount, preparation in zip(ingredients, amounts, preparation):
            # check if ingredient is NULL, if so, skip
            if pd.isnull(ingredient):
                continue        
            ingredient_name = ingredient.lower().strip()

            cursor.execute("INSERT OR IGNORE INTO Ingredients (ingredient_name) VALUES (?)", (ingredient_name,))
            cursor.execute("SELECT ingredient_id FROM Ingredients WHERE ingredient_name = ?", (ingredient_name,))
            ingredient_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO RecipeIngredients (recipe_id, ingredient_id, amount, preparation) VALUES (?, ?, ?, ?)", (recipe_id, ingredient_id, amount, preparation))        
        
        # Add tags to the Tags table, linking them to the recipe in the RecipeTags table
        for tag in tags:
            # check if tag is NULL, if so, skip
            if pd.isnull(tag):
                continue
            tag = tag.strip()
            tag = tag.lower()
            cursor.execute("INSERT OR IGNORE INTO Tags (tag_name) VALUES (?)", (tag,))
            cursor.execute("SELECT tag_id FROM Tags WHERE tag_name = ?", (tag,))
            tag_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO RecipeTags (recipe_id, tag_id) VALUES (?, ?)", (recipe_id, tag_id))

        # Add instructions to the Instructions table
        for i, instruction in enumerate(instructions):
            # check if instruction is NULL, if so, skip
            if pd.isnull(instruction):
                continue
            cursor.execute("INSERT INTO Instructions (recipe_id, step_number, instruction_text) VALUES (?, ?, ?)", (recipe_id, i + 1, instruction))
        
        # Add notes to the Notes table
        for note in notes:
            # check if note is NULL, if so, skip
            if pd.isnull(note):
                continue
            cursor.execute("INSERT INTO Notes (recipe_id, note_text) VALUES (?, ?)", (recipe_id, note))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Example usage
# download the recipe record.xlsx file from Google Drive
main_excel_file_id = '13nvb7SQrreBOXiJbbOkGnAeZuQSMIJWB'
main_destination = 'recipe record.xlsx'
print("Downloading the recipe record from Google Drive...")
download_google_drive.download_google_drive_file(main_excel_file_id, main_destination)
read_recipes_to_db('recipe record.xlsx', 'recipes.db', 'w')

# download the second northway family 
northway_excel_file_id = '1zjv58kosxO-osxiJznOoM71Oxa_dYc0Q'
northway_destination = 'recipe record northway.xlsx'
print("Downloading the Northway recipe record from Google Drive...")
download_google_drive.download_google_drive_file(northway_excel_file_id, northway_destination)
read_recipes_to_db('recipe record northway.xlsx', 'recipes.db', 'a')