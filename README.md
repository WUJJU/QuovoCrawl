# QuovoCrawl
Crawling Mutual Funds by CIK then convert into tab-delimited text file Using Scrapy+etree

follow the link to install Scrapy if you don't have scrapy: https://doc.scrapy.org/en/latest/intro/install.html




-----------------------------------------------------------------------------------

-----------
command run:
cd 到最外层文件下
scrapy   crawl spider文件名 -o out.json -t json

=============
#Pipeline data into MongoDB
1. install scrapy-mongodb 
2. change settings file:

           ITEM_PIPELINES = [
           'scrapy_mongodb.MongoDBPipeline',
          ]
       
           MONGODB_URI = 'mongodb://localhost:27017'
            MONGODB_DATABASE = 'scrapy'
           MONGODB_COLLECTION = 'my_items'

3. off course, you need install MongoDB, create table

=======
Questions left
1 proxy&browser
2 custom pipeline
