# Google Persistent Disk

## 1、介绍

​	Google Persistent Disk 是适用于 Google Cloud Platform 的耐用、高性能块存储服务。Persistent Disk 提供 SSD 和 HDD 存储空间，两者都可以挂接到 Compute Engine 或 Google Kubernetes Engine 中运行的实例。存储卷可以透明地调整大小、快速备份，并支持多个读取器同时读取。

## 2、特性

​	方便数据共享、快照更方便快速、动态扩容、自动加密

## 3、SDK安装 

SDK Reference：https://cloud.google.com/sdk/gcloud/reference/config/set

​	1、安装cloud sdk

​		![image-20200402172817666](C:\Users\59103\AppData\Roaming\Typora\typora-user-images\image-20200402172817666.png)

![image-20200402173924626](C:\Users\59103\AppData\Roaming\Typora\typora-user-images\image-20200402173924626.png)

​	2、配置环境变量

		    ./google-cloud-sdk/install.sh

![image-20200402174142553](C:\Users\59103\AppData\Roaming\Typora\typora-user-images\image-20200402174142553.png)

​	3、初始化sdk

```
    ./google-cloud-sdk/bin/gcloud init
```

## 4、创建和挂接永久性磁盘

​	![image-20200402175601329](C:\Users\59103\AppData\Roaming\Typora\typora-user-images\image-20200402175601329.png)

ERROR：

 Could not fetch resource:

 - Insufficient Permission: Request had insufficient authentication scope

进行授权：![image-20200402180537862](C:\Users\59103\AppData\Roaming\Typora\typora-user-images\image-20200402180537862.png)