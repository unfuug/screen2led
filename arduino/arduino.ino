#define LED_R 3
#define LED_G 5
#define LED_B 6
#define CAP 255

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
char tempChars[numChars];       // temporary array for use when parsing

boolean newData = false;

int R = 255;
int G = 255;
int B = 255;


void setup() {
  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);
  update();
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
}


void test() {
  // soft on led band
  for (int i=0; i<=CAP; i++) {
    analogWrite(LED_R, i);
    analogWrite(LED_G, CAP-i);
    int j = i/2;
    int m = i%2;
    if (m == 0) {
      m = -1;
    }
    analogWrite(LED_B, (CAP / 2) + (j * m));
    delay(5);
  }
  // soft off led band
  for (int i=CAP; i>=0; i--) {
    analogWrite(LED_R,  i);
    analogWrite(LED_G, -i);
    int j = i/2;
    int m = i%2;
    if (m == 0) {
      m = -1;
    }
    analogWrite(LED_B, (CAP / 2) + (j * m));
    delay(5);
  }
}


void receiveSerialData() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '(';
  char endMarker = ')';
  char rc;
  
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
            ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }

    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}


void parse() {
  char * strtokIndx;

  strtokIndx = strtok(tempChars, ",");
  R = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ",");
  G = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ",");
  B = atoi(strtokIndx);
}


void update() {
  analogWrite(LED_R, R);
  analogWrite(LED_G, G);
  analogWrite(LED_B, B);
}

void loop() {
  receiveSerialData();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    parse();
    update();
    newData = false;
  }
}