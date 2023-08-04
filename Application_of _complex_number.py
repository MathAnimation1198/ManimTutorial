from manimlib import *

def glow_dot(point, r_min=0.05, r_max=0.3, color=YELLOW, n=20, opacity_mult=1.0):
    result = VGroup(*(
        Dot(point, radius=interpolate(r_min, r_max, a))
        for a in np.linspace(0, 1, n)
    ))
    result.set_fill(color, opacity=opacity_mult / 10)
    return result


class Application(Scene):
    def construct(self) -> None:
        axes=Axes()
        axes.coords_to_point()
        square=Square(fill_color=RED,fill_opacity=0.2).rotate(10*DEGREES,about_point=[-1,0,0]).scale(1).move_to([-1,0,0],aligned_edge=LEFT+DOWN)
        square1=Square(fill_color=GREEN,fill_opacity=0.2).move_to(square.get_vertices()[2],aligned_edge=LEFT+UP).rotate(-60*DEGREES,about_point=square.get_vertices()[2])\
        .scale(1.1,about_point=square.get_vertices()[2])
        square2=Square(fill_color=YELLOW,fill_opacity=0.2).move_to(square1.get_vertices()[0],aligned_edge=LEFT+UP)\
            .rotate(30*DEGREES,about_point=square1.get_vertices()[0])\
            .scale(0.9,about_point=square1.get_vertices()[0])
        def normal(point):
            x,y,_=point
            return np.array([-y,x,0])
        def mag(point):
            return sum([x**2 for x in point])**0.5
        lent=mag(-square.get_vertices()[3]+square2.get_vertices()[0])
        a=square2.get_vertices()[0]-square2.get_vertices()[1]
        b=square.get_vertices()[3]-square.get_vertices()[0]
        square3=Polygon(square.get_vertices()[3],square2.get_vertices()[0],square2.get_vertices()[0]+lent*(a/mag(a)),
                        square2.get_vertices()[0] + lent * (a / mag(a))+lent*(normal(a)/mag(a)),fill_color=PINK,fill_opacity=0.2)
        vector=Arrow(square.get_vertices()[2],square.get_vertices()[3],color=YELLOW,buff=0)
        vector1 = Arrow(square3.get_vertices()[0], square3.get_vertices()[1], buff=0,color=RED)
        vector2 = Arrow(square3.get_vertices()[1], square2.get_vertices()[1], buff=0,color=BLUE)
        vector3 = Arrow(square2.get_vertices()[1], square.get_vertices()[2], buff=0,color=PINK)
        group=VGroup(square,square3,square1,square2)
        dot=glow_dot(square.get_vertices()[2],color=GREEN)
        tex=Tex('2a','2b','2c','2d').scale(0.5)
        tex[0].next_to(vector,DOWN,buff=0)
        tex[1].next_to(vector1, LEFT,buff=0)
        tex[2].next_to(vector2, UP,buff=0).shift(0.3*DOWN+0.2*LEFT)
        tex[3].next_to(vector3, RIGHT,buff=0).shift(0.3*LEFT+0.2*DOWN)
        dots=VGroup(*[Dot(group[i].get_center()) for i in range(4)])
        line1=Arrow(dots[0].get_center(),dots[3].get_center(),color=BLUE,buff=0)
        line2 =Arrow(dots[1].get_center(), dots[2].get_center(),buff=0)
        group1=VGroup(vector, vector1, vector2, vector3)
        point=line_intersection([line1.get_start(),line1.get_end()],[line2.get_start(),line2.get_end()])
        label=Tex('p','q','r','s','A','B')
        label[0].next_to(dots[0],UP)
        label[1].next_to(dots[1], RIGHT)
        label[2].next_to(dots[2], DOWN)
        label[3].next_to(dots[3], LEFT)
        label[4].next_to(line1,RIGHT,buff=0).shift(0.5*RIGHT)
        label[5].next_to(line2, LEFT,buff=0).shift(1.2*UP+RIGHT)
        d1=normalize(line1.get_end()-line1.get_start())
        d2=normalize(line2.get_end()-line2.get_start())
        angle=Polygon(point,point-d1*0.3,d2*0.3+point-d1*0.3,point+d2*0.3)
        group2=VGroup(dots,label,angle,dot,tex)
        maing=VGroup(group,group2,group1).shift(2*RIGHT+UP)
        self.play(ShowCreation(maing))
        self.play(ShowCreation(line1.shift(2*RIGHT+UP)))
        self.play(ShowCreation(line2.shift(2*RIGHT+UP)))
        self.play(ShowCreation(dot))
        # path=Polygon(dot.get_center(),vector.get_end(),vector1.get_end(),vector2.get_end())
        cond=Tex('2a+2b+2c+2d=0').shift(4.7*LEFT+3*UP)
        cond1=Tex('2(a+b+c+d)=0').move_to(cond)
        cond2 = Tex('a+b+c+d=0').move_to(cond1)


        # self.play(MoveAlongPath(dot,path),run_time=8)
        # self.play(ShowCreation(cond))
        # for i in [cond1,cond2]:
        #     self.play(Transform(cond,i))
        #     self.wait()
        pvector, pvector1=vector.copy(),vector.copy()
        tex1=Tex('p=','a','+','ai').next_to(cond2,DOWN,aligned_edge=LEFT)
        tex2=Tex('q=2a+b+bi','s=2a+2b+c+ci','r=2a+2b+2c+d+di')
        tex2[0].next_to(tex1,DOWN,aligned_edge=LEFT)
        tex2[1].next_to(tex2[0], DOWN, aligned_edge=LEFT)
        tex2[2].next_to(tex2[1], DOWN, aligned_edge=LEFT)

        tex3=Tex('B','=','s','-','p','2a+2b+c+ci','a+ai')
        tex3[:5].next_to(tex2[2],DOWN,aligned_edge=LEFT)
        tex34=Tex('B','=','2a+2b+c+ci','-','(a+ai)').next_to(tex3[:5],DOWN,aligned_edge=LEFT)

        tex4 = Tex('A', '=', 'r', '-', 'q', '2a+2b+2c+d+di', '2a+b+bi')
        tex4[:5].next_to(tex34, DOWN, aligned_edge=LEFT)
        tex35 = Tex('A', '=', '2a+2b+2c+d+di', '-', '(2a+b+bi)').next_to(tex4[:5], DOWN, aligned_edge=LEFT)
        self.play(ShowCreation(tex1[0:2]))
        self.play(pvector.animate.scale(0.5,about_point=pvector1.get_start()),TransformFromCopy(tex[0],tex1[1],path_arc=3),run_time=5)

        pvector1.scale(0.5,about_point=pvector1.get_start()).shift(pvector.get_end()-pvector.get_start()).set_stroke(color=ORANGE)
        self.play(TransformFromCopy(pvector,pvector1,path_arc=2))
        self.play(Rotate(pvector1,PI/2,about_point=pvector1.get_start()),TransformFromCopy(tex[0],tex1[2:]))
        self.play(Write(tex2[0]))
        self.play(Write(tex2[1]))
        self.play(Write(tex2[2]))

        self.play(Write(tex3[:5]),Indicate(line1))
        self.play(Write(tex34[:2]))
        self.play(TransformFromCopy(tex3[2],tex34[2],path_arc=2))
        self.play(TransformFromCopy(tex3[4], tex34[3:5]),path_arc=2)

        self.play(Write(tex4[:5]),Indicate(line2))
        self.play(Write(tex35[:2]))
        self.play(TransformFromCopy(tex4[2], tex35[2], path_arc=2))
        self.play(TransformFromCopy(tex4[4], tex35[3:5]), path_arc=2)
        self.remove(tex1,tex2,tex3,tex4)
        self.play(ApplyMethod(tex34.shift,2*UP),ApplyMethod(tex35.shift,3.5*UP),ApplyMethod(tex34.shift,3*UP),ApplyMethod(maing.shift,1.5*RIGHT),
                  ApplyMethod(pvector.shift,1.5*RIGHT),ApplyMethod(pvector1.shift,1.5*RIGHT),ApplyMethod(line1.shift,1.5*RIGHT),
                  ApplyMethod(line2.shift,1.5*RIGHT))
        line1c=line1.copy()
        self.play(Rotate(line1c,-PI/2,about_point=line_intersection([line1.get_start(),line1.get_end()],[line2.get_start(),line2.get_end()])))
        self.play(ApplyMethod(line1c.shift,-mag(line2.get_center()-line_intersection([line1.get_start(),line1.get_end()],[line2.get_start(),line2.get_end()]))*normalize(dots[1].get_center()-dots[2].get_center())))
        tex34s=Tex('B','=','a+2b+c+ci','-','ai').move_to(tex34)
        tex35s = Tex('A', '=', 'b+2c+d+di', '-', 'bi').move_to(tex35).next_to(tex34s,DOWN,aligned_edge=LEFT)
        self.play(Transform(tex34,tex34s))
        self.play(Transform(tex35, tex35s))
        final=Tex('A+iB','=','b+2c+d+di', '-', 'bi','+i(a+2b+c+ci','-','ai)').next_to(tex35s,DOWN,aligned_edge=LEFT).shift(LEFT)
        final.scale(0.8,about_point=final[0][0].get_start())
        final1 = Tex('A+iB', '=', 'b+2c+d+di', '-', 'bi', '+(ai+2bi+ci-c', '+', 'a)').next_to(final, DOWN,
                                                                                             aligned_edge=LEFT)
        final1.scale(0.8, about_point=final[0][0].get_start())
        final2 = Tex('A+iB', '=', 'a+b+c+d', '+i(a+b+c+d)',).next_to(final1, DOWN,
                                                                                              aligned_edge=LEFT,buff=0.5)
        final2.scale(0.8, about_point=final[0][0].get_start())
        self.play(Write(final))
        self.play(Write(final1))
        self.play(Write(final2))


        path = Polygon(dot.get_center(), vector.get_end(), vector1.get_end(), vector2.get_end())

        self.play(MoveAlongPath(dot,path),run_time=8)
        self.play(ShowCreation(cond))
        for i in [cond1,cond2]:
            self.play(Transform(cond,i))
            self.wait()

        self.play(Transform(final2[2],Tex('0').move_to(final2[2])))
        self.play(Transform(final2[3], Tex('+0').move_to(final2[3])))
        last=Tex('=0').next_to(final2,RIGHT)
        self.play(ShowCreation(last))




