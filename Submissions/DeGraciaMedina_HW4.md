## Name: Xenia De Gracia Medina.
### Homework #4
### Date: September 21, 2020.
___
### Grade
3/3 - Nice work! I'm so happy your computer is up and running smoothly!  See instructions in next week assignment for how to include images in your markdown. 

---
### Table of Contents:
1. [ Weekly Forecast](#weekly)
1. [ Seasonal Forecast](#seasonal)
1. [ Assignment Questions](#questions)
1. [ Good News!](#news)

---
<a name="weekly"></a>
### **Weekly forecast**

To forecast the 1st week, I used the average flow of the last 19 days and for the 2nd week forecast, I used the average flow of the last 14 days only.


---
<a name="seasonal"></a>
### **Seasonal Forecast**

For the Seasonal forecast, I continue using the average of 2019.


---
<a name="questions"></a>
### **Assignment questions**

**1. Include discussion of the quantitative analysis that lead to your prediction. This can include any analysis you complete but must include at least two histograms and some quantitative discussion of flow quantiles that helped you make your decision.**

![Histogram](C:/Users/xy_22/Documents/MSc._Hydrology/2020_Fall/599-HAS_Tools/homework-xenidegracia/Submissions/Week4Histogram.png)

- From the histograms I can see that the majority of the flow values are between 50 and 90 cf/s and also between 190 and 2010 cf/s. As this is a dry season, I will maintain my forecast as lower as I can.
There are few values of flow that are over the 500 cf/s.
From the quantiles I can see that the median value is 158 cf/s and my 25% of my values are 62, which is the closest value from my prediction.

**2. Describe the variable flow_data:**
- What is it?
  - It is a **'numpy.ndarray'**.
- What type of values is it composed of?
  - The values  stored within "flow_data" are all **floats**.
- What is the dimension, and total size?
  - The dimension of flow_data is: **2**
  - The total size of flow_data is: **46340**. It means that it has 46340 elements.
  - The shape of the flow_data is: **(11585, 4)**


**3. How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)?**

- Times that the flow was greater than my 1st week prediction = **239**

- Times in % that the daily flow was greater than my 1st week prediction = **25.18 %**


**4. How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage)**

- *For the month of September and before 2000:*

  - Times that the flow was greater than my 1st week prediction Before year 2000 = **132**

  - Times in % that the daily flow was greater than my 1st week prediction Before year 2000 = **66.38 %**

- *For the month of September and after 2010:*

  - Times that the flow was greater than my 1st week prediction After year 2010 = **53**

  - Times in % that the daily flow was greater than my 1st week prediction After year 2010 = **74.92 %**


**5. How does the daily flow generally change from the first half of September to the second?**

- The mean flow of the First Half of September is greater than the mean flow of the Second Half

---
<a name="news"></a>
## **Good News!**
I finally got my new computer and could work on it perfectly! :D Thanks for all your help * - *
