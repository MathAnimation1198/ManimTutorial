from manimlib import *
class Integral(Scene):
    def construct(self) -> None:
        x = lambda t: 1* np.cos(t)
        y = lambda t: 1 * np.sin(t)
        dx = lambda t: -1 * np.sin(t)
        dy = lambda t: 1 * np.cos(t)
        plane=NumberPlane()
        field=VectorField(lambda x,y:np.array([-y,x,0]),plane)
        strem=StreamLines(lambda x,y:np.array([-y,x,0]),plane)
        self.add(field)
        astrem=AnimatedStreamLines(strem).set_stroke(color=BLUE)
        self.add(astrem)
        self.wait(2)
        circle=Circle(color=PINK).set_stroke(width=2)
        self.play(ShowCreation(circle))
        self.remove(astrem)
        self.play(circle.scale,5,run_time=5,rate_func=there_and_back)

        for i in [*np.arange(0, TAU, TAU / 4), TAU / 8]:
            t = i
            inp = x(t), y(t)
            out = dx(t), dy(t)
            vect = Vector(np.array([*out, 0]), color=BLUE).shift(np.array([*inp, 0]))
            vect.scale(0.4,about_point=vect.get_start())
            self.play(ShowCreation(vect))

class Drawing(Scene):
    def construct(self) -> None:
        func=lambda x,y:np.array([-y,x,0])
        plane=NumberPlane()
        self.add(plane)
        vectors=VGroup()
        for i in [[1,0],[0,1],[-1,0],[0,-1]]:
            out=func(*i)
            vect=Vector(out,color=YELLOW)
            vect.shift(np.array([*i,0]))
            self.play(ShowCreation(vect))
        vect1=VMobject()
        fun=Tex('f(x,y)=').next_to(7*LEFT+3*UP)
        mat=matrix_to_mobject(['-y','x']).next_to(fun,RIGHT)
        equal=Tex('=').next_to(mat,RIGHT)
        self.add(mat,fun,equal)
        vect2=VMobject()
        vect3=VMobject()
        vect4=VMobject()
        vect5 = VMobject()
        for x,y in zip(random.choices(np.arange(-3,3,0.1),k=10),random.choices(np.arange(-3,3,0.1),k=10)):
            dot=Dot(np.array([x,y,0]),color=RED)
            out = func(x,y)
            vect = Vector(out, color=YELLOW)
            vect.shift(np.array([x,y, 0]))
            val=Tex(f"({round(x,2)},{round(y,2)})").next_to(dot,DOWN).scale(0.5)
            tfunc=Tex(f"f({round(x,2)},{round(y,2)})=").scale(0.5).move_to(fun)

            mat1 = matrix_to_mobject(['-y', 'x']).scale(0.5).next_to(tfunc, RIGHT)
            equal1=Tex('=').next_to(mat1,RIGHT)
            tout = matrix_to_mobject([f"{round(out[0], 2)}", f"{round(out[1], 2)}"]).scale(0.5).next_to(equal1, RIGHT)
            line1=DashedLine(dot.get_center(),dot.get_center()+np.array([out[0],0,0]))
            line2 = DashedLine(dot.get_center()+np.array([out[0],0,0]),dot.get_center()+np.array([out[0],0,0])+np.array([0,out[1],0]))
            label=Tex(f"{round(out[0],2)}",f"{round(out[1],2)}").scale(0.4)
            label[0].next_to(line1,DOWN)
            label[1].next_to(line2, RIGHT)
            group1=VGroup(line1,line2)
            group=VGroup(dot,vect)
            self.play(Transform(vect1,group),Transform(fun,tfunc),Transform(vect2,tout),Transform(mat,mat1),Transform(equal,equal1),Transform(vect3,group1)
                      ,Transform(vect4,label),Transform(vect5,val))

class Parametric(Scene):
    def construct(self) -> None:
        x=lambda t:2*np.cos(t)
        y = lambda t: 2*np.sin(t)
        dx=lambda t:-2*np.sin(t)
        dy = lambda t: 2*np.cos(t)
        xl=Tex('x(t)=2\\cos(t)').shift(5*LEFT+3*UP)
        yl =Tex('y(t)=2\\sin(t)').next_to(xl,DOWN,aligned_edge=LEFT)
        xld=Tex('x(t)^{\\prime}=-2\\sin(t)').next_to(yl,DOWN,aligned_edge=LEFT,buff=2)
        yld = Tex('y(t)^{\\prime}=2\\cos(t)').next_to(xld,DOWN,aligned_edge=LEFT)


        curve=ParametricCurve(lambda t:np.array([2*np.cos(t),2*np.sin(t),0]),t_range=[0,TAU,0.1],color=YELLOW)
        tl = Tex('t=',color=GREEN)
        val=ValueTracker(0)
        tval=DecimalNumber(val.get_value()).scale(0.6).next_to(tl,RIGHT)
        self.play(AnimationGroup(*[ShowCreation(i) for i in [xl,yl]],lag_ratio=2))
        self.add(tl,tval)
        tval.add_updater(lambda v:v.set_value(val.get_value()))

        tl.add_updater(lambda v:v.next_to(curve.get_end(),RIGHT,buff=0))
        tval.add_updater(lambda v: v.next_to(tl, RIGHT))
        self.add(curve)
        self.play(ApplyMethod(val.set_value,TAU),ShowCreation(curve),run_time=2,rate_func=linear)

        ax1 = NumberLine(x_range=[-2.0, 2.0, 1.0])
        ax2 = NumberLine(x_range=[-2.0, 2.0, 1.0]).rotate(PI / 2, about_point=ORIGIN)
        self.add(ax1,ax2)


        self.play(AnimationGroup(*[ShowCreation(i) for i in [xld,yld]],lag_ratio=1))

        for i in [*np.arange(0,TAU,TAU/4),TAU/8]:
            t = i
            inp = x(t), y(t)
            out = dx(t), dy(t)
            vect = Vector(np.array([*out, 0]), color=RED).shift(np.array([*inp, 0]))
            self.play(ShowCreation(vect))