class Suppor(Scene):
    def construct(self) -> None:
        plane=ComplexPlane()
        label=plane.add_coordinate_labels()
        self.play(ShowCreation(label))
        vect=Vector(RIGHT,color=RED)
        self.play(ShowCreation(vect))
        tex=Tex('i',color=YELLOW)
        texc = Tex('-i', color=YELLOW)
        tex.next_to(vect,RIGHT,buff=0)
        self.play(FadeInFromPoint(tex,ORIGIN))
        copy=vect.copy()
        tex.add_updater(lambda v:v.move_to(copy.get_end()))
        texc.add_updater(lambda v: v.move_to(vect.get_end()))

        self.play(Rotate(copy,PI/2,about_point=ORIGIN))
        self.play(FadeInFromPoint(texc, ORIGIN))
        self.play(Rotate(vect, -PI / 2, about_point=ORIGIN))
class Support(Scene):
    def construct(self) -> None:
        plane=ComplexPlane()
        label = plane.add_coordinate_labels()
        self.play(ShowCreation(label))
        vect=Tex('A=1+i',color=YELLOW)
        vect1=Tex('B=-1+i',color=PINK)
        rvect=Vector(RIGHT+UP,color=YELLOW)
        rvect1=Vector(LEFT+UP,color=PINK)
        vect.next_to(rvect,UP,aligned_edge=rvect.get_end()).shift(RIGHT).scale(0.6)
        vect1.next_to(rvect1, UP, aligned_edge=rvect1.get_end()).shift(LEFT).scale(0.6)
        self.play(ShowCreation(vect),ShowCreation(rvect))
        self.play(ShowCreation(vect1), ShowCreation(rvect1))
        pr=Tex('A','=','-iB').shift(4*LEFT+3*UP)
        su=SurroundingRectangle(pr[2])
        self.play(ShowCreation(pr))
        self.play(Rotate(rvect1, -PI / 2, about_point=ORIGIN),ShowCreation(su))
        pr1=Tex('A','+','iB=0').shift(4*LEFT+3*UP)
        self.remove(su)
        self.play(Transform(pr,pr1))

