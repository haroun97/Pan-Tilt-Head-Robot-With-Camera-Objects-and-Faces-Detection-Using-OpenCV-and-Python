#include <Servo.h>
Servo servoX;
Servo servoY;
int x=90 ;
int y=90 ;
const int led=4;// Declaration Pin 3 for LED
const int button=3;// Declaration Pin 3 for button
int stateb=0;// Initialisation the state of the button 
char input = ' '; //serial input is stored in this variable
void setup() {
  Serial.begin(9600);
  // Input/output Configuration 
  pinMode(led,OUTPUT);
  pinMode(button,INPUT_PULLUP);
  servoX.attach(8);
  servoY.attach(9);
  servoX.write(x);
  servoY.write(y);
  delay(1000);
}
void loop() {
 stateb=digitalRead(button);
 if(stateb==LOW)// if button ON 
 { 
 digitalWrite(led,LOW); 
 if(Serial.available()){ //checks if any data is in the serial buffer
  input = Serial.read(); //reads the data into a variable
  if(input == 'D'){
   y += 1;               //updates the value of the angle
   servoY.write(y);    //adjusts the servo angle according to the input

  }
  
  else if(input == 'd')
  {
   y += 2;               //updates the value of the angle
   servoY.write(y);    //adjusts the servo angle according to the input

  }
  
  else if(input == 'U'){ 
   y -= 1;
   servoY.write(y);
  }
  
  else if(input == 'u'){ 
   y -= 2;
   servoY.write(y);
  }
 /* else{
   servoY.write(y);
  } */
  if(input == 'L'){
  x -= 1;  
  servoX.write(x);
  }
  
  else if(input == 'l'){
  x -= 2;  
  servoX.write(x);
  }
  
  else if(input == 'R'){
  x += 1;
  servoX.write(x);
  }
  
  else if(input == 'r'){
  x += 2;
  servoX.write(x);
  }
//  else 
//  {
//  servoX.write(x);
//  }
  input = ' ';           //clears the variable
 }
 }// end if
   else
  {
     digitalWrite(led,HIGH);
  }
  
}
 


