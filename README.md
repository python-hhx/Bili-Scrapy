# Bili-Scrapy
抓取用户个人简介、视频、文章及关注粉丝等内容

# 使用到的工具有：
1、Mysql：用于存放爬取数据
2、Redis：用来存放爬虫的用户mid，这里使用Redis的原因是因为，我可以随时停止，然后再随时从同一个mid开始爬取
3、Scrapy: Python爬虫框架
