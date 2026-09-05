import gpiozero as gpio
import time


threshold = 0.02
adjust12 = -0.01 #0.042
adjust23 = 0.03 #-0.005
panel1=gpio.MCP3008(channel=0)
panel2=gpio.MCP3008(channel=1)
panel3=gpio.MCP3008(channel=2)
print(f"panel1 {panel1.value}")
print(f"panel2 {panel2.value}")
sum1 = 0.0
sum2 = 0.0
sum3 = 0.0

#setup motors and controler
motor1 = gpio.Motor(24,25)
motor2 = gpio.Motor(12,13)
motor1on = gpio.DigitalOutputDevice(23)
motor2on = gpio.DigitalOutputDevice(18)


#setup switches
check1 = gpio.Button(17, pull_up=True)
check2 = gpio.Button(27, pull_up=True)
check3 = gpio.Button(22, pull_up=True)
check4 = gpio.Button(5, pull_up=True)

#check if demo mode
demo = gpio.Button(26, pull_up=False)

def avgcheck(num):
    times = num
    global sum1
    global sum2
    global sum3
    global adjust12
    sum1 = 0.0
    sum2 = 0.0
    sum3 = 0.0
    while times>0:
        sum1 = sum1 + panel1.value + adjust12
        sum2 = sum2 + panel2.value
        sum3 = sum3 + panel3.value + adjust23
        time.sleep(0.02)
        times -=1
    sum1 = sum1/float(num)
    sum2 = sum2/float(num)
    sum3 = sum3/float(num)

def pancheck():
    global check1
    global check2
    return check1.is_pressed or check2.is_pressed

def tiltcheck():
    global check3
    global check4
    return check3.is_pressed or check4.is_pressed

def init():
    global count, direction, previous_direction
    count = 0
    direction = 0
    previous_direction = 3
    avgcheck(3)

def tilt():
    global sum1, sum2, sum3,  motor2, direction, previous_direction, count, threshold, motor2on
    motor2on.on()
    init()
    while abs(sum2-sum3) > threshold:
        print(f"panel2 {sum2}")
        print(f"panel3 {sum3}")
        if sum3 > sum2:
            motor2.forward(0.1)
            time.sleep(1)
            motor2.stop()
            direction = 0
        else:
            motor2.backward(0.1)
            time.sleep(1)
            motor2.stop()
            direction = 1
        
        avgcheck(3)    
        if previous_direction == 3:
            previous_direction = direction
        elif previous_direction != direction:
            print("abs sum exceed threshold, direction changed")
            
            print(f"panel2 abs exceed {sum2}")
            print(f"panel3 abs exceed {sum3}")
            break        
        #avgcheck(3)
        if check3.is_pressed or check4.is_pressed:
            break
        print(f"check3 {check3.is_pressed} check4 {check4.is_pressed}")


    #continue in previous 
    if previous_direction != 3 and previous_direction == direction:
        print("continue move")

        
        count = 0.0
        panel2_max = sum2
        panel3_max = sum3
        panel2_count_at_max = 0.0
        panel3_count_at_max = 0.0
        
        while abs(sum2-sum3)<threshold:
            print(f"panel 2 continue  {sum2}")
            print(f"panel 3 continue  {sum3}")
            count += 1
            print(count)
            if panel3_max < sum3:
                panel3_max = sum3
                panel3_count_at_max = count
            if panel2_max < sum2:
                panel2_max = sum2   
                panel2_count_at_max = count 

            if direction == 0:
                motor2.forward(0.1)
                time.sleep(1)
                motor2.stop()
            else:
                motor2.backward(0.1)
                time.sleep(1)
                motor2.stop()
                    
            #count += 1
            #print(count)
            
            avgcheck(3)

            if check3.is_pressed or check4.is_pressed:
                break

        #reversal
        print(f"panel 2 exit continue  {sum2}")
        print(f"panel 3 exit continue  {sum3}")
        print(f"panel 2 exit panel2_max  {panel2_max}")
        print(f"panel 3 exit panel3_max  {panel3_max}")
        print(f"panel2 exit panel2_count_at_max  {panel2_count_at_max}")
        print(f"panel3 exit panel3_count_at_max  {panel3_count_at_max}")
        

        if direction == 0:
            motor2.backward(0.1)
        else:
            motor2.forward(0.1)
    #    time.sleep((count+1)/2.0)
        time.sleep(count-(panel3_count_at_max+panel2_count_at_max)/2)
        print(f"reverse {count-(panel3_count_at_max+panel2_count_at_max)/2}")
        avgcheck(3)
        print(f"panel 2 current  {sum2}")
        print(f"panel 3 current  {sum3}")
        
        
        
    else:
        print("no further move")    
    print("stopping motor2 ...")    
    motor2.stop()
    motor2on.off()
    print("motor2 stopped")

