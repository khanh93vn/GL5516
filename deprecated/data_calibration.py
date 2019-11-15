import numpy as np
import pandas as pd

from utils import *

# -----------------------------------------------------------------------------
# Preprocessing

# Declare paths:
input_paths = ["raw_data/fbuffers.csv",
               "raw_data/rbuffers.csv"]
output_path = "processed_data/calibration.csv"
fig_IO_path = "figures/IO_curve.png"
fig_log_path = "figures/IO_curve_log.png"
fig_nonlin_path = "figures/nonlinearity.png"
fig_hyst_path = "figures/hysteresis.png"

# Read data-frames:
buffers, rbuffers = [pd.read_csv(path) for path in input_paths]

# Drop duplicated index column:
buffers = buffers.drop(buffers.columns[0], axis=1)
rbuffers = rbuffers.drop(rbuffers.columns[0], axis=1)

# Put data into arrays:
I = np.concatenate((np.array(buffers.columns[:-1]),
                    np.array(rbuffers.columns))).astype(int)

Os = np.concatenate((buffers.to_numpy()[:, :-1], # Remove duplicates.
                     rbuffers.to_numpy()), axis=1)

# Compute output means:
O = Os.mean(axis=0)

# -----------------------------------------------------------------------------
# Linear model and sensitivity

# Compute ideal straight line:
K = (O[10] - O[0]) / (I[10] - I[0])
a = O[0] - K*I[0]

# Plot data:
plt.cla()
x = np.linspace(0, 600, 20)
plt.plot(x, K*x + a,
         label="Ideal straight line")
plt.plot(I, O,
         color='r', marker='o',
         label="IO curve")
plt.fill(I, O, fill=False, color='r')
plt.legend()
decorate_ldr_plot(title="Resistance of light-dependent resistor")
set_figure_size(8.0, 6.0)
plt.savefig(fig_IO_path)

plt.yscale('log')
plt.xscale('log')
plt.title("Resistance of light-dependent resistor (log-scale)")
plt.savefig(fig_log_path)

# Non-linearity:
N = np.abs(O - (K*I + a))
max_nl = N.max() / (O.max() - O.min())
plt.cla()
plt.plot(I, N)
decorate_ldr_plot("Non-linearity", xlabel="I", ylabel="N(I)")
set_figure_size(8.0, 6.0)
plt.savefig(fig_nonlin_path)

# Hysteresis:
H = O[:11] - O[-1:9:-1]
max_h = (H.max() - H.min()) / (O.max() - O.min())
plt.cla()
plt.plot(I[:11], H)
decorate_ldr_plot("Hysteresis", xlabel="I", ylabel="H(I)")
set_figure_size(8.0, 6.0)
plt.savefig(fig_hyst_path)

# Save data:
df = pd.DataFrame((I, O)).T
df.columns = ['I', 'O']
df.to_csv(output_path, index=False)

# -----------------------------------------------------------------------------
# IO mapping

# Proposed model: O = exp(K*log(I+1e-20) + a) = exp(a) * (I+1e-20)^K
l = 1e-20
K, a = np.polyfit(np.log(I+l), np.log(O), 1)

# -----------------------------------------------------------------------------