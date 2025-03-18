from .engine import *
from enum import Enum

class Phase(Enum):
    MAIN = 0
    BATTLE = 1
    DRAW = 2

class LinearStateMachine:
    '''Một biến tấu của FSM (máy trạng thái hữu hạn) cho game thẻ bài
    Chạy luôn tuyến tính theo: Main phase --> Battle phase --> Draw phase
    '''
    states: list[list['FiniteState']] = [[], [], []]
    current_state: 'FiniteState'
    i_phase: int = 0
    j_state: int = 0

    @classmethod
    def add_state(cls, phase: Phase, state: 'FiniteState'):
        cls.states[phase.value].append(state)

    @classmethod
    def start(cls):
        cls.current_state = cls.states[0][0]
        cls.current_state.begin_wrapper()

    @classmethod
    def next_state(cls):
        cls.current_state.end_wrapper()

        cls.j_state += 1
        if cls.j_state >= len(cls.states[cls.i_phase]):
            cls.j_state = 0
            cls.i_phase += 1
            if cls.i_phase >= len(cls.states):
                cls.i_phase = 0
                
        cls.current_state = cls.states[cls.i_phase][cls.j_state]
        cls.current_state.begin_wrapper()



class FiniteState:
    def __init__(self, user: 'Controller', phase: Phase):
        LinearStateMachine.add_state(phase, self)
        self.user = user
        self.e_begin: Event = Event()
        self.e_end: Event = Event()

    def begin_wrapper(self): 
        self.e_begin.notify()
        self.begin(self.user)

    def end_wrapper(self):
        self.e_end.notify()
        self.end(self.user)

    def begin(self, user: 'Controller'): pass
    def end(self, user: 'Controller'): pass