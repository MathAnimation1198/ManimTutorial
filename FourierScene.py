from manimlib import *
class fourier1(Scene):
    CONFIG = {
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.35,
            "fill_opacity": 0.75,
    }
    }

    def construct(self) -> None:
        #create frame
        frame=self.camera.frame

        # mobject with point
        square= Tex('m').set_height(4).family_members_with_points()[0]
        coff = self.get_coefficients_of_path(square)
        print(self.freq)

        #initial vector
        vect=Vector(RIGHT,**self.vector_config).scale(abs(coff[0]),about_point=ORIGIN)
        vect.rotate(np.log(coff[0]).imag)

        t=ValueTracker(0)
        last=vect
        group=VGroup()
        def updated1(f,pv,v):
            def updat(mob):
                mob.set_angle(np.log(v).imag+t.get_value() * TAU * f)
                mob.shift(pv.get_end()-mob.get_start())
            return updat
        #remaining all vector
        for v,f in zip(coff[1:],self.freq[1:]):
            vec=Vector(RIGHT,**self.vector_config)
            vec.scale(abs(v),about_point=ORIGIN)
            vec.rotate(np.log(v).imag)
            vec.add_updater(updated1(f,last,v))
            group.add(vec)
            last=vec


        self.add(vect,group)
        def updated(f):
            def updat(mob):
                mob.set_angle(np.log(coff[1]).imag+t.get_value() * TAU * f)
            return updat




        dot=Dot(group[-1].get_points()[-1],color=RED).scale(0.001)
        dot.move_to(group[-1].get_end())



        dot.add_updater(lambda v: v.move_to(group[-1].get_end()))

        self.add(dot)

        def path_update(dot,path):

           def updater(mob):
               line=Line(path.get_end(),dot.get_center()).set_stroke(width=0.01)
               path.append_vectorized_mobject(line)
               mob.become(path)



           return updater
        vect.add_updater(updated(self.freq[0]))

        #creating path initial path
        path1 = Line(dot.get_center(),dot.get_center()+UP*0.00001,color=YELLOW).set_stroke(width=0.5)
        self.add(path1)
        #adding updater in path
        path1.add_updater(path_update(dot,path1))

        # for camera scaling
        # frame.scale(0.01)
        # frame.add_updater(lambda v:v.move_to(dot))
        self.play(ApplyMethod(t.set_value,1),run_time=10,rate_func=linear)

    def get_coefficients_of_path(self, path, n_samples=8000, freqs=None):
        freqs=list(range(50,-50,-1))
        print(len(freqs))
        freqs.sort(key=abs)
        self.freq=freqs
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])
        samples -= ORIGIN
        complex_samples = samples[:, 0] + 1j * samples[:, 1]

        result = []
        for freq in freqs:
            riemann_sum = np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt
            result.append(riemann_sum)

        return result
