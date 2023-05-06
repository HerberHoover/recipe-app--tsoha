# Recipe Application


RecipeApp is an easy-to-use web application that helps users manage and organize their favorite recipes. With a simple interface, this app makes it easy to create, view, update, and delete recipes. Users can also sort their recipes into categories, making it quick and convenient to find the right dish for any occasion. 

First you only need to create a user and then you can start saving and categorizing recipes

## Features For Future


- Recipe Sharing
- Implement a search functionality based on recipe names.
- Allow users to search for recipes using specific ingredients.
- Enable the use of pre-existing ingredients to search for recipes, possibly through a linked database or integration.
- Introduce a "Recipe of the Day" notification feature.


## Prerequisites

- Python 3.x


## Setting up the virtual environment

1. Create and activate virtual environment:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```


2. Install dependencies


```bash
pip install -r ./requirements.txt
```


3. Create .env file to project root

```bash
DATABASE_URL=<local-database-address>
SECRET_KEY=<secret-key>
```

4. Run application

```bash
flask run
```


Please report any issues or suggestions for improvement on the project's GitHub repository.

