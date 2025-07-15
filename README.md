# Vacancy_Database_Saver
This application provides a tool for searching open vacancies of given companies, 
creating PostGreSQL database and providing methods for selecting vacancies.

## Program functionality
Package src containing the following modules:

1. *companies_fetcher* - containing class **HeadHunterCompanies**. 
Searching for the ***id*** of given list of employers from HeadHunter.
2. *vacancies_fetcher* - containing class **HeadHunterVacancies**.
Searching for the ***open vacancies*** of given list of employers id from HeadHunter.
3. *db_manager* - containing class **DBManager**.
Providing methods for creating PostGreSQL database and tables. 
Filling up tables with information provided by classes  **HeadHunterCompanies** and **HeadHunterVacancies**.
Providing methods used in main function for working with database.
4. *logger.py* - setup for logger.

### How program works

+ Application starts with asking the list of companies user would like to search. 
**If field left blank** - default list of companies will be chosen. (See notes)

+ User connecting to database and creating tables for filling up.

+ Search is initializing. Parsed information filling up into tables

+ User choosing one of option from choice menu.

#### Notes

+ Default list of companies is: ***(Pooling, Amigoweb, Doubletapp, InlyIT, PUSK, Digital Sail, Skillline, Mindbox, SPRINTHOST, Voximplant)***

+ Project using virtual environment ***Poetry***. Information about dependencies
located in ***pyproject.toml***. 

For smooth installation of dependencies recommended to use ***Poetry*** virtual environment. 

To install dependencies use command:

```
poetry install
```