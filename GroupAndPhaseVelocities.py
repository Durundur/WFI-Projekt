import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.widgets import TextBox



######################
#starting values

a1 = 5
k1 = 17
freq1 = 7
a2 = 3
k2 = 13
freq2 = 7

######################


x = np.linspace(0,6,300)
fig = plt.figure()

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.6)
fig.set_size_inches(11,7)

ax1=plt.subplot(411)
ax2=plt.subplot(412)
ax3=plt.subplot(413)


ax1.set_xlim([0,6])
ax1.set_ylim([-10,10])
ax1.set_title(r'$f_1 (t) = A_1  \cos(k_1 x - \omega_1 t)$')


ax2.set_xlim([0,6])
ax2.set_ylim([-10,10])
ax2.set_title('$f_2 (t) = A_2  \cos(k_2 x - \omega_2 t)$')


ax3.set_xlim([0,6])
ax3.set_ylim([-21,21])
ax3.set_title(r'$f_3 (t) = f_1 (t) + f_2 (t) = (A_1 + A_2 )\cos(k_{mod} x - \omega_{mod} t) \cos(k_{śr} x - \omega_{śr} t)  $')
ax3.set_title('prędkość fazowa', loc='right',color='r')
ax3.set_title('prędkość grupowa', loc='left', color = 'g')




ax1.grid()
ax2.grid()
ax3.grid()

ln1, = ax1.plot([],[])
ln2, = ax2.plot([],[])
ln3, = ax3.plot([],[])
obw31, = ax3.plot([],[], "--", color='grey',linewidth=0.5)
obw32, = ax3.plot([],[], "--", color='grey', linewidth=0.5)
pv1, = ax1.plot([],[], "ro")
pv2, = ax2.plot([],[], "ro")
pv3, = ax3.plot([],[], "ro")
gv3, = ax3.plot([],[], "go")


ax5=plt.axes([.25,.1,.15,.01])
ax6=plt.axes([.25,.15,.15,.01])
ax7=plt.axes([.25,.2,.15,.01])


sfreq1 = Slider(ax5, r'$f_1 $', .1, 7.0, valinit=freq1, valstep=.1)
samp1 = Slider(ax6, r'$A_1 $', .1, 10.0, valinit=a1, valstep=.1)
sk1 = Slider(ax7, r'$k_1 $', .1, 20.0, valinit=k1, valstep=.1)



ax7=plt.axes([.65,.1,.15,.01])
ax8=plt.axes([.65,.15,.15,.01])
ax9=plt.axes([.65,.2,.15,.01])
ax10=plt.axes([.25,.25,.25,.03])
ax11=plt.axes([.65,.25,.25,.03])


sfreq2 = Slider(ax7, r'$f_2 $', 0.1, 7.0, valinit=freq2,valstep=.1)
samp2 = Slider(ax8, r'$A_2 $', 0.1, 10.0, valinit=a2,valstep=.1)
sk2 = Slider(ax9, r'$k_2 $', 0.1, 20.0, valinit=k2,valstep=.1)

ax10 = TextBox(ax10,'prędkosc grupowa = ')
ax11 = TextBox(ax11,'prędkosc fazowa = ')





def init():
    ln1.set_data([], [])
    ln2.set_data([], [])
    ln3.set_data([], [])
    obw31.set_data([],[])
    obw32.set_data([],[])
    pv1.set_data([],[])
    pv2.set_data([],[])
    pv3.set_data([],[])
    gv3.set_data([],[])
    return ln1, ln2,ln3,obw31,obw32, pv1,pv2,pv3,gv3

def animate(f):
    w1 = 2 * np.pi * freq1
    w2 = 2 * np.pi * freq2
    a3 = a1 + a2
    wmod = 0.5 * (w1 - w2)
    wsr = 0.5 * (w1 + w2)
    kmod = 0.5 * (k1 - k2)
    ksr = 0.5 * (k1 + k2)

    def update1(val):
        global a1
        a1 = samp1.val
        global freq1
        freq1 = sfreq1.val
        global k1
        k1 = sk1.val
        global a2
        a2 = samp2.val
        global freq2
        freq2 = sfreq2.val
        global k2
        k2 = sk2.val
        ax10.set_val(wmod / kmod)
        ax11.set_val(wsr / ksr)

    def f1(x, t):
        return a1 * np.cos(k1 * x - w1 * t)

    def f2(x, t):
        return a2 * np.cos(k2 * x - w2 * t)

    def f3(x, t):
        return a3 * np.cos(kmod * x - wmod * t) * np.cos(ksr * x - wsr * t)


    ##times
    dt = 50
    frame1 = int(k1 * dt / freq1)

    frame2 = int(k2 * dt / freq2)

    w33 = wmod / np.pi
    if(w33==0): w33=1
    frame3 = int(kmod * dt * 2 / w33)
    w44 = wsr / np.pi
    frame4 = int(ksr * dt * 2 / w44)

    t1 = (f%frame1)/dt
    t2 = (f%frame2)/dt
    t3 = (f%frame3)/dt
    t4 = (f%frame4)/dt
    y1 = f1(x,t1)
    y2 = f2(x,t2)
    y3= f3(x,t4)

    ##plots
    obw1=a3*np.cos(kmod*x-wmod*t4)
    obw2 = obw1*(-1)
    pv1x = t1*w1/k1
    pv1y = f1(pv1x,t1)
    pv2x = t2*w2/k2
    pv2y = f2(pv2x,t2)

    gv3x = t3*wmod/kmod
    gv3y = a3*np.cos(kmod*gv3x-wmod*t4)

    pv3x = t4*wsr/ksr
    pv3y = f3(pv3x,t4)

    ln1.set_data((x,y1))
    ln2.set_data((x,y2))
    ln3.set_data((x,y3))
    obw31.set_data((x,obw1))
    obw32.set_data((x,obw2))
    pv1.set_data((pv1x, pv1y))
    pv2.set_data((pv2x,pv2y))
    pv3.set_data((pv3x,pv3y))
    gv3.set_data((gv3x,gv3y))

    ##sliders update
    sfreq1.on_changed(update1)
    samp1.on_changed(update1)
    sk1.on_changed(update1)
    sfreq2.on_changed(update1)
    samp2.on_changed(update1)
    sk2.on_changed(update1)

    update1(1)
    return ln1,ln2,ln3,obw31,obw32, pv1, pv2,pv3,gv3

anim = FuncAnimation(fig,animate, interval=20, blit=True)
plt.show()




