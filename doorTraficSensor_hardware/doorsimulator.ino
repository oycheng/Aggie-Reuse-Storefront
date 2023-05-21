#include <HCSR04.h>

#define TRIGGER1 5
#define ECHO1 6
#define TRIGGER2 7
#define ECHO2 8

HCSR04 hc(TRIGGER1,ECHO1);
HCSR04 hc2(TRIGGER2,ECHO2);

const int MAX_DISTANCE = 120;
const int FSM_SIZE = 4;
const int MAX_ERROR = 5;
const int MAX_CORRECT = 1;
int currentBoolIndex = 0;
bool passedDoor = false;
int inputState = 0;
int errBuffer = 0;
int correctBuffer = 0;
int counter = 0;
struct BoolPair {
  bool bool1;
  bool bool2;
};

BoolPair boolArray[FSM_SIZE];

void setup() {
  Serial.begin(9600);
  boolArray[0].bool1 = false;
  boolArray[0].bool2 = false;
  boolArray[1].bool1 = true;
  boolArray[1].bool2 = false;
  boolArray[2].bool1 = true;
  boolArray[2].bool2 = true;
  boolArray[3].bool1 = false;
  boolArray[3].bool2 = true;
}

void loop() {
  checkFSM();
  Serial.print("bool state: ");
  Serial.print(currentBoolIndex);
  Serial.print(" counter: ");
  Serial.println(counter);
}
//if currect change ++
//if no change done increment
//else reset index

int combineConditionals(bool condition1, bool condition2) {
  if ((condition1 == boolArray[0].bool1) && (condition2 == boolArray[0].bool2)) {
    return 0;  // Return 1 if both conditionals are true
  }
  if ((condition1 == boolArray[1].bool1) && (condition2 == boolArray[1].bool2)) {
    return 1;  // Return 1 if both conditionals are true
  }
  if ((condition1 == boolArray[2].bool1) && (condition2 == boolArray[2].bool2)) {
    return 2;  // Return 1 if both conditionals are true
  }
  if ((condition1 == boolArray[3].bool1) && (condition2 == boolArray[3].bool2)) {
    return 3;  // Return 1 if both conditionals are true
  }
  else {
    return 0;  // Return 0 for any other combination
  }
}

void checkFSM() {
  // bool tempBool1 = boolArray[currentBoolIndex].bool1;
  // bool tempBool2 = boolArray[currentBoolIndex].bool2;
  
  // if( ((hc.dist() < MAX_DISTANCE && (hc.dist() > 0.0)) == boolArray[currentBoolIndex].bool1)
  //   && ((hc2.dist() < MAX_DISTANCE && (hc2.dist() > 0.0)) == boolArray[currentBoolIndex].bool2) ) {
  //   currentBoolIndex++;
  //   if(currentBoolIndex >= (sizeof(boolArray) / sizeof(boolArray[0]))) {
  //     passedDoor = true;
  //     currentBoolIndex = 0;
  //   }
  // }
  // else {
  //   if (((hc.dist() < MAX_DISTANCE && hc.dist() > 0.0) == tempBool1) &&
  //       ((hc2.dist() < MAX_DISTANCE && hc2.dist() > 0.0) == tempBool2)) {
  //     // No change in conditions, keep currentBoolIndex unchanged
  //   }
  //   else {
  //     currentBoolIndex = 0;
  //   }
  // }
  bool condition1 = (hc.dist() < MAX_DISTANCE && (hc.dist() > 0.0));
  bool condition2 = (hc2.dist() < MAX_DISTANCE && (hc2.dist() > 0.0));
  if(combineConditionals(condition1, condition2) == currentBoolIndex) {
    errBuffer = 0;
  }
  else if((combineConditionals(condition1, condition2) % 4) == (currentBoolIndex + 1) % 4) {
    if(correctBuffer < MAX_ERROR) {
      ++correctBuffer;
    }
    else {
      currentBoolIndex++;
      errBuffer = 0;
      correctBuffer = 0;
      if(currentBoolIndex >= FSM_SIZE) {
        passedDoor = true;
        Serial.println("hit");
        counter++;
        currentBoolIndex = 0; 
      }
    }
  }
  else {
    if(errBuffer < MAX_ERROR) {
      ++errBuffer;
    }
    else {
      currentBoolIndex = 0;
      errBuffer = 0;
      correctBuffer = 0;
    }
  }

}
