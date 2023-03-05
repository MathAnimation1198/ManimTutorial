from manimlib import *
class Epicycle(Scene):
    def construct(self) -> None:
        m1=self.first(mu=2.2)
        m2=self.first(ran=range(3,20,2),mu=0)
        m3 = self.first(ran=range(3, 250, 2), mu=-2.2)
        label=Tex(f"n={len(range(3,10,2))+1}",f"n={len(range(3,20,2))+1}",f"n={len(range(3,250,2))+1}")
        label[0].next_to(m1,LEFT)
        label[1].next_to(m2, LEFT)
        label[2].next_to(m3, LEFT)
        self.add(m1,m2,m3,label)
        self.wait(20)

    def first(self,ran=range(3,10,2),mu=2):
        vect = Vector(color=GREY_A)
        value = ValueTracker(0)
        rate = 0.24
        value.add_updater(lambda v, dt: v.set_value(dt * rate))
        self.add(value)
        vect.add_updater(lambda v: v.set_angle(v.get_angle() + 1 * TAU * value.get_value()))

        # vect2=Vector().shift(vect.get_end()).scale(1/3)
        def update(pv, f):

            def updat(mob):
                mob.set_angle(mob.get_angle() + f * value.get_value() * TAU, about_point=pv.get_end())
                mob.shift(pv.get_end() - mob.get_start())

            return updat

        last = vect
        vgroup = VGroup()
        rang = ran
        for i in rang:
            vect2 = Vector().scale(1 / i)
            vect2.add_updater(update(last, i))
            vgroup.add(vect2)
            last = vect2

        line = Line(vgroup[-1].get_end(), vgroup[-1].get_end() + np.array([1 - vgroup[-1].get_end()[0] + 1, 0, 0]))
        line.add_updater(
            lambda v: v.become(
                Line(vgroup[-1].get_end(), vgroup[-1].get_end() + np.array([1 - vgroup[-1].get_end()[0] + 1, 0, 0]))))

        path = Line(vgroup[-1].get_end(), vgroup[-1].get_end() + UP * 0.00001).set_stroke(width=0.5)

        circ3 = Circle()

        def cupdat(v):
            def upd(mob):
                mob.move_to(v.move_to(v.get_start()))

            return upd

        for i, j, c in zip(range(len(rang)), rang,
                           np.random.choice([YELLOW, BLUE, GREEN, PINK, PURPLE, MAROON, GOLD, TEAL], size=len(rang))):
            circ = Circle(radius=1 / j, color=c).set_stroke(width=2)

            circ.add_updater(cupdat(vgroup[i]))
            self.add(circ)

        def path_update(mob):
            line1 = Line(path.get_end(), line.get_end())
            path.append_vectorized_mobject(line1)
            path.shift(RIGHT * value.get_value() * 3)
            mob.become(path)

        path.add_updater(path_update)

        # frame=self.camera.frame
        # frame.scale(0.5)
        # frame.add_updater(lambda v:v.move_to(vgroup[1]))

        # dot=Dot(vgroup[-1].get_end(),color=RED)
        # dot.add_updater(lambda v:v.move_to(vgroup[-1].get_end()))
        fgroup = VGroup(vect, vgroup, line, path, circ3)
        fgroup.shift( mu*UP)
        return fgroup

class Sin(Scene):
    def construct(self) -> None:
        circle=Circle().shift(5*LEFT)
        vect=Vector().shift(5*LEFT)
        t=ValueTracker(0)
        rate=1
        t.add_updater(lambda v,dt:v.increment_value(dt*rate))
        vect.add_updater(lambda v: v.set_angle(t.get_value()))
        self.add(t,circle,vect)


        line=Line(vect.get_end(),vect.get_end()+np.array([1-vect.get_end()[0]-4,0,0]))
        line.add_updater(lambda v:v.become(Line(vect.get_end(),vect.get_end()+np.array([1-vect.get_end()[0]-4,0,0]))))



        axes=NumberLine(x_range=[0,TAU+1,1])
        axes.next_to(line,RIGHT,buff=0)


        self.add(line)
        path=VMobject(color=YELLOW)
        path.set_points_as_corners([line.get_end(),line.get_end()+UP*0.0001])



        def path_upadate(mob,dt):
            line1st=Line(path.get_end(),line.get_end())
            path.append_vectorized_mobject(line1st)
            path.shift(RIGHT*dt*0.5)

        path.add_updater(path_upadate)

        self.add(path)


        self.wait(20)

