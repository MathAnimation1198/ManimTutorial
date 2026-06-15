from manim import *
import numpy as np

class Scene1_Hook(Scene):
    def construct(self):

        title = Text(
            "Linear Regression vs Ridge Regression",
            font_size=42
        )

        subtitle = Text(
            "Can One Outlier Ruin Our Model?",
            font_size=32,
            color=YELLOW
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.1
        )

        self.play(
            Write(title),
            run_time=2
        )

        self.play(
            FadeIn(subtitle),
            run_time=1.5
        )

        self.wait(1)

        self.play(
            title.animate.scale(0.7).to_edge(UP),
           
        )
        self.play( subtitle.animate.scale(0.7).next_to(title,DOWN))

        axes = Axes(
            x_range=[0,10,1],
            y_range=[0,18,2],
            x_length=6,
            y_length=3.5,
            axis_config={"include_numbers":True}
        )

        axes.shift(DOWN*0.5)

        self.play(
            Create(axes)
        )

        x = np.array([1,2,3,4,5,6,7,8])
        y = np.array([3,4,6,8,10,11,13,15])

        dots = VGroup()

        for xi,yi in zip(x,y):

            dots.add(
                Dot(
                    axes.coords_to_point(
                        xi,
                        yi
                    ),
                    radius=0.06
                )
            )

        self.play(
            LaggedStart(
                *[
                    FadeIn(dot)
                    for dot in dots
                ],
                lag_ratio=0.15
            )
        )

        question = Text(
            "What line best fits these points?",
            font_size=28,
            color=BLUE
        )

        question.next_to(
            axes,
            DOWN
        )

        self.play(
            Write(question)
        )

        self.wait(2)


import numpy as np

