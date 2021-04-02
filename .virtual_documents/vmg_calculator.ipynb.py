get_ipython().run_line_magic("matplotlib", " inline")
from datetime import datetime
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns 
sns.set(style="darkgrid")


def calculate_vmg_target_speed(min_twa, max_twa, log=True, target_speed=100):
    twa_dist = {}
    distance = 100
    for twa_deg in range(min_twa, max_twa+1):
        twa_rad = np.deg2rad(twa_deg)
        prev_distance = distance
        distance = round(np.abs(np.cos(twa_rad)**-1)*100, 2)
        extra = round(distance - prev_distance, 2)
        if log==True:
            print(f"TWA {twa_deg}: {distance}% distance required (+{extra})")
        twa_dist[twa_deg] = distance
        
    for twa_deg in twa_dist:
        req_speed = round((twa_dist[twa_deg]/100) * target_speed, 2)
        
    return twa_dist


# -- NB: Too many graphs causes jupyter to hang --
min_twa = 25
max_twa = 65

twa_dist = calculate_vmg_target_speed(min_twa, max_twa)
twa = list(twa_dist.keys())
distance = list(twa_dist.values())

fig, ax = plt.subplots()
plt.ylim([100, 300])
ax.plot(twa, distance)
ax.set_title("Distance vs TWA for same VMG")
ax.set_ylabel('Distance')
ax.set_xlabel('TWA')
print()


# Polar Diagram

csv_path = 'boat_figaro3.csv'
# csv_path = 'boat_Imoca2015.csv'

polar_data = pd.read_csv(csv_path, delimiter=';', header=0)
polar_data.add_suffix('_kts')    
polar_data.head()

twa_tws = polar_data.loc[:,'TWA\TWS']
ten_kts = polar_data.loc[:,'10']
twenty_kts = polar_data.loc[:,'20']
thirty_kts = polar_data.loc[:,'30']

theta = np.deg2rad(twa_tws)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

# blue
ax.plot(theta, ten_kts)
# orange
ax.plot(theta, twenty_kts)
# green
ax.plot(theta, thirty_kts)

# ax.set_rmax(20)
# Fewer radial ticks
# ax.set_rticks([4, 8, 12, 16, 20])  
# Move radial labels away from plotted line
ax.set_rlabel_position(270)  
ax.grid(True)

# ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()


# def calculate_vmg(polar):
#     twa_dist = {}
    
   
    
#     for (twa_deg, speeds) in polar[1:].iteritems():
#         #print('Colunm Name : ', columnName)
#         #print('Column Values : ', columnData.values)
#         twa_rad = np.deg2rad(float(twa_deg))
#         twa_dist[twa_deg] = []
#         for speed in speeds.values:  
#             vmg = np.abs(np.cos(twa_rad)**-1)*speed
#             vmg_rounded = round(vmg, 2)
#             twa_dist[twa_deg].append(vmg_rounded)
#     return twa_dist

# # calculate_vmg(theta, ten_kts)
# calculate_vmg(polar_data)

# for (columnName, columnData) in df.iteritems():
#     print('Colunm Name : ', columnName)
#     print('Column Values : ', columnData.values)


twa_dist = {}
for twa_deg, speed in zip(twa_tws, ten_kts):
    #print(f"twa_deg: {twa_deg}, speed: {speed}")
    twa_rad = np.deg2rad(float(twa_deg))
    #print(f"rads: {twa_rad}")
    vmg = speed / np.abs(np.cos(twa_rad)**-1) 
    vmg_rounded = round(vmg, 2)
    twa_dist[twa_deg] = vmg_rounded


twa = list(twa_dist.keys())
distance = list(twa_dist.values())

fig, ax = plt.subplots()
ax.plot(twa, distance)
ax.set_title("VMG vs TWA")
ax.set_ylabel('VMG')
ax.set_xlabel('TWA')
print()


# 90 degrees is elem 12
upwind_twas = list(twa_dist.keys())[:12]
upwind_vmgs = list(twa_dist.values())[:12]
downwind_twas = list(twa_dist.keys())[12:]
downwind_vmgs = list(twa_dist.values())[12:]

max_vmg_up = max(upwind_vmgs)
max_vmg_up_twa = upwind_twas[upwind_vmgs.index(max(upwind_vmgs))]
max_vmg_down = max(downwind_vmgs)
max_vmg_down_twa = downwind_twas[downwind_vmgs.index(max(downwind_vmgs))]

print(f"max vmg up {max_vmg_up} at {max_vmg_up_twa}")
print(f"max vmg down {max_vmg_down} at {max_vmg_down_twa}")



