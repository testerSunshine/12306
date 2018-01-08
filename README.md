### 12306

- python版本支持
  - 2.7
- 依赖库
  - 依赖打码兔 需要去打码兔注册账号，打码兔账号地址：http://www.dama2.com，一般充值1元就够用了
  - 项目依赖包 requirements.txt
  - 安装方法 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

- 项目开始
  - 修改config/ticket_config.yaml文件，按照提示更改自己想要的信息
  - 运行根目录run.py，即可开始

- 项目思路


- 项目声明：
  - 本软件只供学习交流使用，务作为商业用途，作者qq 931128603

- 2017.5.13跟新
1. 增加登陆错误判断（密码错误&ip校验）
2. 修改queryOrderWaitTime，校验orderId字段bug，校验msg字段bug，校验messagesbug
3. 修改checkQueueOrder  校验 data 字段的列表推导式bug
4. 增加代理ip方法，目前已可以过滤有用ip


- 2018.1.7 号更新
1. 增加自动配置
    ```
    #station_date:出发日期，格式ex：2018-01-06
    #from_station: 始发站
    #to_station: 到达站
    #set_type: 坐席(商务座,二等座,特等座,软卧,硬卧,硬座,无座)
    #is_more_ticket:余票不足是否自动提交
    #select_refresh_interval:刷新间隔时间，1为一秒，0.1为100毫秒，以此类推
    #ticke_peoples: 乘客
    #damatu：打码图账号，用于自动登录
    ```
2. 优化订票流程
3. 支持自动刷票，自动订票

- 2018.1.8 号更新
1. 增加小黑屋功能
2. 修复bug若干
3. 增加多账号同时订票功能
4. 增加按照选定车次筛选购买车次
