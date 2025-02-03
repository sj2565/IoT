#pragma once
#define NUM_HAN_BYTE (3)

class MyNumber
{
public:
	MyNumber(void)
	{

	}

	~MyNumber()
	{

	}
	// 3 bytes == 1����
	int getNumHanChar(const String& sInput)
	{
		return sInput.length() / NUM_HAN_BYTE;
	}
	// nPos: 0, 1, 2, ... ������ -1
	String getHanChar(const String& sInput, int nHanPos)
	{
		return sInput.substring(nHanPos * NUM_HAN_BYTE, (nHanPos + 1) * NUM_HAN_BYTE);
	}
	long toLong(const String& sChar)
	{
		if (sChar == '��') return 1;
		else if (sChar == '��') return 2;
		else if (sChar == '��') return 3;
		else if (sChar == '��') return 10;
		else if (sChar == '��') return 100;
		else return 0;
		 
	}
	boolean isCarryChar(const String& sChar)
	{
		return false;
	}
};