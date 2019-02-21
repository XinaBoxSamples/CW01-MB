from microbit import *
uart.init(baudrate=9600, bits=8, parity=None, stop=1, tx=pin20, rx=pin19)


def CW01(parm):
    # Parm must follow this format:
    # start with a '+'
    # then a number 1,2,3 etc. See below
    # then a seperator '@'
    # then a parameter followed by a seperator '@'
    # last parameter is ended with a end symbol '$'
    # Commands:
    # 1 for WiFi:          "+1@ssid@secret$"
    # 2 for login to MQTT: "+2@username@password$"
    # 3 for MQTT server:   "+3@server@port$"
    # 4 for ubidot:        "+4@device@variable@value$" (creates a MQTT publish)
    # 5 for MQTT publish:  "+5@topic@payload$"
    # 6 for MQTT subscribe:"+6@topic$" (maximum 1 subscription)
    # always start with "$" just to clean out the serial buffer
    display.clear()
    uart.write(parm)
    sleep(500)
    data = uart.readline()
    while(data is None):
        data = uart.readline()
    # print("Something") # You can't print - it becomes input to the CW01
    if int(data[:1]) == 1:
        display.show(Image.YES)
    elif int(data[:1]) == 0:
        display.show(Image.NO)
    else:
        display.scroll(data[1:-1])
    sleep(500)


display.show(Image.SQUARE)
sleep(2000)
uart.write("$") # Clean out Serial buffer
sleep(100)
uart.write("+9@?$") # Reboot CW01
sleep(5000)
uart.write("$") # Clean out Serial buffer
sleep(500)

CW01("+1@XinaBox@RapidIoT$")

# CW01("+2@BBFF-RnSiiNYcfp2Nw3jKlA8aSasnsjlVBb@?$") # UbiDot
CW01("+2@?@?$")

# CW01("+3@industrial.api.ubidots.com@1883$") # UbiDot
# CW01("+3@test.mosquitto.org@1883$")
CW01("+3@broker.hivemq.com@1883$")

CW01("+6@/v1.6/devices/OC03/state/lv$")

while True:
    CW01("+4@blue@temperature@" + str(temperature()) + "$")
    CW01("+4@blue@a@"+str(button_a.is_pressed())+"$")
    CW01("+4@blue@b@"+str(button_b.is_pressed())+"$")
    sleep(500)
