# Wordcloud generator for Eclipse IOT projects

Using scrapy, `nltk` library for automatically generate wordcloud for projects listed in eclipse iot site

Steps:

1.	Define a project list (a simple .json file, with 4 attribute for each project: IsCrawled, CrawDepthLevel, IsWordcloudGenerated, SiteUrl. The steps follow will repeat for all the project in the list)
2.	Crawl the site with re-defined depth level, extract all text into a .txt file (a series of paragraph, we can use this later to find out relationship between projects)
3.	Preprocessing crawled data
  a.	Sentence Tokenize the paragraphs
  b.	Word Tokenize the sentences
  c.	Stem the words (since at this point, we don’t need the other forms of a word)
  d.	Remove all stop words (with English list of stop words and my own redefined stop word, for example `eclips`, `github`, `project`, etc)
  e.	Extract all programming languages (If we want to include the programming languages in wordcloud, we must choose between the language the project is written in/the languages the project support)
4.	Draw the wordcloud
  a.	Get frequency distribution of each keywords in step 3, select the 50 most common keywords (can choose any number, not just 50 😃 )
  b.	Feed the drawing python lib to create the picture above, then save/serve the picture
