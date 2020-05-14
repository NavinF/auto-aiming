#include <math.h>
#include <Stepper.h>

Stepper::Stepper() 
  : motor_power_(motor_maxpower),
    velocity_(1),
    step_num_(0)
{
  fill_microstep_array();
}

void Stepper::attach(int Af, int Ab, int Bf, int Bb) {
  pinMode(Af, OUTPUT);
  pinMode(Ab, OUTPUT);
  pinMode(Bf, OUTPUT);
  pinMode(Bb, OUTPUT);
  Af_ = Af;
  Ab_ = Ab;
  Bf_ = Bf;
  Bb_ = Bb;
  digitalWrite(Af, HIGH);
}

void Stepper::setPower(float power_normalized) {
  motor_power_ = (int)nearbyintf(power_normalized * motor_maxpower);
  
  fill_microstep_array();
}

void Stepper::setTargetAngle(float angle_in_degrees) {
  target_step_num_ = (int)nearbyintf(angle_in_degrees * steps_per_degree);
}

void Stepper::update() {
  // TODO: should this be target_step_num_ - step_num_ ?
  int dir = step_num_ + target_step_num_;
  if (abs(dir) > 100 && velocity_ < 5)
    velocity_ += 0.02;
  else if((velocity_ > 1) && (abs(dir) < 100))
    velocity_ -= 0.02;
  if (dir < 0)
    step_num_ += 1;
  if (dir > 0)
    step_num_ += -1;

  step();
}

void Stepper::step() {
  int A = microstep_table_[(microstep_table_entries + (step_num_ % microstep_table_entries)) % microstep_table_entries][0];
  int B = microstep_table_[(microstep_table_entries + (step_num_ % microstep_table_entries)) % microstep_table_entries][1];
  if(A > 0){
    analogWrite(Af_, A);
    analogWrite(Ab_, 0);
  }
  if(A < 0){
    analogWrite(Ab_, -A);
    analogWrite(Af_, 0);
  }
  if(B > 0){
    analogWrite(Bf_, B);
    analogWrite(Bb_, 0);
  }
  if(B < 0){
    analogWrite(Bb_, -B);
    analogWrite(Bf_, 0);
  }
}

void Stepper::fill_microstep_array() {
  for(int i = 0; i < microstep_table_entries; i++){
    microstep_table_[i][0] = motor_power_ * cos((M_PI*i/microsteps)/2);
    microstep_table_[i][1] = motor_power_ * sin((M_PI*i/microsteps)/2);
  }
}
