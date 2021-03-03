# 公募基金/理财复现与组合顾问系统（EPC）软件用户手册

[toc]

# 1. 引言

### 1.1 编写目的

本文档旨在为公募基金/理财复现与组合顾问系统（EPC）软件的使用者提供使用说明

### 1.2 项目背景

本项目为2020花旗杯竞赛南京大学“精神小伙”团队软件部分的产品，供演示使用

## 2. 软件概述

本软件能为银行客户经理提供客户咨询分析服务，为他的客户提供投资历史复现与比较复现服务，为其提供用户追踪表功能，进而为其推销公募基金和理财产品提供方便，同时提供投资组合顾问服务。

本软件能为个人投资者提供投资组合顾问，在不同风险等级下提供基金投资组合推荐服务。

本软件能为银行网点的分析人员提供系统性的分析报告服务。

## 3. 运行环境

### 3.1 硬件

常见现代通用计算机即可

### 3.2 支持软件

- python运行环境，版本3.0以上，并需要flask库相关运行环境
- NodeJS运行环境，最新稳定版本即可，需要使用npm安装相关依赖
- Windows7及以上版本
- Chrome或EDGE等主流浏览器

## 4. 使用说明

### 4.1 启动

- 运行app.py文件

- 在前端项目位置启动终端，运行npm run serve启动vue框架

### 4.2 实际使用

#### 4.2.1 登录、注册

填写用户名字段和密码字段，点击登录按钮即可完成登录流程

填写用户名字段和密码字段、选择用户类型，点击注册按钮即可完成注册流程

![image-20210303105809439](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20210303105809439.png)

#### 4.2.2 选择用户角色

在银行客户经理、个人投资者、银行网点分析人员三个选项中选择，点击进入

![image-20201027102428060](C:%5CUsers%5CDaiqj%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201027102428060.png)

#### 4.2.3 银行客户经理

- ##### 4.2.3.1 投资记录上传

  选择基金、理财选项后在上传模块上传用户的买入记录和赎回记录

  点击确认开始计算复现

  ![image-20210225143216546](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20210225143216546.png)

- ##### 4.2.3.2 投资历史复现

  根据用户上传的投资历史记录生成投资历史记录

  若为基金类型，红线为用户历史收益曲线，蓝线为沪深三百指数曲线

  ![image-20201027103335771](C:%5CUsers%5CDaiqj%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201027103335771.png)

  若为理财类型，蓝线为理财产品收益曲线即用户历史收益曲线

  ![image-20201027112246743](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112246743.png)

- ##### 4.2.3.3 比较复现

  根据用户选择的不同风险等级展示在对应等级下投资组合推荐的收益曲线与用户历史收益曲线（以某用户C的基金投资为例），红线为用户历史收益曲线，蓝线为对应风险投资组合的收益曲线。可以在高中低风险情况下进行推荐的投资组合与用户投资历史的收益情况比较，显示出推荐的投资组合的优越性![image-20201027111726786](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027111726786.png)
  
  ![image-20201027111715706](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027111715706.png)
  
  ![image-20201027111651231](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027111651231.png)
  
- ##### 4.2.3.4 投资组合推荐
  
  根据选择的高中低风险提供不同风险等级的投资组合推荐，并附有用户案例供参考
  
  
  
  ![image-20201027112358360](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112358360.png)
  
  ![image-20201027112408628](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112408628.png)
  
- ##### 4.2.3.5 推荐历史查看
  
  可选择查看历史上某月份所对应的投资组合推荐情况，选择风险等级并在日期选择栏中选择对应月份点击查看按钮即可查看
  
  ![image-20201027112637500](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112637500.png)
  
  ![image-20201027112728955](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112728955.png)
  
- ##### 4.2.3.6 客户追踪表

  为理财经理用户提供客户追踪表，为其定期联络客户提供方便
  
  ![image-20210225143050954](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20210225143050954.png)
  
  ![image-20210225143142472](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20210225143142472.png)

#### 4.2.4 个人投资者

- ##### 4.2.4.1 投资组合推荐
  
  根据选择的高中低风险提供不同风险等级的投资组合推荐，同时以案例的形式展示该风险等级的投资组合的投资表现
  
  ![image-20201027112903360](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112903360.png)
  
  ![image-20201027112914969](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112914969.png)
  
  ![image-20201027112923788](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112923788.png)
  
- ##### 4.2.4.2 推荐历史查看
  
  可选择查看历史上某月份所对应的投资组合推荐情况，选择风险等级并在日期选择栏中选择对应月份点击查看按钮即可查看
  
  ![image-20201027112637500](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112637500.png) 
  
  ![image-20201027113305770](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027113305770.png)
  
  ![image-20201027113340853](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027113340853.png)

#### 4.2.3 银行网点分析人员

- ##### 4.2.3.1 查看投资组合推荐详情

  点击组合详情分析选项即可在新标签页打开投资组合推荐详情pdf，并可通过浏览器进行下载（以下为部分内容展示）

![image-20201027113406898](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027113406898.png)

![image-20201027113609111](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027113609111.png)

