from manim import *
import random

class change_basis(Scene):
    def construct(self):
        value1=ValueTracker(1)
        value2=ValueTracker(1)

        x_hat=always_redraw(lambda : Vector(RIGHT*value1.get_value(),color=GREEN))
        y_hat=always_redraw(lambda :Vector(UP*value2.get_value(),color=YELLOW))
        self.add(x_hat)

        # point=Dot(self.plane.coords_to_point(2,1),color=RED)

        # self.add(point,point_label)
        # self.play(Indicate(point))
        # value= ValueTracker(0)
        # r_line= always_redraw(lambda: DashedLine(ORIGIN,2*RIGHT*value.get_value(),color=RED))
        #
        x_axis = Matrix([
            [1],
            [0]
        ]).set_color(GREEN).to_corner(LEFT+UP).shift(RIGHT)
        mltply=MathTex("\\times",font_size=30,color=PINK).next_to(x_axis,LEFT,0)
        label1 = always_redraw(lambda: DecimalNumber(value1.get_value(),font_size=24).next_to(mltply,LEFT,buff=0))
        self.add(x_axis,label1,mltply)
        self.play(value1.animate.set_value(4),rate_func=there_and_back,run_time=2)
        self.play(value1.animate.set_value(-4),rate_func=there_and_back,run_time=2)

        #
        # x_axis.add_updater(lambda v:v.next_to(r_line,RIGHT))
        #
        # self.add(r_line,x_axis)
        # self.play(value.animate.set_value(1))
        # x_axis.clear_updaters()
        # r_line.clear_updaters()
        # self.remove(x_axis)
        # r_line1 = always_redraw(lambda: DashedLine(2 * RIGHT, 2 * RIGHT + UP * value.get_value(), color=YELLOW))
        y_axis = Matrix([
            [0],
            [1]
        ]).set_color(YELLOW).next_to(x_axis,RIGHT,buff=1.5)
        mltply_copy = mltply.copy().next_to(y_axis, LEFT, 0)
        label2 = always_redraw(lambda: DecimalNumber(value2.get_value(), font_size=24).next_to(mltply_copy, LEFT, buff=0))
        plus = MathTex("+","=")
        plus[0].next_to(x_axis,RIGHT)
        self.add(y_axis, label2, mltply_copy,y_hat,plus[0])
        self.play(value2.animate.set_value(4),rate_func=there_and_back,run_time=2)
        self.play(value2.animate.set_value(-4),rate_func=there_and_back,run_time=2)
        plane=NumberPlane()
        self.play(Create(plane))
        point=Dot(2*RIGHT+3*UP)
        point_label = MathTex("(2,3)").next_to(point, UP)
        self.add(point,point_label)
        self.play(value1.animate.set_value(2), run_time=2)
        self.play(value2.animate.set_value(3), run_time=2)
        copy_j_hat=y_hat.copy()
        self.play(ApplyMethod(copy_j_hat.next_to,2*RIGHT,UP,0,path_arc=-1))
        equal=plus[1].next_to(y_axis,RIGHT)
        self.add(equal)
        result = Matrix([
            [2],
            [3]
        ]).set_color(RED).next_to(equal, RIGHT)
        self.play(Create(result))
        self.wait()
        # y_axis.add_updater(lambda v: v.next_to(r_line1, UP))
        # self.add(r_line1, y_axis)
        # value.set_value(0)
        # self.play(value.animate.set_value(1))
        # self.remove(y_axis)
        # line=DashedLine(ORIGIN,2 * RIGHT + UP,color=YELLOW)
        # self.play(Create(line))
        # bases_mat=Matrix([
        #     [1,0],
        #     [0,1]
        # ]).set_color(RED).scale(0.5).to_edge(LEFT+UP)
        # self.play(Create(bases_mat))
        # self.wait()

