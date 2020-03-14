
#include <Servo.h>
#include <math.h>

Servo myServo;

int pan_velocity = 0;
constexpr int pan_motor_maxpower = 255;
int pan_motor_power = pan_motor_maxpower;
int step_delay = 3;
float tilt_angle = 10;
int stepnum = 0;
int pan_stepnum_setpoint = 0;
constexpr int microsteps = 2;
float steps_per_degree = microsteps * 200 / 360.0;
char mode = '\0';

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(PB6, OUTPUT);
  pinMode(PB7, OUTPUT);
  pinMode(PB8, OUTPUT);
  pinMode(PA10, OUTPUT);
  myServo.attach(PB9);
  Serial.begin(115200); // open a serial connection to your computer
}

constexpr auto Af = PB6;
constexpr auto Ab = PB7;
constexpr auto Bf = PB8;
constexpr auto Bb = PA10;

void pwmWrite(int pin, int value){
  analogWrite(pin, (value==HIGH)*pan_motor_power);
}

int microstep_table[4*microsteps][2];

void fill_microstep_array(){
  for(int i = 0; i < 4*microsteps; i++){
    
  }
}

void pan_step(int stepnum) {
  delay(step_delay);
  switch ((8 + (stepnum % 8)) % 8) {
    case 0:
      pwmWrite(Bf, HIGH);
      break;
    case 1:
      pwmWrite(Af, LOW);
      break;
    case 2:
      pwmWrite(Ab, HIGH);
      break;
    case 3:
      pwmWrite(Bf, LOW);
      break;
    case 4:
      pwmWrite(Bb, HIGH);
      break;
    case 5:
      pwmWrite(Ab, LOW);
      break;
    case 6:
      pwmWrite(Af, HIGH);
      break;
    case 7:
      pwmWrite(Bb, LOW);
      break;

  }
}


void loop() {
  digitalWrite(Af, HIGH);
  for (int loopnum = 0;; loopnum++) {
    int dir = stepnum + pan_stepnum_setpoint;
    if (dir < 0)
      stepnum += 1;
    if (dir > 0)
      stepnum += -1;

    pan_step(stepnum);
    while (Serial.available()) {
      switch (Serial.read()) {
        case 's': //Set
          mode = 's';
          break;
        case 't': //Tilt angle
          if (mode == 's')
            tilt_angle = Serial.parseFloat();
          mode = '\0';
          break;
        case 'p': //Pan angle
          if (mode == 's')
            pan_stepnum_setpoint = (int)nearbyintf(Serial.parseFloat() * steps_per_degree);
          mode = '\0';
          break;
        case 'w': //motor power
          if (mode == 's')
            pan_motor_power = (int)nearbyintf(Serial.parseFloat() * pan_motor_maxpower);
          mode = '\0';
          break;
         case 'd': //step Delay
          if (mode == 's')
            step_delay = Serial.parseInt();
          mode = '\0';
          break;
          
      }
    }

    if(loopnum % 16 ==0){
      Serial.print("tilt_angle ");
      Serial.println(tilt_angle);
      Serial.print("stepnum ");
      Serial.println(stepnum);
      Serial.print("pan_angle_setpoint ");
      Serial.println(pan_stepnum_setpoint / steps_per_degree);
      Serial.print("pan_angle ");
      Serial.println(-stepnum / steps_per_degree);
      Serial.print("pan_motor_power ");
      Serial.println(1.0*pan_motor_power / pan_motor_maxpower);
      Serial.print("step_delay ");
      Serial.println(step_delay);
    }
    //    if(lo!=-1)
    //      Serial.print((char)lo);
    // set the servo position
    myServo.write((int)nearbyintf(tilt_angle + 90));
  }
}
