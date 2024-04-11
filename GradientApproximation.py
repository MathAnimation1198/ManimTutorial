from manim import *
class gradientApproximation(MovingCameraScene):
    def construct(self):
        self.camera.frame.move_to(ORIGIN)
        self.camera.frame.scale(2)
        # boy=Boys().shift([-5,-1,0]).rotate(80*DEGREES,axis=UP)
        tittle=Tex("Gradient Descent Algorithm Helping Me").shift(6*UP)
        text=Tex("To Find Best Fit Approximated Curve").next_to(tittle,DOWN)

        # image=SVGMobject("Cartoon_thought_bubble.svg").next_to(boy,UP,buff=0,aligned_edge=LEFT)
        # hello = Text('Wow',color=RED).move_to(image)
        self.add(tittle,text)
        def func(x, a, b, c, d):
            return a * x ** 3 + b * x ** 2 + c * x + d

        def app(x):
            return np.sin(x)

        def grad(x, a, b, c, d):
            return [2 * x ** 3 * (func(x, a, b, c, d) - app(x)), 2 * x ** 2 * (func(x, a, b, c, d) - app(x)),
                    2 * x * (func(x, a, b, c, d) - app(x)), 2 * (func(x, a, b, c, d) - app(x))]

        axes = Axes(x_length=8,y_length=6).shift(DOWN)
        graph = axes.plot(lambda x: np.sin(x),color=YELLOW)
        a, b, c, d = 1, 1, 1, 1
        x = np.arange(-1.5, 1.5, 0.01)
        graph1=axes.plot(lambda x:a*x**3+b*x**2+c*x+d)
        text=MathTex(*[str(round(a,2)),"x^{3}+",str(round(b,2)),"x^{2}+",str(round(c,2)),"x+",str(round(d,2))]).shift(np.array([0,4,0]))
        self.add(axes, graph,text)
        self.wait()
        rate=0.8
        graphG=VGroup()
        textG=VGroup()
        for i in range(20):
            a = a - (rate* np.mean(grad(x, a, b, c, d)[0]))
            b = b - (rate* np.mean(grad(x, a, b, c, d)[1]))
            c = c - (rate* np.mean(grad(x, a, b, c, d)[2]))
            d = d - (rate* np.mean(grad(x, a, b, c, d)[3]))

            graph2 = axes.plot(lambda x: a * x ** 3 + b * x ** 2 + c * x + d,color=RED)
            text1 = MathTex(
                *[str(round(a, 2)), "x^{3}+", str(round(b, 2)), "x^{2}+", str(round(c, 2)), "x+", str(round(d, 2))],).shift(np.array([0, 4, 0]))
            graphG.add(graph2)
            textG.add(text1)
        for tex,gra in zip(textG[:10],graphG[:10]):
            self.play(Transform(text,tex),Transform(graph1,gra))
        code='''
        a, b, c, d = 1, 1, 1, 1
        x = np.arange(-1.5, 1.5, 0.01)
        def func(x, a, b, c, d):
            return a * x ** 3 + b * x ** 2 + c * x + d

        def app(x):
            return np.sin(x)

        def grad(x, a, b, c, d):
            return [2 * x ** 3 * (func(x, a, b, c, d) - app(x)),
             2 * x ** 2 * (func(x, a, b, c, d) - app(x)),
                    2 * x * (func(x, a, b, c, d) - app(x)), 
                    2 * (func(x, a, b, c, d) - app(x))]

        for i in range(20):
            a = a - (rate* np.mean(grad(x, a, b, c, d)[0]))
            b = b - (rate* np.mean(grad(x, a, b, c, d)[1]))
            c = c - (rate* np.mean(grad(x, a, b, c, d)[2]))
            d = d - (rate* np.mean(grad(x, a, b, c, d)[3]))
        '''
        cod=Code(code=code,background="window",language="python",font="Monospace").stretch_to_fit_height(self.camera.frame.get_height()*0.8).\
            stretch_to_fit_width(self.camera.frame.get_width())
        coff=Tex("Code I Am Using To Find Cofficient").next_to(cod,UP,0.1)
        self.play(Write(coff))
        self.play(Write(cod))
        self.wait(2)
        self.play(FadeOut(cod),FadeOut(coff))
        full_code=Tex("Full Manim Code Given In Comment").shift(3*DOWN)
        self.play(Write(full_code))
        self.wait(2)