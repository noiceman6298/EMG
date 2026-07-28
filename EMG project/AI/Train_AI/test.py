import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from matplotlib.widgets import Button  # Added for the button widget

# 1. Load data
df = pd.read_csv(r'C:\Users\alifa\OneDrive\Documents\.vscode\VS CODE CODE\EMG project\AI\Data_Collector\emg_data.csv')

features = ['rms', 'std', 'min', 'max', 'mav', 'wfl', 'aac', 'zc', 'wamp', 'afb']
"""
# 2. Scale the features globally (Keeping original DataFrame intact)
SC = MinMaxScaler()
df_scaled = df.copy()
df_scaled[features] = SC.fit_transform(df[features])

# 3. Interactive plotting setup
plt.ion()
fig, ax = plt.subplots(figsize=(8, 5))

# --- BUTTON SETUP ---
# Adjust plot position to make room for a button at the bottom
plt.subplots_adjust(bottom=0.2)
ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])  # [left, bottom, width, height]
btn_next = Button(ax_button, 'Next')

# State variable to track clicks
class IndexTracker:
    def __init__(self):
        self.clicked = False
    def next_plot(self, event):
        self.clicked = True

tracker = IndexTracker()
btn_next.on_clicked(tracker.next_plot)
# --------------------

# Loop through and plot each scaled feature
for feature in features:
    ax.clear()

    # Filter and plot histograms using the scaled dataframe
    ax.hist(df_scaled[df_scaled.label == 0][feature], bins=30, alpha=0.5, label="Rest")
    ax.hist(df_scaled[df_scaled.label == 1][feature], bins=30, alpha=0.5, label="Moving")

    ax.set_title(f"Scaled Feature: {feature.upper()}")
    ax.set_xlabel(feature)
    ax.set_ylabel("Count")
    ax.legend()

    plt.draw()
    
    # Wait until the user explicitly clicks the "Next" button
    tracker.clicked = False
    while not tracker.clicked:
        plt.pause(0.1)  # Keeps window responsive to mouse clicks but ignores keyboard Enter

plt.ioff()
plt.close()
print("Visualization finished.")
"""
import matplotlib.pyplot as plt

print(df.groupby("label")[['rms', 'std', 'mav', 'wfl', 'aac', 'zc', 'wamp']].mean())

for col in ['rms', 'std', 'mav', 'wfl']:
    plt.figure()
    plt.hist(df[df.label == 0][col], bins=30, alpha=0.5, label="Rest")
    plt.hist(df[df.label == 1][col], bins=30, alpha=0.5, label="Moving")
    plt.title(col)
    plt.legend()
    plt.show()