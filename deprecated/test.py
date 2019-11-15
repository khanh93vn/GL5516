import numpy as np
import matplotlib.pyplot as plt

f1 = lambda x: 18280.96075851505*(x+1e-15)**(-0.6057442348870001)
f2 = lambda x: -1069.6144984118494 * x + 621852.9411764706

x = np.linspace(25, 125, 30)

plt.plot(x, f1(x), label='ham mu')
plt.plot(x, f2(x), label='tuyen tinh')
plt.legend()
plt.show()