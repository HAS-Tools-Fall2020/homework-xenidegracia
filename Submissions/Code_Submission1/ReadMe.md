## Homework #8: *Final graded script from section 1* :tada: :fireworks:
### Author of the code:  *Xenia De Gracia Medina*.
### Date: *October 19, 2020*.

---
### Table of Content:
- [ Summary](#summary)
- [ Instructions from Xenia :)](#instructions)
- [ Weekly forecast for submission](#weekly)
- [ Regression based Forecast](#regression)
- [ Code review following the rubric](#review)
- [ Extra information (just in case)](#extra)
---

---
<a name="summary"></a>

- A brief summary of the AR model you built and why. Use whatever graphs you find helpful.

The AR model that I built this time, defers from my last code, due to I decided to change the train data to evaluate just the 2019 because it was a dry year too.

- An explanation of how you generated your forecasts and why (i.e. did you use your AR model or not?)

In my code I have two methods to obtain my values. The AR model, and the average of the values of 2019. I decided to use my model values due to the average forecast is not working as I wish it could do.

- A brief summary of what you got out of the peer evaluation. How did you make your script better?

From my peer evaluation I obtain feedback about improving the path of the data, to make it available for everyone that wants to run my code, also on the writing of my code through the use of more cells to facilitate the execution of it.

- Describe the part of your script that you are most proud of and why.
When I could finally get how to use the datetime as an object to locate the data that I wanted to process. Also when I got the 16 values of my average and AR forecasting. The fact that now the flake8 corrects me less than at the beginning of the course.

---
<a name="weekly"></a>
>### **AVERAGE Weekly forecast**

- Week 1: 62.66
- Week 2: 65.35

---
<a name="regression"></a>
>### **Regression based Forecast for submission**

- Week 1: 46.92
- Week 2: 62.32

---

Week # |  Start Date  | Flow
 ----- | ------------ | ----- |
Week 1 | 2020-08-22   | 37.59
Week 2 | 2020-08-30   | 0.09 ??
Week 3 | 2020-09-06   | 12.46 ??
Week 4 | 2020-09-13   |  59.69
Week 5 | 2020-09-20   |  38.61
Week 6 | 2020-09-27   |  43.88
Week 7 | 2020-10-04   |  63.54
Week 8 | 2020-10-11   |  87.46
Week 9 | 2020-10-18   |  103.68
Week 10 | 2020-10-25  |  89.89
Week 11 | 2020-11-01  |  104.69
Week 12 | 2020-11-08  |  136.92
Week 13 | 2020-11-15  |  191.45
Week 14 | 2020-11-22  |  203.61
Week 15 | 2020-11-29  |  238.07
Week 16 | 2020-12-06  |  304.97


---
<a name="instructions"></a>
>### **Instructions from the author :)**
*Hi there! Here are the instructions to run my code in your own computer:*
1. Clone my repo into your computer. I posted the link in here for your easy access: [homework-xenidegracia](https://github.com/HAS-Tools-Fall2020/homework-xenidegracia)
2. Please download the data from: [USGS Station 09506000 VERDE RIVER](https://waterdata.usgs.gov/nwis/dv?referred_module=sw&site_no=09506000). Since January 1st, 1989, until today.
3. Save it as **".txt"** format, with the name of the current course week: **"streamflow_week8.txt"**, in the **"data"** folder inside the repository: [homework-xenidegracia/data](https://github.com/HAS-Tools-Fall2020/homework-xenidegracia/tree/master/data).
4. Inside the code: Update the path of the data saved now in your computer to enable the code running.
5. Run the code and get the weekly forecasting values.



<a name="review"></a>
>### **Code review following the rubric**
*Special space for the code review.*
(Adapted from Kyle Mandli [Intro to Numerical Methods](https://github.com/mandli/intro-numerical-methods))
![](assets/ReadMe-ff0ecab3.png)

- Readability:   
- Style:         
- Code awesome:  




<a name="extra"></a>
>### **Extra information (just in case)**
The final equation for the model:
  - **y = -59.91 + 2.03X**

Coefficient of determination:
  - **0.76**

### **Plot #1.**
![]()



### **Plot #2.**
![](assets/ReadMe-28291ce1.png)

### **Plot #3.**
![](assets/ReadMe-36891864.png)

### **Plot #4.**
![](assets/ReadMe-8525de0f.png)

### **Plot #5.**
![](assets/ReadMe-25cf19df.png)

### **Plot #6.**
