from manimlib import *
class projectile(Scene):

    def construct(self) -> None:
        frame = self.camera.frame
        frame.scale(0.6)
        frame.set_euler_angles(theta=45 * DEGREES, phi=-45 * DEGREES)
        for index,angle in enumerate([45,65,85,30]):
            self.launch_at_angle(7,angle)
            if index==0:
                self.play(frame.increment_theta, -20 * DEGREES)
                self.play(frame.increment_phi, -20 * DEGREES)

    def launch_at_angle(self,u,theta):

        surface = ParametricSurface(lambda x, y: np.array([x, y, 0]), u_range=(-0.5, 0.5), v_range=(-0.5, 0.5))
        texture = TexturedSurface(surface, 'grass.jpg')
        thetlabel=theta
        theta=theta*DEGREES
        axes = ThreeDAxes()
        total = 2 * u * np.sin(theta) / 9.8
        ball = Sphere(radius=0.1, color=RED).move_to(axes.c2p(0, 0))
        # ball=SVGMobject('rocket.svg').scale(0.5).move_to(axes.c2p(0, 0)).fix_in_frame()

        # curve = ParametricCurve(
        #     lambda t: axes.c2p(t*u*np.cos(theta),t*u*np.sin(theta)-0.5*9.8*t**2),
        #     t_range=(0, total))
        path = Line(ball.get_center(), ball.get_center() + UP * 0.0001)

        self.add(texture, axes)

        def update_path(mob):
            line = Line(path.get_end(), ball.get_center())
            path.append_vectorized_mobject(line)
            mob.become(path)

        def update(mob, alpha):
            intial_t = interpolate(0, total, alpha)
            inarr = axes.c2p(intial_t * u * np.cos(theta), intial_t * u * np.sin(theta) - 0.5 * 9.8 * intial_t ** 2)
            finarr = np.array([inarr[0], 0, -inarr[1]])
            mob.move_to(finarr)

        self.add(path)
        self.add(ball)
        path.add_updater(update_path)


        self.play(UpdateFromAlphaFunc(ball, update), run_time=4)
        vector = Arrow(axes.c2p(0, 0), axes.c2p(2, 0), buff=0,color=YELLOW)
        vector.rotate(theta, axis=UP, about_point=axes.c2p(0, 0))
        self.play(ShowCreation(vector))

        arc = ArcBetweenPoints(0.5 * RIGHT, vector.point_from_proportion(0.3), angle=theta)
        self.play(ShowCreation(arc))
        label = Tex(f"{thetlabel}","^{\\circ}",color=YELLOW).scale(0.5).next_to(arc.point_from_proportion(0.5), RIGHT,buff=0.5).fix_in_frame()
        self.play(ShowCreation(label))
        self.wait()
        self.play(FadeOut(arc),FadeOut(vector),FadeOut(label))