class Application2(Scene):
    def construct(self) -> None:
        frame=self.camera.frame
        circle=Circle()
        theta=Tex('\\theta_{1}',color=YELLOW).scale(0.5)
        theta2 = Tex('\\theta_{2}',color=PINK).scale(0.5)
        theta3 = Tex('(\\theta_{1}+\\theta_{2})', color=GREEN).scale(0.3)
        point=np.array([np.cos(45*DEGREES),np.sin(45*DEGREES),0])
        point1 = np.array([np.cos(120 * DEGREES), np.sin(120 * DEGREES), 0])
        point2 = np.array([np.cos(165 * DEGREES), np.sin(165 * DEGREES), 0])

        line=DashedLine(ORIGIN,point)
        line1 = DashedLine(ORIGIN, point1)
        line3 = DashedLine(ORIGIN, point2)
        arc=Arc(0,45*DEGREES,radius=0.3,color=YELLOW)
        arc1 = Arc(0, 120 * DEGREES, radius=0.4,color=PINK)
        arc2=Arc(0, 165 * DEGREES, radius=0.5,color=GREEN)
        line2=Line(ORIGIN,RIGHT)
        line2.add_updater(lambda v:v.become(Line(ORIGIN,circle.get_end())))
        theta.next_to(arc,RIGHT)
        theta2.next_to(arc1, RIGHT).shift(0.3*UP+0.5*LEFT)
        theta3.next_to(arc2,UP).shift(0.6*LEFT+0.3*DOWN).rotate(45*DEGREES)
        euler=Tex('e^{i\\theta}=\\cos(\\theta)+i\\sin(\\theta)',color=YELLOW).shift(4*LEFT+3*UP).fix_in_frame()
        firstp=Tex('e^{i\\theta_{1}}',color=YELLOW).shift(point*1.4).scale(0.5)
        secondp = Tex('e^{i\\theta_{2}}',color=PINK).shift(point1*1.2).scale(0.5)
        thirdp = Tex('e^{i(\\theta_{1}+\\theta_{2})}',color=GREEN).shift(point2 * 1.4).scale(0.5)
        euler1 = Tex('e^{i(\\theta_{1}+\\theta_{2})}=\\cos(\\theta_{1}+\\theta_{2})+i\\sin(\\theta_{1}+\\theta_{2})', color=GREEN).shift(4 * LEFT + 3 * UP).scale(0.6).fix_in_frame()
        euler1.next_to(euler,DOWN,aligned_edge=LEFT)
        lhs=Tex('L.H.S=e^{i(\\theta_{1}+\\theta_{2})}').next_to(euler1,DOWN,aligned_edge=LEFT).fix_in_frame()
        split=Tex('=e^{i\\theta_{1}}e^{i\\theta_{2}}').next_to(lhs,DOWN,aligned_edge=LEFT).fix_in_frame()
        further=Tex('=(\\cos(\\theta_{1})+i\\sin(\\theta_{1}))(\\cos(\\theta_{2})+i\\sin(\\theta_{2}))').scale(0.8).next_to(split,DOWN,aligned_edge=LEFT).fix_in_frame()
        more=Tex('=\\cos(\\theta_{1})\\cos(\\theta_{2})+i\\sin(\\theta_{1})\\cos(\\theta_{2})+i\\cos(\\theta_{1})\\sin(\\theta_{2})-\\sin(\\theta_{1})\\sin(\\theta_{2})').scale(0.6).next_to(further,DOWN,aligned_edge=LEFT).fix_in_frame()
        more1 = Tex(
            '=\\cos(\\theta_{1})\\cos(\\theta_{2})-\\sin(\\theta_{1})\\sin(\\theta_{2})+i(\\sin(\\theta_{1})\\cos(\\theta_{2})+\\cos(\\theta_{1})\\sin(\\theta_{2}))').scale(
            0.6).next_to(more, DOWN, aligned_edge=LEFT).fix_in_frame()

        touch=Tex('\\cos(\\theta_{1})\\cos(\\theta_{2})-\\sin(\\theta_{1})\\sin(\\theta_{2})+i(\\sin(\\theta_{1})\\cos(\\theta_{2})+\\cos(\\theta_{1})\\sin(\\theta_{2}))=\\cos(\\theta_{1}+\\theta_{2})+i\\sin(\\theta_{1}+\\theta_{2})').scale(
            0.6).next_to(more1, DOWN, aligned_edge=LEFT,buff=1).fix_in_frame()
        cos=Tex('\\cos(\\theta_{1}+\\theta_{2})=\\cos(\\theta_{1})\\cos(\\theta_{2})-\\sin(\\theta_{1})\\sin(\\theta_{2})').scale(0.8).next_to(touch,DOWN,aligned_edge=LEFT).fix_in_frame()

        sin=Tex('\\sin(\\theta_{1}+\\theta_{2})=\\sin(\\theta_{1})\\cos(\\theta_{2})+\\cos(\\theta_{1})\\sin(\\theta_{2})').scale(0.8).next_to(cos,DOWN,aligned_edge=LEFT).fix_in_frame()


        group=VGroup(circle,theta,theta2,line1,line,arc,arc1,line2,firstp,secondp,line3,arc2,theta3,thirdp)
        self.play(ShowCreation(line2))
        self.play(ShowCreation(circle))
        line2.clear_updaters()
        self.play(Write(euler))
        self.play(frame.scale,0.4)
        self.play(ShowCreation(line), Write(theta), ShowCreation(arc), ShowCreation(firstp))
        self.play(ShowCreation(line1), Write(theta2), ShowCreation(arc1), ShowCreation(secondp))
        self.play(ShowCreation(line3), Write(theta3), ShowCreation(arc2), ShowCreation(thirdp))

        self.play(group.shift,1.5*RIGHT+0.29*UP)
        for i in [ euler1, lhs, split, further, more,more1,touch,cos,sin]:
            self.play(ShowCreation(i))
            self.wait()
        # self.add(euler, euler1, lhs, split, further, more,more1,touch,cos,sin)

        #
