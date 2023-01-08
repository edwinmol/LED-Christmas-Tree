#include <TimerOne.h>
#include <SPI.h>

//define the pin numbers
#define latch_pin 8 //can be any pin we choose
#define blank_pin 9 //can be any pin we choose
#define data_pin 11 //used by SPI, must be 11 (MOSI)
#define clock_pin 13 //used by SPI, must be 13

#define layer_pin_0 4 //can be any pin we choose
#define layer_pin_1 5 //can be any pin we choose
#define layer_pin_2 6 //can be any pin we choose

//setup the data structures
byte layer = 0; //keep track of the current layer
byte bamcounter = 0; //4bit resolution = 15 passes per cycle (x8 layers = 120)
byte BAMBit = 0; //0 to 3 -> 0 = Most Significant Bit

// Now the data for the LEDs
// We have to store this in performance optimized format,
// such that when these values are written to the LEDs, we use as less cpu cycles as possible
//
// Given that fact that we use BAM, we will store the bits in byte arrays that can be pushed 
// out very directly.
// We use a multidimensional array:
// - the first index is the BAM bit
// - the second index is the layer
// - the last index is the bit array containing the bits to shift into the shift registers
byte rgb[4][8][3];

void setup() {

  pinMode(blank_pin, OUTPUT);//Output Enable  important to do this first, so LEDs do not flash on boot up
  digitalWrite(blank_pin, HIGH);//Disable output

  //Setup SPI
  SPI.setBitOrder(MSBFIRST); 
  SPI.setDataMode(SPI_MODE0); //mode0 rising edge of data
  SPI.setClockDivider(SPI_CLOCK_DIV2); //run data at 16MHz/2 = 8MHz.
  
  //while setting up, we don't want to get thrown out of the setup function
  noInterrupts(); 

  //finally set up the Outputs
  pinMode(latch_pin, OUTPUT);//Latch
  pinMode(data_pin, OUTPUT);//MOSI DATA
  pinMode(clock_pin, OUTPUT);//SPI Clock

   // LAYER SELECT
  pinMode(layer_pin_0, OUTPUT);
  pinMode(layer_pin_1, OUTPUT);
  pinMode(layer_pin_2, OUTPUT);
  
  //start up the SPI library
  SPI.begin();
  
  //125 uSeconds = 8kHz sampling fequency. 
  Timer1.initialize(125);   //timer in microseconds
  Timer1.attachInterrupt(driveLayer);  // attaches driveLayer() as a timer overflow interrupt

  clear();
  interrupts(); //re-enable interrupts

}

void driveLayer()
{
 
  //first turn the output off
  digitalWrite(blank_pin, HIGH);
  
  //select layer
  selectLayer(layer);
  
  //write the RGB values
  writeValues();
  
  //latch the data
  digitalWrite(latch_pin,HIGH);
  digitalWrite(latch_pin,LOW);

  //turn the output on
  digitalWrite(blank_pin, LOW);
  

  //Finally set the BAMBit 
  if (bamcounter < 64) {
    BAMBit = 0;
  } else if (bamcounter < 96) {
    BAMBit = 1;
  } else if (bamcounter < 112) {
    BAMBit = 2;
  } else {
    BAMBit = 3;
  }  

  if (++layer==8) {
    layer = 0;
  }
  if (++bamcounter == 120) {
    bamcounter = 0;
  }
  
}

void writeOutput(byte value,byte mask, byte pin) {
    if (value & mask) {
        digitalWrite(pin,HIGH);
    } else {
        digitalWrite(pin,LOW);
    } 
}

void selectLayer(byte layer) {
    //check layer and convert to 3 bits output
    writeOutput(layer,0b00000001,layer_pin_0);
    writeOutput(layer,0b00000010,layer_pin_1);
    writeOutput(layer,0b00000100,layer_pin_2);
}

