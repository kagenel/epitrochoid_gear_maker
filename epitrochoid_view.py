#coding: utf-8
# 
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


i = 9   # 減速比
tp = i+1 # 外ピンの数(MAX)
tc = tp - 1 # 曲線板の歯数(最大の減速比)
e = 2 # 偏心距離
r = 30 # 外ピン配置半径
#i = tc / (tp - tc)    # 減速比

print(i)
D = 20*r # サンプリング点

# パラメータの決定
r2 = r / (1 + i)
r1 = i * r2
rd = e

# 内ピン
rout = 4       # 内ピンの半径
rin = rout + e # 内ピンを通す穴の半径

rin_cam = r/2 + rout/2

print(rout)
print(rin)
print(rin_cam)

if rd > r2:
    print("rd が大きすぎる")

fig, ax = plt.subplots()

def update(num):

    for i in range(tp):
        pins[i].set_data(rd * np.cos(theta) + x_move[i][num] + en_x_move[num], rd * np.sin(theta) + y_move[i][num] + en_y_move[num])
    
    cam.set_data(2*np.cos(theta) + en_x_move[num], 2*np.sin(theta) + en_y_move[num])
    en.set_data(en_x + en_x_move[num], en_y + en_y_move[num])
 
    #cam_mount.set_data(mount_x + en_x_move[0], mount_y + en_y_move[0])

    for i in range(6):
        in_rings[i].set_data(rin_x + x_move2[i][0], rin_y + y_move2[i][0])
        in_pins[i].set_data(rout_x + x_move2[i][0] + en_x_move[num], rout_y + y_move2[i][0] + en_y_move[num])
    in_com.set_data(rcom_x + en_x_move[num], rcom_y + en_y_move[num])
     
    theta_str = r'$\theta=$'
    ax.set_title(theta_str + str(theta[num]/np.pi)[:4] + str(r' $\pi$'))

def anime():
    ani = animation.FuncAnimation(fig, update, D, interval=100)
    #ani.save('episaikuroid.mp4', writer="ffmpeg",dpi=100)
    plt.show()


ax.grid()
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_aspect('equal')

# plot data
theta = np.linspace(0, 2*np.pi,D)

# エピコロイド曲線
x = (r1 + r2)*np.cos(theta) - rd * np.cos((r1+r2)/r2*theta)
y = (r1 + r2)*np.sin(theta) - rd * np.sin((r1+r2)/r2*theta)
plt.plot(x, y, 'k-', lw=1)

# エピトロコイド平行曲線
dx = (r1 + r2) * (-np.sin(theta) + (rd/r2) * np.sin((r1+r2)/r2*theta))
dy = (r1 + r2) * (np.cos(theta) - (rd/r2) * np.cos((r1+r2)/r2*theta))

x2 = [x[i] + (rd/(np.sqrt(dx[i]**2 + dy[i]**2)) * -dy[i]) for i in range(D)]
y2 = [y[i] + (rd/(np.sqrt(dx[i]**2 + dy[i]**2)) * dx[i]) for i in range(D)]

plt.plot(x2, y2, 'y-', lw=2)

plt.plot((r1 + r2)*np.cos(theta), (r1 + r2)*np.sin(theta), 'k-', linestyle='dashed', lw=1) # エピコロイド曲線を書く小円の中心軌道

# 外ピン
pins = []
for i in range(tp):
    pin, = plt.plot([], [], 'r-', lw=2)
    pins.append(pin)

pin_theta = [(np.linspace(0, 2*np.pi/(i+1),D)) + 2*np.pi*k/tp for k in range(tp)]
x_move = [(r)*np.cos(pin_theta[i]) for i in range(tp)]
y_move = [(r)*np.sin(pin_theta[i]) for i in range(tp)]

# 動作確認
cam, = plt.plot([], [], 'c-', lw=2)  # 偏心距離の軌跡（入力軸）
en, = plt.plot([], [], 'r-', lw=1)   # 外ピンの動き（点）
#gawa, = plt.plot([], [], 'r-', linestyle='dashed', lw=1) # 外ピンの動き（円柱）
cam_mount, = plt.plot([], [], 'k-', lw=2)

# 軌道生成
en_x = (r)*np.cos(theta)
en_y = (r)*np.sin(theta)

en_x_move = -e*np.cos(theta)
en_y_move = -e*np.sin(theta)

mount_x = (r+e)/4*np.cos(theta)
mount_y = (r+e)/4*np.sin(theta)

# 内ピン
in_rings = []
in_pins = []
for i in range(6):
    in_ring, = plt.plot([], [], 'k-', lw=2)
    in_pin, = plt.plot([], [], 'g-', lw=2)
    in_rings.append(in_ring)
    in_pins.append(in_pin)

pin_theta2 = [(np.linspace(0, 2*np.pi/(i+1),D)) + 2*np.pi*k/6 for k in range(6)]
x_move2 = [(rin_cam)*np.cos(pin_theta2[i]) for i in range(6)]
y_move2 = [(rin_cam)*np.sin(pin_theta2[i]) for i in range(6)]

rout_x = rout*np.cos(theta)
rout_y = rout*np.sin(theta)
rin_x = rin*np.cos(theta)
rin_y = rin*np.sin(theta)

in_com, = plt.plot([], [], 'g-', lw=1)
rcom_x = rin_cam*np.cos(theta)
rcom_y = rin_cam*np.sin(theta)

plt.xlim(-2*r, 2*r)
plt.ylim(-2*r, 2*r)

anime()