class Scene2_LinearTraining(Scene):

    def construct(self):

        # ---------------------------------------------------
        # Title
        # ---------------------------------------------------
        title = Text(
            "How Linear Regression Learns",
            font_size=38
        ).to_edge(UP)

        self.play(Write(title))

        # ---------------------------------------------------
        # MSE Formula
        # ---------------------------------------------------
        mse_formula = MathTex(
            r"L = \frac{1}{n}\sum (y-\hat y)^2"
        ).scale(0.8)

        mse_formula.next_to(
            title,
            DOWN,
            buff=0.3
        )

        self.play(
            Write(mse_formula)
        )

        # ---------------------------------------------------
        # Axes
        # ---------------------------------------------------
        axes = Axes(
            x_range=[0,10,1],
            y_range=[0,18,2],
            x_length=6,
            y_length=3.5,
            axis_config={
                "include_numbers": True
            }
        )

        axes.shift(DOWN*0.8)

        self.play(Create(axes))

        # ---------------------------------------------------
        # Data
        # ---------------------------------------------------
        x = np.array([1,2,3,4,5,6,7,8])

        y = np.array([
            3,4,6,8,
            10,11,13,15
        ])

        dots = VGroup()

        for xi, yi in zip(x, y):

            dots.add(
                Dot(
                    axes.coords_to_point(
                        xi,
                        yi
                    ),
                    radius=0.06,
                    color=BLUE
                )
            )

        self.play(
            LaggedStart(
                *[
                    FadeIn(dot)
                    for dot in dots
                ],
                lag_ratio=0.08
            )
        )

        # ---------------------------------------------------
        # Trackers
        # ---------------------------------------------------
        w_tracker = ValueTracker(0)
        b_tracker = ValueTracker(0)
        loss_tracker = ValueTracker(0)
        epoch_tracker = ValueTracker(0)

        # ---------------------------------------------------
        # Live Regression Line
        # ---------------------------------------------------
        regression_line = always_redraw(
            lambda:
            axes.plot(
                lambda xx:
                w_tracker.get_value()*xx +
                b_tracker.get_value(),
                color=YELLOW,
                x_range=[0,10]
            )
        )

        self.add(regression_line)

        # ---------------------------------------------------
        # Residual Lines
        # ---------------------------------------------------
        def get_residuals():

            lines = VGroup()

            w = w_tracker.get_value()
            b = b_tracker.get_value()

            for xi, yi in zip(x, y):

                pred_y = w*xi + b

                lines.add(
                    DashedLine(
                        axes.coords_to_point(
                            xi,
                            pred_y
                        ),
                        axes.coords_to_point(
                            xi,
                            yi
                        ),
                        dash_length=0.05
                    )
                )

            return lines

        residuals = always_redraw(
            get_residuals
        )

        self.add(residuals)

        # ---------------------------------------------------
        # Statistics Panel
        # ---------------------------------------------------
        stats = always_redraw(
            lambda:
            VGroup(

                Text(
                    f"Epoch : {int(epoch_tracker.get_value())}",
                    font_size=24
                ),

                Text(
                    f"Weight : {w_tracker.get_value():.2f}",
                    font_size=24
                ),

                Text(
                    f"Bias : {b_tracker.get_value():.2f}",
                    font_size=24
                ),

                Text(
                    f"Loss : {loss_tracker.get_value():.2f}",
                    font_size=24
                )

            )
            .arrange(
                DOWN,
                aligned_edge=LEFT
            )
            .scale(0.75)
            .to_corner(RIGHT+DOWN)
        )

        self.add(stats)

        # ---------------------------------------------------
        # Initial Label
        # ---------------------------------------------------
        learning_text = Text(
            "Training Starts...",
            font_size=28,
            color=GREEN
        )

        learning_text.to_corner(
            LEFT+DOWN
        )

        self.play(
            FadeIn(learning_text)
        )

        # ---------------------------------------------------
        # Gradient Descent
        # ---------------------------------------------------
        lr = 0.01

        w = 0
        b = 0

        epochs = 20

        for epoch in range(epochs):

            pred = w*x + b

            dw = (
                -2/len(x)
            ) * np.sum(
                x*(y-pred)
            )

            db = (
                -2/len(x)
            ) * np.sum(
                y-pred
            )

            w -= lr*dw
            b -= lr*db

            mse = np.mean(
                (
                    y -
                    (w*x+b)
                )**2
            )

            self.play(

                w_tracker.animate.set_value(w),

                b_tracker.animate.set_value(b),

                loss_tracker.animate.set_value(mse),

                epoch_tracker.animate.set_value(
                    epoch+1
                ),

                run_time=0.25
            )

        # ---------------------------------------------------
        # Final Message
        # ---------------------------------------------------
        final_text = Text(
            "Loss is decreasing ✓",
            font_size=30,
            color=GREEN
        )

        final_text.to_corner(
            LEFT+DOWN
        )

        self.play(
            Transform(
                learning_text,
                final_text
            )
        )

        self.wait(2)



