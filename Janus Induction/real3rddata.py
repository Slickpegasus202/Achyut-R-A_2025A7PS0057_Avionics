import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation

df = pd.read_excel("Raw_Test_Flight_Data_25(2).xlsx",header=0) #reading data from excel file and saving as pandas dataframe


flightdata = pd.to_numeric(df.iloc[:,0],errors="coerce") #first it takes the all rows(entries) from first column, converts them to 
                                                          #int/float and invalid datas are converted to nan

flightdata = flightdata.interpolate() #basically removes the nan datas and fills in the empty spaces by joining the points with a straight
                                       #line whenever a nan shows up (eg if data 2,3,4 are invalid, then 1 and 5 are joined by a linear line)
flightdata = flightdata.tolist() #converts the pandas dataframe to a list for easy use
kalman = []
realvel = []
velocity = []
filtvelocity = []

#setup for simple 1D kalman filter, which helps us reduce noise in our data that can be caused due to a variety of reasons
P = 0.001  #estimate error covariance (the p we are settting now is just for the initial state, as p will be automatically updated later on)
Q= 1 #process noise covariance
R= 3 #measurement noise covariance (a measure of how accurate your sensor is)

a = (44330*(1-pow((flightdata[0]/101325),(1/5.255))))  #taking initial pressure as my ground level pressure


for i in range(0,len(flightdata)):
  
   flightdata[i] = (44330*(1-pow((flightdata[i]/101325),(1/5.255))))-a #simple height calculation with adjustment to get actual height

   
x = flightdata[0] #we are going to append x into the array names kalman, this is us initializing the first prediction,
                  # we are just keeping it as our measure first value

for c in flightdata : 
    P = P+Q   #p is changing after every cycle

    K=P/(P+R) 
    x = (1-K)*x + K*c

    #the first line is to calculate the kalman gain,K note that the higher the value of R(measurement noise), lower the vale of K
    #the second line predicts our estimate based on our last estimate and our current measurement. weighing based on value of k (basically by how high R is)

    P = (1-K)*P  #updating p, again based on how much measurement noise there is 
    kalman.append(x)
    
#simple velocity calc
for i in range(0,len(kalman)-2):
    velocity.append((-kalman[i]+kalman[i+1])) #vel from filtered altitude data
   

#another 1D kalman filter to filter our vel
p1 = 0.001
q1 = 0.75
r1 = 1.5
x1 = velocity[0]

for i in velocity:

    
    p1 = p1+q1

    k1 = p1/(p1+r1)
    p1 = p1*(1-k1)
    x1 = x1*(1-k1)+k1*i

    filtvelocity.append(x1)
   
#plotting the graphs

fig1, ax1 = plt.subplots(figsize=(12,6))  #creating a figure and the actual plot

line1, line2 = ax1.plot(flightdata,'o-',kalman, 'o-') #plotting onto our plot object
line1.set_label("Original altitude data")
line2.set_label("Filtered data")

#setting up the graph to make it look readable

ax1.set_title("Altitude V/S Time")
ax1.set_xlabel("Time")
ax1.set_ylabel("Altitude")
ax1.legend()
ax1.grid(True)
fig1.tight_layout()


#initializing the lines to empty x,y coordinates
def init1():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2

#we need to basically make it so that the graph appears to update every second, we are given each data point is after 1 sec interval
#we just need to add one new data point every time into out update function (the interval can be dealt with later)  


def update1(time):
    x = list(range(time+1))
    y1 = flightdata[:time+1]
    y2 = kalman[:time+1]
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2

time = len(flightdata) #setting the total number of frames the anim shows


ani1 = animation.FuncAnimation(
    fig1, update1, frames=time, init_func=init1, interval=100, repeat = False)  #sets which fig is to be shown, what rate it updates at
#the  initialization function, the update function and the time between each data point being shown, repeat = false means the whole graph doesnt restart when anim ends.
plt.show()  #shows the plot



#same thing for the other graph
fig2,ax2 = plt.subplots(figsize = (12,6))


line3, line4 = ax2.plot(velocity, 'o-', filtvelocity, 'o-')
line3.set_label("raw velocity data")
line4.set_label("filtered velocity data")   


ax2.set_title("Velocity V/S Time")
ax2.set_xlabel("Time")
ax2.set_ylabel("Velocity")
ax2.legend()
ax2.grid(True)
fig2.tight_layout()

def init2():
    line3.set_data([],[])
    line4.set_data([],[])
    return line3,line4  

def update2(frame):
    x = list(range(frame+1))
    y1 = velocity[:frame+1]
    y2 = filtvelocity[:frame+1]
    line3.set_data(x, y1)
    line4.set_data(x, y2)
    return line3, line4

frames = len(velocity)
ani1 = animation.FuncAnimation(fig2, update2, frames=frames, init_func=init2, interval=100, blit=True, repeat=False)
plt.show()

#Line 1 and line 3 are just references to compare with the filtered data, if needed can be commented out