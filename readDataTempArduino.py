# TEMPERATURA BATERIA 1 (ºC)
		valor = arduino_1.data[1]
		valor = (valor<<8)|arduino_1.data[0] # Traiem el valor del missatge
		valor = valor*0.01 # Apliquem el factor de multiplicació
		if valor != 0:
			temperatura1 = valor
		# TEMPERATURA BATERIA 2 (ºC)
		valor = arduino_1.data[3]
		valor = (valor<<8)|arduino_1.data[2] # Traiem el valor del missatge
		valor = valor*0.01 # Apliquem el factor de multiplicació
		if valor != 0:
			temperatura2 = valor
		# TEMPERATURA BATERIA 3 (ºC)
		valor = arduino_1.data[5]
		valor = (valor<<8)|arduino_1.data[4] # Traiem el valor del missatge
		valor = valor*0.01 # Apliquem el factor de multiplicació
		if valor != 0:
			temperatura3 = valor
		# TEMPERATURA BATERIA 4 (ºC)
		valor = arduino_1.data[7]
		valor = (valor<<8)|arduino_1.data[6] # Traiem el valor del missatge
		valor = valor*0.01 # Apliquem el factor de multiplicació
		if valor != 0:
			temperatura4 = valor
      
