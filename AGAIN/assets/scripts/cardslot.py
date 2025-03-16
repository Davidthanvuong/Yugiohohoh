from pytnk.engine import *
from itertools import chain
from typing import cast

class CardSlot(IClickable):
    dragging  : No['CardSlot'] = None
    selecting : No['CardSlot'] = None
    sides: tuple[list['CardSlot'], list['CardSlot']] = ([], [])
    
    # Generator và dãy hỗ trợ
    @staticmethod
    def getSide(side: int):
        if side == BOTH:
              slots = list(chain(CardSlot.sides[PLAYER], CardSlot.sides[OPPONENT]))
        else: slots = list(CardSlot.sides[side])
        shuffle(slots)
        yield from slots

    @staticmethod
    def get_occupiedSlots(side: int):
        yield from (slot for slot in CardSlot.getSide(side) if slot.isOccupied())

    @staticmethod
    def get_emptySlots(side: int):
        yield from (slot for slot in CardSlot.getSide(side) if not slot.isOccupied())

    @staticmethod
    def getAny_occupiedSlot(side: int):
        return next(CardSlot.get_occupiedSlots(side))

    @staticmethod
    def getAny_emptySlot(side: int):
        return next(CardSlot.get_emptySlots(side))

    @staticmethod
    def getAny_occupiedFrontSlot(side: int):
        assert side != BOTH
        frontline = [10, 11, 12, 13, 14]
        shuffle(frontline)
        for slot in frontline:
            slot = CardSlot.sides[side][slot]
            if slot.isOccupied(): return slot
            
        return CardSlot.getAny_occupiedSlot(side)

    @staticmethod
    def isEmpty(side: int):
        return not any(slot.isOccupied() for slot in CardSlot.getSide(side))
    
    @staticmethod
    def isAnySideEmpty():
        return CardSlot.isEmpty(PLAYER) or CardSlot.isEmpty(OPPONENT)

    @staticmethod
    def isFull(side: int):
        return all(slot.isOccupied() for slot in CardSlot.getSide(side))

    @staticmethod
    def get_hoveredSlot(side: int) -> 'CardSlot | None':
        select = CardSlot.selecting
        if not select: return None
        if (side != BOTH) and (select.side != side): return None
        return select

    # @staticmethod
    # def getAvailableSlot(mySide: bool, oppoSide: bool, searchOccupied = False, getAny = False) -> 'CardSlot':
    #     total: list[CardSlot] = []
    #     if mySide: total += CardSlot.my_slots
    #     if oppoSide: total += CardSlot.oppo_slots
    #     if getAny: return choice(total)
    #     shuffle(total)

    #     print("[WARNING] getAvailableSlot bay game nếu không có slot trống")
    #     for slot in total:
    #         occupied = slot.isOccupied()
    #         if occupied == searchOccupied: return slot
    #     raise Exception("Full")
    
    # @staticmethod
    # def getState(allEmpty: bool, search: bool) -> bool:
    #     slots = CardSlot.oppo_slots if search else CardSlot.my_slots

    #     if allEmpty: # Ngưng khi có 1 cái không rỗng
    #         for slot in slots:
    #             if slot.isOccupied(): return False
    #         return True
        
    #     # Ngưng khi có 1 cái rỗng
    #     for slot in slots:
    #         if not slot.isOccupied(): return False
    #     return True

    

    @staticmethod
    def create(slots: 'GameObject', user: 'UserControl', x = 0, y = 0, **kw):
        forward = -1 if user.side else 1
        slotId = (x * 5 + y) + (user.side * 100)
        slot = GameObject('Card Slot', slots, pos=(forward * x * 150, y * 120), **kw)
        slot += Image("card_back.png", (120, 80), support_overlay=True, overrideHitbox=True)
        slot += CardSlot(user, slotId)

    def __init__(self, user: 'UserControl', myId = -1):
        super().__init__(draggable=True)
        self.myId = myId
        self.user = user
        self.side = user.side
        self._occupy: No[ref[Monster]] = None
        self.selectMotion = Motion.linear(0, 150, 0.3, True, True)
        CardSlot.sides[self.side].append(self)

    def after_init(self):
        self.com_img = self.go.getComponent(Image)

    def update_logic(self):
        selecting = CardSlot.selecting is self
        dragging = CardSlot.dragging is self

    def on_startHover(self):
        CardSlot.selecting = self

    def on_stopHover(self):
        if CardSlot.selecting is self:
            CardSlot.selecting = None


    def on_startDrag(self):
        if CardSlot.dragging is None:
            CardSlot.dragging = self
            self.selectMotion.start()

    def on_dragging(self):
        # Đè lên tính năng drag (không cho phép drag vật, chỉ drag mũi tên)
        if CardSlot.dragging is self:
            self.com_img.overlay_opacity = self.selectMotion.value

    def on_stopDrag(self):
        self.com_img.overlay_opacity = 0
        drag = CardSlot.dragging
        select = CardSlot.selecting
        if (drag is None) or (select is None):
           CardSlot.dragging = None
           return 
        if (drag is not self): return
        print(f"{drag.myId} --> {select.myId}")
        CardSlot.dragging = None
        CardSlot.selecting = None

        if (self.user.turn_heroActionLeft <= 0) or (not select.isOccupied()): 
            print(f"[{self.myId} {self.user.go.name}] Hết lượt, hết cứu. Khỏi đánh")
            return
        if not self._occupy: return
        mon = self._occupy() # Test weakref và di chuyển monster đến vị trí slot
        if not mon: return

        mon.setTarget(select)
        if mon.side != select.side: # Khác phe thì đánh
              mon.actions.append(mon.action_attack())
        # else: mon.start_action(mon.action_support())

    def update_render(self):
        if (not CardSlot.dragging) or (CardSlot.dragging is not self): return

        pos1 = CardSlot.dragging.transf.g_pos
        select = CardSlot.selecting
        pos2 = select.transf.g_pos if select else Mouse.pos
        pg.draw.line(App.screen, Color.forward, pos1, pos2, 5)

    @property
    def occupy(self) -> 'Monster':
        '''Dám làm thì cho làm'''
        return self._occupy() # type: ignore
    
    @occupy.setter
    def occupy(self, mon: No['Monster']):
        if mon is None: self._occupy = None
        else: self._occupy = ref(mon)

    def tryGetOccupy(self) -> 'Monster | None':
        if self._occupy:
            occupy = self._occupy()
            if not occupy: self._occupy = None
            return occupy
        return None

    def isOccupied(self) -> bool:
        if self._occupy:
            occupy = self._occupy()
            if occupy is None: self._occupy = None
            return occupy is not None
        return False