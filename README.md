
Task 1

started off with extracting the data from the excel file using pandas,cleaned up the nan values,the data we imported was pressure data, so i converted that to altidude data using the basic conversion formula(ignoring temp change) then i did a basic plot of this data using matplotlib, the data was not as smooth as one would expect it to be as there is noise due to multiple factors, so i added a kalman filter to smoothen out the data and make it a bit better, then using this data you can find velocity as we know how frequently we get data from the system. The this data was also filtered using a kalman filter.
After i had all my data all i had to do was plot it using the lib.

Task 2 

I started by learning how to connect the force sensor onto my circuit and adding 3 LEDs for use later (ascending,descending,apogee) and adding the piezo,
then i set the pin modes and wrote the code, i used a kalman filter here, but it wasnt really needed as there was no measurement noise, but on a real force sensor it would be important (the filter may kinda be useful here as you make entries with a manual bar which is not really accurate), then after we start getting inputs from our force sensor we use the basic logic: if force due to pressure increases, it means our altitude is decreasin and vise-versa