class SinCos(Scene):
    def construct(self) -> None:
        circle=Circle().shift(5*LEFT+2*UP)
        vect=Vector().shift(5*LEFT+2*UP)
        t=ValueTracker(0)
        rate=2
        t.add_updater(lambda v,dt:v.increment_value(dt*rate))
        vect.add_updater(lambda v: v.set_angle(t.get_value()))
        self.add(t,circle,vect)


        line=Line(vect.get_end(),vect.get_end()+np.array([1-vect.get_end()[0]-4,0,0]))
        line.add_updater(lambda v:v.become(Line(vect.get_end(),vect.get_end()+np.array([1-vect.get_end()[0]-4,0,0]))))

        line1 = Line(vect.get_end(), vect.get_end() + np.array([0,1 - vect.get_end()[1] - 1, 0]))
        line1.add_updater(
            lambda v: v.become(Line(vect.get_end(), vect.get_end() + np.array([0,1 - vect.get_end()[1] - 1, 0]))))

        axes=NumberLine(x_range=[0,TAU+1,1])
        axes.next_to(line,RIGHT,buff=0)
        axes1 = NumberLine(y_range=[0, TAU, 1]).rotate(90*DEGREES)
        axes1.next_to(line1, DOWN, buff=0)
        axes1.shift(1*LEFT)

        self.add(line,line1,axes,axes1)
        path=VMobject(color=YELLOW)
        path.set_points_as_corners([line.get_end(),line.get_end()+UP*0.0001])

        path1 = VMobject(color=YELLOW)
        path1.set_points_as_corners([line1.get_end(), line1.get_end() + UP * 0.0001])

        def path_upadate(mob,dt):
            line1st=Line(path.get_end(),line.get_end())
            path.append_vectorized_mobject(line1st)
            path.shift(RIGHT*dt*rate)
        def path_upadate1(mob,dt):
            line2nd=Line(path1.get_end(),line1.get_end())
            path1.append_vectorized_mobject(line2nd)
            path1.shift(DOWN*dt*rate)
        path.add_updater(path_upadate)
        path1.add_updater(path_upadate1)
        self.add(path,path1)


        self.wait(10)
class cos2(Scene):
    def construct(self) -> None:
        vect=Vector(RIGHT)
        circ=Circle()
        t=ValueTracker(0)
        rate=0.5
        t.add_updater(lambda m,dt:m.increment_value(
                rate * dt
            ))
        self.add(vect,circ,t)
        vect.add_updater(lambda v:v.become(Vector(((np.exp(1*TAU*t.get_value()*1j)
                                                    +np.exp(1*TAU*t.get_value()*1j))*1).real*RIGHT+UP*((np.exp(1*TAU*t.get_value()*1j)
                                                                                                             +np.exp(-1*TAU*t.get_value()*1j))*1).imag)))


        def get_vertically_falling_tracing(vector, color, stroke_width=3, rate=rate):
            path = VMobject()
            path.set_stroke(color, stroke_width)
            path.set_points_as_corners([vector.get_end(),vector.get_end()+UP*0.0001])
            path.vector1 = vector
            def update_path(mob,dt):

                path.append_vectorized_mobject(Line(path.get_end(),vector.get_end()))
                path.shift(rate*dt* DOWN)
                mob.become(path)



            path.add_updater(update_path)
            return path
        path1=get_vertically_falling_tracing(vect,YELLOW)
        self.add(path1)
        self.wait(10)
