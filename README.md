## 金陵医派五运六气

本程序主要是为了五运六气金陵医派微信小程序提供后端数据服务，扫码体验

![Alt text](fig/xcx.png)

### 原理

运气结构图：

司天之气——

客    气——

大    运——

主    气——

在泉之气——

 

1.大运的计算规则：

（1） 每年的岁运起始，岁（中）运太过之年，起于大寒前13日，岁（中）运不及之年，起于大寒后13日。

（2）甲己年——土运（太阴湿土），乙庚——金运（阳明燥金），丙辛——水运（太阳寒水），丁壬——木运（厥阴风木），戊癸——火运（少阳相火）

（3）甲、庚、丙、壬、戊——太过之年；乙、丁、己、辛、癸——不及之年。

（4）一个大运管的时间是一年。

 

2.司天的计算规则：

| **十二支**       | **子午** | **丑未** | **寅申** | **卯酉** | **辰戌** | **巳亥** |
| ---------------- | -------- | -------- | -------- | -------- | -------- | -------- |
| **三阴三阳**     | **少阴** | **太阴** | **少阳** | **阳明** | **太阳** | **厥阴** |
| **六气（司天）** | **君火** | **湿土** | **相火** | **燥金** | **寒水** | **风木** |

 

3.六个气的划分

一年分为六个时段：

  初之气：大寒到春分

  二之气：春分到小满

  三之气：小满到大暑

  四之气：大暑到秋分

  五之气：秋分到小雪

  终之气：小雪到大寒

 

（1）主气：厥阴风木（初）——少阴君火（二）——少阳相火（三）——太阴湿土（四）——阳明燥金（五）——太阳寒水（终）

（2）客气顺序：

——厥阴风木——少阴君火——太阴湿土——少阳相火——阳明燥金——太阳寒水——厥阴风木       

（3）客气的三之气与司天之气相同，然后根据以上顺序，可以推导出其余的5个气。

（4）在泉之气与客气的终之气相同。

### 编译运行

创建python3.9的虚拟环境

```conda create -n great_contri python=3.9```

```conda activate great_contri```

安装包

```pip install cnlunar```

```pip install flask```

### optional

修改flask_demo.py文件中第25行代码，pem和key文件为自己的文件

```app.run(host='0.0.0.0', port=8080, ssl_context=('8840426_zhongyi.wesky.online.pem', '8840426_zhongyi.wesky.online.key'))```

如果不需要使用https，将25行代码改为

```app.run(host='0.0.0.0', port=8080)```

考虑到微信小程序必须使用8080端口，所以我们必须使用阿里云。但是阿里云上部署flask，会出现莫名的无响应的问题，无法解决。所以我们使用了nginx在阿里云（zhongyi.wesky.online）8080端口上做SSL反向代理，进入我们另外一台主机(ltcmf.ddns.net)5000端口上，对外链接访问方式保持不变，依旧是https://zhongyi.wesky.online:8080，实际上他确是在访问http://ltcmf.ddns.net:5000的服务。部署方式如下：

```sudo apt-get install nginx
sudo apt-get install nginx
```

修改/etc/nginx/sites-enabled/default文件并添加下列代码

```
server {
        listen 8080;
#       listen [::]:80;
#
        server_name  zhongyi.wesky.online;
        ssl on;
        ssl_certificate  cert/8840426_zhongyi.wesky.online.pem;
        ssl_certificate_key  cert/8840426_zhongyi.wesky.online.key;
        ssl_session_timeout  5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4; #使用此加密套件。
         ssl_protocols TLSv1 TLSv1.1 TLSv1.2; #使用该协议进行配置。
         ssl_prefer_server_ciphers on;
#
#       root /var/www/example.com;
#       index index.html;
#
        location / {
#               try_files $uri $uri/ =404;
            proxy_pass  http://ltcmf.ddns.net:5000;
        }
}
```

 重启nginx服务即可

```sudo service nginx restart
sudo service nginx restart
```



### 服务测试链接

https://zhongyi.wesky.online:8080/date?date=2022-11-15

该链接可以测试到五运六气的json数据，形式如下

```
[{
"gongli": "2022-11-15", 
"nongli": "二零二二十月大廿二", 
"ganzhi": "壬寅 辛亥 壬申", 
"qi_shunxu": "终之气", 
"jieqi": "小雪", 
"sitian": "少阳相火（17）", 
"keqi": "厥阴风木（410）", 
"dayun": "厥阴风木（410）^", 
"zhuqi": "太阳寒水（39）", 
"zaiquan": "厥阴风木（410）", 
"dong": "dong3", 
"nan": "nan1", 
"zhong": "zhong0", 
"xi": "xi0", 
"bei": "bei1"
}]
```

