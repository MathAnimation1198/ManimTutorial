from manimlib import *

class Myscreen(Rectangle):
    def __init__(self,height=4):
        self.height=height
        self.width=self.height*(16/9)
        Rectangle.__init__(self,width=self.width,height=height)
    def get_right(self):
        return self.width/2
    def get_left(self):
        return -self.width/2
    def get_top(self):
        return self.height/2
    def get_down(self):
        return -self.height/2

class Ball(Circle):
    def __init__(self,radius=1):
        self.radius=radius
        self.mass=PI*self.radius**2
        Circle.__init__(self,radius=self.radius,color=BLUE)
        self.set_fill(color=BLUE,opacity=1)
    def get_right(self):
        return self.get_center()[0]+self.radius
    def get_left(self):
        return self.get_center()[0]-self.radius
    def get_top(self):
        return self.get_center()[1]+self.radius
    def get_down(self):
        return self.get_center()[1]-self.radius


class OneBallCollision(Scene):
    def construct(self) -> None:
        screen=Myscreen(height=5)
        velocities=[2*RIGHT]
        colors=[RED]
        position=[RIGHT * 2]
        for i,rad in zip(range(1),[0.5]):
            ball=Ball(radius=rad).set_color(color=colors[i])
            ball.id=i
            ball.velocity=velocities[i]
            ball.shift(position[i])


        def update(mob,dt):
            mob.acceleration=np.array([0,-0.1,0])
            mob.velocity+=mob.acceleration
            mob.shift(mob.velocity*dt)
            handle_with_box(mob,screen)

        def handle_with_box(bal,scren):

            if bal.get_right()>=scren.get_right() or \
            bal.get_left()<=scren.get_left():
                self.add_sound('hit.mp3',time_offset=-0.3)
                bal.velocity[0]=-bal.velocity[0]

            if bal.get_top()>=scren.get_top() or \
            bal.get_down()<=scren.get_down():
                self.add_sound('hit.mp3',time_offset=-0.3)
                bal.velocity[1]=-bal.velocity[1]

        # this code is taken from
        # https://github.com/nipunramk/Reducible/blob/master/2021/Collision/collision.py

        ball.add_updater(update)
        self.add(ball,screen)
        self.wait(30)

class TwoBallCollision(Scene):
    def construct(self) -> None:
        screen=Myscreen(height=4)
        balls=[]
        velocities=[RIGHT * 2 + UP * 2, LEFT * 1 + UP * 2]
        colors=[RED,YELLOW]
        position=[RIGHT * 2, RIGHT * -2]
        for i,rad in zip(range(2),[0.3,0.4]):
            ball=Ball(radius=rad).set_color(color=colors[i])
            ball.id=i
            ball.velocity=velocities[i]
            ball.shift(position[i])
            balls.append(ball)

        def update(mob,dt):
            mob.shift(mob.velocity*dt)
            handle_with_box(mob,screen)
            handle_ball_collisions(mob)

        def handle_with_box(bal,scren):

            if bal.get_right()>=scren.get_right() or \
            bal.get_left()<=scren.get_left():
                self.add_sound('hit.mp3', time_offset=-0.3)
                bal.velocity[0]=-bal.velocity[0]
            if bal.get_top()>=scren.get_top() or \
            bal.get_down()<=scren.get_down():
                self.add_sound('hit.mp3', time_offset=-0.3)
                bal.velocity[1]=-bal.velocity[1]
        # this code is taken from
        # https://github.com/nipunramk/Reducible/blob/master/2021/Collision/collision.py
        def handle_ball_collisions(ball):
            t_colors = [RED, ORANGE, GREEN_SCREEN, GOLD, PINK, WHITE]
            i = 0
            for other_ball in balls:
                if ball.id != other_ball.id:
                    dist = np.linalg.norm(ball.get_center() - other_ball.get_center())
                    if dist<= (ball.radius + other_ball.radius):
                        self.add_sound('hit.mp3', time_offset=-0.3)
                        v1, v2 = get_response_velocities(ball, other_ball)
                        ball.velocity = v1
                        other_ball.velocity = v2

        def get_response_velocities(ball, other_ball):
            # https://en.wikipedia.org/wiki/Elastic_collision
            v1 = ball.velocity
            v2 = other_ball.velocity
            m1 = ball.mass
            m2 = other_ball.mass
            x1 = ball.get_center()
            x2 = other_ball.get_center()

            ball_response_v = compute_velocity(v1, v2, m1, m2, x1, x2)
            other_ball_response_v = compute_velocity(v2, v1, m2, m1, x2, x1)
            return ball_response_v, other_ball_response_v

        def compute_velocity(v1, v2, m1, m2, x1, x2):
            return v1 - (2 * m2 / (m1 + m2)) * np.dot(v1 - v2, x1 - x2) / np.linalg.norm(x1 - x2) ** 2 * (x1 - x2)




        for ball in balls:
          ball.add_updater(update)
          self.add(ball)
        self.add(screen)
        self.wait(40)

