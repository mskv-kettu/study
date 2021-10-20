import numpy as np
import matplotlib.pyplot as plt

with open("settings.txt", "r") as settings_file:
    settings = [float(i) for i in settings_file.read().split(" ")]
with open("data.txt", "r") as data_file:
    data = np.loadtxt("data.txt", dtype=int)

Time = settings[0]
Voltage = settings[2]
N = data.size
dt = Time / N
data = data * Voltage
time = np.arange(N) * dt

mark = np.linspace(0, N, 500)
markers_on = [mark]

fig, ax = plt.subplots(figsize = (16, 10), dpi = 400)
ax.plot(time, data, color='blue', linewidth=2, markersize=10, markevery=100, marker="*", label = "voltage")

plt.legend()
ax.grid()
mdata = data.max() * 1.1
mtime = time.max() * 1.1
ax.set_ylim(0,mdata)
ax.set_xlim(0,mtime)
ax.minorticks_on()
ax.grid(which='minor', 
        color = 'k', 
        linestyle = ':')
plt.xlabel(u'Time, sec')
plt.ylabel(u'Voltage, V')
plt.title("Obrabotka dannih, graph")
plt.text(0.8 * N*dt,2.2, "Time of charge: {}".format(np.argmax(data) * dt))
plt.text(0.8* N*dt ,2, "Time of discharge: {}".format(Time - np.argmax(data) * dt))

fig.savefig("test.png")
print("done")