class Scene3_OutlierProblem(Scene):

    def construct(self):

        # ----------------------------------------
        # Title
        # ----------------------------------------
        title = Text(
            "The Outlier Problem",
            font_size=38
        ).to_edge(UP)

        self.play(Write(title))

        # ----------------------------------------
        # Axes
        # ----------------------------------------
        axes = Axes(
            x_range=[0,10,1],
            y_range=[0,30,5],
            x_length=6,
            y_length=4,
            axis_config={
                "include_numbers":True
            }
        )

        axes.shift(DOWN*0.5)

        self.play(Create(axes))

        # ----------------------------------------
        # Original Data
        # ----------------------------------------
        x = np.array([1,2,3,4,5,6,7,8])

        y = np.array([
            3,4,6,8,
            10,11,13,15
        ])

        dots = VGroup()

        for xi, yi in zip(x,y):

            dots.add(
                Dot(
                    axes.coords_to_point(
                        xi,
                        yi
                    ),
                    color=BLUE
                )
            )

        self.play(
            FadeIn(dots)
        )

        # ----------------------------------------
        # Previously Trained Line
        # ----------------------------------------
        w_initial = 1.75
        b_initial = 0.80

        line = axes.plot(
            lambda xx:
            w_initial*xx+b_initial,
            color=YELLOW
        )

        self.play(
            Create(line)
        )

        self.wait()

        # ----------------------------------------
        # Message
        # ----------------------------------------
        text1 = Text(
            "Everything looks good...",
            font_size=30,
            color=GREEN
        )

        text1.to_edge(DOWN)

        self.play(
            Write(text1)
        )

        self.wait(2)

        # ----------------------------------------
        # Outlier
        # ----------------------------------------
        outlier = Dot(
            axes.coords_to_point(
                8,
                27
            ),
            color=RED,
            radius=0.09
        )

        outlier_label = Text(
            "Outlier",
            font_size=28,
            color=RED
        )

        outlier_label.next_to(
            outlier,
            RIGHT
        )

        self.play(
            FadeIn(
                outlier,
                shift=UP
            ),
            run_time=2
        )

        self.play(
            Write(outlier_label)
        )

        self.wait()

        # ----------------------------------------
        # Warning Text
        # ----------------------------------------
        warning = Text(
            "A single unusual point appears",
            font_size=30,
            color=RED
        )

        warning.to_edge(DOWN)

        self.play(
            Transform(
                text1,
                warning
            )
        )

        self.wait(2)

        # ----------------------------------------
        # Add Outlier to Dataset
        # ----------------------------------------
        x_new = np.append(x,8)
        y_new = np.append(y,27)

        # ----------------------------------------
        # Retraining
        # ----------------------------------------
        w_tracker = ValueTracker(
            w_initial
        )

        b_tracker = ValueTracker(
            b_initial
        )

        dynamic_line = always_redraw(
            lambda:
            axes.plot(
                lambda xx:
                w_tracker.get_value()*xx+
                b_tracker.get_value(),
                color=YELLOW
            )
        )

        self.remove(line)

        self.add(dynamic_line)

        stats = always_redraw(
            lambda:
            Text(
                f"Weight = {w_tracker.get_value():.2f}",
                font_size=28
            ).to_corner(RIGHT+DOWN)
        )

        self.add(stats)

        w = w_initial
        b = b_initial

        lr = 0.005

        for _ in range(25):

            pred = w*x_new+b

            dw = (
                -2/len(x_new)
            ) * np.sum(
                x_new*(y_new-pred)
            )

            db = (
                -2/len(x_new)
            ) * np.sum(
                y_new-pred
            )

            w -= lr*dw
            b -= lr*db

            self.play(
                w_tracker.animate.set_value(w),
                b_tracker.animate.set_value(b),
                run_time=0.12
            )

        self.wait()

        # ----------------------------------------
        # Highlight Weight Growth
        # ----------------------------------------
        box = SurroundingRectangle(
            stats,
            color=RED
        )

        self.play(
            Create(box)
        )

        self.wait()

        # ----------------------------------------
        # Conclusion
        # ----------------------------------------
        final_text = Text(
            "The line is being pulled toward the outlier!",
            font_size=30,
            color=RED
        )

        final_text.to_edge(DOWN)

        self.play(
            Transform(
                text1,
                final_text
            )
        )

        self.wait(2)

        question = Text(
            "Can we stop this?",
            font_size=36,
            color=YELLOW
        )

        question.move_to(ORIGIN)

        self.play(
            Write(question)
        )

        self.wait(3)



