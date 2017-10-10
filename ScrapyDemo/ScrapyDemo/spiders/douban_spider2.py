# -*- coding: utf-8 -*-

import scrapy,urllib,re
from scrapy.http import Request,FormRequest
from ScrapyDemo.items import DoubanSpiderItem


# 模拟登陆
class DoubanSpider(scrapy.Spider):

    name = "douban2"
    url = 'https://www.douban.com/people/163296676/rev_contacts?start=0'
    allowed_domains = ["douban.com"]
    #start_urls = ['http://douban.com/']
    header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

    # 将登陆页面入列
    def start_requests(self):
        url='https://www.douban.com/accounts/login'
        return [Request(url=url,headers= self.header,meta={"cookiejar":1},callback=self.parse)]#可以传递一个标示符来使用多个。如meta={'cookiejar': 1}这句，后面那个1就是标示符

    # 回调函数 -- 登陆
    def parse(self, response):
        print response.status
        captcha=response.xpath('//*[@id="captcha_image"]/@src').extract()  #获取验证码图片的链接
        print captcha
        if len(captcha)>0:
            '''此时有验证码'''
            #人工输入验证码
            urllib.urlretrieve(captcha[0],filename="captcha.png")
            captcha_value=raw_input('查看captcha.png,有验证码请输入:')

            #用快若打码平台处理验证码--------验证码是任意长度字母，成功率较低
            # captcha_value=ruokuai.get_captcha(captcha[0])
            # reg=r'<Result>(.*?)</Result>'
            # reg=re.compile(reg)
            # captcha_value=re.findall(reg,captcha_value)[0]
            print '验证码为：',captcha_value

            data={
                'redir': 'https://www.douban.com/',
                "form_email": "192088480@qq.com",
                "form_password": "zhenxi58695",
                "captcha-solution": captcha_value,
                'login': u'登录'
                #"redir": "https://www.douban.com/people/151968962/",      #设置需要转向的网址，由于我们需要爬取个人中心页，所以转向个人中心页
            }
        else:
            '''此时没有验证码'''
            print '无验证码'
            data={
                'redir': 'https://www.douban.com/',
                "form_email": "192088480@qq.com",
                "form_password": "zhenxi58695",
                'login': u'登录'
                #"redir": "https://www.douban.com/people/151968962/",
            }
        print '正在登陆中......'
        ####FormRequest.from_response()进行登陆
        return [
            FormRequest.from_response(
                response,
                meta={"cookiejar":response.meta["cookiejar"]},
                headers=self.header,
                formdata=data,
                callback=self.get_content,
            )
        ]

    # 回调函数 -- 检测登陆是否成功
    def get_content(self,response):
        title=response.xpath('//title/text()').extract()[0]
        if u'登录豆瓣' in title:
            print '登录失败，请重试！'
        else:
            print '登录成功'
            '''
            可以继续后续的爬取工作
            '''
            return [Request(url=self.url,headers= self.header,meta={"cookiejar":response.meta["cookiejar"]},callback=self.parse2)]

    # 回调函数 -- 取所需内容
    def parse2(self,response):
        print response
        for index in response.xpath("//dl[@class='obu']"):
            item = DoubanSpiderItem()
            item['name'] = index.xpath(".//img/attribute::alt").extract_first()
            item['image'] = index.xpath(".//img/attribute::src").extract_first()
            item['href'] = index.xpath(".//a/attribute::href").extract_first()
            yield item
            next_page = response.xpath("//span[@class='next']/a/attribute::href").extract_first()
            if next_page is not None:
                yield response.follow(url=next_page.encode("ascii"),headers=self.header,meta={"cookiejar":response.meta["cookiejar"]},callback=self.parse2)