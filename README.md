**Scrapy**

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
  - 自定义存储：改写pipelines.py

**豆瓣爬虫**

- 使用cookies
- 账号密码登陆：使用meta传递cookies


**AJAX**

- 通用方案：selenium + 浏览器驱动（PhantomJS、Chrome等）
- scrapy - splash：lua脚本


**增量式**

- 本身不支持，但可以结合第三方组件 scrapy-deltafetch   
- https://github.com/scrapy-plugins/scrapy-deltafetch

**分布式**

- 采用第三方组件scrapy-redis

  ![2017.10.08](http://scrapy-chs.readthedocs.io/zh_CN/0.24/_images/scrapy_architecture.png)

  ​

  ​	![2017.10.08](https://www.biaodianfu.com/wp-content/uploads/2016/12/scrapy-redis.jpg)

- dequeue — redis