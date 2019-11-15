import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

res_label = "Resistance ($\Omega$)"

# -----------------------------------------------------------------------------
# Constants

DATA_PATH = "data/calibration.csv"
FIG_CURVE_PATH = "figures/IO_curve.png"
FIG_LOG_PATH = "figures/IO_curve_log.png"
FIG_NONLIN_PATH = "figures/nonlinearity.png"
FIG_HYST_PATH = "figures/hysteresis.png"

# -----------------------------------------------------------------------------
# Functions

def decorate_ldr_plot(title,
                      xlabel="Light intesity (lux)",
                      ylabel=res_label,
                      xlog=False, ylog=False):
    """Decorate intensity-resistance plot"""
    plt.title(title)
    if xlog:
        plt.xscale('log')
    if ylog:
        plt.yscale('log')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def set_figure_size(x, y):
    fig = plt.gcf()
    fig.set_size_inches(x, y)

def set_ticks(scale, xaxis=False, yaxis=False):
    ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*scale))
    ax = plt.gca()
    if xaxis:
        ax.xaxis.set_major_formatter(ticks)
    if yaxis:
        ax.yaxis.set_major_formatter(ticks)