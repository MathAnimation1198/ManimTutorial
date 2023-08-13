from manimlib.imports import *

#use this command to run this file in cairo backened
#python -m manim Projectile_cairo_backened.py -l -r "670,1024" --video_dir F:/

class projectile(ThreeDScene):
    CONFIG = {
        "camera_config": {
            "background_image": "grass.jpg",
        }
    }

    def construct(self) -> None:
        self.set_camera_orientation(phi=45 * DEGREES, theta=-45 * DEGREES)
        self.first(7,45*DEGREES)

        self.play(self.camera.theta_tracker.increment_value, -20 * DEGREES)

        self.play(self.camera.phi_tracker.increment_value, 20 * DEGREES)
        self.first(7, 60 * DEGREES)
        self.first(7, 75 * DEGREES)
        self.first(7, 30 * DEGREES)


    def first(self,u,theta):
        axes = ThreeDAxes(x_range=[0, 5, 1], y_range=[0, 5, 1], width=3, height=4)
        self.add(axes)
        total = 2 * u * np.sin(theta) / 9.8
        ball = Sphere(radius=0.1 ).move_to(axes.c2p(0, 0))
        # curve = ParametricCurve(
        #     lambda t: axes.c2p(t*u*np.cos(theta),t*u*np.sin(theta)-0.5*9.8*t**2),
        #     t_range=(0, total))
        path = Line(ball.get_center(), ball.get_center() + UP * 0.0001)

        def update_path(mob):
            line = Line(path.get_end(), ball.get_center())
            path.append_vectorized_mobject(line)
            mob.become(path)

        def update(mob, alpha):
            intial_t = interpolate(0, total, alpha)
            inarr = axes.c2p(intial_t * u * np.cos(theta), intial_t * u * np.sin(theta) - 0.5 * 9.8 * intial_t ** 2)
            finarr = np.array([inarr[0], 0, inarr[1]])
            mob.move_to(finarr)

        self.add(path)
        path.add_updater(update_path)
        self.play(UpdateFromAlphaFunc(ball, update), run_time=4)


