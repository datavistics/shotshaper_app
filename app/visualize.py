import math

import numpy as np
import plotly.graph_objects as go
from plotly.colors import sequential
from plotly.subplots import make_subplots
from stl.mesh import Mesh


def get_stl(stl_file):
    """
    Taken from https://community.plotly.com/t/view-3d-cad-data/16920/9
    """
    stl_mesh = Mesh.from_file(stl_file)
    return stl_mesh


def visualize_disc(stl_mesh, x_angle, y_angle, z_angle):
    """
    Taken from https://community.plotly.com/t/view-3d-cad-data/16920/9
    """
    stl_mesh.rotate([1, 0, 0], math.radians(x_angle))
    stl_mesh.rotate([0, 1, 0], math.radians(y_angle))
    stl_mesh.rotate([0, 0, 1], math.radians(z_angle))

    p, q, r = stl_mesh.vectors.shape  # (p, 3, 3)
    # the array stl_mesh.vectors.reshape(p*q, r) can contain multiple copies of the same vertex;
    # extract unique vertices from all mesh triangles
    vertices, ixr = np.unique(stl_mesh.vectors.reshape(p * q, r), return_inverse=True, axis=0)
    I = np.take(ixr, [3 * k for k in range(p)])
    J = np.take(ixr, [3 * k + 1 for k in range(p)])
    K = np.take(ixr, [3 * k + 2 for k in range(p)])
    #     facecolor = np.vectorize(get_stl_color)(stl_mesh.attr.flatten())
    x, y, z = vertices.T
    trace = go.Mesh3d(x=x, y=y, z=z, i=I, j=J, k=K)
    # optional parameters to make it look nicer
    trace.update(flatshading=True, lighting_facenormalsepsilon=0, lighting_ambient=0.7)

    fig = go.Figure(trace)
    fig.update_layout(
            scene=dict(
                    xaxis=dict(nticks=4, range=[-0.11, 0.11], ),
                    yaxis=dict(nticks=4, range=[-0.11, 0.11], ),
                    zaxis=dict(nticks=4, range=[-0.11, 0.11], ), ))
    return fig


def get_plot(x, y, z, reverse):
    xm = np.min(x) - 1.5
    xM = np.max(x) + 1.5
    ym = -5
    yM = np.max(y) + 1.5
    N = len(x)

    # Create figure
    # fig = make_subplots(rows=1, cols=2)
    fig = go.Figure(
            data=[go.Scatter(x=x, y=y,
                             mode="lines",
                             line=dict(width=1, color='black')),

                  go.Scatter(x=x, y=y,
                             mode="markers", marker_colorscale=sequential.Peach,
                             marker=dict(color=z, size=3, showscale=True), ),
                  ],
            layout=go.Layout(
                    xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
                    yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
                    title_text="Flight Path", hovermode="closest",
                    updatemenus=[dict(
                            type="buttons",
                            buttons=[
                                dict(
                                        label="Play",
                                        method="animate",
                                        args=[None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]
                                        ),
                                dict(
                                        label="Pause",
                                        method="animate",
                                        args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate",
                                                       "transition": {"duration": 0}}]
                                        )
                                ],
                            showactive=False,
                            x=0.05,
                            y=0.05
                            )]),
            frames=[go.Frame(
                    data=[go.Scatter(
                            x=[x[k]],
                            y=[y[k]],
                            mode="markers",
                            marker=dict(color="red", size=10))])
                for k in range(N)]
            )
    if reverse:
        fig.update_xaxes(autorange="reversed")
    fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
            )

    # Add green rectangle at the bottom of the plot
    fig.update_layout(
            shapes=[dict(type="rect", xref="x", yref="y",
                         x0=-1, y0=0, x1=1, y1=-4, fillcolor="gray",
                         opacity=1, layer="below")],
            plot_bgcolor="green",
            )

    return fig