class FourBallCollision(Scene):
    def construct(self) -> None:
        screen=Myscreen(height=4)
        balls=[]
        velocities=[RIGHT * 2 + UP * 2, LEFT * 1 + UP * 2, RIGHT * 1 + UP * 1 ,LEFT+DOWN]
        colors=[RED,YELLOW,GREEN,PINK]
        position=[RIGHT * 2, RIGHT * -2,UP+RIGHT,LEFT+UP]
        for i,rad in zip(range(4),[0.3,0.3,0.3,0.3]):
            ball=Ball(radius=rad).set_color(color=colors[i])
            ball.id=i
            ball.velocity=velocities[i]
            ball.shift(position[i])
            balls.append(ball)

        def update(mob,dt):
            mob.shift(mob.velocity*dt)
            handle_with_box(mob,screen)
            handle_ball_collisions(mob)

        def handle_with_box(bal,scren):

            if bal.get_right()>=scren.get_right() or \
            bal.get_left()<=scren.get_left():
                self.add_sound('hit.mp3', time_offset=-0.3)
                bal.velocity[0]=-bal.velocity[0]
            if bal.get_top()>=scren.get_top() or \
            bal.get_down()<=scren.get_down():
                self.add_sound('hit.mp3', time_offset=-0.3)
                bal.velocity[1]=-bal.velocity[1]
        # this code is taken from
        # https://github.com/nipunramk/Reducible/blob/master/2021/Collision/collision.py
        def handle_ball_collisions(ball):
            t_colors = [RED, ORANGE, GREEN_SCREEN, GOLD, PINK, WHITE]
            i = 0
            for other_ball in balls:
                if ball.id != other_ball.id:
                    dist = np.linalg.norm(ball.get_center() - other_ball.get_center())
                    if dist<= (ball.radius + other_ball.radius):
                        self.add_sound('hit.mp3', time_offset=-0.3)
                        v1, v2 = get_response_velocities(ball, other_ball)
                        ball.velocity = v1
                        other_ball.velocity = v2

        def get_response_velocities(ball, other_ball):
            # https://en.wikipedia.org/wiki/Elastic_collision
            v1 = ball.velocity
            v2 = other_ball.velocity
            m1 = ball.mass
            m2 = other_ball.mass
            x1 = ball.get_center()
            x2 = other_ball.get_center()

            ball_response_v = compute_velocity(v1, v2, m1, m2, x1, x2)
            other_ball_response_v = compute_velocity(v2, v1, m2, m1, x2, x1)
            return ball_response_v, other_ball_response_v

        def compute_velocity(v1, v2, m1, m2, x1, x2):
            return v1 - (2 * m2 / (m1 + m2)) * np.dot(v1 - v2, x1 - x2) / np.linalg.norm(x1 - x2) ** 2 * (x1 - x2)




        for ball in balls:
          ball.add_updater(update)
          self.add(ball)
        self.add(screen)
        self.wait(40)