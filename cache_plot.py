import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("134B_ms - Sheet1.csv")
names = df['Way'].values
x = np.arange(len(names))
w = 0.3
plt.bar(x-w, df['exclusive'].values, width=w, label='exclusive')
plt.bar(x, df['non-inclusive'].values, width=w, label='non-inclusive')
plt.bar(x+w, df['inclusive'].values, width=w, label='inclusive')
plt.ylim([0,100])
plt.xticks(x, names)
plt.tight_layout()
plt.xlabel('Inclusiveness')
plt.ylabel('MISSRATE')
plt.title("TRACE_134B")
plt.savefig("Barplots.png", bbox_inches="tight")
plt.legend()
plt.show()
