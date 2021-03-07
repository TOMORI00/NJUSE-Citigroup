# 公募基金/理财复现与组合顾问系统（EPC）软件用户手册

[toc]

# 1. Introduction

### 1.1 Document Purposes

This document is intended to provide instructions for users of the Public Funds / Wealth Management Recurring and Portfolio Advisor (EPC) software

### 1.2 Project background

This project is a product of the software part of the "Spirit Guy" team of Nanjing University in the 2020 Citi Cup competition, for demonstration purposes.

## 2. Software Overview

This software can provide customer consultation and analysis services for bank account managers, investment history recurrence and comparison recurrence services for his customers, user tracking table functions for them, which in turn facilitate their marketing of public funds and financial products, and portfolio advisory services.

The software can provide portfolio advisory services for individual investors, providing fund portfolio recommendation services under different risk levels.

This software can provide systematic analysis report service for analysts in bank branches.

## 3. Running Environment

### 3.1 Hardware

Common modern general-purpose computers

### 3.2 Supporting Software

- Python runtime environment: version 3.0 or above, and requires flask library related runtime environment
- Node.js runtime environment: the latest stable version，also need to use npm to install dependencies
- Windows7 and above
- Major broser such as Chorme or Edge

## 4. Using Instructions

### 4.1 Initiate

- run app.py
- start the terminal in the front-end project location and run npm run serve to start the vue framework

### 4.2 Using

#### 4.2.1 Login, Signup

Fill in the user name field and password field, and click the login button to complete the login process

Fill in the user name field and password field, select the user type, and click the Register button to complete the registration process

![image-20210303105809439](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20210303105809439.png)

#### 4.2.2 Choosing User

Select from the three options of bank account manager, individual investor, and bank branch analyst, and click to enter

![image-20201027102428060](C:%5CUsers%5CDaiqj%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201027102428060.png)

#### 4.2.3 Bank Account Manager

- ##### 4.2.3.1 Investment Record Upload

  Select the fund and wealth management options and upload the user's purchase and redemption records in the upload module

  Click on Confirm to start calculating recurrence

  ![image-20210225143216546](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20210225143216546.png)

- ##### 4.2.3.2 Investment History Replay

  Generate investment history based on the investment history uploaded by users

  If it is a fund type, the red line is the user's historical return curve, and the blue line is the CSI 300 index curve

  ![image-20201027103335771](C:%5CUsers%5CDaiqj%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201027103335771.png)

  If it is a financial type, the blue line is the financial product return curve that is the user's historical return curve

  ![image-20201027112246743](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112246743.png)

- ##### 4.2.3.3 Comparative Reproduction

  According to the different risk levels selected by the user, the recommended return curve of the portfolio under the corresponding level and the user's historical return curve are displayed (take the fund investment of a user C as an example), the red line is the user's historical return curve and the blue line is the return curve of the corresponding risk portfolio. The recommended portfolio can be compared with the user's investment history in the case of high, medium and low risks, showing the superiority of the recommended portfolio
  
  ![image-20201027111726786](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027111726786.png)
  
  ![image-20201027111715706](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027111715706.png)
  
  ![image-20201027111651231](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027111651231.png)
  
- ##### 4.2.3.4 Portfolio Recommendations
  
  Provide portfolio recommendations with different risk levels according to the selected high, medium and low risks, with user cases for reference
  
  ![image-20201027112358360](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112358360.png)
  
  ![image-20201027112408628](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112408628.png)
  
- ##### 4.2.3.5 Recommended History View
  
  Users can choose to view the portfolio recommendations for a particular month in history by selecting the risk level and choosing the corresponding month in the date selection field and clicking the View button.
  
  ![image-20201027112637500](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112637500.png)
  
  ![image-20201027112728955](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112728955.png)
  
- ##### 4.2.3.6 Customer Tracking Form

  Provide client tracking forms for money manager users to facilitate regular contact with their clients
  
  ![image-20210225143050954](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20210225143050954.png)
  
  ![image-20210225143142472](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20210225143142472.png)

#### 4.2.4 Individual Investors

- ##### 4.2.4.1 Portfolio Recommendations
  
  Provide portfolio recommendations for different risk levels according to the selected high, medium and low risks, and also show the investment performance of the portfolio for that risk level in the form of case studies
  
  ![image-20201027112903360](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112903360.png)
  
  ![image-20201027112914969](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112914969.png)
  
  ![image-20201027112923788](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112923788.png)
  
- ##### 4.2.4.2 Recommended History View
  
  Users can choose to view the portfolio recommendations for a particular month in history by selecting the risk level and choosing the corresponding month in the date selection field and clicking the View button.
  
  ![image-20201027112637500](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027112637500.png) 
  
  ![image-20201027113305770](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027113305770.png)
  
  ![image-20201027113340853](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027113340853.png)

#### 4.2.3 Bank branch analysts

- ##### 4.2.3.1 View portfolio recommendation details

  Click on the portfolio details analysis option to open the portfolio recommendation details pdf in a new tab and download it via your browser (some of the contents are shown below)

![image-20201027113406898](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027113406898.png)

![image-20201027113609111](C:/Users/Daiqj/AppData/Roaming/Typora/typora-user-images/image-20201027113609111.png)

