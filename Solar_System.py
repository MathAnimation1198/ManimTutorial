from manimlib import *
class Planetry(ThreeDScene):
    def construct(self) -> None:


        frame=self.camera.frame
        frame.set_euler_angles(
            theta=50 * DEGREES,
            phi=60 * DEGREES,
        )
        frame.scale(0.4)
        axes=ThreeDAxes()
        self.add(axes)


        g=1
        m1=1
        m2=1
        r1=2
        v1=0.5

        sun1=Sphere(radius=0.3,color=YELLOW)
        link='https://dm0qx8t0i9gc9.cloudfront.net/thumbnails/image/rDtN98Qoishumwih/sun-texture_GJFqg5qO_thumb.jpg'
        sun=TexturedSurface(sun1,link)
        planet1=Sphere(radius=0.2,color=YELLOW).move_to(r1*RIGHT)
        day_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"

        planet=TexturedSurface(planet1,day_texture)

        planet.p=m2*np.array([0.0,v1,0.0])

        self.add(sun,planet)

        self.t=0
        self.step=0.001
        self.counter=0
        def update(mob,dt):
            if self.counter==0:
                r = planet.get_center() - sun.get_center()
                f = -g * m1 * m2 * normalize(r) / get_norm(r) ** 2

                planet.p = planet.p + f * dt

                mob.move_to(planet.get_center() + planet.p * dt / m2)
                self.start=planet.get_center() + planet.p * dt / m2

            elif self.counter==100:
                r = planet.get_center() - sun.get_center()
                f = -g * m1 * m2 * normalize(r) / get_norm(r) ** 2

                planet.p = planet.p + f * dt

                mob.move_to(planet.get_center() + planet.p * dt / m2)
                end=planet.get_center() + planet.p * dt / m2
                arc=ArcBetweenPoints(self.start,end,angle=50*DEGREES).set_stroke(width=0).set_fill(color=BLUE,opacity=0.5)
                line=Polygon(ORIGIN,self.start,end).set_stroke(width=0).set_fill(color=BLUE,opacity=0.5)

                group=VGroup(line,arc)
                self.add(group)
                self.add(planet)
            elif self.counter==220:
                r = planet.get_center() - sun.get_center()
                f = -g * m1 * m2 * normalize(r) / get_norm(r) ** 2

                planet.p = planet.p + f * dt

                mob.move_to(planet.get_center() + planet.p * dt / m2)
                self.start=planet.get_center() + planet.p * dt / m2

            elif self.counter==320:
                r = planet.get_center() - sun.get_center()
                f = -g * m1 * m2 * normalize(r) / get_norm(r) ** 2

                planet.p = planet.p + f * dt

                mob.move_to(planet.get_center() + planet.p * dt / m2)
                end=planet.get_center() + planet.p * dt / m2
                arc=ArcBetweenPoints(self.start,end,angle=117*DEGREES).set_stroke(width=0).set_fill(color=BLUE,opacity=0.5)
                line=Polygon(ORIGIN,self.start,end).set_stroke(width=0).set_fill(color=BLUE,opacity=0.5)

                group=VGroup(line,arc)
                self.add(group)
                self.add(sun)
                self.add(planet)
            else:
                r = planet.get_center() - sun.get_center()
                f = -g * m1 * m2 * normalize(r) / get_norm(r) ** 2

                planet.p = planet.p + f * dt

                mob.move_to(planet.get_center() + planet.p * dt / m2)





            self.t+=self.step

            self.counter+=1
        planet.add_updater(update)

        path=Line(planet.get_center(),planet.get_center()).set_stroke(width=0.05)
        def path_update(mob):
            line=Line(path.get_end(),planet.get_center()).set_stroke(width=0.05)
            path.append_vectorized_mobject(line)
            mob.become(path)
        def planet_update(mob,dt):
            mob.rotate(dt)


        path.add_updater(path_update)

        planet.add_updater(planet_update)
        self.add(path)

        self.wait(60)