class Application3(Scene):
    def construct(self) -> None:
        plane = ComplexPlane(x_range=[-10,10,1],y_range=[-8,8,1])
        label = plane.add_coordinate_labels()
        self.play(ShowCreation(label))
        point=np.array([2,1,0])
        pointl=Tex('2+i')
        pointl1=Tex('1+2i')
        line=DashedLine(ORIGIN,point)
        dot=Dot(point,color=RED)
        base=Vector(RIGHT,color=YELLOW)
        dot1=Dot(UP+RIGHT)
        self.play(ShowCreation(base))
        self.play(Rotate(base,90*DEGREES,about_point=ORIGIN))
        self.wait()
        self.remove(base)

        pointl.shift(1.5*point)
        self.play(ShowCreation(pointl),ShowCreation(dot),ShowCreation(dot1))
        self.remove(pointl)
        self.play(plane.shift,RIGHT)
        self.play(plane.shift, UP)
        self.play(Rotate(dot,PI/2,about_point=RIGHT+UP))
        self.play(plane.shift, -RIGHT)
        self.play(plane.shift, -UP)
        pointl1.next_to(dot,UP)
        self.play(ShowCreation(pointl1))
        rect=FullScreenRectangle().shift(LEFT*8)
        self.play(ShowCreation(rect))
        form=Tex('z','=','(','z_{1}','-a',')','e^{i\\theta}','+','a').shift(5*LEFT+3*UP)
        form1 = Tex('z', '=', '(', '(2+1i)', '-(1+1i)', ')', 'e^{i\\frac{\\pi}{2}}', '+', '(1+1i)').\
                scale(0.7).next_to(form,DOWN,aligned_edge=LEFT)
        simp=Tex('z', '=', '(', '1', '+0i)', ')', 'i', '+', '(1+1i)').next_to(form1,DOWN,aligned_edge=LEFT)
        fina=Tex('z=1+2i').next_to(simp,DOWN,aligned_edge=LEFT)
        self.play(ShowCreation(form))
        self.add(form1[0:3],form1[5:8])
        self.play(TransformFromCopy(form[3],form1[3]))
        self.play(TransformFromCopy(form[8], form1[8]),TransformFromCopy(form[4], form1[4]))
        self.play(ShowCreation(simp))
        self.play(ShowCreation(fina))

