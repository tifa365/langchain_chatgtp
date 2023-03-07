# Import lxml and parse the XML string

from lxml import etree

# Define a dictionary of namespaces
namespaces = {
  "excerpt": "http://wordpress.org/export/1.2/excerpt/",
  "content": "http://purl.org/rss/1.0/modules/content/",
  "wfw": "http://wellformedweb.org/CommentAPI/",
  "dc": "http://purl.org/dc/elements/1.1/",
  "wp": "http://wordpress.org/export/1.2/"
}

# Import the XML file and parse as etree 
tree = etree.parse("wordliner_artikel.xml")

# Find all item elements under root using namespaces
items = root.findall("channel/item", namespaces=namespaces)

# Loop through each item and print its title
for item in items:
  # Find the title element under each item and get its text content using namespaces
  title = item.find("title", namespaces=namespaces).text
  
  # Find the main text element under each item using Xpath and get its text content using namespaces
  main_text = item.xpath("content:encoded/text()", namespaces=namespaces)[0]
  
  # Find the creator element under each item using Xpath and get its text content using namespaces
  creator = item.xpath("dc:creator/text()", namespaces=namespaces)[0]
  
  # Find the pubDate element under each item using Xpath or tag name and get its text content
  pubDate = item.find("pubDate").text
  
  # Find the link element under each item using Xpath or tag name and get its text content
  link = item.find("link").text
  
  
 ## Create a database and write the extracted data to it

import pandas as pd
from sqlalchemy import create_engine

# Create sqlite database and cursor
engine = create_engine('sqlite:///wordliner_magazin.db', echo=False)

# Create a data frame from your extracted data
data = []
for item in items:
  # Extract the title, main text, creator and pubDate of each item
  title = item.find("title", namespaces=namespaces).text
  main_text = item.xpath("content:encoded/text()", namespaces=namespaces)[0]
  creator = item.xpath("dc:creator/text()", namespaces=namespaces)[0]
  pubDate = item.find("pubDate").text
  
  # Append a tuple of the extracted data to the data list
  data.append((title, main_text, creator, pubDate))

# Create a data frame from the data list with column names
df = pd.DataFrame(data, columns=['title', 'main_text', 'creator', 'pubDate'])

# Write the data frame to a table named 'items' in the database using pandas
df.to_sql('items', engine, if_exists='append', index=False)