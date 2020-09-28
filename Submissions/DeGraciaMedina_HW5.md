
# **Xenia has its Markdown Free Week** (^-^)
## *P.D. She started to work on it, until she remembered, so the markdown is incomplete.*
---
---
## Name: Xenia De Gracia Medina.
### Homework #4
### Date: September 21, 2020.


---
### Table of Contents:
- [ Weekly Forecast](#weekly)
- [ Seasonal Forecast](#seasonal)
- [ Question 1](#Q1)
- [ Question 2](#Q2)
- [ Question 3](#Q3)
- [ Question 4](#Q4)
- [ Question 5](#Q5)

---
<a name="weekly"></a>
>### **Weekly forecast**

*To forecast the 1st week, I used the average flow of the last 21 days and for the 2nd week forecast, I used the average flow of the last 14 days only.*


---
<a name="seasonal"></a>
>### **Seasonal Forecast**

*For the Seasonal forecast, I continue using the average of 2019.*


---
>### **Assignment questions**

In addition to providing a summary of the forecast values you picked and why include the following analysis in your homework submission. Note that questions 3-5 are the same as last weeks questions, however this time you are expected to calculate your answer using the numpy array rather than lists.

<a name="Q1"></a>
1. Provide a summary of the data frames properties.
  - What are the column names?
  - What is its index?
  - What data types do each of the columns have?

| # | Column | Non-Null Count | Dtype |
|--- | ----- | -------------- | ----- | 
 0 | agency_cd| 11592 non-null | object
 1 | site_no |  11592 non-null | int64  
 2 | datetime|  11592 non-null | object 
 3 | flow |     11592 non-null | float64
 4 | code |     11592 non-null | object 
 5 | year |     11592 non-null | int32  
 6 | month|     11592 non-null | int32  
 7 | day  |     11592 non-null | int32

<a name="Q2"></a>
2. Provide a summary of the flow column including the min, mean, max, standard deviation and quantiles.

Summary | Number
------| --------
count | 11592.00
mean  |   345.63
std   |  1410.83
min   |    19.00
25%   |    93.70
50%   |   158.00
75%   |   216.00
max   | 63400.00

<a name="Q3"></a>
3. Provide the same information but on a monthly basis. (Note: you should be able to do this with one or two lines of code)

<a name="Q4"></a>
4. Provide a table with the 5 highest and 5 lowest flow
values for  the period of record. Include the date, month and flow values in your summary.

<a name="Q5"></a>
5.  Find the highest and lowest flow  values for every month of the year (i.e. you will find 12 maxes and 12 mins) and report back what year these occurred in.

<a name="Q6"></a>
6. Provide a list of historical dates with flows that are within 10% of your week 1 forecast value. If there are none than increase the %10 window until you have at least one other  value and report the date and the new window you used