class change_of_basis_matrix(LinearTransformationScene,MovingCameraScene):
    def __init__(self, *kwargs):
        LinearTransformationScene.__init__(self, show_basis_vectors=True,background_plane_kwargs={"x_range":(-20,20,1),"y_range":(-10,10,1)})
        MovingCameraScene.__init__(self)
    def construct(self):
        # self.camera.background_color=WHITE
        self.camera.frame.save_state()
        self.camera.frame.scale(2.2)
        # line=Line(-15*np.array([1,-1,0]),15*np.array([1,-1,0]))
        # line1 = Line(-15 * np.array([1, -2, 0]), 15 * np.array([1, -2, 0]))
        # # self.add(line,line1)
        # vect=Vector(np.array([-1,1,0]))
        # vect1 = Vector(np.array([1, -2, 0]))
        # self.moving_vectors += list(vect)
        c_b_m=[
            [1,-1],
            [2,4]
        ]
        self.apply_matrix(c_b_m)
        mat=Matrix(c_b_m).set_column_colors(GREEN,RED)
        self.play(mat.animate.shift(np.array([-11,6,0])))
        column = mat.get_columns()
        mat1 = Matrix(
            [
                [1],
                [2]
            ]
        ).set_column_colors(GREEN).move_to(column[0])
        mat2 = Matrix(
            [
                [-1],
                [4]
            ]
        ).set_column_colors(RED).move_to(column[1])
        self.play(mat1.animate.next_to(self.i_hat,UP))
        self.play(mat2.animate.next_to(self.j_hat, UP))
        self.wait(2)
        self.remove(mat1,mat2)
        self.moving_mobjects=[]
        self.apply_inverse(c_b_m)
        matn=always_redraw(lambda : Matrix(
            [
                [1],
                [2]
            ]
        ).set_column_colors(GREEN).move_to(self.i_hat.get_end(),aligned_edge=LEFT))
        matn1 = always_redraw(lambda: Matrix(
            [
                [-1],
                [4]
            ]
        ).set_column_colors(RED).move_to(self.j_hat.get_end(), aligned_edge=RIGHT))
        # points = []
        # for p_p in range(-20, 20, 1):
        #     for p in range(-10, 10, 1):
        #         points.append(np.array([p_p, p, 0]))
        # dots = VGroup(*[Dot(p) for p in points])
        # self.play(Create(dots))
        example1=Matrix([
            [2],
            [1]
        ]).next_to(mat,RIGHT,buff=0.1)

        example_point=Dot(np.array([2,1,0]),color=YELLOW)
        example_label=MathTex("=","(2,1)","(1,8)")
        example_label[0].next_to(example1,RIGHT,buff=0.1)
        example1_result = Matrix(np.dot(c_b_m, [[2], [1]])).next_to(example_label[0],RIGHT,buff=0.2)
        example_point_label=always_redraw(lambda :example_label[1].next_to(example_point,UP))
        self.wait(2)
        self.play(Create(example_label[0]), Create(example_point_label),Create(example1))
        self.moving_mobjects=[example_point]
        # self.add_transformable_mobject(dots)
        self.apply_matrix(c_b_m)
        self.play(Transform(example_point_label,example_label[2].move_to(example_point_label)),Create(example1_result))
        self.wait()
        x_v,y_v=self.basis_vectors
        x_x_v,y_v_c=x_v.copy(),y_v.copy()
        self.play(Wiggle(mat,scale_value=1.5,rotation_angle=0.04*TAU))
        self.play(ApplyMethod(x_x_v.shift,x_v.get_end(),path_arc=PI))
        self.play(ApplyMethod(y_v_c.shift, x_x_v.get_end(), path_arc=PI))
        label1=BraceBetweenPoints(ORIGIN,x_x_v.get_end())
        label2=BraceBetweenPoints(x_x_v.get_end(),y_v_c.get_end())
        lab=MathTex("2","1")
        pnt=x_v.get_end()
        rpnt=np.array([-pnt[1],pnt[0],0])
        lab[0].move_to(pnt-rpnt*0.4)
        lab[1].next_to(label2,RIGHT)
        self.play(Create(label1),Create(label2),Create(lab))
        self.wait()
        self.remove(label1,label2,lab,x_x_v,y_v_c)
        self.moving_mobjects=[]
        self.apply_inverse(c_b_m)
        self.wait()
        x_v, y_v = self.basis_vectors
        x_x_v, y_v_c = x_v.copy(), VGroup(*[y_v.copy() for _ in range(8)])
        first=y_v_c[0]
        self.play(ApplyMethod(first.shift,RIGHT,path_arc=PI))
        for i in y_v_c[1:]:
            self.play(ApplyMethod(i.next_to,first.get_end(),UP,0,path_arc=PI),run_time=0.5)
            first=i
        self.wait()
        label1 = BraceBetweenPoints(ORIGIN, x_x_v.get_end())
        label2 = BraceBetweenPoints(x_x_v.get_end(), y_v_c[-1].get_end())
        lab = MathTex("8", "1")
        lab[0].next_to(label2,RIGHT)
        lab[1].next_to(label1, DOWN)
        our=np.array([
            [1,0],
            [0,1]
        ])
        our_m=Matrix(our).set_column_colors(GREEN,RED).next_to(label2,RIGHT,buff=2)
        self.add(label1, label2, lab,our_m)
        self.wait()
        # self.moving_mobjects=[]
        # self.apply_inverse(c_b_m)
        # points = []
        # for p_p in range(-20, 20, 1):
        #     for p in range(-10, 10, 1):
        #         points.append(np.array([p_p, p, 0]))
        # dots = VGroup(*[Dot(p) for p in points])
        # self.play(Create(dots))
        # self.moving_mobjects=[dot for dot in dots]
class MatrixMultiplication(Scene):
    def construct(self):
        c_b_m = [
            [1, -1],
            [2, 4]
        ]
        c_b = [
            [2],
            [1]
        ]
        mat=Matrix(c_b_m).shift(LEFT).set_column_colors(GREEN, RED)
        v=Matrix(c_b).next_to(mat,RIGHT,0.1)
        equal=MathTex("=").next_to(v,RIGHT)
        taget_mat=MobjectMatrix([
            [MathTex("(1)(2)+","(-1)(1)")],
            [MathTex("(2)(2)+","(4)(1)")]
        ]
        ).next_to(equal,RIGHT)
        self.play(Create(mat),Create(v))
        bracket=taget_mat.get_brackets()
        self.add(bracket,equal)
        element=mat.get_rows()
        v_elemet=v.get_entries()
        taget_value=taget_mat.get_entries()
        for row in range(2):
            sour=SurroundingRectangle(element[row]).set_fill(color=YELLOW,opacity=0.4)
            sour1 = SurroundingRectangle(v_elemet).set_fill(color=YELLOW, opacity=0.4)
            self.play(FadeIn(sour),FadeIn(sour1),rate_func=there_and_back,run_time=2)
            for col in range(2):
                elem=element[row][col]
                cir=Circle(color=YELLOW).surround(elem)
                v_ele_a=v_elemet[col]
                v_ele=Circle().surround(v_ele_a)
                self.play(Create(cir),Create(v_ele),rate_func=there_and_back)
                group=VGroup(elem,v_ele_a)
                target_v=taget_value[row][col]
                self.play(TransformFromCopy(group,target_v))
        final_value=MathTex("1","8")
        final_value[0].move_to(taget_value[0])
        final_value[1].move_to(taget_value[1])
        for i in range(2):
            self.play(Transform(taget_value[i],final_value[i]))
        # for i in range(2):
        #     for j in range(2):
        taget_value[1].next_to(taget_value[0],DOWN,0.5)
        self.play(ApplyMethod(taget_value.shift,1.9*LEFT),ApplyMethod(bracket[1].shift,3.5*LEFT))
        self.wait()


# class MatrixMultiplication(Scene):
#     def construct(self):
#         # Define matrices
#         matrix_a = [[1, 2],
#                     [3, 4]]
#         matrix_b = [[5, 6],
#                     [7, 8]]
#
#         # Display matrices
#         matrix_a_tex = Matrix(matrix_a)
#         matrix_b_tex = Matrix(matrix_b)
#
#         matrix_a_tex.next_to(ORIGIN, LEFT)
#         matrix_b_tex.next_to(matrix_a_tex, RIGHT)
#
#         self.play(Write(matrix_a_tex), Write(matrix_b_tex))
#
#         # Calculate multiplication result
#         result = [[0, 0],
#                   [0, 0]]
#         for i in range(2):
#             for j in range(2):
#                 for k in range(2):
#                     result[i][j] += matrix_a[i][k] * matrix_b[k][j]
#
#         # Display result matrix
#         result_tex = Matrix(result)
#         result_tex.next_to(matrix_b_tex, RIGHT)
#
#         self.play(Write(result_tex))
#
#         # Animate multiplication arrows
#         for i in range(2):
#             for j in range(2):
#                 for k in range(2):
#                     arrow_a = Arrow(matrix_a_tex.get_rows()[i][k].get_center(), matrix_b_tex.get_rows()[k][j].get_center(), buff=SMALL_BUFF)
#                     arrow_b = Arrow(matrix_b_tex.get_rows()[k][j].get_center(), result_tex.get_rows()[i][j].get_center(), buff=SMALL_BUFF)
#                     self.play(GrowArrow(arrow_a), GrowArrow(arrow_b))
#
#         self.wait(2)