class Scene4_RidgeIntroduction(Scene):

    def construct(self):

        # ====================================================
        # Title
        # ====================================================

        title = Text(
            "How Ridge Regression Solves This",
            font_size=40
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(1)

        # ====================================================
        # Recap Problem
        # ====================================================

        problem_title = Text(
            "Problem",
            color=RED,
            font_size=34
        )

        problem_title.shift(UP*1)

        problem_text = VGroup(
            Text("Large Weight", font_size=30),
            Text("Overfitting Risk", font_size=30),
            Text("Sensitive to Outliers", font_size=30)
        ).arrange(DOWN, aligned_edge=LEFT)

        problem_text.next_to(
            problem_title,
            DOWN,
            buff=0.4
        )

        self.play(
            FadeIn(problem_title),
            FadeIn(problem_text)
        )

        self.wait(2)

        # ====================================================
        # Move Left
        # ====================================================

        problem_group = VGroup(
            problem_title,
            problem_text
        )

        self.play(
            problem_group.animate.shift(LEFT*3.5)
        )

        # ====================================================
        # Solution
        # ====================================================

        solution_title = Text(
            "Solution",
            color=GREEN,
            font_size=34
        )

        solution_title.shift(
            RIGHT*2.5 + UP*1
        )

        solution_text = Text(
            "Penalize Large Weights",
            font_size=30
        )

        solution_text.next_to(
            solution_title,
            DOWN
        )

        self.play(
            FadeIn(solution_title),
            Write(solution_text)
        )

        self.wait(2)

        self.play(
            FadeOut(problem_group),
            FadeOut(solution_title),
            FadeOut(solution_text)
        )

        # ====================================================
        # Weight Penalty Demonstration
        # ====================================================

        demo_title = Text(
            "Large Weights Become Expensive",
            font_size=34,
            color=YELLOW
        )

        demo_title.to_edge(UP)

        self.play(
            ReplacementTransform(
                title,
                demo_title
            )
        )

        row1 = VGroup(
            MathTex(r"w = 1"),
            MathTex(r"Penalty = 1")
        ).arrange(RIGHT, buff=2)

        row2 = VGroup(
            MathTex(r"w = 3"),
            MathTex(r"Penalty = 9")
        ).arrange(RIGHT, buff=2)

        row3 = VGroup(
            MathTex(r"w = 5"),
            MathTex(r"Penalty = 25")
        ).arrange(RIGHT, buff=2)

        table = VGroup(
            row1,
            row2,
            row3
        ).arrange(
            DOWN,
            buff=0.8
        )

        self.play(
            Write(row1)
        )

        self.wait()

        self.play(
            Write(row2)
        )

        self.wait()

        self.play(
            Write(row3)
        )

        self.wait()

        highlight = SurroundingRectangle(
            row3,
            color=RED
        )

        self.play(
            Create(highlight)
        )

        growth_text = Text(
            "Penalty grows very fast!",
            font_size=28,
            color=RED
        )

        growth_text.next_to(
            highlight,
            DOWN
        )

        self.play(
            Write(growth_text)
        )

        self.wait(2)

        self.play(
            FadeOut(table),
            FadeOut(highlight),
            FadeOut(growth_text)
        )

        # ====================================================
        # Linear Regression Formula
        # ====================================================

        linear_title = Text(
            "Linear Regression Loss",
            font_size=32
        )

        linear_title.shift(UP*1.5)

        linear_formula = MathTex(
            r"L = \frac{1}{n}\sum (y-\hat y)^2"
        )

        linear_formula.scale(1.2)

        self.play(
            FadeIn(linear_title)
        )

        self.play(
            Write(linear_formula)
        )

        self.wait(2)

        # ====================================================
        # Ridge Formula
        # ====================================================

        ridge_title = Text(
            "Ridge Regression Loss",
            font_size=32
        )

        ridge_title.move_to(
            linear_title
        )

        ridge_formula = MathTex(
            r"L = \frac{1}{n}\sum (y-\hat y)^2 + \lambda w^2"
        )

        ridge_formula.scale(1.2)

        ridge_formula.move_to(
            linear_formula
        )

        self.play(
            ReplacementTransform(
                linear_title,
                ridge_title
            ),
            ReplacementTransform(
                linear_formula,
                ridge_formula
            )
        )

        self.wait()

        # Highlight λw²
        penalty_box = SurroundingRectangle(
            ridge_formula[-4:],
            color=YELLOW
        )

        self.play(
            Create(penalty_box)
        )

        penalty_text = Text(
            "Regularization Term",
            font_size=28,
            color=YELLOW
        )

        penalty_text.next_to(
            penalty_box,
            DOWN
        )

        self.play(
            Write(penalty_text)
        )

        self.wait(2)

        # ====================================================
        # Lambda Explanation
        # ====================================================

        lambda0 = MathTex(
            r"\lambda = 0"
        )

        lambda0.shift(DOWN*2)

        self.play(
            Write(lambda0)
        )

        lambda_text = Text(
            "Same as Linear Regression",
            font_size=26,
            color=GREEN
        )

        lambda_text.next_to(
            lambda0,
            DOWN
        )

        self.play(
            Write(lambda_text)
        )

        self.wait(2)

        lambda10 = MathTex(
            r"\lambda = 10"
        )

        lambda10.move_to(lambda0)

        strong_text = Text(
            "Strong Weight Penalty",
            font_size=26,
            color=RED
        )

        strong_text.move_to(
            lambda_text
        )

        self.play(
            ReplacementTransform(
                lambda0,
                lambda10
            ),
            ReplacementTransform(
                lambda_text,
                strong_text
            )
        )

        self.wait(2)

        # ====================================================
        # Final Transition
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    ridge_title,
                    ridge_formula,
                    penalty_box,
                    penalty_text,
                    lambda10,
                    strong_text
                )
            )
        )

        final_text = Text(
            "Let's Train Ridge Regression",
            font_size=40,
            color=BLUE
        )

        self.play(
            Write(final_text)
        )

        self.wait(3)




