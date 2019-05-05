import time
import RPi.GPIO as GPIO
import MFRC522
 
# UID dos cartoes que possuem acesso liberado.
CARDS_ALLOWED = {
    '3C:2F:4F:0:2D': 'Teste',
	'81:8:173:121:141': 'Rolf1',
	'97:244:30:57:178': 'Rolf2',
	'53:188:162:67:104': 'Rolf3',
	'197:248:221:82:178': 'Rolf4',
}
 
try:
	# Inicia o modulo RC522.
	RFIDreader = MFRC522.MFRC522()
	print('Waiting for RFID card')

	while True:
	# Verifica se existe uma tag proxima do modulo.
		status, tag_type = RFIDreader.MFRC522_Request(RFIDreader.PICC_REQIDL)

		if status == RFIDreader.MI_OK:
			print('Card detected!')

			# Efetua leitura do UID do cartao.
			status, uid = RFIDreader.MFRC522_Anticoll()

			if status == RFIDreader.MI_OK:
				uid = ':'.join(['%X' % x for x in uid])
				print('Card UID: %s' % uid)

				# Se o cartao esta liberado exibe mensagem de boas vindas.
				if uid in CARDS_ALLOWED:
					print('Access granted!')
					print('Hello %s.' % CARDS_ALLOWED[uid])
				else:
					print('Access Denied!')
			print('Waiting for TAG')

		time.sleep(.25)
except KeyboardInterrupt:
    # Se o usuario precionar Ctrl + C
    # encerra o programa.
    GPIO.cleanup()
    print('nPrograma encerrado.')
