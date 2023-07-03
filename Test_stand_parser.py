import matplotlib.pyplot as plt
import csv
import os

# Important constants
Cf = 1.38  # Thrust coefficent for given propellant
Throat_area = 0.004**2 * 3.141592
Motor_designation = "H247"
cell_range = 5000.0
propellant_mass = 0.22 #kg
gravity = 9.81


Base_time = 0
Base_force = 0

# Plotting variables
x = []
F = []
P = []

Impulse = 0
prev_time = 0
total_thrust = 0

cnt = 0
trigger = False

# File system
fileList = os.listdir()
csvList = []

for file in fileList:
    if file.startswith("LOG"):
        csvList.append(file)

with open(csvList[0], 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')

    for row in lines:
        if cnt == 0:
            Base_time = float(row[0])
            Base_force = float(row[1])
        elif float(row[1]) - Base_force >= 1.0 and float(row[1]) - Base_force <= cell_range:
            if trigger == False:
                Base_time = float(row[0])
                trigger = True

            x.append((float(row[0]) - Base_time) / 10**6)
            F.append(float(row[1]) - Base_force + 10.0)
            P.append((float(row[1]) - Base_force) / (Cf * Throat_area * 10**6) )

            tempX = round((float(row[0]) - Base_time) / 10**6, 2)
            tempF = round(float(row[1]) - Base_force + 10.0, 2)

            temp = str(tempX) + " " + str (tempF)
            print(temp)

            total_thrust += float(row[1]) - Base_force + 10.0
            if prev_time > 0:
                Impulse += ((float(row[0])) - prev_time) * (float(row[1]) - Base_force +10) /10**6
                prev_time = float(row[0])
            else:
                prev_time = float(row[0])
            #print(Impulse)
        cnt += 1

Motor_designation = "H" + str(total_thrust/cnt)
plt.style.use('dark_background')

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax1.set_xlabel('time [s]')
ax1.grid(True)
ax1.set_title(Motor_designation)

ax1.set_ylabel('Force [N]', color='y')
ax1.tick_params(axis='y', labelcolor='y')
ax1.fill_between(x, F, 0, alpha=0.2, color='y')

ax2.set_ylabel('Pressure [MPa]', color='b')  # we already handled the x-label with ax1
ax2.tick_params(axis='y', labelcolor='b')

ax1.plot(x, F, color='y')
ax2.plot(x, P, color='b')

temp_str = "Total impulse: " + str(round(Impulse,1)) + "Ns\n\nSpecific impulse: " + str( round(Impulse / (gravity * propellant_mass), 1)) + "s"
t = plt.text(0.4, 0.7, temp_str, color='y', transform=ax1.transAxes, fontsize=15)


fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

