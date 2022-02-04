#Sql file to create tables for DB

CREATE TABLE app_scrape_forms (
application TEXT,
url TEXT,
path TEXT,
form_role TEXT,
form_id TEXT,
form_name TEXT,
form_other TEXT,
import_datetime TEXT,
import_date TEXT
);

CREATE TABLE app_scrape_links (
application TEXT,
url TEXT,
path TEXT,
links TEXT,
import_datetime TEXT,
import_date TEXT
);
