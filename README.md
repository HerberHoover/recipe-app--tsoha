# Recipe Application


RecipeApp is a web application that allows users to manage their favorite recipes. Users can create, view, update, and delete recipes. They can also search for recipes based on various criteria.

## Features Completed
The current state of the application includes the following functionality:

- User authentication (login, registration, and logout).
- Creation, viewing, and editing of recipes.
- Organizing recipes into categories.
- Viewing recipes by category.
- Adding recipes to categories.
- Basic error handling and user notifications.

## Features Under Construction


- Search for recipes by name, ingredients, and other criteria
- Improving application layout
- Refactoring main.py, improve modularity.
- Adding tests
- Adding error handling and exceptions
- Fixing the Home Screen issue
- Implementing auto logout functionality


## Prerequisites

- Python 3.x


## Setting up the virtual environment

1. Create and activate virtual environment:

- python3 -m venv venv
- source venv/bin/activate


2. Install dependencies

- pip install -r ./requirements.txt


3. Create .env file to project root

- DATABASE_URL=< local-database-address >
- SECRET_KEY=< secret-key >


4. Run application

- flask run



Please report any issues or suggestions for improvement on the project's GitHub repository.




PS
" In the process of cleaning up main.py - everything's crammed in there together for "consistency's" sake. "
