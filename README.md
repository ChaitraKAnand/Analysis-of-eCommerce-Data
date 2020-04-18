# Analysis-of-eCommerce-Data
This repository consists of work done on analysis of eCommerce(Best Buy) data using Hadoop Components

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
* [Proposed Pipeline](#Proposed Pipeline)




<!-- ABOUT THE PROJECT -->
## About The Project

In the last few years, with the advancement of technologies and digitization, the amount of data generated rapidly increased from Terabytes to Zettabytes and by 2025, it is predicted there would a big and tremendous volume of data collections and that would be nearly 163 zettabytes. To handle this huge volume of data and process them to draw meaningful insights technologies like Hadoop and its ecosystem come to rescue.

To explore on big data technologies – Hadoop and its ecosystem, we opted to work on e-commerce data (Best Buy store website).Data collected includes information on products such as Cell phones, Desktops and Laptops. We aim to store and analyse this data to draw useful insights such as compare price of different cell phones along with the carrier. On the same lines, compare cost of laptops across different brands. Customer top rated products and so on.


### Built With
Below are the technologies used to accomplish this project

1. Two node cluster of Google compute engine - CentOS 6(each 8vCPU's, 32GB RAM)
2. HDP -2.6 installed on 2 node cluster using Ambari
3. MongoDB - 3.2

<!-- GETTING STARTED -->
## Getting Started

Refer to the video to create Google cloud account and build two node cluster compute engine and install HDP -2.6 on it
https://www.youtube.com/watch?v=tCxY8UwcPXs&t=12s

To install MongoDB refer to "https://github.com/nikunjness/mongo-ambari" 

## Proposed pipeline

![BestBuy_Pipeline.PNG](attachment:BestBuy_Pipeline.PNG)

