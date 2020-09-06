//directions looking formwards 
// AD
#include <Servo.h>
Servo top_l;
Servo top_r;
Servo mid_l;
Servo mid_r;
Servo clamp;

int count = 1;
int start1 = 40;
int start2 = 170;


const int top_l_pin = 3;
const int top_r_pin = 5;
const int mid_r_pin = 9;
const int mid_l_pin = 6;
const int clamp_pin = 10;
const int mid_down = A5;
const int mid_up = A4;
const int top_down = A3;
const int top_up = A2;
const int chomp = A1;

int right_angle (int angle)
{
  return 180 - angle;
}
void setup() {
  
  top_l.attach(top_l_pin);
  top_r.attach(top_r_pin);
  mid_r.attach(mid_r_pin);
  mid_l.attach(mid_l_pin);
  clamp.attach(clamp_pin);
  
  top_l.write(40); top_r.write(right_angle(40));
  mid_r.write(170); mid_l.write(right_angle(170));
 
}

void loop() {
  while(analogRead(chomp) > 100 && analogRead(top_up) > 100 && analogRead(top_down) > 100 && analogRead(mid_up) > 100   && analogRead(mid_down) > 100)
  {}

  if(analogRead(chomp) < 100 && count == 1)
  {
   clamp.write(130); 
   count = count*-1;
  }
  else if(analogRead(chomp) < 100 && count == -1)
  {
     clamp.write(160);
     count = count*-1;
  }
  else if (analogRead(top_up) < 100)
  {
    while(analogRead(top_up) < 100 && start1 < 170)
    {
      start1++;
      delay(40);
      top_l.write(start1);
      top_r.write(right_angle(start1));
    }
  }
  else if (analogRead(top_down) < 100)
  {
    while(analogRead(top_down) < 100 && start1 > 10)
    {
      start1--;
      delay(40);
      top_l.write(start1);
      top_r.write(right_angle(start1));
    }
  }
 else if (analogRead(mid_down) < 100)
  {
    while(analogRead(mid_down) < 100 && start2 > 10)
    {
      start2--;
      delay(40);
      mid_r.write(start2);
      mid_l.write(right_angle(start2));
    }
  }
 else if (analogRead(mid_up) < 100)
  {
    while(analogRead(mid_up) < 100 && start2 < 170)
    {
      start2++;
      delay(40);
      mid_r.write(start2);
      mid_l.write(right_angle(start2));
    }
  }
}
