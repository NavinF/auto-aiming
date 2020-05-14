#include <Servo.h>
#include <Stepper.h>

Servo myServo;
Stepper pan_stepper;

int step_delay = 3000;
float tilt_angle = 10;

char mode = '\0';

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pan_stepper.attach(PB6, PB7, PB8, PA10);
  myServo.attach(PB9);
  Serial.begin(115200); // open a serial connection to your computer
}

void loop() {
  for (int loopnum = 0;; loopnum++) {
    // TODO: update constant force code so it does not rely on a variable sleep.
    // This will allow us to run multiple steppers at once.
    pan_stepper.update();
    delayMicroseconds(step_delay/pan_stepper.getVelocity()); 

    while (Serial.available()) {
      switch (Serial.read()) {
        case 's': //Set
          mode = 's';
          break;
        case 't': //Tilt angle
          if (mode == 's') {
            tilt_angle = Serial.parseFloat();
          }
          mode = '\0';
          break;
        case 'p': //Pan angle
          if (mode == 's') {
            pan_stepper.setTargetAngle(Serial.parseFloat());
          }
          mode = '\0';
          break;
        case 'w': //motor power
          if (mode == 's') {
            pan_stepper.setPower(Serial.parseFloat());
          }
          mode = '\0';
          break;
         case 'd': //step Delay
          if (mode == 's') {
            step_delay = Serial.parseInt();
          }
          mode = '\0';
          break;
      }
    }

    if(loopnum % 16 ==0) {
      // The following values are used for communication with coralboard
      Serial.print("tilt_angle ");
      Serial.println(tilt_angle);
      Serial.print("pan_angle ");
      Serial.println(pan_stepper.getCurrentAngle());

      // The following values are for debug purposes
      Serial.print("step_delay ");
      Serial.println(step_delay);
      Serial.print("pan_step_num ");
      Serial.println(pan_stepper.getStepNum());
      Serial.print("pan_target_angle ");
      Serial.println(pan_stepper.getTargetAngle());
      Serial.print("pan_motor_power ");
      Serial.println(pan_stepper.getNormalizedPower());
      Serial.print("pan_velocity ");
      Serial.println(pan_stepper.getVelocity());
    }
    //    if(lo!=-1)
    //      Serial.print((char)lo);
    // set the servo position
    myServo.write((int)nearbyintf(tilt_angle + 90));
  }
}
