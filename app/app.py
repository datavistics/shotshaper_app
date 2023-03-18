import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


from shotshaper.projectile import DiscGolfDisc

proj_dir = Path(__file__).parents[1]

st.title("Shot Shaper")

disc_selection = [disc_path.stem for disc_path in (proj_dir/'shotshaper'/'discs').glob('*yaml')]

disc_selected = st.sidebar.selectbox("Disc Selection", disc_selection)

d = {
    'dd2': 'Innova Wraith',
    'cd1': 'Innova Firebird',
    'cd5': 'Innova Roadrunner',
    'fd2': 'Innova Fairway Driver',
}

U = 24.2
omega = 116.8
z0 = 1.3
pos = np.array((0,0,z0))
pitch = 15.5
nose = 0.0
roll = 14.7


d = DiscGolfDisc(disc_selected)

U = st.sidebar.slider("Throwing Velocity (m/s)", min_value=0.0, max_value=40.0, value=24.2, step=0.1, help='Fastest Throw on record is ~40m/s by Simon Lizotte')
omega = st.sidebar.slider("Omega", min_value=0.0, max_value=200.0, value=116.8, step=0.1)
z0 = st.sidebar.slider("Height (m)", min_value=0.0, max_value=2.0, value=1.3, step=0.1)
pos = np.array((0,0,z0))
pitch = st.sidebar.slider("Pitch Angle (deg)", min_value=0.0, max_value=90.0, value=15.5, step=0.1)
nose = st.sidebar.slider("Nose Angle (deg)", min_value=0.0, max_value=90.0, value=0.0, step=0.1)
roll = st.sidebar.slider("Roll Angle (deg)", min_value=-90.0, max_value=90.0, value=14.7, step=0.1)

shot = d.shoot(speed=U, omega=omega, pitch=pitch, 
            position=pos, nose_angle=nose, roll_angle=roll)

# Plot trajectory
x,y,z = shot.position

# fig = px.scatter(x,y,title='Drift over Distance')
# fig.update_yaxes(
#     scaleanchor = "x",
#     scaleratio = 1,
#   )
# st.plotly_chart(fig)

fig = plt.figure(1)
plt.plot(x,y)
plt.xlabel('Distance (m)')
plt.ylabel('Drift (m)')
plt.axis('equal')
st.pyplot(fig)


arc,alphas,betas,lifts,drags,moms,rolls = d.post_process(shot, omega)
fig, axes = plt.subplots(nrows=2, ncols=3, dpi=80,figsize=(13,5))

axes[0,0].plot(arc, lifts)
axes[0,0].set_xlabel('Distance (m)')
axes[0,0].set_ylabel('Lift force (N)')

axes[0,1].plot(arc, drags)
axes[0,1].set_xlabel('Distance (m)')
axes[0,1].set_ylabel('Drag force (N)')

axes[0,2].plot(arc, moms)
axes[0,2].set_xlabel('Distance (m)')
axes[0,2].set_ylabel('Moment (Nm)')

axes[1,0].plot(arc, alphas)
axes[1,0].set_xlabel('Distance (m)')
axes[1,0].set_ylabel('Angle of attack (deg)')

axes[1,1].plot(arc, shot.velocity[0,:])
axes[1,1].plot(arc, shot.velocity[1,:])
axes[1,1].plot(arc, shot.velocity[2,:])
axes[1,1].set_xlabel('Distance (m)')
axes[1,1].set_ylabel('Velocities (m/s)')
axes[1,1].legend(('u','v','w'))

axes[1,2].plot(arc, rolls)
axes[1,2].set_xlabel('Distance (m)')
axes[1,2].set_ylabel('Roll rate (rad/s)')
plt.tight_layout()


st.pyplot(fig)


