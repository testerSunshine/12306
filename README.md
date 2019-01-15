#### 12306 购票小助手

- python版本支持
  - 2.7.10 - 2.7.15
- 依赖库
  - 依赖若快 若快注册地址：http://www.ruokuai.com/client/index?6726 推荐用若快，打码兔平台已经关闭
  - 项目依赖包 requirements.txt
  - 安装方法-Windows: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
  - 安装方法-Linux:
      - root用户(避免多python环境产生问题): python2 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
      - 非root用户（避免安装和运行时使用了不同环境）: sudo python2 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

- 项目使用说明
  - 需要配置邮箱，可以配置可以不配置，配置邮箱的格式在yaml里面可以看到ex
  - 提交订单验证码哪里依赖打码兔，所以如果是订票遇到验证码的时候，没有打码兔是过不了的，不推荐手动，手动太慢
  - 配置yaml文件的时候，需注意空格和遵循yaml语法格式

- 项目开始
  - 服务器启动:
      - 修改config/ticket_config.yaml文件，按照提示更改自己想要的信息
      - 运行根目录sudo python run.py，即可开始
        - 由于新增对时功能，请务必用sudo，sudo，sudo 执行，否则会报权限错误，windows打开ide或者cmd请用管理员身份执行python run.py，不需要加sudo
  - 如果你的服务器安装了docker与docker-compose, 那么就可以通过`docker-compose`进行启动,`docker.sh`脚本对此进行了封装，可以通过如下命令进行启动
      - 1、`sudo ./docker.sh run` #创建一个镜像并启动容器，如果镜像已经创建过了会直接启动容器。
      - 2、`sudo ./docker.sh reload` #修改配置文件后，通过此名命令可重新加载容器运行
      - 3、`sudo ./docker.sh rm` #删除容器
      - 4、`sudo ./docker.sh drun` #后台运行容器
      - 5、`sudo ./docker.sh logs` #在后台运行时，通过此命令查看运行的内容
      - 注: 若只有docker没有docker-compose. 可通过`pip install docker-compose`进行下载
  - ~~如果你的服务器安装了docker，那么就可以docker启动~~
      - 1、~~docker build -t dockerticket .~~
      - 2、~~docker run dockerticket  python run.py &~~
      - 3、~~本来是可以直接Dockerfile启动的，不知道为毛启动不了，如果有大佬看到问题所在，欢迎提出~~
      - 4、~~docker run -d --name 12306-ticket dockerticket~~

	

- 目录对应说明
  - agency - cdn代理
  - config - 项目配置
  - damatuCode - 打码兔接口
  - init - 项目主运行目录
  - myException - 异常
  - myUrllib - urllib库

- 思路图
     ![image](https://github.com/testerSunshine/12306/blob/master/uml/uml.png)

- 项目声明：
  - 本软件只供学习交流使用，务作为商业用途，交流群号
    - 1群：286271084(已满)
    - 2群：649992274(已满)
    - 3群：632501142(已满)
    - 4群: 606340519(已满)
    - 5群: 948526733(未满)
    - 6群: 444101020(未满)
    - 7群: 660689659(未满)
  - 请不要重复加群，一个群就可以了，把机会留给更多人
  - **进群先看公告！！！进群先看公告！！！进群先看公告！！！ 重要的事情说三遍**
  - 能为你抢到一张回家的票，是我最大的心愿

- 成功log，如果是购票失败的，请带上失败的log给我，我尽力帮你调，也可加群一起交流，程序只是加速买票的过程，并不一定能买到票
    ```
    正在第355次查询  乘车日期: 2018-02-12  车次G4741,G2365,G1371,G1377,G1329 查询无票  代理设置 无  总耗时429ms
    车次: G4741 始发车站: 上海 终点站: 邵阳 二等座:有
    正在尝试提交订票...
    尝试提交订单...
    出票成功
    排队成功, 当前余票还剩余: 359 张
    正在使用自动识别验证码功能
    验证码通过,正在提交订单
    提交订单成功！
    排队等待时间预计还剩 -12 ms
    排队等待时间预计还剩 -6 ms
    排队等待时间预计还剩 -7 ms
    排队等待时间预计还剩 -4 ms
    排队等待时间预计还剩 -4 ms
    恭喜您订票成功，订单号为：EB52743573, 请立即打开浏览器登录12306，访问‘未完成订单’，在30分钟内完成支付！
    ```
- 使用帮助：
    - 测试邮箱是否可用 [邮箱配置问题看issues](https://github.com/testerSunshine/12306/issues/107)
    - 学生票issues [学生票修改](https://github.com/testerSunshine/12306/issues/47)
    - 依赖安装不对的问题（ImportError）[requirements.txt问题](https://github.com/testerSunshine/12306/issues/91)
    - 若快豆子疑问 [点我](https://github.com/testerSunshine/12306/issues/67)
    - IOError: 【Errno 0】 Error 问题 [点我](https://github.com/testerSunshine/12306/issues/159)

    - 测试下单接口是否可用，有两个下单接口，随便用哪个都ok
    - 如果下载验证码过期或者下载失败的问题，应该是12306封ip的策略，多重试几次，12306现在封服务器(阿里云和腾讯云)ip比较严重，尽量不要放在服务器里面
    - 目前12306对服务器ip比较敏感，大家还是在自己家里挂着吧
    - 如果想使用此项目的gui版本，请加群，目前只有mac版本
- 感谢一下小伙伴对本项目提供的帮助
    - @sun7127@126.com
    - @ 才
    - @MonsterTan
    - 以及所有为此项目提供pr的同学
- [更新日志](Update.md)

- 如果觉得项目还不错，可以考虑打赏一波
    -
    ![image](https://github.com/testerSunshine/12306/blob/master/uml/wx.jpeg?imageMogr2/auto-orient/strip)
    ![image](https://github.com/testerSunshine/12306/blob/master/uml/zfb.jpeg?imageMogr2/auto-orient/strip)