class Application4(Scene):
    def construct(self) -> None:
        integ=Tex(*['\\int\\frac{1}{x^{n}-1}'],color=YELLOW)

        ex=Tex(*['\\int\\frac{1}{x^{2}-1}','=','\\int\\left[\\frac{1}{x-1}+\\frac{1}{x+1}\\right]'],color=BLUE).next_to(integ,DOWN)

        ex2=Tex(*['\\int\\frac{1}{x^{4}-1}','=','\\int\\left[\\frac{A}{x-1}+\\frac{B}{x+1}+\\frac{Cx}{x^{2}+1}+\\frac{D}{x^{2}+1}\\right]'],color=YELLOW).next_to(ex,DOWN)

        group=VGroup(integ,ex,ex2)
        self.play(ShowCreation(integ))
        self.play(ShowCreation(ex))
        self.play(ShowCreation(ex2))

        self.wait(1)
        self.play(group.shift,3*UP)
        # ex3=Tex(*['\\int\\frac{1}{x^{5}-1}'],color=BLUE).next_to(group,DOWN)
        ex3=VMobject()
        for i in [5,6,7,'n',3]:
            tr=Tex(*['\\int\\frac{1}{',f'x^{i}','-1}'],color=BLUE).scale(2).next_to(group,DOWN)
            self.wait(1)
            self.play(Transform(ex3,tr))
        self.play(ex3.animate.move_to(5*LEFT+3*UP).scale(0.5),FadeOut(group))
        circl=Circle(color=YELLOW)
        self.add(circl)
        point=Dot(RIGHT*3,color=RED)
        lablep=Tex(*['p']).next_to(point,UP).scale(0.7)
        self.add(point,lablep)
        line=Line(circl.get_center(),point.get_center(),color=BLUE)
        self.add(line)
        all_point=VGroup()
        all_pointl=VGroup()
        for i in range(3):
           dot1=Dot(np.array([np.exp(1j*i*TAU/3).real,np.exp(1j*i*TAU/3).imag,0]))
           labeld=Tex(*[f"c_{i}"]).scale(0.7).next_to(dot1,UP)

           all_point.add(dot1)
           all_pointl.add(labeld)

        for k,col in enumerate([RED,PINK,GREEN]):

            arc=Arc(start_angle=k*TAU/3,angle=(k+1)*TAU/3-k*TAU/3,color=col)
            self.add(arc)
        brac=Brace(line,DOWN)
        brac1 = Brace(Line(point.get_center(),RIGHT), UP)
        self.add(brac)
        length=Tex('x','x-1').scale(0.7)
        length[0].next_to(brac,DOWN)
        length[1].next_to(brac1,UP)
        self.play(ShowCreationThenFadeOut(length[0],lag_ratio=2),ShowCreationThenFadeOut(brac,lag_ratio=2))
        self.play(ShowCreationThenFadeOut(length[1], lag_ratio=2), ShowCreationThenFadeOut(brac1, lag_ratio=2))

        line1=DashedLine(point.get_center(),all_point[1].get_center())
        line2 = DashedLine(point.get_center(), all_point[2].get_center())
        line3=DashedLine(all_point[1].get_center(),all_point[2].get_center())
        ngon=Polygon(*[i.get_center() for i in all_point])
        ngon1 = Polygon(*[i.get_center() for i in all_point])
        gon4=Polygon(*[np.array([np.exp(1j*i*TAU/4).real,np.exp(1j*i*TAU/4).imag,0]) for i in range(4)])
        gon5 = Polygon(*[np.array([np.exp(1j * i * TAU / 5).real, np.exp(1j * i * TAU / 5).imag, 0]) for i in range(5)])
        self.play(ShowCreation(ngon))
        for i in [gon4,gon5,ngon1]:
            self.play(Transform(ngon,i))
        self.play(ShowCreation(all_point))

        self.play(ShowCreation(all_pointl))
        # self.add(line1,line2,line3)
        self.play(ShowCreation(line1))
        self.play(Indicate(line1))
        c_point = Tex('\\left(-\\frac{1}{2},\\frac{\\sqrt{3}}{2} \\right)').scale(0.5).next_to(all_point[1], UP, buff=1)
        c_point1 = Tex('\\left( -\\frac{1}{2},-\\frac{\\sqrt{3}}{2} \\right)').scale(0.5).next_to(all_point[2], DOWN,
                                                                                                 buff=1)
        c_point2 = Tex('\\left( 1,0 \\right)').next_to(all_point[0], RIGHT)
        p_pont=Tex('\\left( x,0 \\right)').next_to(point, RIGHT)
        self.play(ShowCreation(c_point),ShowCreation(p_pont),ShowCreation(c_point1),ShowCreation(c_point2))

        root_unity=Tex(*['e^{\\frac{2\\pi ik}{n}}']).scale(1.5).shift(5*LEFT+3*UP)
        k_running=Tex('k=0,1,2...n-1').next_to(root_unity,RIGHT,buff=1)
        self.play(ex3.animate.shift(8*RIGHT))
        self.play(ShowCreation(root_unity),ShowCreation(k_running))
        self.play(FadeOut(c_point1),FadeOut(c_point2))
        dista=Tex("\\sqrt{(y_{1}-y_{0})^{2}+(x_{1}-x_{0})^{2}}").next_to(root_unity,DOWN,aligned_edge=LEFT,buff=1).scale(0.8)
        dista1 = Tex("\\sqrt{\\left(0-\\frac{\\sqrt{3}}{2}\\right)^{2}+\\left(x+\\frac{1}{2}\\right)^{2}}").move_to(dista).scale(0.6)
        dista2 = Tex("\\sqrt{\\left(0+\\frac{\\sqrt{3}}{2}\\right)^{2}+\\left(x+\\frac{1}{2}\\right)^{2}}").move_to(
            dista).scale(0.6).next_to(line2.get_center(),DOWN).scale(0.7)

        self.play(Write(dista))
        self.play(Transform(dista,dista1))
        self.play(dista.animate.next_to(line1.get_center(),UP,aligned_edge=ORIGIN).scale(0.7))
        self.play(FadeOut(c_point))
        self.play(FadeIn(c_point1))
        self.play(FadeIn(line2))
        self.play(Write(dista2))

        simply=Tex('x^{n}-1=').move_to(5*LEFT+3*UP)
        pc=Tex('U_{3}(x)=','pc_{0}','.','pc_{1}','.','pc_{2}').next_to(root_unity,DOWN,aligned_edge=LEFT)
        self.play(ShowCreation(pc))
        self.play(ShowCreationThenFadeOut(length[1], lag_ratio=2), ShowCreationThenFadeOut(brac1, lag_ratio=2))
        pc1 = Tex('U_{3}(x)=', '(x-1)', '.', '\\sqrt{\\left(0-\\frac{\\sqrt{3}}{2}\\right)^{2}+\\left(x+\\frac{1}{2}\\right)^{2}}', '.', '\\sqrt{\\left(0+\\frac{\\sqrt{3}}{2}\\right)^{2}+\\left(x+\\frac{1}{2}\\right)^{2}}')\
            .scale(0.5).next_to(root_unity, DOWN, aligned_edge=LEFT)
        pc2=Tex('U_{3}(x)=(x-1)(x^{2}+x+1)',color=BLUE).scale(0.7).next_to(pc1,DOWN,aligned_edge=LEFT)

        self.play(Transform(pc,pc1))
        self.play(Write(pc2))

