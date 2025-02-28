import pygame as pg
from textbox import TextBox
from parameterbox import ParameterBox  # Nếu bạn tách riêng file

def my_callback(x_str, y_str):
    """
    Hàm ví dụ được gọi khi giá trị X hoặc Y thay đổi.
    Bạn có thể parse ra số nguyên, float, hoặc làm gì tuỳ ý.
    """
    print("X =", x_str, "Y =", y_str)
    # Nếu only_numbers=True, ta có thể chuyển sang int:
    # if x_str.isdigit() and y_str.isdigit():
    #     x_val = int(x_str)
    #     y_val = int(y_str)
    #     print("X + Y =", x_val + y_val)

def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    font = pg.font.SysFont("Arial", 24)

    # Tạo một ParameterBox
    param_box = ParameterBox(
        x=50, y=50,
        w=400, h=50,
        name="Position",
        font=font,
        func=my_callback,       # Hàm sẽ được gọi khi X, Y thay đổi
        only_numbers=False      # Cho nhập ký tự bất kỳ, nếu muốn số thì True
    )

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # Truyền event cho param_box
            param_box.handle_event(event)

        screen.fill((255, 255, 255))

        # Vẽ param_box
        param_box.render_update(screen)

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
