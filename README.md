# Data-to-Text Annotation

Web-based annotation tool for creating text labels for CSV data

These labels can, for example, be used to train a data-to-text NLP model

### TODO: add screenshot here

## Set-up

Install pip packages:

    pip install -r requirements.txt

Set-up submodules:

    git submodule update --init --recursive

Set-up database:

    python db.py

## Running the app

    python app.py --csv_dir=/path/to/csv/files/

## Combining several db files

    python post_processing.py --db_dir=/path/to/db/files/
