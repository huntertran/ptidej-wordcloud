Wordcloud generator for Eclipse IOT projects
---

Using scrapy, `nltk` library for automatically generate wordcloud for projects listed in eclipse iot site

<!-- TOC -->

- [Steps](#steps)
- [Install package](#install-package)
- [Run the project:](#run-the-project)
- [Debug](#debug)

<!-- /TOC -->

# 1. Steps

1. Define a project list (a simple .json file, with 4 attribute for each project: IsCrawled, CrawDepthLevel, IsWordcloudGenerated, SiteUrl. The steps follow will repeat for all the project in the list)
2. Crawl the site with re-defined depth level, extract all text into a .txt file (a series of paragraph, we can use this later to find out relationship between projects)
3. Preprocessing crawled data
    1. Sentence Tokenize the paragraphs
    2. Word Tokenize the sentences
    3. Stem the words (since at this point, we don’t need the other forms of a word)
    4. Remove all stop words (with English list of stop words and my own redefined stop word, for example `eclips`, `github`, `project`, etc)
    5. Extract all programming languages (If we want to include the programming languages in wordcloud, we must choose between the language the project is written in/the languages the project support)
4. Draw the wordcloud
    1. Get frequency distribution of each keywords in step 3, select the 50 most common keywords (can choose any number, not just 50 😃 )
    2. Feed the drawing python lib to create the picture above, then save/serve the picture

# 2. Install package

After each run, the `ptidejWordcloud/sitelist.json` file mark the project crawled or wordcloud generated with `true` value. Modify these values if you want to re-run any project

> Requirement: python 3.7 and above

**Install python packages**

```bash
[sudo] python3 -m pip install Twisted
# for windows:
# pip install Twisted[windows_platform]
[sudo] python3 -m pip install Scrapy
[sudo] python3 -m pip install matplotlib
[sudo] python3 -m pip install numpy
[sudo] python3 -m pip install Pillow
[sudo] python3 -m pip install Wordcloud
[sudo] python3 -m pip install tabulate
[sudo] python3 -m pip install pandas
```

Install Natural Language Processing toolkit (nltk)

**Install package**

```bash
[sudo] python3 -m pip install nltk
```

**Download nltk.data**

```bash
python3

>>> import nltk
>>> nltk.download('stopwords')
>>> nltk.download('punkt')
```

**For Windows Machine**

Using python on Windows machine require Microsoft Visual C++ Build Tools.

> You can get the build tools at [https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/).

[Here](https://www.nltk.org/data.html) is more about downloading nltk data

# 3. Run the project:

```bash
cd rootProjectFolder
[sudo] python3 auto_runner.py
```

# 4. Debug

For debugging with Visual Studio Code:

1. Choose Python: Run Scrapy and NLTK at debug menu list

![debug menu](https://i.imgur.com/hnNbMKo.png)

2. Put a break point in any of the python code
3. Press F5 or debug button to start debugging

![debug python with vscode](https://i.imgur.com/VIeMJNC.png)