class Reverse_matrix_quetion(LinearTransformationScene,MovingCameraScene):
    def __init__(self, *kwargs):
        LinearTransformationScene.__init__(self, show_basis_vectors=True,background_plane_kwargs={"x_range":(-20,20,1),"y_range":(-10,10,1)})
        MovingCameraScene.__init__(self)
    def construct(self):
        self.camera.frame.save_state()
        self.camera.frame.scale(2.2)
        c_b_m = [
            [1, -1],
            [2, 4]
        ]
        # self.apply_matrix(c_b_m)
        mat = Matrix(c_b_m).set_column_colors(GREEN, RED)
        mat.shift(np.array([-11, 6, 0]))
        mat_c=mat.copy()
        self.play(Create(mat))
        # dot=Dot(2*RIGHT+UP,color=YELLOW)
        # vect1,vect2=Vector(np.array([1,-2,0])),Vector(np.array([-1,1,0]))
        # line1,line2=Line(10*np.array([1,-2,0]),-10*np.array([1,-2,0])),Line(10*np.array([-1,1,0]),-10*np.array([-1,1,0]))
        # self.add(line1,line2)
        self.moving_mobjects=[]
        # self.moving_vectors+=[vect1,vect2]
        self.apply_matrix(c_b_m)
        unlnown_vector=Matrix(np.array([
            ["x"],
            ["y"]
        ])).next_to(mat,RIGHT,buff=0.2)
        self.add(unlnown_vector)
        equal=MathTex("=").next_to(unlnown_vector,RIGHT,buff=0.2)
        target=Matrix(np.array([
            [1],
            [8]
        ])).next_to(equal,RIGHT)
        target_point=Dot(RIGHT+8*UP,color=YELLOW)
        self.add(target,equal,target_point)
        mat_inv_o=Matrix(c_b_m,right_bracket="]^{-1}").set_column_colors(GREEN, RED).next_to(equal,RIGHT,0.1)
        mat_inv=Matrix([
            ["\\frac{4}{6}","\\frac{1}{6}"],
            ["\\frac{-2}{6}","\\frac{1}{6}"]
        ],v_buff=1.5)
        x_v, y_v = self.basis_vectors
        x_x_v, y_v_c = x_v.copy(), y_v.copy()
        mat_inv.next_to(equal,RIGHT,0.2).set_column_colors(GREEN, RED)
        self.play(ApplyMethod(target.next_to,mat_inv,RIGHT,0.1))
        self.play(AnimationGroup(Wiggle(x_v, scale_value=1.5, rotation_angle=0.03 * TAU),Wiggle(y_v, scale_value=1.5, rotation_angle=0.03 * TAU),lag_ratio=0.5),run_time=2)
        self.play(Transform(mat,mat_inv_o,path_arc=1),rate_func=linear,run_time=2)
        # self.play(Transform(mat,mat_c))
        self.wait()
        self.play(Transform(mat,mat_inv),run_time=2)
        known_vector=Matrix([
            [2],
            [1]
        ]).move_to(unlnown_vector)
        equal_c=equal.copy().next_to(target,RIGHT)
        known_vector.next_to(equal_c,RIGHT)

        self.play(Create(equal_c))
        self.play(Create(known_vector))
        # x_v, y_v = self.basis_vectors
        # x_x_v, y_v_c = x_v.copy(), y_v.copy()
        self.play(ApplyMethod(x_x_v.shift, x_v.get_end(), path_arc=PI))
        self.play(ApplyMethod(y_v_c.shift, x_x_v.get_end(), path_arc=PI))
        label1 = BraceBetweenPoints(ORIGIN, x_x_v.get_end())
        label2 = BraceBetweenPoints(x_x_v.get_end(), y_v_c.get_end())
        lab = MathTex("2", "1")
        pnt = x_v.get_end()
        rpnt = np.array([-pnt[1], pnt[0], 0])
        lab[0].move_to(pnt - rpnt * 0.4)
        lab[1].next_to(label2, RIGHT)
        self.play(Create(label1))
        self.play(Create(label2))
        self.play(Create(lab))
        self.wait()
from functools import reduce
class eigen_basis(Scene):

    def construct(self):
        plane=NumberPlane()
        self.background_plane_kwargs = {
            "color": GREY,
            "axis_config": {
                "color": GREY,
            },
            "background_line_style": {
                "stroke_color": GREY,
                "stroke_width": 1,
            },

        }
        backgroun=NumberPlane(**self.background_plane_kwargs)
        self.add(backgroun)

        eigen = np.array([
            [1, -1],
            [0, 1]
        ])
        vect1=Vector(RIGHT,color=GREEN)
        vect2=Vector(UP,color=YELLOW)
        transformable=[plane,backgroun]
        new_matrix = np.identity(3)
        new_matrix[:2, :2] = eigen
        moving_vector=[vect1,vect2]
        anim=[ApplyPointwiseFunction(lambda p:np.dot(p,new_matrix.T),t)  for t in transformable]+[self.moving_vectors(moving_vector,new_matrix)]
        print(anim)
        self.play(*anim,run_time=2)
        eigen1=np.array([
            [3,0],
            [0,2]
        ]
        )
        new_matrix1 = np.identity(3)
        new_matrix1[:2, :2] = eigen1
        line=Line(ORIGIN,LEFT+UP,color=YELLOW)
        transformable1=[plane,vect2,vect1]
        self.final_mat = reduce(np.dot, [new_matrix, new_matrix1, np.linalg.inv(new_matrix)])
        def change_of_base(p):
            # in_him=np.dot(p,np.linalg.inv(new_matrix).T)
            # t_p=np.dot(in_him,new_matrix1.T)
            return np.dot(p,self.final_mat.T)
        anim1=[ApplyPointwiseFunction(change_of_base,t)  for t in transformable1]+[self.moving_vectors([vect2,vect1],self.final_mat)]
        self.play(*anim1,run_time=2)
        self.wait()

    def get_piece_movement(self, pieces):

        start = VGroup(*pieces)
        target = VGroup(*(mob.target for mob in pieces))
        return Transform(start, target)

    def moving_vectors(self,moving_vectors,matrix):
        for v in moving_vectors:
            v.target = Vector(np.dot(v.get_end(),matrix.T), color=v.get_color())
            norm = np.linalg.norm(v.target.get_end())
            if norm < 0.1:
                v.target.get_tip().scale(norm)
        return self.get_piece_movement(moving_vectors)


