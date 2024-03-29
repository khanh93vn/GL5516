"""
Process static calibration data, draw plots and fit model.
Xu ly du lieu ve dac tinh tinh, ve do thi va tim phuong trinh quan he vao ra.
"""

# ----------------------------------------------------------------------------
# Imports

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from scipy.optimize import curve_fit

# ----------------------------------------------------------------------------
# Constants

PATH_DATA_MEASURED = "data/measured.csv"
PATH_DATA_MEASURED_REPEATABILITY = "data/measured_repeatability.csv"
PATH_DATA_CALIBRATION = "data/calibration.csv"

PATH_FIG_IDEAL_LINE = "figures/ideal_straight_line.png"
PATH_FIG_TRANSFER_CURVE = "figures/transfer_curve.png"
PATH_FIG_TRANSFER_CURVE_LIMITED = "figures/transfer_curve_limited.png"
PATH_FIG_NONLINEARITY = "figures/nonlinearity.png"
PATH_FIG_HYSTERESIS = "figures/hysteresis.png"
PATH_FIG_LOG_IO = "figures/log_io.png"
PATH_FIG_LOG_IO_LINE = "figures/log_io_line.png"
PATH_FIG_DISTRIBUTION = "figures/distribution.png"

LABEL_ILLUMINATION = "Light intesity (lux)"
LABEL_RESISTANCE = "Resistance ($\Omega$)"

# ----------------------------------------------------------------------------
# Script

