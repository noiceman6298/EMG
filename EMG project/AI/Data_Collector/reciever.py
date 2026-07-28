import tkinter as tk
import serial
import csv
import os
import numpy as np
import pandas as pd

ser = serial.Serial('COM9', 115200)

x = []
y = None
data = []
session_rest = 0
session_moving = 0
session_id = 0
sample_counter = 0

def compute_features(w):
    w = np.array(w)
    rms = np.sqrt(np.mean(w**2))
    std = np.std(w)
    minimum = np.min(w)
    maximum = np.max(w)
    mav = np.mean(np.abs(w))
    wfl = np.sum(np.abs(np.diff(w)))
    aac = np.mean(np.abs(np.diff(w)))
    zc = np.sum(np.diff(np.sign(w)) != 0)
    threshold = np.std(w) * 0.2
    wamp = np.sum(np.abs(np.diff(w)) > threshold)
    afb = np.max(np.abs(w))
    return [rms, std, minimum, maximum, mav, wfl, aac, zc, wamp, afb]

def get_file_counts():
    if os.path.exists('emg_data.csv') and os.path.getsize('emg_data.csv') > 0:
        df = pd.read_csv('emg_data.csv')

        counts = df['label'].value_counts()

        rest_count = counts.get(0, 0)
        moving_count = counts.get(1, 0)

        if 'session' in df.columns:
            rest_sessions = df[df['label'] == 0]['session'].nunique()
            moving_sessions = df[df['label'] == 1]['session'].nunique()
        else:
            rest_sessions = 0
            moving_sessions = 0

        return rest_count, moving_count, rest_sessions, moving_sessions

    return 0, 0, 0, 0

def get_next_session_id():
    if os.path.exists('emg_data.csv') and os.path.getsize('emg_data.csv') > 0:
        df = pd.read_csv('emg_data.csv')
        if 'session' in df.columns:
            return int(df['session'].max()) + 1
    return 1

def update_counts():
    file_rest, file_moving, rest_sessions, moving_sessions = get_file_counts()

    current_rest = 0
    current_moving = 0

    if y == 0:
        current_rest = len(x)
    elif y == 1:
        current_moving = len(x)

    current_rest_sessions = rest_sessions
    current_moving_sessions = moving_sessions

    if y == 0 and len(x) > 0:
        current_rest_sessions += 1

    if y == 1 and len(x) > 0:
        current_moving_sessions += 1

    count_label.config(
        text=
        f"Current Recording\n"
        f"REST: {current_rest}   MOVING: {current_moving}\n\n"
        f"Dataset\n"
        f"REST: {file_rest} ({current_rest_sessions} sessions)\n"
        f"MOVING: {file_moving} ({current_moving_sessions} sessions)"
    )

def start_rest():
    global y, data, session_id

    if rest.cget("text") == "REST":
        session_id = get_next_session_id()

        y = 0
        data = []
        window.clear()
        rest.config(text="Recording REST")
    else:
        save()
        y = None
        rest.config(text="REST")

def start_moving():
    global y, data, session_id

    if moving.cget("text") == "MOVING":
        session_id = get_next_session_id()

        y = 1
        data = []
        window.clear()
        moving.config(text="Recording MOVING")
    else:
        save()
        y = None
        moving.config(text="MOVING")

def save():
    global session_rest, session_moving
    file_exists = os.path.exists('emg_data.csv') and os.path.getsize('emg_data.csv') > 0
    with open('emg_data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            header = [
                'rms', 'std', 'min', 'max', 'mav',
                'wfl', 'aac', 'zc', 'wamp', 'afb'
            ]

            header += [f'raw_{i}' for i in range(100)]
            header += ['label', 'session']

            writer.writerow(header)
        data = [features + [y, session_id] for features in x]
        writer.writerows(data)
        
        session_rest = 0
        session_moving = 0

    x.clear()
    update_counts()

window = []

def read_serial():
    global window, sample_counter
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        try:
            sample = float(line)
            if y is not None:
                window.append(sample)

                if len(window) > 100:
                    window.pop(0)

                sample_counter += 1

                if len(window) == 100 and sample_counter >= 10:
                    sample_counter = 0

                    features = compute_features(window)
                    features.extend(window.copy())

                    x.append(features)

                    update_counts()

        except:
            pass
    root.after(2, read_serial)

root = tk.Tk()
rest = tk.Button(root, text="REST", command=start_rest)
moving = tk.Button(root, text="MOVING", command=start_moving)
count_label = tk.Label(root, text="Session  —  REST: 0   MOVING: 0\nTotal     —  REST: 0   MOVING: 0", font=("Arial", 14))

rest.pack()
moving.pack()
count_label.pack(pady=10)

update_counts()
root.after(2, read_serial)
root.mainloop()