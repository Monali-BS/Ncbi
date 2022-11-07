"""Write to script to fetch artile details fromm ncbi
 pubmed database (eg. pubmed_id,
 article_link,article title and article description
 And convert to csv file
 Return: csv file containing pubmed_id,
 article_link,article title and article description columns
 """
import requests
import xml.etree.ElementTree as Xet
import pandas as pd
import xmltodict
# include related python libraries here

baseUrl = "https://pubmed.ncbi.nlm.nih.gov/" # Article base link

gene = "EGFR" # gene to be searched for article reference
# urls to fetch data as per gene
# have to study the url structure
url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={gene}&mindate=2022/09/01&maxdate=2022/09/15&datetype=edat&retmax=100000"

#here using this url can get the article details using pubmed_Id
# url_1 = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={id}&retmode=xml"

response = requests.request("GET", url)
with open('test.xml', 'wb') as f:
    f.write(response.content)

# create element tree object
tree = Xet.parse("test.xml")

# get root element
root = tree.getroot()

ids = []
for item in root:
    pubmed_ids = item.findall("Id")
    for id in pubmed_ids:
        ids.append(id.text)

query_list = ' '.join(map(str,ids))
url_1 = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={query_list}&retmode=xml"

response_1 = requests.request("GET", url_1)
data = xmltodict.parse(response_1.content)
items = data.get('PubmedArticleSet').get('PubmedArticle')   

table_data = []
for item in items:
    pubmedID = item.get("MedlineCitation", {}).get('PMID', {}).get('#text', "")
    url = baseUrl + pubmedID
    articleTitle = item.get('MedlineCitation', {}).get('Article', {}).get('ArticleTitle', "")
    articleDescription =item.get('MedlineCitation', {}).get('Article', {}).get('Abstract', {}).get('AbstractText', "")
    table = {
        "ID":pubmedID,
        "Title":articleTitle,
        "Description": str(articleDescription),
        "link": url
    }
    table_data.append(table)

df = pd.DataFrame(table_data)
df.to_csv('output.csv')
print("+============================================")


