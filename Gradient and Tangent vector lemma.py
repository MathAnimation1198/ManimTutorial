from manimlib import *
def length_func(point):
    out=point
    norm=get_norm(out)
    func=lambda nor:0.45*sigmoid(nor)
    out*=func(norm)/norm
    return out


class first(ThreeDScene):
    def construct(self) -> None:
        frame = self.camera.frame
        frame.set_euler_angles(theta=40 * DEGREES, phi=60 * DEGREES)
        surface=ParametricSurface(lambda x,y:np.array([x,y,x**2+y**2]),u_range=(-1.8,1.8),v_range=(-1.8,1.8),color=BLUE)
        surfaceplane=ParametricSurface(lambda x,y:np.array([x,y,1]),u_range=(-1.8,1.8),v_range=(-1.8,1.8),color=RED,opacity=0.4)
        axes=ThreeDAxes()


        curve=ParametricCurve(lambda t:np.array([np.sqrt(0.75)*np.cos(t),np.sqrt(0.75)*np.sin(t),0.75]),t_range=[0,TAU],color=PINK)
        curve1 = ParametricCurve(lambda t: np.array([0.5* np.cos(t), 0.5 * np.sin(t), (0.5)**2]), t_range=[0, TAU], color=GREEN)
        curve2 = ParametricCurve(lambda t: np.array([ 1* np.cos(t), 1 * np.sin(t), 1]), t_range=[0, TAU],
                                 color=YELLOW)

        # mes=SurfaceMesh(surface)
        func = Tex('f(x,y)=x^{2}+y^{2}').fix_in_frame().shift(4 * LEFT + 3 * UP)
        cost = Tex('f(x,y)=x^{2}+y^{2}=c=f^{-1}(c)').fix_in_frame().next_to(func, DOWN, aligned_edge=LEFT)
        grad=Tex("\\nabla f(x,y)=").fix_in_frame().next_to(cost, DOWN, aligned_edge=LEFT,buff=1)
        mat=matrix_to_mobject(['2x','2y']).fix_in_frame().next_to(grad, RIGHT)
        self.add(surface,axes,func)
        self.play(ShowCreation(surfaceplane),run_time=5)
        self.play(ShowCreation(curve2))



        cylinder=ParametricSurface(lambda u,v:np.array([1*np.cos(u),1*np.sin(u),v]),u_range=(0,TAU),v_range=(0,1),opacity=1,color=PINK)
        self.play(ShowCreation(cylinder),ShowCreation(cost))
        self.play(frame.increment_phi,40*DEGREES,rate_func=there_and_back,run_time=3)

        self.play(frame.increment_theta,180*DEGREES,run_time=3)






        self.play(ApplyPointwiseFunction(lambda p:np.array([p[0],p[1],0]),surface),

                  ApplyPointwiseFunction(lambda p:np.array([p[0],p[1],0]),curve2),
                  ApplyPointwiseFunction(lambda p:np.array([p[0],p[1],0]),cylinder),
                  FadeOut(surfaceplane))





        plane=NumberPlane(x_range=[-8,8,2],y_range=[-4,4,2])

        realf = VectorField(lambda x, y: np.array([2 * x, 2 * y, 0]), plane)
        self.play(AnimationGroup(*[ShowCreation(i) for i in [realf,grad,mat]], lag_ratio=0.2), AnimationGroup(*[FadeOut(i) for i in [surface]], lag_ratio=0.2))

        self.wait()
        self.play(ApplyMethod(frame.set_euler_angles, 0, 0), rate_func=linear, run_time=2)

        for i in np.linspace(0,TAU,9):

            vect=Vector(np.array([-1 * np.sin(i), 1 * np.cos(i),0]),color=BLUE).shift(np.array([1 * np.cos(i), 1 * np.sin(i),0]))
            vect.scale(0.6,about_point=vect.get_start())

            self.play(ShowCreation(vect))
            self.wait()
        self.play(AnimationGroup(*[FadeOut(i) for i in [func,cost,grad,mat]], lag_ratio=0.2))





