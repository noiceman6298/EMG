import serial
import pickle
import tkinter as tk
import numpy as np

ser = serial.Serial('COM9', 115200)

with open(r'', 'rb') as f:
    model = pickle.load(f)

root = tk.Tk()
label = tk.Label(root, text="...", font=("Arial", 48))
label.pack(padx=40, pady=40)

window = []
history = []

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

    threshold = 0.01
    wamp = np.sum(np.abs(np.diff(w)) > threshold)

    afb = np.max(np.abs(w[:10]))

    return [rms, std, minimum, maximum, mav, wfl, aac, zc, wamp, afb]

def read_serial():
    global window

    while ser.in_waiting:
        try:
            sample = float(ser.readline().decode().strip())
            window.append(sample)

            if len(window) == 100:

                features = compute_features(window)
                features.extend(window)

                prediction = model.predict([features])[0]

                history.append(prediction)

                if len(history) > 5:
                    history.pop(0)

                vote = round(sum(history) / len(history))
            
            


                prob = model.predict_proba([features])[0]

                label.config(
                    text=f"{'MOVING' if prob[1] > 0.5 else 'REST'}\n"
                        f"{max(prob):.1%}"
                )

        except Exception as e:
            print(e)

    root.after(1, read_serial)

root.after(1, read_serial)
root.mainloop()
