from manimlib import *
class Windind(Scene):
    def construct(self) -> None:
        value = ValueTracker(0.0)

        def func(f=0.1,step=0.001):
            out=lambda t:0.5*(2 + 1 * np.cos(TAU * t * 3)+1 * np.cos(TAU * t * 2)) * np.exp(-TAU * 1j * t * f)
            dt = step
            ran = np.arange(0, 6, dt)
            Int = sum([out(i) * dt for i in ran])
            return (1/6)*np.array([Int.real,Int.imag,0])



        def complex_to_real(f):
            z=lambda t:0.5*(2+1*np.cos(TAU*t*3)+1*np.cos(TAU*t*2))*np.exp(-TAU*1j*t*f)
            return lambda t:np.array([z(t).real,z(t).imag,0])
        curve=ParametricCurve(complex_to_real(value.get_value()),t_range=[0,6,0.01],color=YELLOW)
        dot = Dot(func(),color=RED)
        dot.add_updater(lambda v:v.become(Dot(func(f=value.get_value()),color=RED)))



        axes=Axes(x_range=[0,5,1],y_range=[-1,1,1],width=4,height=3)
        axes1=Axes(x_range=[0,5,1],y_range=[0,2,1],width=4,height=1.5).shift(4.5*RIGHT+3*UP)
        graph=axes1.get_graph(lambda t:1+np.cos(TAU*t*3),color=BLUE)
        axes2 = Axes(x_range=[0, 5, 1], y_range=[0, 2, 1], width=4, height=1.5).next_to(axes1,DOWN,aligned_edge=LEFT,buff=0.5)
        graph2 = axes2.get_graph(lambda t: 1 + np.cos(TAU * t * 2), color=YELLOW)
        axes3 = Axes(x_range=[0, 5, 1], y_range=[0, 2, 1], width=4, height=1.5).next_to(axes2, DOWN, aligned_edge=LEFT,buff=2)
        graph3 = axes3.get_graph(lambda t: 2 + np.cos(TAU * t * 2)+np.cos(TAU*t*3), color=PINK)
        axes.shift(4.5*LEFT+2*UP)
        axes.add_coordinate_labels()
        tex1=TexText('2 beat/per second','3 beat/ per second','mix').scale(0.5)
        tex1[0].next_to(graph,LEFT)
        tex1[1].next_to(graph2, UP)
        tex1[2].next_to(graph3, UP)


        freq=Tex('Frequency').next_to(axes.x_axis,DOWN,aligned_edge=RIGHT)
        yl=Text('x coordinate of center of mass')
        yl.scale(0.5,about_point=yl[0].get_start()).next_to(axes.y_axis,RIGHT,aligned_edge=UP)


        dot1=Dot(axes.c2p(value.get_value(),dot.get_center()[0]))
        dot1.add_updater(lambda v:v.move_to(axes.c2p(value.get_value(),dot.get_center()[0])))
        path=Line(dot1.get_center(),dot1.get_center(),color=RED)
        def path_update(mob):
            path.add_smooth_curve_to(dot1.get_center())
            mob.become(path)

        path.add_updater(path_update)
        plane=ComplexPlane(x_range=[-2,2,1],y_range=[-2,2,1])

        self.add(plane,freq,yl)
        self.add(curve,dot,axes,dot1,path,axes1,graph,graph2,axes2,axes3,graph3,tex1)


        curve.add_updater(lambda v:v.become(ParametricCurve(complex_to_real(value.get_value()),t_range=[0,5,0.001],color=YELLOW)))
        self.play(value.set_value,2,run_time=12,rate_func=linear)
        self.wait()
        self.play(value.set_value, 3, run_time=6, rate_func=linear)
        self.wait()
        self.play(value.set_value, 5, run_time=12, rate_func=linear)


class fwindind(Scene):
    def construct(self) -> None:

        def four(t):
            if t<-0.5 or t>0.5:
                return 0
            else:
                return 1


        axes=Axes(x_range=[-5,5,1],y_range=[-2,2,1],height=3,width=8).shift(2*DOWN)
        axes1=Axes(x_range=[-5,5,1],y_range=[-2,2,1],height=3,width=8).next_to(axes,UP)
        line1=Line(axes1.c2p(-0.5,0),axes1.c2p(-0.5,1))
        line2 = Line(axes1.c2p(0.5, 0), axes1.c2p(0.5, 1))
        line3 = Line(axes1.c2p(-0.5, 1), axes1.c2p(0.5, 1))


        tex=Tex('f(\\omega)=\\int_{-\\infty}^{\\infty}g(t)e^{-2\\pi i \\omega t}dt').shift(4*LEFT)
        square = VGroup(line1, line2, line3).set_color(YELLOW)
        arr = CurvedArrow(axes1.c2p(0, 0),tex.get_center()+UP*0.8 ,color=YELLOW)
        arr1 = CurvedArrow(tex.get_center() +5.5*RIGHT * 0.5,axes.get_center()+UP,angle=-TAU/4,color=BLUE)


        def integral(f,step=0.001):
            dt=step
            sample=np.arange(-6,6,dt)
            z=sum([four(t)*np.exp(-TAU*1j*t*f)*dt for t in sample])
            return z.real+z.imag



        curve=axes.get_graph(lambda t:integral(t),color=BLUE)

        self.play(AnimationGroup(*[ShowCreation(i) for i in [axes1,square,arr,tex,arr1,axes,curve]],lag_ratio=1))