class FinalCurve(Scene):
    def construct(self) -> None:
        tex=Tex('x=x_{1}(t)','y=x_{2}(t)').shift(4*LEFT+3*UP)
        tex[1].next_to(tex[0],DOWN)
        tex1=Tex('\\frac{dx}{dt}=-y','\\frac{dy}{dt}=x')

        tex1[0].next_to(tex, DOWN)
        tex1[1].next_to(tex1[0], DOWN)
        dou = Tex('\\frac{d^{2}x}{dt^{2}}=-','\\frac{dy}{dt}')
        self.play(AnimationGroup(*[ShowCreation(i) for i in [tex, tex1]], lag_ratio=1))
        point=VectorizedPoint(tex1[1].get_center())
        point1=VectorizedPoint(tex1[0].get_center())
        self.play(ApplyMethod(tex1[0].move_to,point),ApplyMethod(tex1[1].move_to,point1))
        dou.next_to(tex1[0],RIGHT,buff=2)
        self.play(ShowCreation(dou))
        cop=tex1[1][-1].copy().move_to(dou[1])
        self.play(Transform(dou[1],cop))
        ex=Tex('x=\\cos(t)','\\frac{dx}{dt}=-\\sin(t)','\\frac{d^{2}x}{dt^{2}}=-\\cos(t)=-x',color=YELLOW).next_to(dou,DOWN,aligned_edge=LEFT,buff=1)

        self.add(ex[0])
        for i in range(1,3):
            ex[i].move_to(ex[i-1])
        for i in range(1,3):
            self.play(Transform(ex[0],ex[i]))
        self.remove(ex)
        ex1 = Tex('x=\\sin(t)', '\\frac{dx}{dt}=\\cos(t)', '\\frac{d^{2}x}{dt^{2}}=-\\sin(t)=-x', color=YELLOW).next_to(dou,
                                                                                                                    DOWN,
                                                                                                                    aligned_edge=LEFT,
                                                                                                                    buff=1)

        self.add(ex1[0])
        for i in range(1, 3):
            ex1[i].move_to(ex1[i - 1])
        for i in range(1, 3):
            self.play(Transform(ex1[0], ex1[i]))

        self.remove(ex1)
        ex2 = Tex('x=\\cos(t)+\\sin(t)', '\\frac{dx}{dt}=-\\sin(t)+\\cos(t)', '\\frac{d^{2}x}{dt^{2}}=-\\cos(t)-\\sin(t)=-x', color=YELLOW).next_to(
            dou,
            DOWN,
            aligned_edge=LEFT,
            buff=1)

        self.add(ex2[0])
        for i in range(1, 3):
            ex2[i].move_to(ex2[i - 1])
        for i in range(1, 3):
            self.play(Transform(ex2[0], ex2[i]))
        self.remove(ex2)
        sol=Tex('x=','A\\cos(t)+B\\sin(t)',color=RED).next_to(
            dou,
            DOWN,
            aligned_edge=LEFT,
            buff=1)
        self.add(sol)
        solc=sol[1].copy().move_to(tex1[1][-1],aligned_edge=LEFT)
        self.play(Transform(tex1[1][-1],solc))
        self.play(tex1[1][3:5].next_to,sol[1].copy().move_to(tex1[1][-1]),RIGHT)
        self.remove(tex1[1][2])
        sol1=Tex('y=A\\sin(t)-B\\cos(t)',color=RED).move_to(tex1[1],aligned_edge=LEFT)
        solg=VGroup(tex1[1],solc)
        self.play(Transform(solg,sol1))
        self.play(solg.next_to,sol,DOWN,aligned_edge=LEFT)
        self.remove(dou)
        self.play(ApplyMethod(sol.shift,5*UP),ApplyMethod(solg.shift,5*UP))
        initial=Tex('(x(0),y(0))=(1,0)').next_to(solg,DOWN,aligned_edge=LEFT)
        appl=Tex('1=A\\cos(0)+B\\sin(0)','0=A\\sin(0)-B\\cos(0)')
        appl[0].next_to(initial,DOWN,aligned_edge=LEFT)
        appl[1].next_to(appl[0], DOWN, aligned_edge=LEFT)

        ulfinsol=Tex('x=\\cos(t)','y=\\sin(t)')
        ulfinsol[0].next_to(appl[1], DOWN, aligned_edge=LEFT)
        ulfinsol[1].next_to(ulfinsol[0], DOWN, aligned_edge=LEFT)

        for i in [initial,appl,ulfinsol]:
            self.play(ShowCreation(i))


