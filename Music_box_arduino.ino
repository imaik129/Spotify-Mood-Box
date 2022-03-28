#include <Servo.h>

int sun_servo_curr_pos = 0;
Servo sun_Servo; 
Servo disco_Servo;

//variable_name: type_room#_color_identifier
//room_1
int LED_1_B_a = 11;
int LED_1_B_b = 10;
int LED_1_B_c = 9;
//to change brightness 
int star_curr_val = 0;
int star_change_val = 2;

//room_2
int LED_2_Y_a = 8;
int LED_2_Y_b = 7;
int LED_2_R_c = 6;
//to change brightness
int sun_curr_val = 0;
int sun_change_val = 3;

////room_3
int LED_3_W_a = 5;
int LED_3_W_b = 4;
int cloud_curr_val = 0;
int cloud_change_val = 5;
//
////room_4
int LED_4_G_a = 3;
int LED_4_G_b = 2;
int jungle_curr_val = 0;
int jungle_change_val = 3;

////room_5
//
int LED_5_B_a = 40;
int LED_5_W_b = 41;
//int panic_curr_val = 0;
//int panic_change_val = 1;

//
////room_6
int LED_6_B_a = 42;
int LED_6_B_b = 43;
int LED_6_R_c = 44;
int LED_6_R_d = 45;
int LED_6_Y_e = 46;
int LED_6_Y_f = 47;
int disco_servo_curr_pos = 0;


//array to hold rooms 
int rooms[7];


void setup() {
  // initialize both serial ports:
  Serial.begin(9600);
  Serial.print('A');
  //room_1
  pinMode(LED_1_B_a, OUTPUT);
  pinMode(LED_1_B_b, OUTPUT);
  pinMode(LED_1_B_c, OUTPUT);
  //room_2
  pinMode(LED_2_Y_a, OUTPUT);
  pinMode(LED_2_Y_b, OUTPUT);
  pinMode(LED_2_R_c, OUTPUT);
  sun_Servo.attach(39);
  //room_3
  pinMode(LED_3_W_a, OUTPUT);
  pinMode(LED_3_W_b, OUTPUT);
  //room_4
  pinMode(LED_4_G_a, OUTPUT);
  pinMode(LED_4_G_a, OUTPUT);
  //room_5
  pinMode(LED_5_B_a, OUTPUT);
  pinMode(LED_5_W_b, OUTPUT);
  //room_6
  pinMode(LED_6_B_a, OUTPUT);
  pinMode(LED_6_B_b, OUTPUT);
  pinMode(LED_6_R_c, OUTPUT);
  pinMode(LED_6_R_d, OUTPUT);
  pinMode(LED_6_Y_e, OUTPUT);
  pinMode(LED_6_Y_f, OUTPUT);
  disco_Servo.attach(38);

}

bool check_status(int room_num, int room_status){
  if (room_num == room_status){
    return true;
   }
   else{
    return false;
    }
  }

//void change_light(int light[], int curr_val, int change_val,int delay_val){
//    Serial.print("in change_light function");
//    curr_val += change_val;
//    int array_size = sizeof(light)/sizeof(light[0]);
//    for (int i = 0; i < array_size-1; i++){ 
//      analogWrite(light[i], curr_val);
//      if (0 >= curr_val || 255 <= curr_val) {
//         delay(delay_val);
//         star_change_val= -star_change_val;
//      }
//     }
// }

void activate_room_1(int room_val){
  int room_1 = 1; 
  if (check_status(room_1,room_val)){
  analogWrite(LED_1_B_a, star_curr_val);
  analogWrite(LED_1_B_b, star_curr_val);
  analogWrite(LED_1_B_c, star_curr_val);
  
  star_curr_val = star_curr_val + star_change_val;
  
  if (star_curr_val <= 0 || star_curr_val >= 255) {
    star_change_val = -star_change_val;
  }

  delay(30);
  }
}


void activate_room_2(int room_val){
  int room_2 = 2; 
//  int newVal = ((sun_curr_val * 180) / 255);
//  Serial.print(newVal);
  if (check_status(room_2, room_val)){
  analogWrite(LED_2_Y_a, sun_curr_val);
  analogWrite(LED_2_Y_b, sun_curr_val);
  analogWrite(LED_2_R_c, sun_curr_val);

  sun_servo_curr_pos  = ((sun_curr_val * 180) / 255);
 
  sun_Servo.write(sun_servo_curr_pos );

  
  sun_curr_val = sun_curr_val + sun_change_val;
  if (sun_curr_val <= 0){
    delay(1000);
    }
  if (sun_curr_val <= 0 || sun_curr_val >= 255) {
    sun_change_val = -sun_change_val;
  }
  
  
  delay(30);
  }

}

