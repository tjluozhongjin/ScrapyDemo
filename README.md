**Scrapy**

![2017.10.08](http://scrapy-chs.readthedocs.io/zh_CN/0.24/_images/scrapy_architecture.png)

- 组成
  - 引擎（Engine）：控制数据流在系统中所有组件中流动
  - 调度器（Scheduler）：管理请求队列
  - 下载器（Downloader）：获取页面
  - Spiders：处理页面
  - Item Pipeline：数据存储，清理、验证等


- 流程
  - 引擎向调度器请求下一个要爬取的URL
  - 调度器返回下一个要爬取的URL给引擎，引擎将URL通过下载中间件转发给下载器(Downloader)
  - 下载器(Downloader)获取页面，一旦页面下载完毕，下载器生成一个该页面的Response，并将它返回给调度器（Engine）
  - 引擎从下载器中接收到Response并通过Spider中间件发送给Spider处理。
  - Spider处理Response并返回爬取到的Item及(跟进的)新的Request给引擎。
  - 引擎将(Spider返回的)爬取到的Item交给Item Pipeline，将Request交给调度器。
  - 回到第一步


- 爬

  - start_urls
  - start_requests

- 取
  - 方式：CSS & XPATH
  - Item 字典：一般来说，Spider将会将爬取到的数据以 Item 对象返回。
  - parse是个迭代器

- 存
  - 内置存储：Feed exports
    - JSON
    - JSON lines
    - CSV
    - XML

    ```
    scrapy crawl myspider -o test.json
    ```

  - 自定义存储：改写pipelines.py

**豆瓣爬虫**

- 使用cookies
- 账号密码登陆：使用meta传递cookies


**AJAX**

- 通用方案：selenium + 浏览器驱动（PhantomJS、Chrome等）
- scrapy - splash：lua脚本
- https://github.com/scrapy-plugins/scrapy-splash


**增量式**

- 本身不支持，但可以结合第三方组件 scrapy-deltafetch   
- https://github.com/scrapy-plugins/scrapy-deltafetch

**分布式**

- 采用第三方组件scrapy-redis

- dequeue — redis

- https://github.com/rmax/scrapy-redis

  ![2017.10.08](http://scrapy-chs.readthedocs.io/zh_CN/0.24/_images/scrapy_architecture.png)

  ​

  ​		![2017.10.08](https://www.biaodianfu.com/wp-content/uploads/2016/12/scrapy-redis.jpg)



- 页面加载的问题
  - 足够长的等待：time.sleep()，隐式&显式
  - 根据特定的网站写条件等待