class eigen_basis1(Scene):

    def construct(self):
        plane=NumberPlane()
        self.background_plane_kwargs = {
            "color": GREY,
            "axis_config": {
                "color": GREY,
            },
            "background_line_style": {
                "stroke_color": GREY,
                "stroke_width": 1,
            },

        }
        backgroun=NumberPlane(**self.background_plane_kwargs)
        self.add(backgroun)

        eigen = np.array([
            [1, -1],
            [0, 1]
        ])
        vect1=Vector(RIGHT,color=GREEN)
        vect2=Vector(UP,color=YELLOW)
        transformable=[plane,backgroun]
        new_matrix = np.identity(3)
        new_matrix[:2, :2] = eigen
        moving_vector=[vect1,vect2]
        anim=[ApplyPointwiseFunction(lambda p:np.dot(p,new_matrix.T),t)  for t in transformable]+[self.moving_vectors(moving_vector,new_matrix)]
        print(anim)
        self.play(*anim,run_time=2)
        eigen1=np.array([
            [3,0],
            [0,2]
        ]
        )
        new_matrix1 = np.identity(3)
        new_matrix1[:2, :2] = eigen1
        line=Line(ORIGIN,LEFT+UP,color=YELLOW)
        transformable1=[plane,vect2,vect1]
        self.final_mat = reduce(np.dot, [new_matrix, new_matrix1, np.linalg.inv(new_matrix)])
        def change_of_base(p):
            # in_him=np.dot(p,np.linalg.inv(new_matrix).T)
            # t_p=np.dot(in_him,new_matrix1.T)
            return np.dot(p,self.final_mat.T)
        anim1=[ApplyPointwiseFunction(change_of_base,t)  for t in transformable1]+[self.moving_vectors([vect2,vect1],self.final_mat)]
        self.play(*anim1,run_time=2)
        self.wait()

    def get_piece_movement(self, pieces):

        start = VGroup(*pieces)
        target = VGroup(*(mob.target for mob in pieces))
        return Transform(start, target)

    def moving_vectors(self,moving_vectors,matrix):
        for v in moving_vectors:
            v.target = Vector(np.dot(v.get_end(),matrix.T), color=v.get_color())
            norm = np.linalg.norm(v.target.get_end())
            if norm < 0.1:
                v.target.get_tip().scale(norm)
        return self.get_piece_movement(moving_vectors)




class Introduction_of():
    def construct(self):
        tx=MathTex("AMA^{-1}",color=YELLOW)

