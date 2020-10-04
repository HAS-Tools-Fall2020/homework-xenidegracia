# %%
print("Hello world")
Panama_precip_in=[0.50,0.60,0.70]
print(Panama_precip_in)
# %%
print
print("The length of the Precipitation list is:", len(Panama_precip_in))

# EXERCISE 1: 
#1a.  Create a 3X3 matrix with values ranging from 2-10  
#1.b  Make a matrix with all of the even values from 2-32
# 1.c Make a matrix with all of the even values from 2-32
# But this time have the values arrange along columns rather than rows

# %%

# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

a = np.array([(2,3,4),
(5,6,7),
(8,9,10)
])

print(a)




# %%
Matrix1b = [[:2,0]
].to_numpy()

# %%
xc=np.reshape(np.arange(2,33,2),(4,4), order='F')
xd=np.arange(2,33,2).reshape(4,4, order='F')

# %%
# WORKING ON THIS
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Matrix1a = np.arange(2,11).reshape(3,3)
print(Matrix1a)

Matrix1b = np.arange(2,33,2).reshape(-1,4)
print(Matrix1b)

Matrix1c= Matrix1b.T
print(Matrix1c)

Matrix1c = np.arange(2,33,2).reshape(-1,4,order='F')
print(Matrix1c)

# %%
# BONUS
MatrixD = np.arange(2,5).reshape(3,1)
print("MatrixD")
print(MatrixD)
MatrixDT = MatrixD.T
print("MatrixDT")
print(MatrixDT)
MatrixE = np.arange(5,8).reshape(1,3)
print("MatrixE")
print (MatrixE)
MatrixET = MatrixE.T
print("MatrixET")
print(MatrixET)

MatrixD+

# %%
Matrix1b = [[:2,0]
].to_numpy()

np.full((2,3),8) - 2x3 array with all values 8

# BONUS:
# Create the same 3x3 matrix with value ranging from 2-10 as you did 
# in part a but this time do so by combining one 3X1 matrix and one 1X3 matrix

MatrixBonus3x1 = np.array(arange(2,11,1).reshape(3,3)
MatrixBonus3x1 = [[:2,0]
].to_numpy()



# %%
import matplotlib.pyplot as plt
# Import pandas with alias pd
import pandas as pd
avg_monthly_precip = pd.DataFrame(columns=["month", "precip_in"],
data=[["Jan", 0.70],  ["Feb", 0.75],  ["Mar", 1.85],  ["Apr", 2.93],["May", 3.05],  ["June", 2.02], ["July", 1.93], ["Aug", 1.62], ["Sept", 1.84], ["Oct", 1.31], ["Nov", 1.39],  ["Dec", 0.84]
])
# Notice the nicely formatted output without use of print
avg_monthly_precip

# %%
f, ax = plt.subplots()
avg_monthly_precip.plot(x="month",
                        y="precip_in",
                        title="Plot of Pandas Data Frame using Pandas .plot",
                        ax=ax)
plt.show()
# %%

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#1. Get the largest integer that is less than or equal to the division
# of the inputs x1 and x2 where x1 is all the integers from 1-10 and x2=1.3



# 2. given an array x1=[0, 4, 37,17] and a second array with the values
# x2=[1.2, 3, 4.6, 7] return x1/x2 rounded to two decimal places

x1=np.array([0, 4, 37,17])
print (x1)
x2=np.array([1.2, 3, 4.6, 7])
print (x2)
x3=x1/x2
print(np.ceil(x3))


# 3. Create a 10 by 100 matrix with 1000 random numbers and report the 
# average and standard deviation across the entire matrix and 
# for each of the 10 rows. Round your answer to  two decimal places

# Hints: np.random, np.round, np.mean, np.std
# %%
data = np.ones((7,3))
data_frame = pd.DataFrame(data, 
                columns = ['data1', 'data2', 'data3'],
                index=['a','b','c','d','e','f','g'])
A) Change the values for all of the vowel rows to 3
B) multiply the first 4 rows by 7
C) Make the dataframe into a checkerboard  of 0's and 1's using loc
# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %%
# A) Change the values for all of the vowel rows to 3
data = np.ones((7,3))
data_frame = pd.DataFrame(data, 
                columns = ['data1', 'data2', 'data3'],
                index=['a','b','c','d','e','f','g']
                )
print(data_frame)
data_frame.loc[['a','e']]=3

# %%

# B) multiply the first 4 rows by 7



# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data_frame = pd.DataFrame([[1, np.nan, 2],
                            [2, 3, 5],
                            [np.nan, 4, 6]])

# %%
# 1) Use the function fill.na to fill the na values with 999
data_frame9 = data_frame.fillna(999)
# %%
data_frame9[data_frame9==999]=np.nan

# %%

2) Turn the 999 values back to nas. See how many different ways you can do this
data_frame=data_frame.iloc[:4,]*7
print(data_frame)

# C) Make the dataframe into a checkerboard  of 0's and 1's using loc



# %%
