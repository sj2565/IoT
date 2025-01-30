#pragma once

#include <StringTok.h>
#define SERIAL_WAIT_DELAY (100)
#define LED_PORT_MIN (2)
#define LED_PORT_MAX (13)

class LedCtrl {
public:
	LedCtrl() {

	}

	~LedCtrl() {

	}

private:
	StringTok m_sInput;
	String m_sToken;

protected:
	void initLedCtrl() {
		for (int i = LED_PORT_MIN; i <= LED_PORT_MAX; i++)
		{
			pinMode(i, OUTPUT);
			digitalWrite(i, LOW);
		}
	}

	void appendSerial() {
		while (Serial.available() > 0) {
			m_sInput.appendSerial();
			delay(SERIAL_WAIT_DELAY);
		}		
	}

	void cutToken() {
		m_sToken = m_sInput.cutToken().toString();
	}

	void exeCommand() {
		cutToken();
	}

public:
	void setup() {
		initLedCtrl();
	}

	void loop() {
		appendSerial();
		exeCommand();
	}
};