void activate_room_3(int room_val){
  int room_3 = 3; 
  if (check_status(room_3, room_val)){
  analogWrite(LED_3_W_a, cloud_curr_val);
  analogWrite(LED_3_W_b, cloud_curr_val);
  
  cloud_curr_val = cloud_curr_val + cloud_change_val;
  if (cloud_curr_val <= 0 || cloud_curr_val >= 255) {
    cloud_change_val = -cloud_change_val;
  }
  
  
  delay(30);
  }
}


void activate_room_4(int room_val){
  int room_4 = 4; 
  if (check_status(room_4, room_val)){
  analogWrite(LED_4_G_a, jungle_curr_val);
  analogWrite(LED_4_G_b, jungle_curr_val);
  
  jungle_curr_val = jungle_curr_val + jungle_change_val;
  if (jungle_curr_val <= 0 || jungle_curr_val >= 255) {
    jungle_change_val = -jungle_change_val;
  }

  delay(30);
  }
}

void activate_room_5(int room_val){
  int room_5 = 5; 
  if (check_status(room_5, room_val)){
  long random_number = random(1000);
  digitalWrite(LED_5_B_a, HIGH);
  digitalWrite(LED_5_W_b, HIGH);
  delay(random_number);
  digitalWrite(LED_5_B_a, LOW);
  digitalWrite(LED_5_W_b, LOW);
  delay(random_number);
  }
}

void activate_room_6(int room_val){
  int room_6 = 6; 
  if (check_status(room_6, room_val)){
    digitalWrite(LED_6_B_a, HIGH);
    digitalWrite(LED_6_B_b, HIGH);
    digitalWrite(LED_6_R_c, HIGH);
    digitalWrite(LED_6_R_d, HIGH);
    digitalWrite(LED_6_Y_e, HIGH);
    digitalWrite(LED_6_Y_f, HIGH);
    delay(10);
    digitalWrite(LED_6_B_a, LOW);
    digitalWrite(LED_6_B_b, LOW);
    digitalWrite(LED_6_R_c, LOW);
    digitalWrite(LED_6_R_d, LOW);
    digitalWrite(LED_6_Y_e, LOW);
    digitalWrite(LED_6_Y_f, LOW);
    long random_number = random(180);
    disco_Servo.write(random_number);
    delay(1000);
    disco_Servo.write(random_number);
    delay(1000);
    disco_Servo.write(random_number);
    delay(1000);

   }
   else{
    disco_Servo.write(0);
    }
   


}




void loop() {
//  activate_room_1();
//  activate_room_2();
//  activate_room_3();
//  activate_room_4();
//  activate_room_5();
//  activate_room_6();

  int play_status;
  int room_1;
  int room_2;
  int room_3;
  int room_4;
  int room_5;
  int room_6;
//  if (Serial.available() > 0) {
//    int inByte = Serial.read();
////    Serial.print("data byte received:");  
////    Serial.println(inByte);
//  }
  
  if(Serial.available()>=7) {
    for (int i = 0; i < 7; i++) {
      rooms[i] = Serial.read();
    }
    play_status = rooms[0];
    room_1 = rooms[1];
    room_2 = rooms[2];
    room_3 = rooms[3];
    room_4 = rooms[4];
    room_5 = rooms[5];
    room_6 = rooms[6];
    
    Serial.print(play_status);
    Serial.print(", ");
    Serial.print(room_1);
    Serial.print(", ");
    Serial.print(room_2);
    Serial.print(", ");
    Serial.print(room_3);
    Serial.print(", ");
    Serial.print(room_4);
    Serial.print(", ");
    Serial.print(room_5);
    Serial.print(", ");
    Serial.print(room_6);
    Serial.println("");
    
    if(play_status == 1){
      activate_room_1(room_1);
      activate_room_2(room_2);
      activate_room_3(room_3);
      activate_room_4(room_4);
      activate_room_5(room_5);
      activate_room_6(room_6);
    }
    else{
      activate_room_1(8);
      activate_room_2(8);
      activate_room_3(8);
      activate_room_4(8);
      activate_room_5(8);
      activate_room_6(8);
      Serial.println("no status");
      }
  }

  
}