class Application41(Scene):
    def construct(self) -> None:
        pc2 = Tex('U_{3}(x)=(x-1)(x^{2}+x+1)', color=BLUE).scale(0.7)
        ex = Tex(*['\\int\\frac{1}{x^{3}-1}', '=', '\\int\\frac{1}{(x-1)(x^{2}+x+1)}'],
                 color=YELLOW).next_to(pc2, DOWN)
        part=Tex("=\\int\\frac{1}{3(x-1)}+\\int\\frac{-(x+2)}{3(x^2+x+1)}",color=BLUE).scale(0.7)
        self.add(pc2,ex)
        self.play(ex[2].animate.scale(0.7).next_to(ex,DOWN,aligned_edge=LEFT))
        part.next_to(ex[2],RIGHT)
        self.play(Write(part))
        self.play(AnimationGroup(*[FadeOut(i) for i in [pc2,ex,part]]))
        circl = Circle(color=YELLOW)
        gon5 = Polygon(*[np.array([np.exp(1j * i * TAU / 5).real, np.exp(1j * i * TAU / 5).imag, 0]) for i in range(5)])
        self.play(ShowCreation(circl))
        self.play(ShowCreation(gon5))

        point = Dot(RIGHT * 3, color=RED)
        lablep = Tex(*['p']).next_to(point, UP).scale(0.7)
        self.add(point, lablep)
        line = Line(circl.get_center(), point.get_center(), color=BLUE)
        self.add(line)
        for i in [np.array([np.exp(1j * i * TAU / 5).real, np.exp(1j * i * TAU / 5).imag, 0]) for i in range(5)]:
            lin=DashedLine( point.get_center(),i, color=RED_E)
            self.play(ShowCreation(lin))
        u5=Tex("U_{5}(x)=(x-1).\\left(x^{2}+\\left[\\frac{1+\\sqrt{5}}{2}\\right]x+1\\right)."
               "\\left(x^{2}+\\left[\\frac{1-\\sqrt{5}}{2}\\right]x+1\\right)",color=BLUE).scale(0.7)  .next_to(circl,DOWN)
        self.play(ShowCreation(u5),run_time=4)
        self.wait(2)


class Root_of_unity(Scene):
    def construct(self) -> None:
        root_unity = Tex(*['e^{\\frac{2\\pi ik}{n}}']).scale(1.5).shift(5 * LEFT + 3 * UP)
        k_running = Tex('k=0,1,2...n-1').next_to(root_unity, RIGHT, buff=1)
        self.play(Write(root_unity))
        self.play(Write(k_running))
        exp=Tex("x^{n}-1=0").next_to(root_unity,DOWN,aligned_edge=LEFT)
        self.play(Write(exp))
        circl = Circle(color=YELLOW).scale(2)
        gon5 = Polygon(*[np.array([np.exp(1j * i * TAU / 8).real, np.exp(1j * i * TAU / 8).imag, 0]) for i in range(8)],color=RED).scale(2)
        self.play(ShowCreation(circl))
        self.play(ShowCreation(gon5))