def pan():
    global sum1, sum2, sum3,  motor1, direction, previous_direction, count, threshold, motor1on
    motor1on.on()
    init()
    while abs(sum1-sum2) > threshold:
        print(f"panel1 {sum1}")
        print(f"panel2 {sum2}")
        if sum1 > sum2:
            motor1.forward(0.1)
            time.sleep(1)
            motor1.stop()
            direction = 0
        else:
            motor1.backward(0.1)
            time.sleep(1)
            motor1.stop()
            direction = 1
        avgcheck(3)    
        if previous_direction == 3:
            previous_direction = direction
        elif previous_direction != direction:
            print("abs sum exceed threshold, direction changed")
            print(f"panel1 abs exceed {sum1}")
            print(f"panel2 abs exceed {sum2}")
            break        
        #avgcheck(3)
        if check1.is_pressed or check2.is_pressed:
            break


    #continue in previous 
    if previous_direction != 3 and previous_direction == direction:
        print("continue move")

        
        count = 0.0
        panel1_max = sum1
        panel2_max = sum2
        panel1_count_at_max = 0.0
        panel2_count_at_max = 0.0
        
        while abs(sum1-sum2)<threshold:
            print(f"panel 1 continue  {sum1}")
            print(f"panel 2 continue  {sum2}")
            count += 1
            print(count)
            if panel1_max < sum1:
                panel1_max = sum1
                panel1_count_at_max = count
            if panel2_max < sum2:
                panel2_max = sum2   
                panel2_count_at_max = count 

            if direction == 0:
                motor1.forward(0.1)
                time.sleep(1)
                motor1.stop()
            else:
                motor1.backward(0.1)
                time.sleep(1)
                motor1.stop()
                    
            #count += 1
            #print(count)
            
            avgcheck(3)

            if check1.is_pressed or check2.is_pressed:
                break

        #reversal
        print(f"panel 1 exit continue  {sum1}")
        print(f"panel 2 exit continue  {sum2}")
        print(f"panel 1 exit panel1_max  {panel1_max}")
        print(f"panel 2 exit panel2_max  {panel2_max}")
        print(f"panel1 exit panel1_count_at_max  {panel1_count_at_max}")
        print(f"panel2 exit panel2_count_at_max  {panel2_count_at_max}")
        

        if direction == 0:
            motor1.backward(0.1)
        else:
            motor1.forward(0.1)
    #    time.sleep((count+1)/2.0)
        time.sleep(count-(panel1_count_at_max+panel2_count_at_max)/2)
        print(f"reverse {count-(panel1_count_at_max+panel2_count_at_max)/2}")
        avgcheck(3)
        print(f"panel 1 current  {sum1}")
        print(f"panel 2 current  {sum2}")
        
        
        
    else:
        print("no further move")    
    print("stopping motor1 ...")    
    motor1.stop()
    motor1on.off()
    print("motor1 stopped")

avgcheck(3)
"""checkcount = 0
while checkcount < 20:
    time.sleep(1)
    avgcheck(3)
    #print(f"panel1 {sum1}")
    print(f"panel2 {sum2}")
    print(f"panel3 {sum3}")
    print(" ")

    checkcount += 1
    """

if demo.is_pressed:                             #Checks to see if a switch is turned on to perform the full swivel
    
    motor2on.on()
    print("moving forwards")
    if not check3.is_pressed:                   #Tilts the maximum amount upwards until it hits the switch
        motor2.forward(0.3)
        check3.wait_for_press()
        motor2.stop()
    motor2on.off()
    time.sleep(1)

    #tilt
    motor2on.on()                               #Tilts down to a starting angle
    motor2.backward(0.3)
    time.sleep(3)
    motor2.stop()
    motor2on.off()

    #pan
    maxdetected = 0                             
    maxcount = 0
    count = 0
    motor1on.on()
    if not check1.is_pressed:                   #Pans the maximum amount clockwise until it hits the switch
        motor1.forward(0.5)
        check1.wait_for_press()
    motor1.stop()


    while not check2.is_pressed:
        avgcheck(3)
        motor1.backward(0.3)                    #Pans counterclockwise incrementally, measuring and recording the maximum output and time.
        if (sum1+sum2)>maxdetected:
            maxdetected = (sum1+sum2)
            maxcount = count
        count +=1
        time.sleep(1)
        motor1.stop()

    motor1.forward(0.3)                         #Pans back clockwise to the position of maximum output based on the recorded time
    print(maxcount)
    print(count)
    time.sleep(count-maxcount)
    motor1.stop()


    avgcheck(3)
    if sum1 > max(sum2,sum3):                   #Checks whether which part has a larger signal and starts in that directino.
        pan()
        tilt()
    else:
        tilt()
        pan()
else:                                           #Immediately begins trackinging towards the side with the greater signal
    avgcheck(3)
    if sum1 > max(sum2,sum3):                   #Checks whether which part has a larger signal and starts in that directino.
        pan()
        tilt()
    else:
        tilt()
        pan()
    