class Texfun(Scene):
    def construct(self) -> None:
        func = Tex('f(x,y)=x^{2}+y^{2}').shift(4 * LEFT + 3 * UP)
        cost = Tex('f(x,y)=x^{2}+y^{2}=c=f^{-1}(c)').next_to(func, DOWN, aligned_edge=LEFT)

        param = Tex('\\alpha(t)=r(\\cos(t),\\sin(t))').next_to(cost, DOWN, aligned_edge=LEFT)
        param1 = Tex('f(\\alpha(t))=r^{2}(\\cos(t))^{2}+r^{2}(\\sin(t))^{2}=r^{2}').next_to(param, DOWN,
                                                                                                           aligned_edge=LEFT)
        deri = Tex("\\frac{df(\\alpha(t))}{dt}=0").next_to(param1, DOWN, aligned_edge=LEFT)
        grad = Tex("\\nabla f(\\alpha(t)). \\dot\\alpha(t)=0").next_to(deri, DOWN, aligned_edge=LEFT)

        example=func.copy().next_to(grad, DOWN, aligned_edge=LEFT)
        param2=Tex('\\alpha(t)=(t,t^{2})').next_to(example, DOWN, aligned_edge=LEFT)

        comp=Tex('f(\\alpha(t)))=f((t,t^{2}))=t^{2}+(t^{2})^{2}').next_to(param2, DOWN, aligned_edge=LEFT)

        dcomp=Tex('\\frac{df(\\alpha(t)))}{dt}=\\frac{f((t,t^{2}))}{dt}=2t+4t^{3}').next_to(func, RIGHT)

        gf=matrix_to_mobject(["2t",'2t^{2}']).next_to(dcomp, DOWN)

        galpha=matrix_to_mobject(['1','2t']).next_to(gf, RIGHT,buff=0.1)

        final=Tex('=2t+4t^{3}').next_to(galpha, RIGHT,buff=0.1)





        self.play(AnimationGroup(*[ShowCreation(i) for i in [func, cost,param, param1, deri, grad]],
                                 lag_ratio=2))

class Texfunc2(Scene):
    def construct(self) -> None:
        example = Tex('f(x,y)=x^{2}+y^{2}').shift(4 * LEFT + 3 * UP)
        param2 = Tex('\\alpha(t)=(t,t^{2})').next_to(example, DOWN, aligned_edge=LEFT)

        comp = Tex('f(\\alpha(t)))=f((t,t^{2}))=t^{2}+(t^{2})^{2}').next_to(param2, DOWN, aligned_edge=LEFT)

        dcomp = Tex('\\frac{df(\\alpha(t)))}{dt}=\\frac{f((t,t^{2}))}{dt}=2t+4t^{3}').next_to(comp, DOWN)

        grad = Tex("\\nabla f(\\alpha(t)). \\dot\\alpha(t)=").next_to(dcomp, DOWN,aligned_edge=LEFT,buff=1)
        gf = matrix_to_mobject(["2t", '2t^{2}']).next_to(grad,RIGHT)

        galpha = matrix_to_mobject(['1', '2t']).next_to(gf, RIGHT, buff=0.2)

        final = Tex('=2t+4t^{3}').next_to(galpha, RIGHT, buff=0.1)


        self.play(AnimationGroup(*[ShowCreation(i) for i in [example, param2, comp, dcomp, grad,gf,galpha, final]],lag_ratio=2))
class helperDiff(Scene):
    def construct(self) -> None:
        tex=Text("The gradient of f at p").shift(3*LEFT)
        tex1=Tex("\\in f^{-1}(c)","f^{-1}(c)")
        tex1[0].next_to(tex, RIGHT)
        tex2=Text("is orthogonal to all vectors tangent to ").next_to(tex,DOWN,aligned_edge=LEFT)
        tex1[1].next_to(tex2,DOWN,aligned_edge=LEFT)

        text3=Text("at p").next_to(tex1[1],RIGHT)


        self.play(AnimationGroup(*[ShowCreation(i) for i in [tex,tex1[0],tex2,text3,tex1[1]]],lag_ratio=0.5))

