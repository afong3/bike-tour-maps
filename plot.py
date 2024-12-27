from ridge_map import RidgeMap
import numpy as np
from matplotlib import pyplot as plt


def overlay_tests():
    # Define bounding box
    bbox = (19.668274, 42.508718, 20.190124, 42.821543)  # (min_lon, min_lat, max_lon, max_lat)
    rm = RidgeMap(bbox)

    # Get elevation data and preprocess
    values = rm.get_elevation_data(num_lines=150)
    values = rm.preprocess(
        values=values,
        lake_flatness=2,
        water_ntile=10,
        vertical_ratio=180,
    )

    # Configurable row for points
    y = 149  # Row index for the scatter points
    x_values = np.arange(0, values.shape[1], 1)  # Select points every 10 units in x

    # Prepare points for scatter plot
    scatter_x = x_values
    scatter_y = values[y, x_values]  # Elevation values at the selected x coordinates
    line_x, line_y = scatter_x, scatter_y

    # Plot the map
    ax = rm.plot_map(
        values=values,
        label="Montenegro",
        label_y=0.1,
        label_x=0.55,
        label_size=40,
        linewidth=1,
    )

    # # Plot line through the points
    ax.plot(
        line_x, (line_y + (-6 * y)) ,  # Offset y-values slightly for visibility
        color='red', linewidth=2, label=f"Highlighted Line (Row {y})", zorder = y + 1, alpha=0.4
    )

    test_x = 50

    idx = 0
    for point_x, point_y in zip(np.repeat(test_x, values.shape[0]), values[:, test_x] + np.arange(start = 0, stop = -6 * (values.shape[0]), step = -6)):
        ax.scatter(
            point_x, point_y,
            color = 'green', s = 1, zorder = idx
        )
        idx +=1
    # Display the plot

    ax.xaxis.set_visible(True)
    ax.yaxis.set_visible(True)
    plt.show()

def main():
    RidgeMap().plot_map()
    plt.show()

if __name__ == "__main__":
    overlay_tests()