class Scene5_RidgeTraining(Scene):

    def construct(self):

        # ==================================================
        # Title
        # ==================================================

        title = Text(
            "Training Ridge Regression",
            font_size=40
        ).to_edge(UP)

        self.play(
            Write(title)
        )

        # ==================================================
        # Ridge Formula
        # ==================================================

        formula = MathTex(
            r"L=MSE+\lambda w^2"
        )

        formula.scale(0.9)

        formula.next_to(
            title,
            DOWN,
            buff=0.2
        )

        self.play(
            Write(formula)
        )

        # ==================================================
        # Axes
        # ==================================================

        axes = Axes(
            x_range=[0,10,1],
            y_range=[0,30,5],
            x_length=6,
            y_length=4,
            axis_config={
                "include_numbers":True
            }
        )

        axes.shift(DOWN*0.7)

        self.play(
            Create(axes)
        )

        # ==================================================
        # Dataset + Outlier
        # ==================================================

        x = np.array([1,2,3,4,5,6,7,8,8])

        y = np.array([
            3,4,6,8,10,
            11,13,15,
            27
        ])

        dots = VGroup()

        for i,(xi,yi) in enumerate(zip(x,y)):

            color = RED if i == len(x)-1 else BLUE

            dots.add(
                Dot(
                    axes.coords_to_point(
                        xi,
                        yi
                    ),
                    color=color
                )
            )

        self.play(
            FadeIn(dots)
        )

        # ==================================================
        # Trackers
        # ==================================================

        w_tracker = ValueTracker(0)
        b_tracker = ValueTracker(0)

        loss_tracker = ValueTracker(0)

        epoch_tracker = ValueTracker(0)

        # ==================================================
        # Ridge Line
        # ==================================================

        ridge_line = always_redraw(

            lambda:

            axes.plot(
                lambda xx:
                w_tracker.get_value()*xx
                +
                b_tracker.get_value(),

                color=GREEN,

                x_range=[0,10]
            )
        )

        self.add(ridge_line)

        # ==================================================
        # Stats
        # ==================================================

        stats = always_redraw(

            lambda:

            VGroup(

                Text(
                    f"Epoch : {int(epoch_tracker.get_value())}",
                    font_size=24
                ),

                Text(
                    f"Weight : {w_tracker.get_value():.2f}",
                    font_size=24
                ),

                Text(
                    f"Bias : {b_tracker.get_value():.2f}",
                    font_size=24
                ),

                Text(
                    f"Loss : {loss_tracker.get_value():.2f}",
                    font_size=24
                )

            )
            .arrange(
                DOWN,
                aligned_edge=LEFT
            )
            .scale(0.75)
            .to_corner(RIGHT+DOWN)
        )

        self.add(stats)

        # ==================================================
        # Lambda Value
        # ==================================================

        lambda_text = Text(
            "λ = 1.0",
            font_size=30,
            color=YELLOW
        )

        lambda_text.to_corner(
            LEFT+DOWN
        )

        self.play(
            FadeIn(lambda_text)
        )

        # ==================================================
        # Training
        # ==================================================

        lr = 0.01

        lam = 1.0

        w = 0
        b = 0

        epochs = 25

        for epoch in range(epochs):

            pred = w*x + b

            mse_grad_w = (
                -2/len(x)
            ) * np.sum(
                x*(y-pred)
            )

            ridge_grad = (
                2*lam*w
            )

            dw = mse_grad_w + ridge_grad

            db = (
                -2/len(x)
            ) * np.sum(
                y-pred
            )

            w -= lr*dw
            b -= lr*db

            mse = np.mean(
                (
                    y-(w*x+b)
                )**2
            )

            ridge_loss = (
                mse
                +
                lam*(w**2)
            )

            self.play(

                w_tracker.animate.set_value(w),

                b_tracker.animate.set_value(b),

                loss_tracker.animate.set_value(
                    ridge_loss
                ),

                epoch_tracker.animate.set_value(
                    epoch+1
                ),

                run_time=0.2
            )

        self.wait()

        # ==================================================
        # Highlight Weight
        # ==================================================

        final_box = SurroundingRectangle(
            stats[1],
            color=GREEN
        )

        self.play(
            Create(final_box)
        )

        self.wait()

        final_text = Text(
            "Weight growth is controlled!",
            font_size=30,
            color=GREEN
        )

        final_text.to_edge(DOWN)

        self.play(
            Write(final_text)
        )

        self.wait(3)




