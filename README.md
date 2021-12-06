#Project Instruction

## Web crawle
File: CrawlAllNews.py 

First use function GetLoadedPageContent(url, n) to simulate cilck the web by 20 times,
and get the content of the Web.

Then use function GetAllNewsUrl(Text) to get all the News'Url in the content.
Save all the url in NewsUrl.xlsx.

Finally use function GetNewsContext(url) to extract the News'content
then download it to .txt file. Save all the News in News holder.

Output:NewsUrl.xlsx||News

## Pre Processing
I used the News 'amazon-announces-premiere-date-for-as-we-see-it.txt'
First use spacy lib to NER, indentifng Organiztions' names in News, and delete all the names.
Then the Re to delete punctuation and number. And I performed a words split and removed stop words and lemmatizate 
the News' tokens.





