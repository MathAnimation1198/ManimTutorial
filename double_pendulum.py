from manimlib import *

class Pendulum(VGroup):
    def __init__(self,x,y,length=1,mass=1):
        self.mass=mass
        self.length=length
        VGroup.__init__(self)
        self.wall=self.get_wall()
        self.wall.shift(x*RIGHT+y*UP)
        self.pendulum=self.get_pendulum()
        self.line1=Line(self.dot.get_center(),self.dot.get_center()+self.length*DOWN)
        self.dot1=Dot(radius=self.mass).move_to(self.line1.get_end()).set_fill(color=YELLOW,opacity=1)
        self.second=VGroup(self.line1,self.dot1)
    def get_wall(self):
        line=Line(2*LEFT,2*RIGHT)
        line.shift(3*UP)
        return line
    def get_pendulum(self):
        line=Line(ORIGIN,self.length*DOWN)
        line.move_to(self.wall.get_center(),aligned_edge=UP)
        dot=Circle(radius=self.mass).set_fill(color=RED,opacity=1)
        dot.move_to(line.get_edge_center(DOWN),aligned_edge=ORIGIN)
        self.dot=dot
        self.line=line
        return self.add(dot,line)

class SingleP(Scene):
    def construct(self) -> None:
        pend=Pendulum(-3,0,length=3,mass=0.3)
        pend.pendulum.save_state()
        pend.second.save_state()
        theta=Tex('\\theta')


        value=ValueTracker(0)
        value.add_updater(lambda mob,dt: mob.increment_value(dt))



        self.add(pend.pendulum,pend.wall,value)



        self.play(ShowCreation(pend.pendulum))
        self.play(Rotate(pend.pendulum,75*DEGREES,about_point=pend.wall.get_center()))
        dline=DashedLine(pend.wall.get_center(),pend.wall.get_center()+DOWN)
        arc = ArcBetweenPoints(pend.pendulum[1].point_from_proportion(0.2), pend.wall.get_center()+0.6*DOWN,angle=-40*DEGREES)
        theta.next_to(arc.get_center()+0.5*DOWN,buff=0)
        self.add(arc,dline,theta)


        self.wait(2)



        b = 0.03
        m = 0.1
        g = 9.81
        l = 1
        x0 = 75*DEGREES
        v0 = 0

        dt = 0.015
        point=[]
        dot_tra=[]

        label=TexText('Damping Factor/Air Resistance','g','m','L','Initial angle','initial velocity').scale(0.7).shift(-2*RIGHT+0.8*DOWN)
        label.arrange(DOWN,center=False,aligned_edge=LEFT)
        outp=Tex('=0.3','=9.81','=0.1','=1','=75^{\\circ}','=0')
        for lab,o in zip(label,outp):
            o.next_to(lab,RIGHT)

        self.add(label,outp)

        axes=Axes(x_range=[0,15,1],y_range=[-1.5,1.5,1],width=6,height=2).shift(3*RIGHT)

        for h   in np.arange(0, 200, dt):
            dot_tra.append([h,x0])
            v0 = v0 + (-b * (v0 / m) - (g / l) * np.sin(x0)) * dt
            x0 = x0 + v0 * dt
            point.append([x0,v0])

        self.counter=0
        def update(mob):
              pend.pendulum.restore()
              mob.rotate(point[self.counter][0], about_point=pend.wall.get_center())
              self.counter+=1
        path=Line(axes.c2p(*dot_tra[0]),axes.c2p(*dot_tra[0]))
        self.tracker=1
        self.other1=0
        def line_upda(mob):
              line=Line(path.get_end(),axes.c2p(*dot_tra[self.tracker]))
              mob.become(path.append_vectorized_mobject(line))
              self.tracker+=1
        path.add_updater(line_upda)
        self.add(path,axes)
        arc.add_updater(lambda v,dt:v.become(ArcBetweenPoints(pend.pendulum[1].point_from_proportion(0.2), pend.wall.get_center()+0.6*DOWN,angle=-np.sign(point[self.counter][0])*40*DEGREES)))
        theta.add_updater(lambda v:v.next_to(arc.get_center()+0.5*DOWN,buff=0))
        pend.pendulum.add_updater(update)
        self.wait(40)

class DoubleP(Scene):
    def construct(self) -> None:
        g=9.8
        M1=0.15
        M2=0.15
        R1=1.8
        R2=1.8

        theta1=90*DEGREES
        theta1dot=0
        theta2=10*DEGREES
        theta2dot=0
        gravity=Tex('G=9.8','M_{1}=0.15','M_{1}=0.15','R_{1}=1.8','R_{2}=1.8','\\theta_{1}=90^{\circ}','\\dot{\\theta_{1}}=0','\\theta_{2}=10^{\circ}','\\dot{\\theta_{2}}=0').shift(1*RIGHT+3*UP)
        gravity.arrange(DOWN,center=False,aligned_edge=LEFT)
        self.add(gravity)

        mas1=Dot(radius=M1,color=YELLOW).move_to(np.array([R1*np.sin(theta1),-R1*np.cos(theta1),0]))
        string = Line(ORIGIN,mas1.get_center() )
        mas2 = Dot(radius=M2,color=RED).move_to(mas1.get_center()+np.array([R2 * np.sin(theta2), -R2* np.cos(theta2), 0]))
        string1 = Line(mas1.get_center(), mas2.get_center())

        self.add(mas1,mas2,string,string1)

        t = 0
        dt = 0.04
        point=[]

        while t < 300:

            num=-g*(2*M1+M2)*np.sin(theta1) - M2*g*np.sin(theta1-2*theta2) - 2*np.sin(theta1-theta2)*M2*(theta2dot**2*R2+theta1dot**2*R1*np.cos(theta1-theta2))
            den=R1*(2*M1+M2-M2*np.cos(2*theta1-2*theta2))

            num1=2*np.sin(theta1-theta2)*(theta1dot**2*R1*(M1+M2)+g*(M1+M2)*np.cos(theta1)+theta2dot**2*R2*M2*np.cos(theta1-theta2))
            den1=R2*(2*M1+M2-M2*np.cos(2*theta1-2*theta2))

            theta2ddot=num1/den1
            theta2dot = theta2dot + theta2ddot * dt
            theta2 = theta2 + theta2dot * dt

            theta1ddot=num/den
            theta1dot = theta1dot + theta1ddot * dt
            theta1 = theta1 + theta1dot * dt

            point.append([theta1,theta2])
            t = t + dt
        self.counter=0
        def massupd(mob,dt):
            mob.move_to(np.array([R1*np.sin(point[self.counter][0]),-R1*np.cos(point[self.counter][0]),0]))
            self.counter+=1
        self.counter1=0
        def mass1upd(mob,dt):
            mob.move_to(mas1.get_center()+np.array([R2 * np.sin(point[self.counter][1]), -R2* np.cos(point[self.counter][1]), 0]))
            self.counter1+=1
        mas1.add_updater(massupd)
        mas2.add_updater(mass1upd)
        string.add_updater(lambda v:v.become(Line(ORIGIN,mas1.get_center() )))
        string1.add_updater(lambda v: v.become(Line(mas1.get_center(), mas2.get_center())))
        self.wait(100)