//function to control a LED
void LED (byte layer, byte column, byte r, byte g, byte b) {
  //write to the data structure, the driveLayer interrupt will push it to the HW
  for (int i=0; i<4; i++) {      
      int bitindex = column*3+3;
      int byteindex = bitindex/8; 
      bitWrite(rgb[i][layer][bitindex/8],7-(bitindex%8),bitRead(r,3-i));        
      bitindex++;
      bitWrite(rgb[i][layer][bitindex/8],7-(bitindex%8),bitRead(g,3-i));
      bitindex++;
      bitWrite(rgb[i][layer][bitindex/8],7-(bitindex%8),bitRead(b,3-i));     
  }
}

void writeValues() {  
  for (int i=0; i<3; i++) {
    SPI.transfer(rgb[BAMBit][layer][i]);
  }
} 

void clear() {
  for (int l=0;l<8;l++) {
    for (int i=0;i<7;i++) {
      LED (l,i,0,0,0);
    }
  }
}

void loop() {
  RGB();
  glow();
  spinner();
  snake();
  fireworks();
  android(15,0,15);
  tree(0,15,0);  
  fill(15,8,0);
  doRandom();  
}

// ANIMATION CODE

void RGB() {
  turn(15,0,0,10);
  delay(1000);  
  turn(0,15,0,10);
  delay(1000);  
  turn(0,0,15,10);
  delay(1000);  
}

void glow() {
  for (int i=0; i<4; i++) {
    for (int r=1; r<32; r++) {
        int c = r>15?31-r:r;
        all(c,c,c);
        delay(30);      
    }
  }
  clear();
}

void spinner() {
  for (int a=0; a<12; a++) {
    for (int i=0; i<6; i++) {
      column(1+i,0,0,15); 
      delay(80);
      column(1+i,0,0,0); 
    }
  }
  clear();
}
void column(byte c, byte r, byte g, byte b) {
  for (int i=0; i<8; i++) {
      LED(i, c, r,g,b);
  } 
}
void snake() {  
  for (int i=7; i>=0; i--) {    
    for (int j=1; j<7; j++) {
      LED(i, j, random(16), random(16), random(16));
      delay(100);
    }           
  }
  for (int i=0; i<8; i++) {
    LED(i, 0, random(16), random(16), random(16));
    delay(100);
  }
  delay(1000);
  clear();
}

void android(byte r,byte g, byte b) {
  for (int j=0; j<3; j++) {
    for (int i=0;i<8;i++) {
      row(i,r,g,b);
      delay(50+i*10);
      row(i,0,0,0);
    }
    for (int i=7;i>=0;i--) {
      row(i,r,g,b);
      delay(50+i*10);
      row(i,0,0,0);
    }
    delay(500);
  }
}

void fill(byte r,byte g, byte b) {      
  for (int l=0; l<8; l++) {
      row(l,r,g,b);
      delay(500);
  }  
  delay(1000);
  clear();
}

void row(byte l, byte r, byte g, byte b) {
    for (int i=0;i<7;i++) {
      LED (l,i,r,g,b);
    }
}

void all(byte r, byte g, byte b) {
  for (int l=0;l<8;l++) {
    for (int i=0;i<7;i++) {
      LED (l,i,r,g,b);
    }
  }
}

void tree(byte r, byte g, byte b) {
  clear();
  turn(r,g,b,150);
  delay(1000);
}

void turn(byte r, byte g, byte b, int d) {
  for (int l=0;l<8;l++) {
    for (int i=0;i<7;i++) {
      LED (l,i,r,g,b);
      delay(d);
    }
  }
}

void fireworks() {
  for (int i=7; i>=0; i--) {
    LED(i, 0, 15, 15, 15);
    delay(10+i*40);    
  }
  LED(0, 0, 15, 2, 0);
  for (int i=0; i<8; i++) {    
    for (int j=1; j<7; j++) {
      LED(i, j, 15, 2, 0);
    }
    LED(7-i, 0, 0, 0, 0);
    delay(200-i*20);        
  }

}

void doRandom() {
  clear();
  for (int i=0; i<100; i++) {
    LED(random(8), random(7), random(16), random(16), random(16));
    delay(random(150));    
  }
  clear();
}
