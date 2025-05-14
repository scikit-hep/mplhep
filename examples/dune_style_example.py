"""
DUNE style example for mplhep.
"""

import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

# Set the style
hep.style.use(hep.style.DUNE)

# Create some sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.exp(-0.2 * x)

# Create a figure
fig, ax = plt.subplots(figsize=(10, 8))

# Plot the data
ax.plot(x, y1, label=r'$\sin(x)$')
ax.plot(x, y2, label=r'$\cos(x)$')
ax.plot(x, y3, label=r'$\sin(x) \cdot e^{-0.2x}$')

# Add a legend
ax.legend(frameon=False)

# Add axis labels
ax.set_xlabel('x [a.u.]')
ax.set_ylabel('f(x) [a.u.]')

# Add experiment labels
hep.dune.label(label="Preliminary", data=False)

# Alternative label styles
# hep.dune.preliminary()
# hep.dune.wip()
# hep.dune.simulation()
# hep.dune.simulation_side()
# hep.dune.official()

# Add a corner label
hep.dune.corner_label("Example plot")

# Use only DUNE logo colors
# hep.dune.set_dune_logo_colors()

# Save the figure
plt.savefig('dune_style_example.png', dpi=300, bbox_inches='tight')

# Show the figure
plt.show()