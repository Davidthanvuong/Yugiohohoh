from pytnk.engine import *

@dataclass
class Blendkey:
    rgba: RGBA
    k: float

class ColorBlend:
    '''Pha từ một đống màu và key'''
    def __init__(self, keys: list[Blendkey]):
        self.keys = keys

    def interpolate(self, t) -> RGBA:
        if len(self.keys) == 1:
            k = self.keys[0]
            return k.rgba
        
        keys = self.keys
        for i in range(len(self.keys) - 1):
            k1, c1 = keys[i].k, keys[i].rgba
            k2, c2 = keys[i + 1].k, keys[i + 1].rgba
            
            if k1 <= t <= k2:
                if k1 == k2: return c1
                f = (t - k1) / (k2 - k1)
                return (
                    int(c1[0] + (c2[0] - c1[0]) * f),
                    int(c1[1] + (c2[1] - c1[1]) * f),
                    int(c1[2] + (c2[2] - c1[2]) * f),
                    int(c1[3] + (c2[3] - c1[3]) * f)
                )

        return self.keys[0 if (t < self.keys[0].k) else -1].rgba


# Hiện tại có 2 cái, anh em có thể thêm vô.
burnPreset = [
    ColorBlend([
        Blendkey((0, 0, 255, 0), 0),        # Blue alpha
        Blendkey((0, 255, 255, 255), 0.2),  # Cyan
        Blendkey((0, 0, 255, 255), 0.35),    # Blue
        Blendkey((0, 0, 0, 255), 0.6),      # Black
        Blendkey((0, 0, 0, 255), 0.8),      # Black
        Blendkey((0, 0, 0, 0), 1.0),        # Black alpha
    ]),
    ColorBlend([
        Blendkey((255, 0, 0, 0), 0),        # Red alpha
        Blendkey((255, 255, 0, 255), 0.2),  # Yellow
        Blendkey((255, 0, 0, 255), 0.35),    # Red
        Blendkey((0, 0, 0, 255), 0.6),      # Black
        Blendkey((0, 0, 0, 255), 0.8),      # Black
        Blendkey((0, 0, 0, 0), 1.0),        # Black alpha
    ])
]


class Shader_BurningCard(Component):
    def __init__(self, targetImg: pg.Surface, imgsize: No[vec] = None, start_count = 20, outboundness = 0.2, 
                 noiseStrength = 3, iv_res = 5, burn_time = 1.5):
        self.targetImg = targetImg.copy()
        self.imgsize = imgsize if imgsize else vec(self.targetImg.get_size())
        self.burn_time = burn_time
        self.iv_res = iv_res                    # Inverse resolution - Kích thước mô phỏng. CPU lag lỏ 2 fps
        
        # Shader
        self.start_count = start_count          # Số pixel cháy / 100 * diện tích pixel
        self.outboundness = outboundness        # độ ngoại biên của tập điểm để tránh key tập trung ở giữa
        self.strengthWeight = noiseStrength     # cường độ ngẫu nhiên của một điểm cháy

        self.rel_time = 0.0
        self.blend = choice(burnPreset)

        self.sinceStart = time()
        scaled = self.imgsize / self.iv_res
        self.sim_size = (int(scaled.x), int(scaled.y))
        bound = scaled * outboundness
        self.bound_size = [int(-bound.x), int(scaled.x + bound.x), 
                           int(-bound.y), int(scaled.y + bound.y)]
        
    def start(self):
        self.distMap = self.get_burnNoisemap()

    def get_burnNoisemap(self):
        '''Tạo ma trận khoảng cách Manhattan từ một tập điểm ngẫu nhiên
        \nĐể mô phỏng giả hiệu ứng và cách loang của đám cháy'''
        points = [(rint(self.bound_size[0], self.bound_size[1]),
                   rint(self.bound_size[2], self.bound_size[3]))
                   for _ in range(self.start_count)] # 2 range tọa độ

        distmap = [[0.0 for _ in range(self.sim_size[0])] 
                      for _ in range(self.sim_size[1])] # for Y for X
        
        # Tìm khoảng cách cực đại để normalize sang dạng 0 đến 1
        maxdist = 0
        for y in range(self.sim_size[1]):
            for x in range(self.sim_size[0]):
                mindist = 9999
                for px, py in points:
                    dist = (abs(x - px) + abs(y - py)) # Manhattan
                    #dist += ((x - px)**2 + (y - py)**2) ** 0.5
                    mindist = min(mindist, dist)
                distmap[y][x] = mindist + rint(0, self.strengthWeight)
                maxdist = max(maxdist, mindist)

        # Normalize nó
        return [[x / maxdist for x in row] for row in distmap]

    def dist2color(self, matrix: list[list[float]], rel_t: float = 0) -> pg.Surface:
        '''Trả về màu theo giá trị của ma trận'''
        sf = pg.Surface(self.sim_size, pg.SRCALPHA)
    
        for y in range(self.sim_size[1]):
            for x in range(self.sim_size[0]):
                color = self.blend.interpolate(matrix[y][x] - 1 + rel_t * 2)
                sf.set_at((x, y), color)

        sf = pg.transform.scale(sf, vec(self.sim_size) * self.iv_res)
        return sf

    def update_logic(self):
        dt = time() - self.sinceStart
        self.rel_time = dt / self.burn_time

        if dt >= self.burn_time:
            self.go.destroy()

    def update_render(self):
        overlay = self.dist2color(self.distMap, self.rel_time)
        self.targetImg.set_alpha(max(0, int((1 - self.rel_time * 1.3) * 255)))
        
        rect = overlay.get_rect(center = self.transf.g_pos)
        App.display.blit(self.targetImg, rect)
        App.display.blit(overlay, rect)