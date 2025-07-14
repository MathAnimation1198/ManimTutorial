from manim import *

class BubbleSortWithCodeAndPointer(Scene):
    def construct(self):
        # ✅ Step 1: Use Code object for syntax-highlighted code
        code = Code(
            code="""
arr = [6, 4, 3, 8, 2, 1]
n = len(arr)
for i in range(n):
    for j in range(n - i - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
""",
            tab_width=4,
            background_stroke_width=1,
            language="python",
            font="Monospace",
            style="monokai",
            line_spacing=0.6,
        ).scale(0.6).to_corner(UL)

        self.add(code)

        # ✅ Triangle pointer
        pointer = Triangle(fill_color=RED, fill_opacity=1).scale(0.2).rotate(-PI / 2)
        pointer.next_to(code.code[0], LEFT, buff=0.2)
        self.play(FadeIn(pointer))
        self.wait(0.5)

        # ✅ Step 2: Visual array setup
        arr = [6, 4, 3, 8, 2, 1]
        boxes = []
        spacing = 1.3
        start_x = -3

        for i, val in enumerate(arr):
            rect = RoundedRectangle(width=1.2, height=1.2, corner_radius=0.2)
            num = Text(str(val), font="Arial").scale(0.6).move_to(rect.get_center())
            group = VGroup(rect, num)
            group.move_to(RIGHT * i * spacing + RIGHT * start_x + DOWN * 2)
            boxes.append(group)

        self.play(*[FadeIn(b) for b in boxes])
        self.wait(0.5)

        # ✅ Step 3: Bubble Sort animation + pointer movement
        for i in range(len(arr)):
            self.play(pointer.animate.move_to(code.code[2].get_left() + LEFT * 0.3), run_time=0.2)

            for j in range(len(arr) - i - 1):
                self.play(pointer.animate.move_to(code.code[3].get_left() + LEFT * 0.3), run_time=0.2)

                b1 = boxes[j]
                b2 = boxes[j + 1]
                val1 = int(b1[1].text)
                val2 = int(b2[1].text)

                self.play(
                    ApplyWave(b1[0]),
                    ApplyWave(b2[0]),
                    run_time=1
                )

                if val1 > val2:
                    self.play(pointer.animate.move_to(code.code[4].get_left() + LEFT * 0.3), run_time=0.2)
                    self.play(pointer.animate.move_to(code.code[5].get_left() + LEFT * 0.3), run_time=0.2)

                    # 🔄 Smooth swap animation (up ➝ across ➝ down)
                    up = UP * 1
                    right = RIGHT * spacing
                    left = LEFT * spacing

                    path1 = VMobject().set_points_as_corners(
                        [b1.get_center(), b1.get_center() + up + right, b2.get_center()])
                    path2 = VMobject().set_points_as_corners(
                        [b2.get_center(), b2.get_center() + up + left, b1.get_center()])

                    self.play(
                        MoveAlongPath(b1, path1),
                        MoveAlongPath(b2, path2),
                        run_time=1
                    )

                    boxes[j], boxes[j + 1] = boxes[j + 1], boxes[j]

        # ✅ Final highlight
        for box in boxes:
            self.play(box[0].animate.set_stroke(GREEN, width=4), run_time=0.2)

        self.wait(2)
