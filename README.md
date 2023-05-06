# Recipe Application


RecipeApp is a web application that allows users to manage their favorite recipes. Featuring an intuitive interface, users can easily create, view, update, and delete recipes. Users can also organize recipes by categories


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

