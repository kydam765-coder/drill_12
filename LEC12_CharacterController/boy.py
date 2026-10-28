from pico2d import *
from transitions import Machine


class Autorun:
    DURATION = 5.0
    INITIAL_SPEED = 100.0
    ACCELERATION = 140.0
    MAX_SPEED = 700.0
    SCALE_GROWTH = 0.6
    MAX_SCALE = 4.0

    def __init__(self):
        self.started_at = 0.0
        self.previous_update_at = 0.0

    def enter(self):
        self.started_at = get_time()
        self.previous_update_at = self.started_at

    def exit(self, boy):
        boy.scale = 1.0

    def update(self, boy):
        now = get_time()
        elapsed = now - self.started_at
        if elapsed >= self.DURATION:
            boy.finish_autorun()
            return

        delta_time = max(0.0, now - self.previous_update_at)
        self.previous_update_at = now
        boy.scale = min(1.0 + self.SCALE_GROWTH * elapsed, self.MAX_SCALE)

        left_edge = 50 * boy.scale
        right_edge = 800 - left_edge
        boy.x = min(right_edge, max(left_edge, boy.x))
        speed = min(
            self.INITIAL_SPEED + self.ACCELERATION * elapsed,
            self.MAX_SPEED,
        )
        boy.x += boy.face_dir * speed * delta_time

        while boy.x < left_edge or boy.x > right_edge:
            if boy.x < left_edge:
                boy.x = left_edge + (left_edge - boy.x)
                boy.face_dir = 1
            elif boy.x > right_edge:
                boy.x = right_edge - (boy.x - right_edge)
                boy.face_dir = -1

        boy.frame = (boy.frame + 1) % 8


class Boy:
    SPRITE_FOOT_OFFSET = 38

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.scale = 1.0
        self.image = load_image('animation_sheet.png')
        self.autorun = Autorun()
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN', 'AUTORUN'],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                {'trigger': 'start_running', 'source': 'IDLE', 'dest': 'RUN'},
                {'trigger': 'stop_running', 'source': 'RUN', 'dest': 'IDLE'},
                {'trigger': 'start_autorun', 'source': 'IDLE', 'dest': 'AUTORUN'},
                {'trigger': 'cancel_autorun', 'source': 'AUTORUN', 'dest': 'RUN'},
                {'trigger': 'autorun_timeout', 'source': 'AUTORUN', 'dest': 'IDLE'},
            ],
        )

    def update(self):
        if self.state == 'AUTORUN':
            self.autorun.update(self)
        elif self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x = min(750, max(50, self.x + self.face_dir * 5))

    def update_direction_keys(self, pressed_directions):
        if self.state == 'AUTORUN' and pressed_directions:
            self.face_dir = pressed_directions[-1]
            self.cancel_autorun()
            self.autorun.exit(self)
            self.frame = 0
        elif self.state == 'IDLE' and pressed_directions:
            self.face_dir = pressed_directions[-1]
            self.start_running()
            self.frame = 0
        elif self.state == 'RUN':
            if not pressed_directions:
                self.stop_running()
                self.frame = 0
            else:
                self.face_dir = pressed_directions[-1]

    def begin_autorun(self):
        if self.state == 'IDLE':
            self.start_autorun()
            self.autorun.enter()
            self.frame = 0

    def finish_autorun(self):
        self.autorun_timeout()
        self.autorun.exit(self)
        self.frame = 0

    def draw(self):
        if self.state in ('RUN', 'AUTORUN'):
            row_y = 100 if self.face_dir == 1 else 0
        else:
            row_y = 300 if self.face_dir == 1 else 200
        draw_y = self.y + self.SPRITE_FOOT_OFFSET * (self.scale - 1)
        self.image.clip_draw(
            self.frame * 100, row_y, 100, 100, self.x, draw_y,
            100 * self.scale, 100 * self.scale,
        )