class Scene6_Comparison(Scene):

    def construct(self):

        # ====================================================
        # Title
        # ====================================================

        title = Text(
            "Linear Regression vs Ridge Regression",
            font_size=40
        ).to_edge(UP)

        self.play(
            Write(title)
        )

        # ====================================================
        # Left Axis
        # ====================================================

        left_axes = Axes(
            x_range=[0,10,1],
            y_range=[0,30,5],
            x_length=4,
            y_length=3,
            axis_config={"include_numbers":False}
        )

        left_axes.shift(
            LEFT*3 + DOWN*0.5
        )

        # ====================================================
        # Right Axis
        # ====================================================

        right_axes = Axes(
            x_range=[0,10,1],
            y_range=[0,30,5],
            x_length=4,
            y_length=3,
            axis_config={"include_numbers":False}
        )

        right_axes.shift(
            RIGHT*3 + DOWN*0.5
        )

        self.play(
            Create(left_axes),
            Create(right_axes)
        )

        # ====================================================
        # Labels
        # ====================================================

        linear_label = Text(
            "Linear Regression",
            font_size=28,
            color=RED
        )

        ridge_label = Text(
            "Ridge Regression",
            font_size=28,
            color=GREEN
        )

        linear_label.next_to(
            left_axes,
            UP
        )

        ridge_label.next_to(
            right_axes,
            UP
        )

        self.play(
            Write(linear_label),
            Write(ridge_label)
        )

        # ====================================================
        # Dataset
        # ====================================================

        x = np.array([
            1,2,3,4,
            5,6,7,8,8
        ])

        y = np.array([
            3,4,6,8,
            10,11,13,15,
            27
        ])

        left_dots = VGroup()
        right_dots = VGroup()

        for i,(xi,yi) in enumerate(zip(x,y)):

            color = RED if i==8 else BLUE

            left_dots.add(
                Dot(
                    left_axes.coords_to_point(
                        xi,
                        yi
                    ),
                    color=color,
                    radius=0.05
                )
            )

            right_dots.add(
                Dot(
                    right_axes.coords_to_point(
                        xi,
                        yi
                    ),
                    color=color,
                    radius=0.05
                )
            )

        self.play(
            FadeIn(left_dots),
            FadeIn(right_dots)
        )

        # ====================================================
        # Final Linear Line
        # ====================================================

        linear_line = left_axes.plot(
            lambda x:
            2.45*x + 0.5,
            color=YELLOW
        )

        # ====================================================
        # Final Ridge Line
        # ====================================================

        ridge_line = right_axes.plot(
            lambda x:
            1.75*x + 1.2,
            color=YELLOW
        )

        self.play(
            Create(linear_line),
            Create(ridge_line)
        )

        self.wait()

        # ====================================================
        # Weight Comparison
        # ====================================================

        linear_weight = Text(
            "Weight = 2.45",
            font_size=26,
            color=RED
        )

        ridge_weight = Text(
            "Weight = 1.75",
            font_size=26,
            color=GREEN
        )

        linear_weight.next_to(
            left_axes,
            DOWN
        )

        ridge_weight.next_to(
            right_axes,
            DOWN
        )

        self.play(
            Write(linear_weight),
            Write(ridge_weight)
        )

        self.wait()

        # ====================================================
        # Highlight Linear
        # ====================================================

        bad_box = SurroundingRectangle(
            linear_weight,
            color=RED
        )

        self.play(
            Create(bad_box)
        )

        bad_text = Text(
            "Pulled by Outlier",
            font_size=26,
            color=RED
        )

        bad_text.to_edge(DOWN)

        self.play(
            Write(bad_text)
        )

        self.wait(2)

        self.play(
            FadeOut(bad_box),
            FadeOut(bad_text)
        )

        # ====================================================
        # Highlight Ridge
        # ====================================================

        good_box = SurroundingRectangle(
            ridge_weight,
            color=GREEN
        )

        self.play(
            Create(good_box)
        )

        good_text = Text(
            "More Stable",
            font_size=28,
            color=GREEN
        )

        good_text.to_edge(DOWN)

        self.play(
            Write(good_text)
        )

        self.wait(2)

        self.play(
        FadeOut(left_axes),
        FadeOut(right_axes),
        FadeOut(left_dots),
        FadeOut(right_dots),
        FadeOut(linear_line),
        FadeOut(ridge_line),
        FadeOut(linear_label),
        FadeOut(ridge_label),
        FadeOut(linear_weight),
        FadeOut(ridge_weight)
        )

        # ====================================================
        # Final Table
        # ====================================================

        self.play(
            FadeOut(good_box),
            FadeOut(good_text)
        )

        comparison = Table(

            [
                ["High","Lower"],
                ["Sensitive","More Robust"],
                ["Higher Weight","Controlled Weight"]
            ],

            row_labels=[
                Text("Variance"),
                Text("Outlier Impact"),
                Text("Weights")
            ],

            col_labels=[
                Text("Linear"),
                Text("Ridge")
            ],

            include_outer_lines=True
        )

        comparison.scale(0.4)

        comparison.move_to(DOWN*1.8)

        self.play(
            Create(comparison)
        )

        self.wait(3)

        # ====================================================
        # Winner
        # ====================================================

        conclusion = Text(
            "Ridge Regression Controls Complexity",
            font_size=34,
            color=GREEN
        )

        conclusion.move_to(
            ORIGIN
        )

        self.play(
            Write(conclusion)
        )

        self.wait(4)




