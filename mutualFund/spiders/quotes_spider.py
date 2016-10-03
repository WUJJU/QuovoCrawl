import scrapy
import xml.etree.ElementTree as ET


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    def start_requests(self):
        urls = [
            'https://www.sec.gov/edgar/searchedgar/companysearch.html'
        ]
        for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
 
        CIK=getattr(self,'CIK',None)
        return scrapy.FormRequest.from_response(
               response,
               formcss='form#fast-search',
               formdata={'CIK':CIK},
               callback=self.after_click
            )
    #search result
    def after_click(self,response):
        links='links.html'

        for tr in response.css('table.tableFile2 tr'):
             tds=tr.css('td')
             if tds:
                if tds.css('td::text')[0].extract() =='13F-HR':
                    # with open(links,'ab') as l:
                    #     l.write(tds.css('td a::attr(href)')[0].extract())
                    #     l.write('\n\r')
                    next_link=tds.css('td a::attr(href)')[0].extract()
                    if next_link is not None:
                        next_link=response.urljoin(next_link)
                        print("next_link: "+next_link)
                        yield scrapy.Request(next_link,callback=self.result)
                        break

    #get 13F-HR txt 
    def result(self,response):
        for tr in response.css('table.tableFile tr'):
            tds=tr.css('td')
            if tds:
                if tds.css('td::text')[1].extract()=='Complete submission text file':
                    content_link=tds.css('td a::attr(href)')[0].extract()
                    if content_link is not None:
                        content_link=response.urljoin(content_link)
                        # print("content_link: "+content_link)
                        yield scrapy.Request(content_link,callback=self.parse_result)

    #parse html  file                    
    def parse_result(self,response):
        print('parse html'+response.url)
        htmlfile="html.txt"
        with open(htmlfile,'wb') as l:
            l.write(response.body)

        lines=open('html.txt','r')
        count=-1
        while True:
            text=lines.readline()
            if not text: break
            if '<XML>' in text: 
                count=count+1
                xml_f="13F-HR-%s.xml" % count
                with open(xml_f,'a') as f:
                    while True:
                      text=lines.readline()
                      if '</XML>' in text: 
                        f.close()
                        self.convert_xml_td(xml_f)
                        break
                      f.write(text)
                 
                    

    def convert_xml_td(self,filename):
        tree=ET.parse(filename)
        root=tree.getroot()
        print(filename + root.tag)
        r_tag=root.tag.split("}")[-1]
        if r_tag=="edgarSubmission":
            headerData=root.find(root[0].tag)
            self.convert_headerData(headerData,filename)
            formData=root.find(root[1].tag)
            # self.convert_formData(formData,filename)
        elif r_tag=="informationTable":
                print(root.tag+"\n")

    def convert_headerData(self,headerData,filename):
        with open(filename+".txt",'a') as f:

            submissionType=headerData.find(headerData[0].tag).tag
            liveTestFlag=headerData[1].find(headerData[1][0].tag).tag
            cik=headerData[1][1][0].find(headerData[1][1][0][0].tag).tag
            ccc=headerData[1][1][0].find(headerData[1][1][0][1].tag).tag
            periodOfReport=headerData[1].find(headerData[1][2].tag).tag
        
            f.write(submissionType+"\t"+liveTestFlag+"\t"+cik+"\t"+ccc+"\t"+periodOfReport+"\n")
            submissionType=headerData.find(headerData[0].tag).text
            liveTestFlag=headerData[1].find(headerData[1][0].tag).text
            cik=headerData[1][1][0].find(headerData[1][1][0][0].tag).text
            ccc=headerData[1][1][0].find(headerData[1][1][0][1].tag).text
            periodOfReport=headerData[1].find(headerData[1][2].tag).text

            f.write(submissionType+"\t"+liveTestFlag+"\t"+cik+"\t"+ccc+"\t"+periodOfReport+"\n")

    # def convert_formData(self,formData,filename):


        


                                 







