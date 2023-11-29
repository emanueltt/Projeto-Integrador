/*
 *  Programa: Exemplo de uso do driver Ponte H L298N
 *  Autor: Gustavo Nery, Eletrogate.
 *  Arduino 1.8.12
*/

// Iremos fazer uma classe para facilitar o uso da ponte H L298N na manipulação dos motores na função Setup e Loop.

class DCMotor
{
	int spd = 255, pin1, pin2;

public:
	void Pinout(int in1, int in2)
	{ // Pinout é o método para a declaração dos pinos que vão controlar o objeto motor
		pin1 = in1;
		pin2 = in2;
		pinMode(pin1, OUTPUT);
		pinMode(pin2, OUTPUT);
	}

	void Speed(int in1)
	{ // Speed é o método que irá ser responsável por salvar a velocidade de atuação do motor
		spd = in1;
	}

	void Forward()
	{ // Forward é o método para fazer o motor girar para frente
		analogWrite(pin1, spd);
		digitalWrite(pin2, LOW);
	}

	void Backward()
	{ // Backward é o método para fazer o motor girar para trás
		digitalWrite(pin1, LOW);
		analogWrite(pin2, spd);
	}

	void Stop()
	{ // Stop é o metodo para fazer o motor ficar parado.
		digitalWrite(pin1, LOW);
		digitalWrite(pin2, LOW);
	}
};

DCMotor Motor1;

void setup()
{
	Motor1.Pinout(5, 6);
}

void loop()
{
	Motor1.Speed(255);

	Motor1.Backward(); // Comando para o motor ir para trás
	delay(1000);
	Motor1.Stop(); // Comando para o motor parar
	delay(200);
}