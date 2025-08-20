//basic principle
// as we go higher in the atmosphere, atmospheric pressure 
//reduces and hence the force felt by the sensor also reduces.
//here the force sensor starts by default at 0N
//this technically means there is no pressure (vacuum)
//which doesnt really make sense in our use case
//so there is a delay at the start to set default force to
//force due to pressure at ground. Additionally the problem statement says
// the sensor experiences atmospheric force over an area of 0.01m^2
//this doesnt make sense either because the maximum
//force measureable by this force sensor is 10N.

int data[250];
float final[250];
unsigned long time;
 int i = 0; //needed later for comparission
  float p =0.01;
  float q=0.5;
  float r=0.1;
  float k;
  float z;
  float x;
  //all for a simple 1D kalman filter

  
   void setup()
{
   pinMode(A5, INPUT);
     pinMode(10,OUTPUT);
     pinMode(11,OUTPUT);
     pinMode(13,OUTPUT);
     pinMode(8,OUTPUT); //pin setup
  
  delay(5000); //as said earlier, the force starts off at 0 which doesnt make sense, hence there is a 5 sec delay 
  //for you to drag the force to the force due to pressure at ground, this comes out to be more than 1,000 newtons(again max val on sensor is 10N), so just initiallize force due to pressure at ground as 10N
  
  x = analogRead(A5); //just initializing for the kalman filter
 
  
}

void loop()
{


  //simple 1D kalman filter
  z = analogRead(A5);
  p = p+q;
  
  
  k = (p)/(p+r);
  p = (1-k)*p;
  x = (1-k)*x+k*z;
  
  
  final[i] = x;

  //we do not actually need a filter here, as there is 0 measurement noise as we have a draggable bar sensor,with no measurement noise
  // but the filter is added assuming we have a sensor that has some measurement noise (the filter may actually be somewhat usefull here 
//as it is not really possible to drag the bar consistently how we need it
 
  if(i>2){
  
    if(final[i]>final[i-1]){
   
    digitalWrite(10,HIGH);
     }

     //if the  force due to pressure is increasing, it means the altitude is decreasing, hence the red LED comes on

    else if(final[i]<final[i-1]){
    
    digitalWrite(13,HIGH);

    //if the  force due to pressure is decresing, it means the altitude is increasing, hence the green LED comes on
    
    
    
    }
    else if(final[i]  ==466 && final[i-1] == 466){

digitalWrite(10,HIGH);
  digitalWrite(13,HIGH);
  digitalWrite(11,HIGH);    //checking for my defined ground condition, i cant equate the values to 466 because of my filter, which would return exactly 1023 pretty rarely
    }
    else if (abs(final[i] - final[i-1]) <= 1){
      if(analogRead(A5) !=0){
    digitalWrite(11,HIGH);
       tone(8,1000,100);

       //if the change in the force due to pressure is very small (ideally it must be 0, but due to the delay between our loops we mayb never get perfectly same values),
       //it means the rocket has reached its apogee (here the difference of 1 is very small as the analog pin returns a value from 1 to 1023)
      }

    
    }
  
 }
  
  
  if(i == 249){
  final[0]= final[249];
  i = 1;

  }
  //as we are going through a loop each 50 miliseconds, we will fill up our array and we cant use a very large array due to memory limitations, hence, we loop back in in the same array
  // also, we are taking i=1 and not i=0 to avoid the logic error that will show up when it tries to find final[i-1]
  i = i+1;
  delay(50);  // data is updated every 50 seconds
  digitalWrite(10,LOW);
  digitalWrite(13,LOW);
  digitalWrite(11,LOW);  //i have kept the delay and turning off the LEDs at the end but they can also be placed individually after each if statement
  
}
