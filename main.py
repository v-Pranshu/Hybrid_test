from Inputs import UserInputs
from propParam import FuelData
import numpy as np
import matplotlib.pyplot as mp
exp = 0.6
grain = UserInputs(10, 8, 10, 60, 30)     # Outer dia, Core Dia, length, throat area, step size
fuel = FuelData(120, 996, exp, 10, 2000,guess_thrust)      # Go, c_star, exponent(burn rate), coefficient, burn rate,fuel_user
# Grain Volume pi(D2 - d2)/4*length
grainVol = np.pi*(pow(grain.outerDia, 2) - pow(grain.coreDia, 2))*0.25*grain.length

# Grain Mass grainVol*Density
fuelMass = grainVol*fuel.density
massEjected = 0
m_dot  = 56
stepNum = 0
Isp  = 10

print(massEjected)
print(fuelMass)

time = np.zeros(grain.stepSize, dtype = float)

while (stepNum<grain.stepSize):
    c=1;
    
    #initiate radius array R(t)
    radius = np.empty(grain.stepSize, dtype = float)
    radius[stepNum] = 0
    print(radius[stepNum])

    m_dot_ox = np.zeros(grain.stepSize, dtype = float)
    m_dot_f = np.zeros(grain.stepSize, dtype = float)
    m_dot_tot = np.zeros(grain.stepSize, dtype = float)

    m_dot_ox[stepNum] = fuel.Go*grain.portArea

    time[stepNum] = grain.stepSize*stepNum

    alpha = pow(m_dot_ox[stepNum]/np.pi, fuel.exp)

    rad = pow((fuel.coeff*(2*fuel.exp+1)*alpha*time[stepNum]) + pow(grain.coreDia, 2*fuel.exp+1), 1/(2*fuel.exp + 1))
    print(alpha)

    m_dot_f[stepNum] = 2*np.pi*fuel.density*grain.length*alpha*pow(radius[stepNum], 1-2*fuel.exp)

    OF_ratio = np.zeros(grain.stepSize, dtype = float)

    #OF_ratio[stepNum] = m_dot_ox[stepNum]/m_dot_f[stepNum]

    m_dot_tot = np.array(grain.stepSize, dtype = float)

    #m_dot_tot[stepNum] = m_dot_f[stepNum] + m_dot_ox[stepNum]


    thrust = np.zeros(grain.stepSize, dtype = float)
    thrust[stepNum] = m_dot_tot*Isp*fuel.Go
    if(fuel.thrust_user<1.03*thrust[stepNum]and fuel.thrust_user>0.97*thrust[stepNum]):
        break
    elif(fuel.thrust_user<thrust[stepNum]):
        thrust[stepNum]=thrust[stepNum]*(1-(0.5)**c)
    else:
         thrust[stepNum]=thrust[stepNum]*(1+(0.5)**c)
    c=c+1;
    portArea = np.pi*(pow(grain.outerDia, 2) - pow(4*radius[stepNum], 2))*0.25
    stepNum+=1
    massEjected = m_dot*grain.stepSize*stepNum
    #fuelMass = np.pi*fuel.density*grain.length*((radius[stepNum]**2) - (grain.coreDia** 2))
    #print(radius[stepNum])
    print("\n")

mp.plot(thrust, time, color = "red")

mp.show()