if __name__ == "__main__":
    plt.cla()
    plt.style.use("seaborn")
    
    df = pd.read_csv(PATH_DATA_MEASURED)
    
    I, O1, O2 = df.to_numpy().T

    # ------------------------------------------------------------------------
    # Ve dac tuyen quan he vao ra (characteristic line)
    
    I_min = I[0]
    I_max = I[-1]
    O_min = O1[0]
    O_max = O1[-1]
    
    plt.plot(I, O2, label="O - Decreasing input",
             marker='o', linestyle='dashed', color='b')
    plt.plot(I, O1, label="O - Increasing input",
             marker='o', linestyle='dashed', color='r')
    plt.plot([I_min, I_max], [O_min, O_max],
             label="Ideal straight line",
             linewidth=0.5, color='k')
             
    plt.legend()
    plt.title("Resistance of LDR GL5516")
    plt.xlabel(LABEL_ILLUMINATION)
    plt.ylabel(LABEL_RESISTANCE)
    
    # Luu do thi:
    plt.savefig(PATH_FIG_IDEAL_LINE)
    plt.cla()
    
    # ------------------------------------------------------------------------
    # Do nhay (sensitivity)
    
    # Do nhay:
    K = (O_max - O_min) / (I_max - I_min)
    a = O_max - K * I_max
    
    # Phuong trinh dac tuyen:
    O = lambda I: K*I + a
    
    # ------------------------------------------------------------------------
    # Do phi tuyen (non-linearity)
    N = O2 - O(I) # (lay gia tri cua bang do giam)
    
    # Ve do thi:
    plt.plot(I, N)
    plt.title("Non-linearity")
    plt.xlabel("I")
    plt.ylabel("N")
    
    # Full scale deflection (fsd):
    fsd = O2.max() - O2.min()
    
    # Do phi tuyen cuc dai, tinh theo ty le voi fsd:
    N_max_fsd = np.abs(N).max() / fsd
    
    # Ve do phi tuyen cuc dai:
    plt.plot([I[N.argmin()]]*2, [0, N.min()], linestyle='dashed')
    plt.text(I[N.argmin()] + 10,
             N.min() / 2,
             "$\hatN$")
    
    # Luu do thi:
    plt.savefig(PATH_FIG_NONLINEARITY)
    plt.cla()
    
    # Chep do phi tuyen vao bang du lieu:
    df['N'] = N
    
    # ------------------------------------------------------------------------
    # Do tre (hysteresis)
    H = O1 - O2
    
    # Ve do thi:
    plt.plot(I, H)
    plt.title("Hysteresis")
    plt.xlabel("I")
    plt.ylabel("H")
    
    # Do tre cuc dai, tinh theo ty le voi fsd:
    H_max_fsd = H.max() / fsd
    
    # Ve do tre cuc dai:
    plt.plot([I[H.argmax()]]*2, [0, H.max()], linestyle='dashed')
    plt.text(I[H.argmax()] + 10,
             H.max() / 2,
             "$\hatH$")
    
    # Luu do thi:
    plt.savefig(PATH_FIG_HYSTERESIS)
    plt.cla()
    
    # Chep do tre vao bang du lieu:
    df['H'] = H
    
    # ------------------------------------------------------------------------
    # Phuong trinh vao ra (transfer equation)
    
    # Moi quan he vao-ra tro nen (tuong doi) tuyen tinh sau khi duoc chuyen
    # ve khong gian logarit (theo ly thuyet co the o bat ky co so nao).
    # Chuyen so lieu dau vao va dau ra sang khong gian log (co so e):
    I_log = np.log(I)
    O1_log = np.log(O1)
    O2_log = np.log(O2)
    
    # Ve do thi:
    plt.plot(I_log, O2_log, label="O - Decreasing input",
             marker='o', linestyle='none', color='b')
    plt.plot(I_log, O1_log, label="O - Increasing input",
             marker='o', linestyle='none', color='r')
    plt.legend()
    plt.title("log(O) vs. log(I)")
    plt.xlabel("log(I)")
    plt.ylabel("log(O)")
    
    # Luu do thi:
    plt.savefig(PATH_FIG_LOG_IO)
    
    plt.plot([I_log[0], I_log[-1]],
             [O1_log[0], O1_log[-1]],
             label="O - Expected",
             linewidth=0.5, color='k')
    plt.legend()
    plt.savefig(PATH_FIG_LOG_IO_LINE)
    
    plt.cla()
    
    # Phuong trinh quan he vao-ra:
    #     log(O) = m*log(I) + b
    # =>       O = exp(m*log(I) + b)
    # =>       O = exp(b) * I^m
    # Dat c = exp(b):
    # =>       O = c * I^m
    m = (O1_log[-1] - O1_log[0]) / (I_log[-1] - I_log[0])
    c = np.exp(O1_log[0] - m * I_log[0])
    
    # Theo (tai lieu tham khao) dien tro cua quang tro:
    # R_c = 1/(1/R_co + 1/R_cp)
    # Ta thay:
    # Khi R_co >> R_cp, 1/R_co << 1/R_cp
    # => R_c ~ R_cp = a*phi^-lambda
    # Co dang giong voi phuong trinh tim duoc bang thuc nghiem o tren
    # Dua vao datasheet, ta co duoc R_co = 5e+5 Ohm
    # Ham truyen:
    R_co = 5e+5
    f = lambda I: 1/(1/R_co + 1/(c*I**m))
    
    # Ve do thi:
    x = np.linspace(0, I.max(), 200)
    plt.plot(x, f(x), label="O - Estimated",
             linewidth=0.5, color='k')

    # Gia tri dien tro theo datasheet:
    plt.plot(I, O2, label="O - Decreasing input",
             marker='o', linestyle='none', color='b')
    plt.plot(I, O1, label="O - Increasing input",
             marker='o', linestyle='none', color='r')
    
    plt.plot(0, R_co, label="Dark resistance",
             marker='o', linestyle='none', color='k')
    plt.plot(10, 7.5e+3, label="Resistance at 10 lux",
             marker='o', linestyle='none', color='y')
    plt.legend()
    plt.title("Resistance of LDR GL5516")
    plt.xlabel(LABEL_ILLUMINATION)
    plt.ylabel(LABEL_RESISTANCE)
    # plt.yscale('log')
    
    # Luu do thi:
    plt.savefig(PATH_FIG_TRANSFER_CURVE)
    plt.ylim(0, 10000)
    plt.savefig(PATH_FIG_TRANSFER_CURVE_LIMITED)
    plt.cla()
    
    # ------------------------------------------------------------------------
    # Xu ly du lieu do lap (repeatability)
    
    df_rep = pd.read_csv(PATH_DATA_MEASURED_REPEATABILITY)
    _, O = df_rep.to_numpy().T
    
    # Gia tri trung binh (mean):
    mean = O.mean()
    
    # Do lech chuan (standard deviation):
    std = O.std()
    
    # Ve histogram phan bo du lieu:
    plt.hist(O, bins=50, density=True) # Ve do thi phan bo
    
    # Tinh va ve duong phan bo chuan (normal distribution)
    x = np.linspace(O.min(), O.max(), 100)
    y = np.exp(-(x-mean)*(x-mean)/2/std/std)/np.sqrt(2*np.pi*std*std)
    plt.plot(x, y, linewidth=3)
    
    # Trang tri do thi:
    plt.title("Distribution of LDR GL5516 resistance at 88 lux")
    plt.xlabel(LABEL_RESISTANCE)
    plt.ylabel("Proportions")
    plt.text(np.percentile(O, 99), # Hoanh do cua chu thich
             np.percentile(y, 90), # Tung do cua chu thich
             "$\mu$ = %.2f\n$\sigma$ = %.2f\nN = %d"
             %(mean, std, len(O)))

    # Luu do thi:
    plt.savefig(PATH_FIG_DISTRIBUTION)
    
    # ------------------------------------------------------------------------
    # In/luu du lieu da xu ly
    
    df.to_csv(PATH_DATA_CALIBRATION)
    print("Dac tuyen quan he vao ra: O(I) = KI + a\nK = %.2f\na = %.2f"
          %(K, a))
    print("Do phi tuyen cuc dai: %.0f %%" %(N_max_fsd * 100))
    print("Do tre cuc dai: %.0f %%" %(H_max_fsd * 100))
    