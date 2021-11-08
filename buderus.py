import serial
import time


s = serial.Serial(port = 'com3',
                  baudrate = 2400)
                  #timeout=5.0)
s.flushInput ()
s.flushOutput ()


while True:
    sekw = True

    time.sleep(.5)
    s.write (b"\x02")
    time.sleep(.5)
    s.write (b"\xEE\x00\x00\x10\x03\xFD")
    time.sleep(.5)

    pocz = False
    koniec = False
    linia = ""

    while sekw:

        if s.inWaiting ():
            char = s.read()    
            if len (char):

                if ord(char) == 0x10 and pocz:
                    koniec = True
                    pocz = False
                    
                    if(linia == '03000110'): 
                        s.flushInput ()
                        s.flushOutput ()
                        sekw = False                   
                    if(linia.startswith('893C')): 
                        print("Temp zew: " + str(int(linia.replace('893C',''), 16))+ " *C")
                    if(linia.startswith('882B')): 
                        print("Temp akt kotla: " + str(int(linia.replace('882B',''), 16))+ " *C")
                    if(linia.startswith('8426')): 
                        print("Temp ust wody: " + str(int(linia.replace('8426',''), 16)) + " *C")
                    if(linia.startswith('8427')): 
                        print("Temp akt wody: " + str(int(linia.replace('8427',''), 16)) + " *C")
                    
                    #print(linia)
                    linia = ""
                
                if pocz:    
                    linia += '%2.2X'% ord(char)

                if ord (char)== 0x02 and not pocz: 
                    s.write (b"\x10")
                    time.sleep(80/1000)
                    pocz = True
                    s.write (b"\x10")

                if ord (char) == 0x03 and koniec:
                    koniec = False
    
'''
0000 65 11 22 2C 01 22    0000 65  11    22 2C  01       22
                                   lato         tryb

0x8000: „Wartości operacyjne 1 HK1”
0x8001: „Wartości operacyjne 2 HK1”
0x8002: „Docelowa temperatura zasilania OG1” (stopnie)
0x8003: „Rzeczywista temperatura zasilania OG1” (stopnie)
0x8004: `` Ustaw temperaturę pomieszczenia HK1 '' (stopnie)
0x8005: „Rzeczywista temperatura pomieszczenia HK1” (stopnie)
0x8006: `` Czas optymalizacji włączenia HC1 ''
0x8007: 'Czas optymalizacji wyłączenia HC1'
0x8008: `` Wyjście pompy HC1 '' (stopnie)
0x8009: 'Ustawienie mieszacza OG1' (stopnie)
0x800a: „nieużywane”
0x800b: „nieużywane”
0x800c: 'Krzywa grzania OG1 przy + 10 stopni' (stopnie)
0x800d: 'Krzywa grzewcza OG1 przy 0 stopniach' (stopnie)
0x800e: 'Krzywa grzewcza OG1 przy - 10 stopni' (stopnie)
0x800f: „nie używane”
0x8010: „nieużywane”
0x8011: „nieużywane”
#
0x8112: „Wartości operacyjne 1 HK2”
0x8113: „Wartości operacyjne 1 HK2”
0x8114: `` Docelowa temperatura zasilania HC2 '' (stopnie)
0x8115: „Rzeczywista temperatura zasilania HC2” (stopnie)
0x8116: `` Ustaw temperaturę pomieszczenia HC2 '' (stopnie)
0x8117: „Rzeczywista temperatura w pomieszczeniu HC2” (stopnie)
0x8118: `` Czas optymalizacji włączenia HC2 ''
0x8119: `` Czas optymalizacji wyłączenia HC2 ''
0x811a: „Wyjście pompy HK2”
0x811b: „Ustawienie mieszacza HK2”
0x811c: „nieużywane”
0x811d: „nieużywane”
0x811e: 'Krzywa grzewcza OG2 przy + 10 stopni' (stopnie)
0x811f: „Krzywa grzewcza OG2 przy 0 stopniach” (stopnie)
0x8120: `` Krzywa grzewcza OG2 przy - 10 stopni '' (stopnie)
0x8121: „nieużywane”
0x8122: „nieużywane”
0x8123: „nieużywane”
#
0x8424: „Wartości operacyjne 1 WW”
0x8425: „Wartości operacyjne 2 WW”
0x8426: „Docelowa temperatura ciepłej wody” (stopnie)
0x8427: „Rzeczywista temperatura ciepłej wody”, (stopnie)
0x8428: `` Czas optymalizacji ciepłej wody ''
0x8429: „Pompa ładująca” [„wyłączona”, „Pompa ładująca”, „Pompa ciepłej wody”, „obie”]
#
0x882a: `` Ustaw temperaturę zasilania kotła '' (stopnie)
0x882b: „Rzeczywista temperatura na zasilaniu kotła” (stopnie)
0x882c: `` Temperatura włączenia palnika '' (stopnie)
0x882d: `` Temperatura wyłączenia palnika '' (stopnie)
0x882e: „Całka kotła 1”
0x882f: „Całka kotła 2”
0x8830: „Błąd kotła”
0x8831: 'praca kotła'
0x8832: „Kontrola palnika” [„wył.”, „Wł.”]
0x8833: `` Temperatura spalin '' (stopnie)
0x8834: „modularna wartość sterowania palnikiem”
0x8835: „nieużywane”
0x8836: "Czas pracy palnika 1 godziny 2"
0x8837: „Czas pracy palnika 1 godziny 1”
0x8838: „Czas pracy palnika 1 godziny 0”
0x8839: „Czas pracy palnika 2 godziny 2”
0x883a: „Czas pracy palnika 2 godziny 1”
0x883b: „Czas pracy palnika 2 godziny 0”
#
0x893c: „Temperatura zewnętrzna” (stopnie)
0x893d: „tłumiona temperatura zewnętrzna” (stopnie)
0x893e: „Numer wersji VK”
0x893f: „Numer wersji NK”
0x8940: „Identyfikator modułu”
0x8941: „nieużywane”


'''
            