class Rotating_with_matix(Animation):
    def __init__(
        self,
        mobject: Mobject,
        axis: np.ndarray = OUT,
        radians: np.ndarray = TAU,
        about_point: np.ndarray = None,
        about_edge: np.ndarray= None,
        run_time: float = 5,
        rate_func= linear,
        **kwargs,
    ) -> None:
        self.axis = axis
        self.radians = radians
        self.about_point = about_point
        self.about_edge = about_edge
        super().__init__(mobject, run_time=run_time, rate_func=rate_func, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        self.mobject.become(self.starting_mobject)
        rotation_m = rotation_about_z(self.rate_func(alpha)*-self.radians)
        #axis about which you want to rotate and we consider it as z axis
        rotation_about_arr = normalize(self.axis)
        # y-axis with respect to rotation axis
        y_arr = normalize(np.cross(RIGHT, rotation_about_arr))
        # x-axis with respect to rotation axis
        x_arr = np.cross(rotation_about_arr, y_arr)
        #new coordinate system
        perp_vect = np.array([
            x_arr,
            y_arr,
            rotation_about_arr
        ]).T
        #rotation matrix about given axis in our coordinate system in our coordinate system
        final_mat = reduce(np.dot, [perp_vect, rotation_m, np.linalg.inv(perp_vect)])
        self.mobject.apply_matrix(final_mat
        )
class Crossp(Scene):
    def construct(self):
        mat=Matrix([
            [1],
            [1],
            [1]
        ])
        nor=normalize(np.array([1,1,1]))
        normal=[[round(i,2)] for i in nor]
        matn=Matrix(normal).set_color(YELLOW)
        self.play(Transform(mat,matn))
        cros_sign = MathTex("\\times").next_to(mat,RIGHT,0.1)
        riight=Matrix([
            [1],
            [0],
            [0]
        ]).next_to(cros_sign,RIGHT,0.1)
        self.add(riight,cros_sign)
        cross_product=np.cross(RIGHT,nor)
        equal=MathTex("=").next_to(riight,RIGHT,0.1)
        cros_mat=Matrix([[round(j,2)] for j in cross_product]).next_to(equal,RIGHT,0.1)
        self.add(equal,cros_mat)
        norm_cross=normalize(cross_product)
        norm_y=Matrix([[round(k,2)] for k in norm_cross],color=RED).move_to(cros_mat).set_color(RED)
        self.play(Transform(cros_mat,norm_y))
        normal_axis=VGroup(mat,cros_mat).arrange(RIGHT).to_corner(UP+LEFT)
        self.add(normal_axis)
        self.remove(equal,cros_sign,riight)
        c_mat,c_cros_mat=mat.copy(),cros_mat.copy()
        c_mat.move_to(ORIGIN)
        cros_sign.next_to(c_mat,RIGHT,0.1)
        c_cros_mat.next_to(cros_sign,RIGHT,0.1)
        equal.next_to(c_cros_mat,RIGHT,0.1)
        x_vect=Matrix([[round(p,2)] for p in np.cross(norm_cross,nor)]).next_to(equal,RIGHT,0.1).set_color(GREEN)
        self.add(cros_sign,c_cros_mat,c_mat,equal,x_vect)
        x_vect.next_to(cros_mat,RIGHT)
        self.remove(cros_sign,c_cros_mat,c_mat,equal)
        self.wait()


class Application(ThreeDScene):

    def construct(self):
        self.set_camera_orientation(60*DEGREES,-45*DEGREES)
        axes=ThreeDAxes()
        # three=z_to_vector(np.array([1,1,1]))
        self.play(Create(axes))
        self.wait()
        rotation_about_arr=normalize(np.array([1,1,1]))
        rotation_about=Arrow3D(ORIGIN,rotation_about_arr,color=BLUE)
        y_arr=normalize(np.cross(RIGHT,rotation_about_arr))
        y_vect=Arrow3D(ORIGIN,y_arr,color=RED)
        self.play(Create(rotation_about))
        self.play(Flash(rotation_about))
        rotation_about_mat=Matrix([
            [1],
            [1],
            [1]
        ]).scale(0.4).to_corner(corner=UP+LEFT).set_color(PINK).shift(2*RIGHT)
        self.add_fixed_in_frame_mobjects(rotation_about_mat)
        self.play(rotation_about_mat.animate.to_corner(corner=UP+LEFT).set_color(PINK).shift(2*RIGHT))
        # self.begin_3dillusion_camera_rotation()
        # self.wait(2)
        # self.stop_3dillusion_camera_rotation()
        # self.play(FadeIn(rotation_about_mat))
        # self.play(Indicate(rotation_about))
        # self.play(FadeIn(y_vect))
        #############################################################
        self.play(Create(y_vect))
        self.play(FadeOut(rotation_about_mat))
        mat = Matrix([
            [1],
            [1],
            [1]
        ])
        self.add_fixed_in_frame_mobjects(mat)
        # mat.shift(3*UP+3*RIGHT).scale(0.5)
        self.play(mat.animate.shift(3*UP+3*RIGHT).scale(0.5))
        nor = normalize(np.array([1, 1, 1]))
        normal = [[round(i, 2)] for i in nor]
        matn = Matrix(normal).set_color(YELLOW)
        matn.move_to(mat).scale(0.5)
        self.wait()
        self.add_fixed_in_frame_mobjects(matn)
        self.play(Create(matn),FadeOut(mat))
        self.wait()
        cros_sign = MathTex("\\times")
        self.add_fixed_in_frame_mobjects(cros_sign)
        cros_sign.scale(0.5).next_to(matn, LEFT, 0.1)
        riight = Matrix([
            [1],
            [0],
            [0]
        ])
        self.play(Create(cros_sign))
        self.add_fixed_in_frame_mobjects(riight)
        riight.scale(0.5).next_to(cros_sign, LEFT, 0.1)
        right_vect=Arrow3D(ORIGIN,RIGHT,color=PINK)
        #self.add(riight, cros_sign)
        self.play(Create(riight),Create(right_vect))
        self.wait()
        cross_product = np.cross(RIGHT, nor)
        equal = MathTex("=")
        self.add_fixed_in_frame_mobjects(equal)
        equal.scale(0.5).next_to(matn, RIGHT, 0.1)
        self.play(Create(equal))
        cros_mat = Matrix([[round(j, 2)] for j in cross_product]).next_to(equal, RIGHT, 0.1)
        self.add_fixed_in_frame_mobjects(cros_mat)
        cros_mat.scale(0.5).next_to(equal, RIGHT, 0.1)
        self.play(Create(cros_mat))
        #self.add(equal, cros_mat)
        self.wait()
        norm_cross = normalize(cross_product)
        norm_y = Matrix([[round(k, 2)] for k in norm_cross], color=RED).move_to(cros_mat).set_color(RED)

        self.play(FadeOut(cros_mat))
        self.add_fixed_in_frame_mobjects(norm_y)
        norm_y.scale(0.5).move_to(cros_mat)
        self.play(Create(norm_y))
        self.play(Indicate(y_vect,scale_factor=1.5,color=RED))
        self.play(FadeOut(right_vect))
        self.wait(2)
        self.remove(norm_y,matn,riight,cros_sign,equal)

        # ###################x_vect##################################
        x_arr=np.cross(rotation_about_arr,y_arr)
        basis_vect_arr=np.array([
            [round(i,2) for i in x_arr],
            [round(j,2) for j in y_arr],
            [round(k,2) for k in rotation_about_arr]
        ]).T
        x_vect=Arrow3D(ORIGIN,x_arr,color=GREEN)
        self.play(FadeIn(x_vect))
        c_mat,c_cros_mat = Matrix(normal).set_color(YELLOW), Matrix([[round(k, 2)] for k in norm_cross], color=RED)
        self.add_fixed_in_frame_mobjects(c_mat)
        # c_mat.move_to(ORIGIN)
        c_mat.scale(0.5).shift(3*UP+2*RIGHT)
        self.play(Create(c_mat))
        self.wait(2)
        cros_sign.next_to(c_mat, RIGHT, 0.1)
        self.play(Create(cros_sign))
        self.add_fixed_in_frame_mobjects(c_cros_mat)
        c_cros_mat.scale(0.5)
        c_cros_mat.next_to(cros_sign, RIGHT, 0.1)
        self.play(Create(c_cros_mat))
        equal.next_to(c_cros_mat, RIGHT, 0.1)
        self.play(Indicate(rotation_about,scale_factor=1.5,color=BLUE),Indicate(y_vect,scale_factor=1.5,color=RED))
        self.play(Create(equal))
        x_vect_mat = Matrix([[round(p, 2)] for p in np.cross(norm_cross, nor)]).next_to(equal, RIGHT, 0.1).set_color(GREEN)
        self.add_fixed_in_frame_mobjects(x_vect_mat)
        x_vect_mat.scale(0.5).next_to(equal, RIGHT)
        self.play(Create(x_vect_mat))
        self.play(Indicate(x_vect_mat,color=GREEN),Indicate(x_vect,color=GREEN))
        self.wait()
        basis_vect_mat=Matrix(basis_vect_arr).set_column_colors(GREEN,RED,BLUE)
        self.add_fixed_in_frame_mobjects(basis_vect_mat)
        basis_vect_mat.scale(0.5)
        self.play(basis_vect_mat.animate.to_corner(UP+LEFT).shift(4*RIGHT))
        rotation_about_z_matrix=Matrix([

        ])
        self.wait()
        ###########################x_vect_end###################################
        #############################################################
        # x_arr=np.cross(rotation_about_arr,y_arr)
        # basis_vect_arr=np.array([
        #     x_arr,
        #     y_arr,
        #     rotation_about_arr
        # ]).T
        # print(basis_vect_arr)
        # x_vect=Arrow3D(ORIGIN,x_arr,color=GREEN)
        # self.play(FadeIn(x_vect))
        # # self.begin_ambient_camera_rotation(rate=1)
        # # self.wait(2)
        cube=Cube(side_length=1)
        self.play(Create(cube))

        # matrix in differnt coordinate syytem
        rotation_about_axis=normalize(np.array([-1,1,0]))
        y_axis_with_respect_to_rotation_about_axis=normalize(np.cross(RIGHT,rotation_about_axis))
        x_axis_with_respect_to_rotation_about_axis =np.cross(y_axis_with_respect_to_rotation_about_axis,
                                                                        rotation_about_axis)
        #different coordinate system matrix
        matrix_in_different_coordinate_system=np.array([
            x_axis_with_respect_to_rotation_about_axis,
            y_axis_with_respect_to_rotation_about_axis,
            rotation_about_axis
        ]
        ).T
        rotation_about_z_axis_matrix=rotation_about_z(45*DEGREES)
        rotation_matrix_about_axis=reduce(np.dot,[matrix_in_different_coordinate_system,
                                                  rotation_about_z_axis_matrix,
                                                  np.linalg.inv(matrix_in_different_coordinate_system)])

        self.play(cube.animate.apply_matrix(rotation_matrix_about_axis))

        #Created Rotating_with_matix animated class to rotate Mobject with matrix as explained
        self.play(Rotating_with_matix(cube,axis=np.array([1,1,1]),run_time=2))
        # self.move_camera(zoom=2)
        # self.play(Rotating_with_matix(cube, axis=np.array([1, 1, 1])))
        # self.wait()

class Application_Explanation1(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(60 * DEGREES, -45 * DEGREES)
        axes = ThreeDAxes()

        self.play(Create(axes))
        rotation_about_arr = normalize(np.array([1, 1, 1]))
        rotation_about = Arrow3D(ORIGIN, rotation_about_arr, color=BLUE)
        y_arr = normalize(np.cross(RIGHT, rotation_about_arr))
        y_vect = Arrow3D(ORIGIN, y_arr, color=RED)
        self.play(FadeIn(rotation_about))
        x_arr = np.cross(rotation_about_arr, y_arr)
        x_vect = Arrow3D(ORIGIN, x_arr, color=GREEN)
        self.play(FadeIn(y_vect))
        self.play(FadeIn(x_vect))
        basis_vect_arr = np.array([
            [round(i, 2) for i in x_arr],
            [round(j, 2) for j in y_arr],
            [round(k, 2) for k in rotation_about_arr]
        ]).T
        basis_vect_mat = Matrix(basis_vect_arr).set_column_colors(GREEN, RED, BLUE)
        self.add_fixed_in_frame_mobjects(basis_vect_mat)
        basis_vect_mat.scale(0.5).to_corner(LEFT+UP).shift(4*RIGHT)
        self.play(Create(basis_vect_mat))
        self.wait()
        ####################################################basis visual#########################
        all_lines = VGroup()
        for i in np.arange(-2, 2 + 1, 1):
            line = Line(2 * UP + i * RIGHT, -2 * UP + i * RIGHT, color=RED)
            all_lines.add(line)
        for i in np.arange(-2, 2+ 1, 1):
            line = Line(2* RIGHT + i * UP, -2* RIGHT + i * UP, color=GREEN)
            all_lines.add(line)
        plane = VGroup()
        for k in np.arange(-2, 2 + 1, 1):
            p = all_lines.copy()
            p.shift(k * OUT)
            plane.add(p)
        z_lines = VGroup()
        for i in np.arange(-2, 2 + 1, 1):
            for j in np.arange(-2, 2 + 1, 1):
                line = Line(2 * OUT + i * UP + j * RIGHT, -2 * OUT + i * UP + j * RIGHT, color=BLUE)
                z_lines.add(line)
        self.play(Create(z_lines), Create(plane))
        self.play(ApplyPointwiseFunction(lambda p: np.dot(p, basis_vect_arr.T), z_lines),
                  ApplyPointwiseFunction(lambda p: np.dot(p, basis_vect_arr.T), plane), run_time=3)
        all_group=VGroup(z_lines,plane,x_vect,y_vect,rotation_about,axes)
        self.play(all_group.animate.shift(-0.8*OUT))
        self.begin_3dillusion_camera_rotation(rate=1)
        # self.begin_ambient_camera_rotation(rate=1)
        # self.wait(5)
        #####################################################end ################################
        basis_vect_mat_inv = Matrix(basis_vect_arr,right_bracket="]^{-1}").set_column_colors(GREEN, RED, BLUE)
        self.add_fixed_in_frame_mobjects(basis_vect_mat_inv)
        basis_vect_mat_inv.scale(0.45).move_to(basis_vect_mat)
        self.play(AnimationGroup(FadeOut(basis_vect_mat),Create(basis_vect_mat_inv)))
        self.wait()
        rotation_about_z_axis=Matrix([
            ["\\cos(\\theta)","-\\sin(\\theta)",0],
            ["\\sin(\\theta)","\\cos(\\theta)",0],
            [0,0,1]
        ],element_alignment_corner=ORIGIN,h_buff=1.7).set_column_colors(GREEN, RED, BLUE)
        self.add_fixed_in_frame_mobjects(rotation_about_z_axis)
        rotation_about_z_axis.scale(0.4).next_to(basis_vect_mat_inv,LEFT,0.1)
        self.play(Create(rotation_about_z_axis))
        self.wait()
        basis_vect_mat.next_to(rotation_about_z_axis,LEFT,0)
        self.play(Create(basis_vect_mat.scale(0.8)))
        self.wait()

class Application_Explanation(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(60 * DEGREES, -45 * DEGREES)
        axes = ThreeDAxes()

        self.play(Create(axes))
        rotation_about_arr = normalize(np.array([1, 1, 1]))
        rotation_about = Arrow3D(ORIGIN, rotation_about_arr, color=BLUE)
        y_arr = normalize(np.cross(RIGHT, rotation_about_arr))
        y_vect = Arrow3D(ORIGIN, y_arr, color=RED)
        self.play(Create(rotation_about))
        x_arr = np.cross(rotation_about_arr, y_arr)
        x_vect = Arrow3D(ORIGIN, x_arr, color=GREEN)
        self.play(FadeIn(y_vect))
        self.play(FadeIn(x_vect))
        basis_vect_arr = np.array([
            [round(i, 2) for i in x_arr],
            [round(j, 2) for j in y_arr],
            [round(k, 2) for k in rotation_about_arr]
        ]).T
        basis_vect_mat = Matrix(basis_vect_arr).set_column_colors(GREEN, RED, BLUE)
        self.add_fixed_in_frame_mobjects(basis_vect_mat)
        basis_vect_mat.scale(0.5).to_corner(LEFT+UP)
        self.play(Create(basis_vect_mat))
        all_lines=VGroup()
        for i in np.arange(-2,2+1,1):
            line=Line(2*UP+i*RIGHT,-2*UP+i*RIGHT,color=RED)
            all_lines.add(line)
        for i in np.arange(-2, 2 + 1, 1):
            line = Line(2 * RIGHT + i * UP, -2 * RIGHT + i * UP, color=GREEN)
            all_lines.add(line)
        plane=VGroup()
        for k in np.arange(-2,2+1,1):
            p=all_lines.copy()
            p.shift(k*OUT)
            plane.add(p)
        z_lines=VGroup()
        for i in np.arange(-2, 2 + 1, 1):
            for j in np.arange(-2, 2 + 1, 1):
                line = Line(2 * OUT + i * UP+j*RIGHT, -2 * OUT + i * UP+j*RIGHT, color=BLUE)
                z_lines.add(line)


        self.play(Create(z_lines),Create(plane))
        self.play(ApplyPointwiseFunction(lambda p:np.dot(p,basis_vect_arr.T),z_lines),ApplyPointwiseFunction(lambda p:np.dot(p,basis_vect_arr.T),plane),run_time=3)

        self.begin_ambient_camera_rotation(rate=1)
        self.wait(5)

class D2_Example(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(self,show_basis_vectors=False,leave_ghost_vectors=False,include_background_plane=False,
                                           include_foreground_plane=False)
    def construct(self):
        vect=np.array([1,2,0])
        line=Line(-5*vect,5*vect,color=RED)
        axes=Axes()
        self.play(Create(axes))
        self.play(Create(line))
        pop=list(np.arange(-5,5,0.05))
        pop1 = list(np.arange(-4, 4, 0.1))
        rand_p=[(x,y) for x,y in zip(random.sample(list(np.linspace(-3,3,100)),k=20),random.sample(list(np.linspace(-3,3,100)),k=20))]
        point=[]
        for x,y in rand_p:
            if y>2*x:
                point.append(np.array([x,y,0]))
        point=np.array(point)
        dots=VGroup(*[Dot(p,color=YELLOW) for p in point])
        self.play(Create(dots))
        basis_mat=np.array([
            vect,
            [-vect[1],vect[0],0],
            [0,0,1]
        ]).T
        reflection_mat=np.array([
            [1,0,0],
            [0,-1,0],
            [0,0,1]
        ])
        projection=np.array([
            [1,0,0],
            [0,0,0],
            [0,0,1]
        ])
        ref_final_mat=reduce(np.dot,[basis_mat,reflection_mat,np.linalg.inv(basis_mat)])
        final_proje=reduce(np.dot,[basis_mat,projection,np.linalg.inv(basis_mat)])
        final_point=np.dot(point,ref_final_mat)
        project_point=np.dot(point,final_proje)
        lines=VGroup(*[DashedLine(p,q,color=PINK) for p,q in zip(point,project_point)])
        self.play(Create(lines))
        t_dot=[Dot(point[i],color=BLUE) for i in range(len(point))]
        for j in range(len(point)):
            first=DashedLine(point[j],t_dot[j].get_center(),color=PINK)
            first.add_updater(lambda v,k=j:v.become(DashedLine(point[k],t_dot[k].get_center(),color=PINK)))
            self.add(first)
            self.play(t_dot[j].animate.move_to(final_point[j]))
            # self.add_foreground_mobjects(first)

        self.wait()

class D2_Example1(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(self,show_basis_vectors=True,leave_ghost_vectors=False,include_background_plane=True,
                                           include_foreground_plane=True)

    def construct(self):
        self.remove(self.plane,self.background_plane,self.basis_vectors)
        vect = np.array([1, 2, 0])
        unit_vect=normalize(vect)


        line = Line(-5 * vect, 5 * vect, color=RED)
        line_euation = MathTex("y","=","2","x")
        line_euation.set_color_by_tex("y",RED)
        line_euation.set_color_by_tex("x", YELLOW).next_to(np.array([1,2,0]),RIGHT,0.1)
        self.play(Create(line))
        self.play(Create(self.plane),Create(self.background_plane))
        self.play(Create(line_euation))
        x_vector=Vector(unit_vect,color=GREEN)
        pepr_unit_y=np.array([-unit_vect[1],unit_vect[0],0])
        y_vector=Vector(pepr_unit_y,color=RED)
        self.play(Create(x_vector))
        self.play(Create(y_vector))
        bases_matrix=np.array([
            unit_vect,
            pepr_unit_y,
            OUT
        ]
        ).T
        self.moving_mobjects=[]
        self.moving_vectors=[]
        self.apply_matrix(bases_matrix)
        self.play(Wiggle(x_vector,scale_value=1.25,rotation_angle=0.025*TAU),Wiggle(y_vector,scale_value=1.25,rotation_angle=0.025*TAU))
        point=np.dot(np.array([1,1,0]),bases_matrix.T)
        dot=Dot(point,color=PINK)
        new_bases=Matrix([
            [round(unit_vect[0],2),round(pepr_unit_y[0],2)],
            [round(unit_vect[1],2), round(pepr_unit_y[1],2)]
        ],include_background_rectangle=True).scale(0.7).set_column_colors(GREEN,RED).to_corner(UP+LEFT)
        ncol1,ncol2=new_bases.get_columns()
        self.play(Create(new_bases))
        our_basis=Matrix(np.array([
            [*RIGHT[:2]],
            [*UP[:2]]
        ]).T,include_background_rectangle=True).scale(0.7).next_to(new_bases,RIGHT,2.5).set_column_colors(GREEN,RED)
        bracket=our_basis.get_brackets()

        self.play(Create(bracket))
        col1,col2=our_basis.get_columns()
        self.play(TransformFromCopy(ncol1,col1))
        self.play(TransformFromCopy(ncol2,col2))
        self.play(Create(dot))
        self.play(Wiggle(x_vector,scale_value=1.25,rotation_angle=0.025*TAU))
        target_vect=y_vector.copy()
        self.play(ApplyMethod(target_vect.shift,x_vector.get_end(),path_arc=-PI))
        rect1=SurroundingRectangle(col1,fill_color=YELLOW,fill_opacity=0.5)
        rect2 = SurroundingRectangle(col2, fill_color=YELLOW, fill_opacity=0.5)
        self.play(ShowCreationThenFadeOut(rect1),Wiggle(x_vector,scale_value=1.25,rotation_angle=0.025*TAU))
        self.play(ShowCreationThenFadeOut(rect2), Wiggle(target_vect, scale_value=1.25, rotation_angle=0.025 * TAU))
        self.play(AnimationGroup(*[FadeOut(i) for i in [x_vector,y_vector,target_vect,line,line_euation]],lag_ratio=0.2))
        self.moving_mobjects = []
        self.apply_matrix(np.linalg.inv(bases_matrix))
        x_value=ValueTracker(1)
        y_value = ValueTracker(1)
        x,y=always_redraw(lambda :Vector(RIGHT*x_value.get_value(),color=GREEN,max_tip_length_to_length_ratio=0.3,max_stroke_width_to_length_ratio=10)),always_redraw(lambda :Vector(UP*y_value.get_value(),color=RED))
        self.play(Create(x),Create(y))
        self.play(x_value.animate.set_value(point[0]))
        self.play(y_value.animate.set_value(point[1]))
        copy_y=y.copy()
        self.play(ApplyMethod(copy_y.shift,x.get_end(),path_arc=PI))
        point_mat=Matrix([[round(point[0],2)],[round(point[1],2)]],bracket_h_buff=0.05).set_row_colors(GREEN,RED).scale(0.5).next_to(dot,UP,0)
        self.play(Create(point_mat))
        self.play(AnimationGroup(*[FadeOut(i) for i in [x,y,point_mat,copy_y,our_basis]], lag_ratio=0.2))
        self.play(Create(self.basis_vectors))
        self.moving_mobjects = []
        self.moving_vectors=list(self.basis_vectors)
        self.apply_matrix(bases_matrix)
        reflection_mat = np.array([
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ])

        ref_final_mat = reduce(np.dot, [bases_matrix, reflection_mat, np.linalg.inv(bases_matrix)])
        reflected_point=np.dot(point,ref_final_mat.T)
        dotc=dot.copy()
        rpoint=reflected_point-point
        new_bases_inv = Matrix([
            [round(unit_vect[0], 2), round(pepr_unit_y[0], 2)],
            [round(unit_vect[1], 2), round(pepr_unit_y[1], 2)]
        ], include_background_rectangle=True,right_bracket="]^{-1}").scale(0.7).set_column_colors(GREEN, RED).to_corner(UP + LEFT)
        self.play(Transform(new_bases,new_bases_inv))
        self.play(new_bases.animate.shift(4*RIGHT))
        ref_mat=Matrix([
            [*reflection_mat[0,:2]],
            [*reflection_mat[1,:2]]
        ],include_background_rectangle=True).scale(0.6).set_column_colors(GREEN,RED).next_to(new_bases,LEFT,0.1)
        self.play(Create(ref_mat))
        new_bases1 = Matrix([
            [round(unit_vect[0], 2), round(pepr_unit_y[0], 2)],
            [round(unit_vect[1], 2), round(pepr_unit_y[1], 2)]
        ], include_background_rectangle=True).scale(0.6).set_column_colors(GREEN, RED).next_to(ref_mat,LEFT,0.1)
        self.play(ApplyMethod(dotc.shift, rpoint))
        self.play(Create(new_bases1))
        equal=MathTex("=").scale(0.7).next_to(new_bases,RIGHT,0.3)
        final_mat=Matrix([
            [*ref_final_mat[0,:2]],
            [round(ref_final_mat[1,0],2),round(ref_final_mat[1,1],2)]
        ]).scale(0.7).set_column_colors(GREEN,RED).next_to(equal,RIGHT,0.2)
        self.play(Create(equal))
        self.play(Create(final_mat))
        self.wait()

class D2_Example2(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(self,show_basis_vectors=True,leave_ghost_vectors=False,include_background_plane=True,
                                           include_foreground_plane=True)

    def construct(self):
        value=ValueTracker(2)
        point=always_redraw(lambda :Dot(2*RIGHT+value.get_value()*UP,color=YELLOW))
        label=MathTex("(2,2)").next_to(point,UP,buff=0.1)
        self.play(Create(point),Create(label))
        label2=MathTex("(2,-2)").next_to(np.array([2,-2,0]),UP,buff=0.1)
        self.play(ApplyMethod(value.set_value,-2),Transform(label,label2))
        self.wait(2)
class Agenda(Scene):
    def construct(self):
        self.wait(2)
        title=Title("Agenda")
        bulleted_point=BulletedList(r"What Is Change Of Basis",
                           r"Intuition Behind $AMA^{-1}$ and $A^{-1}MA$",
                           r"Application Of Change Of Basis",buff=1.5).scale(0.7).to_corner(LEFT)
        bulleted_point.set_color(YELLOW)
        self.play(Create(title))
        self.play(Write(bulleted_point),run_time=3)
        self.wait()
