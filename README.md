# QuovoCrawl
Crawling Mutual Funds by CIK then convert into tab-delimited text file Using Scrapy+etree.

# Prerequisite
Follow the link to install Scrapy if you don't have scrapy: 
        https://doc.scrapy.org/en/latest/intro/install.html

-----------------------------------------------------------------------------------
# Run the Program
command run:
cd QuovoCrawl/
scrapy crawl quotes -a CIK=0001166559

=============
# Result
1. 13F-HR-0.xml 13F-HR-1.xml are XML files parsed from https://www.sec.gov/Archives/edgar/data/1166559/000110465914039387/0001104659-14-039387.txt (the program will read all <XML>s  seperately and write into xml file)

2. 13F-HR-0.xml.txt is the final result I got. (only convert part of xml)

3.  mutualFund/spiders/quotes_spider.py is the main program, you could see all code there.
=======
# Problem and Some Idea
Due to the time, I only convert <headerData> in <edgarSubmission> to tab-delimited text.I think the left part will be done in almost same way using xml.etree.ElementTree

I see there are slightly difference betweeen these Mutual Funds format. In my opinion, adding if else statement is one way to handle the difference if we know which tags we need. Another way may be the regular expression.
