# Bash script to ingest data
# This involves scraping the data from the web and then cleaning up and putting in Weaviate.
# Error if any command fails

set -e # Set the shell option to exit immediately if any command returns a non-zero status
wget -r -A.html -e robots=off https://docs.wordliner.com/kunden/wordliner-docs-kunden/ # Download all the HTML files recursively from the given URL
python3 ingest.py # Run the Python script named ingest.py that presumably processes the downloaded HTML files
