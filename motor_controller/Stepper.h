#ifndef Stepper_h
#define Stepper_h

#include "Arduino.h"

# define M_PI           3.14159265358979323846
constexpr int microsteps = 16;
constexpr int microstep_table_entries = 4*microsteps; // microsteps per electrical cycle
constexpr float steps_per_degree = microsteps * 200 / 360.0;
constexpr int motor_maxpower = 255;

class Stepper
{
 public:
  Stepper();

  void attach(int Af, int Ab, int Bf, int Bb);
  
  // Sets target angle in degrees
  void setTargetAngle(float angle_in_degrees);

  // power is float in range [0, 1]
  void setPower(float power_normalized);

  // Should be called every step delay
  void update();

  float getVelocity() { return velocity_; }
  float getCurrentAngle() { return -step_num_ / steps_per_degree; }
  float getTargetAngle() { return -target_step_num_ / steps_per_degree; }
  float getStepNum() { return step_num_; }
  float getNormalizedPower() { return 1.0 * motor_power_ / motor_maxpower; }
  
 private:
  void step();
  void fill_microstep_array();

  int target_step_num_;
  int step_num_;
  int motor_power_;
  float velocity_;
  int Af_, Ab_, Bf_, Bb_;
  int microstep_table_[microstep_table_entries][2];
};


#endif  // Stepper_h