class Scene7_Summary(Scene):

    def construct(self):

        # ==========================================
        # Title
        # ==========================================

        title = Text(
            "Key Takeaways",
            font_size=42
        )

        title.to_edge(UP)

        self.play(
            Write(title)
        )

        self.wait()

        # ==========================================
        # Learning Journey
        # ==========================================

        step1 = Text(
            "Linear Regression",
            font_size=32
        )

        step2 = Text(
            "Outlier Appears",
            font_size=32,
            color=RED
        )

        step3 = Text(
            "Large Weight",
            font_size=32,
            color=RED
        )

        step4 = Text(
            "Overfitting Risk",
            font_size=32,
            color=RED
        )

        step5 = Text(
            "Add Ridge Penalty",
            font_size=32,
            color=GREEN
        )

        step6 = Text(
            "Controlled Weight",
            font_size=32,
            color=GREEN
        )

        step7 = Text(
            "Better Generalization",
            font_size=32,
            color=GREEN
        )

        flow = VGroup(
            step1,
            Arrow(ORIGIN, DOWN*0.5),
            step2,
            Arrow(ORIGIN, DOWN*0.5),
            step3,
            Arrow(ORIGIN, DOWN*0.5),
            step4,
            Arrow(ORIGIN, DOWN*0.5),
            step5,
            Arrow(ORIGIN, DOWN*0.5),
            step6,
            Arrow(ORIGIN, DOWN*0.5),
            step7
        )

        flow.arrange(
            DOWN,
            buff=0.15
        )

        flow.scale(0.7)

        self.play(
            LaggedStart(
                *[
                    FadeIn(mob)
                    for mob in flow
                ],
                lag_ratio=0.2
            )
        )

        self.wait(3)

        # ==========================================
        # Remove Flow
        # ==========================================

        self.play(
            FadeOut(flow)
        )

        # ==========================================
        # Ridge Formula
        # ==========================================

        ridge_formula = MathTex(
            r"L = \frac{1}{n}\sum(y-\hat y)^2 + \lambda w^2"
        )

        ridge_formula.scale(1.2)

        self.play(
            Write(ridge_formula)
        )

        self.wait()

        penalty_box = SurroundingRectangle(
            ridge_formula[-4:],
            color=YELLOW
        )

        self.play(
            Create(penalty_box)
        )

        self.wait()

        penalty_text = Text(
            "Controls Weight Size",
            font_size=30,
            color=YELLOW
        )

        penalty_text.next_to(
            ridge_formula,
            DOWN
        )

        self.play(
            Write(penalty_text)
        )

        self.wait(2)

        self.play(
            FadeOut(ridge_formula),
            FadeOut(penalty_box),
            FadeOut(penalty_text)
        )

        # ==========================================
        # When To Use Ridge
        # ==========================================

        use_title = Text(
            "When Should You Use Ridge?",
            font_size=36,
            color=BLUE
        )

        use_title.shift(UP*2)

        self.play(
            Write(use_title)
        )

        use_cases = VGroup(

            Text(
                "✓ Many Features",
                font_size=30
            ),

            Text(
                "✓ Noisy Data",
                font_size=30
            ),

            Text(
                "✓ Outliers Present",
                font_size=30
            ),

            Text(
                "✓ Reduce Overfitting",
                font_size=30
            )

        )

        use_cases.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.4
        )

        self.play(
            LaggedStart(
                *[
                    Write(item)
                    for item in use_cases
                ],
                lag_ratio=0.3
            )
        )

        self.wait(3)

        self.play(
            FadeOut(use_title),
            FadeOut(use_cases)
        )

        # ==========================================
        # Final Message
        # ==========================================

        final_text = Text(
            "Ridge Regression = Accuracy + Simplicity",
            font_size=40,
            color=GREEN
        )

        self.play(
            Write(final_text)
        )

        self.wait(2)

        final_text2 = Text(
            "Better Generalization on Unseen Data",
            font_size=34,
            color=BLUE
        )

        final_text2.next_to(
            final_text,
            DOWN
        )

        self.play(
            Write(final_text2)
        )

        self.wait(4)        
