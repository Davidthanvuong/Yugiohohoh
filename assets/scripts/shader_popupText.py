from pytnk.engine import *

bgPreset = [
    ColorBlend([
        Blendkey((100, 0, 200, 0), 0),
        Blendkey((100, 0, 200, 255), 0.2),        # Dark purple
        Blendkey((255, 0, 100, 255), 0.5),      # Red pink
        Blendkey((100, 0, 200, 255), 0.8),      # Dark purple
        Blendkey((255, 0, 0, 255), 0.9),          # Red
        Blendkey((255, 0, 0, 0), 1.0),          # Red

        # Blendkey((0, 0, 255, 0), 0),        # Blue alpha
        # Blendkey((0, 255, 255, 255), 0.2),  # Cyan
        # Blendkey((0, 0, 255, 255), 0.35),   # Blue
        # Blendkey((0, 0, 0, 255), 0.6),      # Black
        # Blendkey((0, 0, 0, 255), 0.8),      # Black
        # Blendkey((0, 0, 0, 0), 1.0),        # Black alpha
    ]),
]

class Shader_PopupText(Text):
    '''Text ngầu lòi ultra pro max plus'''
    
    @staticmethod
    def create(**kw):
        txt = GameObject('Popup Text', anchor=CENTER, pos=App.center)
        txt += Shader_PopupText(**kw)
        return txt

    def __init__(self, seed_count = 10, seed_spanX = 0.1, seed_outbound = 0.2, random_strength = 0,
                 iv_res = 5, manhattan_stretchX = 3, border_start = 0.8, boxSize: tff = (500, 100),
                 animTime = 1.0, **kwargs):
        
        super().__init__(size=60, notLazy=True, **kwargs)
        self.iv_res = iv_res

        self.seed_count = seed_count                        # Lượng điểm cố định tại tâm
        self.seed_spanX = seed_spanX                        # Phạm vi tỉ lệ X để tính kh cách
        self.seed_outbound = seed_outbound                  # Độ ngoại biên để tránh dồn tâm
        self.manhattan_stretchX = manhattan_stretchX        # Giảm cường độ khoảng cách tính theo X
        self.random_strength = random_strength

        self.boxSize = vec(boxSize)
        self.border_start = border_start                    # Biên trục Y bắt đầu từ tỉ lệ cách tâm
        self.animTime = animTime

        self.blend = choice(bgPreset)
        self.playing = False

    def get_cachedInfo(self):
        scaled = self.boxSize / self.iv_res
        self.sim_size = (int(scaled.x), int(scaled.y))
        bound = scaled * self.seed_outbound
        scaled *= vec(1 / self.manhattan_stretchX, 1).elementwise()
        self.seed_boundsize = [int(-bound.x), int(scaled.x + bound.x), 
                               int(-bound.y), int(scaled.y + bound.y)]
        
        self.border_delta = 1 / (1 - self.border_start)

    def getMap_borderedManhattan(self):
        points = [(rint(self.seed_boundsize[0], self.seed_boundsize[1]),
                   rint(self.seed_boundsize[2], self.seed_boundsize[3]))
                   for _ in range(self.seed_count)] # 2 range tọa độ

        distmap = [[0.0 for _ in range(self.sim_size[0])] 
                      for _ in range(self.sim_size[1])] # for Y for X
        
        # Tìm khoảng cách cực đại để normalize sang dạng 0 đến 1
        maxdist = 0
        halfY = self.sim_size[1] // 2

        for y in range(self.sim_size[1]):
            borderY = abs(y / halfY - 1) - self.border_start
            for x in range(self.sim_size[0]):
                mindist = 9999
                for px, py in points:
                    dist = abs(x - px) / self.manhattan_stretchX + abs(y - py) # Manhattan
                    if borderY >= 0:
                        dist *= 1 - borderY * self.border_delta * 0.6
                    #dist += ((x - px)**2 + (y - py)**2) ** 0.5
                    mindist = min(mindist, dist)
                distmap[y][x] = mindist + rint(0, self.random_strength)
                maxdist = max(maxdist, mindist)

        # Normalize và hợp với biên Y
        for y in range(self.sim_size[1]):
            for x in range(self.sim_size[0]):
                # Mảng dưới lật lên, nhân 2 bù lại (0.5 -> 0 -> 0.5)
                # Trừ để lấy kh cách tương đối với biên
                distmap[y][x] /= maxdist
        return distmap

    def dist2color(self, matrix: list[list[float]], rel_t: float = 0) -> pg.Surface:
        sf = pg.Surface(self.sim_size, pg.SRCALPHA)
    
        for y in range(self.sim_size[1]):
            for x in range(self.sim_size[0]):
                color = self.blend.interpolate(matrix[y][x] - 1 + rel_t * 2)
                sf.set_at((x, y), color)

        sf = pg.transform.scale(sf, vec(self.sim_size) * self.iv_res)
        return sf

    def playText(self, text: str):
        self.playing = True
        self.sinceStart = now()
        self.text = text
        print("start running")

        self.get_cachedInfo()
        self.distmap = self.getMap_borderedManhattan()

    def update_logic(self):
        if not self.playing: return
        self.ratio = (now() - self.sinceStart) / self.animTime
        if self.ratio >= 1:
            self.playing = False
            print("Disabled")

    def get_fullSurface(self):
        overlay = self.dist2color(self.distmap, self.ratio)
        sf, size = self.getNew_textRender()
        textRect = sf.get_rect(center = self.boxSize // 2)

        overlay.blit(sf, textRect, special_flags=pg.BLENDMODE_ADD)
        return overlay, vec(overlay.get_size())

    def update_render(self):
        '''Đè lên render cũ'''
        if not self.playing: return
        self.render_lazy(self.get_fullSurface)