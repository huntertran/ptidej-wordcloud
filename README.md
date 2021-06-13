WordStorms generator for Projects in Ecosystems
---

Keyword for research: Latent Semantic Indexing - WordNet

Using scrapy, `nltk` library for automatically generate wordcloud for projects listed in eclipse iot site

<!-- TOC -->

- [1. Steps](#1-steps)
- [2. Install package](#2-install-package)
- [3. Config Java VM argument](#3-config-java-vm-argument)
- [4. Run the project](#4-run-the-project)
- [5. Debug](#5-debug)

<!-- /TOC -->

# 1. Steps
<a id="markdown-steps" name="steps"></a>

1. Define the following inputs:
    1. A project list. The steps follow will repeat for all the project in the list.
    2. A protocol keyword list: Json file contains array of items. For example

```json
[
    {
        "IsCrawled": true,
        "CrawlDepthLevel": 1,
        "IsWordcloudGenerated": true,
        "SiteUrl": "http://www.eclipse.org/paho/"
    }
]
```

```json
[
    {
        "id": 1,
        "description": "Message Queuing Telemetry Transport",
        "keys": [
            "MQTT",
            "ZMQ",
            "RabbitMQ"]
    }
]
```
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
5. Analyze the crawled data with NLP
    1. Split sentences and tokenize
    2. Find the sentences containing the keywords
    3. Use Grammar rules to identify the relationship implied by the sentence
6. Generate graph of the relationship
7. Draw the graph

> For now, drawing grammar tree only worked on Windows

# 2. Install package
<a id="markdown-install-package" name="install-package"></a>

After each run, the `ptidejWordcloud/sitelist.json` file mark the project crawled or wordcloud generated with `true` value. Modify these values if you want to re-run any project

> Requirement:
> - python 3.7 or above
> - Java 8 or above

**Install Ghostscript**

To handle exporting images from .ps file resulted of nltk grammar scan

```bash
# for Windows: using Chocolatey package manager
choco install ghostscript

# for Linux:
[sudo] apt-get install ghostscript
```

**Install python packages**

```bash
[sudo] python3 -m pip install Twisted
# for windows:
# pip install Twisted[windows_platform]
[sudo] python3 -m pip install Scrapy
[sudo] python3 -m pip install beautifulsoup4
[sudo] python3 -m pip install matplotlib
[sudo] python3 -m pip install Pillow
[sudo] python3 -m pip install Wordcloud
[sudo] python3 -m pip install tabulate
[sudo] python3 -m pip install pandas
[sudo] python3 -m pip install --upgrade gensim
[sudo] python3 -m pip install jsonpickle
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
>>> nltk.download('averaged_perceptron_tagger')
>>> nltk.download('wordnet')
>>> quit()
```

**For Windows Machine**

Using python on Windows machine require Microsoft Visual C++ Build Tools.

> You can get the build tools at [https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/).

[Here](https://www.nltk.org/data.html) is more about downloading nltk data

# 3. Config Java VM argument
<a id="markdown-config-java-vm-argument" name="config-java-vm-argument"></a>

Stanford POS Tagger is resource consuming. You will need to increase Java heap size to avoid `java.lang.OutOfMemoryError` exception

Add/modify this parameters in your vscode settings of Java

```bash
"java.jdt.ls.vmargs": "-Xmx4G -Xms512m [existing settings]"
```

# 4. Run the project
<a id="markdown-run-the-project" name="run-the-project"></a>

```bash
cd rootProjectFolder
[sudo] python3 auto_runner.py
```

# 5. Debug
<a id="markdown-debug" name="debug"></a>

For debugging with Visual Studio Code:

1. Choose Python: Run Scrapy and NLTK at debug menu list

![debug menu](https://i.imgur.com/hnNbMKo.png)

2. Put a break point in any of the python code
3. Press F5 or debug button to start debugging

![debug python with vscode](https://i.imgur.com/VIeMJNC.png)
