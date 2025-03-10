import tkinter as tk
import pygame
import struct

class GifAnimator:
    def __init__(self, filename, position=(0, 0)):
        """
        Initialize the animator with a GIF file.
        
        Args:
            filename (str): Path to the GIF file.
            position (tuple): (x, y) coordinates where the animation will be displayed.
        """
        self.frames, self.delays, self.transparency_indices, self.global_color_table = self._load_gif_data(filename)
        self.position = position
        self.current_frame = 0
        self.frame_time = 0
        self.num_frames = len(self.frames)
        
        # Ensure delays match the number of frames
        default_delay = 0.1  # 100ms default
        if not self.delays or len(self.delays) < self.num_frames:
            self.delays.extend([default_delay] * (self.num_frames - len(self.delays)))
        
        # Ensure transparency indices match frames
        if len(self.transparency_indices) < self.num_frames:
            self.transparency_indices.extend([None] * (self.num_frames - len(self.transparency_indices)))
    
    def _load_gif_data(self, filename):
        """
        Load GIF frames, delays, transparency indices, and color tables.
        
        Returns:
            tuple: (list of Pygame Surfaces, list of delays, list of transparency indices, global color table)
        """
        delays = []
        transparency_indices = []
        global_color_table = []
        local_color_tables = []
        
        # Parse GIF structure
        try:
            with open(filename, 'rb') as f:
                # Verify GIF header
                header = f.read(6)
                if header not in (b'GIF87a', b'GIF89a'):
                    raise ValueError("Not a valid GIF file")
                
                # Logical screen descriptor
                width, height, packed, bg_index, aspect = struct.unpack('<HHBBB', f.read(7))
                global_color_table_flag = packed & 0x80
                if global_color_table_flag:
                    color_table_size = 3 * (2 ** ((packed & 0x07) + 1))
                    global_color_table_data = f.read(color_table_size)
                    for i in range(0, len(global_color_table_data), 3):
                        r, g, b = global_color_table_data[i:i+3]
                        global_color_table.append((r, g, b))
                
                current_delay = 0.1
                current_transparency = None
                while True:
                    block = f.read(1)
                    if not block:
                        break
                    
                    if block == b'\x21':  # Extension block
                        label = f.read(1)
                        if label == b'\xF9':  # Graphic Control Extension
                            block_size = struct.unpack('<B', f.read(1))[0]
                            if block_size != 4:
                                continue
                            packed, delay_low, delay_high, transparent = struct.unpack('<BBBB', f.read(4))
                            delay = (delay_high << 8) | delay_low
                            current_delay = delay / 100.0
                            if packed & 0x01:  # Transparency flag
                                current_transparency = transparent
                            else:
                                current_transparency = None
                            f.read(1)  # Block terminator
                        else:
                            while True:
                                size = struct.unpack('<B', f.read(1))[0]
                                if size == 0:
                                    break
                                f.read(size)
                    
                    elif block == b'\x2C':  # Image descriptor
                        delays.append(current_delay)
                        transparency_indices.append(current_transparency)
                        left, top, width, height, packed = struct.unpack('<HHHHB', f.read(9))
                        local_color_table_flag = packed & 0x80
                        if local_color_table_flag:
                            color_table_size = 3 * (2 ** ((packed & 0x07) + 1))
                            local_color_table_data = f.read(color_table_size)
                            local_color_table = []
                            for i in range(0, len(local_color_table_data), 3):
                                r, g, b = local_color_table_data[i:i+3]
                                local_color_table.append((r, g, b))
                            local_color_tables.append(local_color_table)
                        else:
                            local_color_tables.append(None)
                        # Skip image data
                        while True:
                            size = struct.unpack('<B', f.read(1))[0]
                            if size == 0:
                                break
                            f.read(size)
                    
                    elif block == b'\x3B':  # Trailer
                        break
        except Exception as e:
            print(f"Error parsing GIF data: {e}")
            return [], [], [], []
        
        # Load frames with tkinter
        root = tk.Tk()
        root.withdraw()
        frames = []
        index = 0
        while True:
            try:
                photo = tk.PhotoImage(file=filename, format=f'gif -index {index}')
                width, height = photo.width(), photo.height()
                surface = pygame.Surface((width, height), pygame.SRCALPHA)
                
                # Use the appropriate color table
                color_table = local_color_tables[index] if index < len(local_color_tables) and local_color_tables[index] is not None else global_color_table
                trans_index = transparency_indices[index] if index < len(transparency_indices) else None
                
                for y in range(height):
                    for x in range(width):
                        pixel = photo.get(x, y)
                        if isinstance(pixel, str) and pixel.startswith('#'):
                            r = int(pixel[1:3], 16)
                            g = int(pixel[3:5], 16)
                            b = int(pixel[5:7], 16)
                            # Find the index in the color table
                            pixel_rgb = (r, g, b)
                            pixel_index = color_table.index(pixel_rgb) if pixel_rgb in color_table else -1
                            a = 0 if trans_index is not None and pixel_index == trans_index else 255
                        elif isinstance(pixel, (tuple, list)):
                            r, g, b = pixel[:3]
                            pixel_rgb = (r, g, b)
                            pixel_index = color_table.index(pixel_rgb) if pixel_rgb in color_table else -1
                            a = 0 if trans_index is not None and pixel_index == trans_index else 255
                        else:
                            r, g, b, a = 0, 0, 0, 255
                        surface.set_at((x, y), (r, g, b, a))
                
                frames.append(surface)
                index += 1
            except tk.TclError:
                break
            except Exception as e:
                print(f"Error loading frame {index}: {e}")
                break
        
        root.destroy()
        return frames, delays, transparency_indices, global_color_table
    
    def update(self, dt):
        """
        Update the animation state based on elapsed time.
        
        Args:
            dt (float): Delta time in seconds since last update.
        """
        if not self.frames:
            return
        
        self.frame_time += dt
        if self.frame_time >= self.delays[self.current_frame]:
            self.frame_time = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames
    
    def draw(self, screen):
        """
        Draw the current frame to the Pygame screen.
        
        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        if self.frames:
            screen.blit(self.frames[self.current_frame], self.position)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("GIF Animation with Alpha in Pygame")
    clock = pygame.time.Clock()
    
    # Load and create animator
    gif_file = "assets\\images\\effect\\normal attack.gif"  # Replace with your GIF file path
    animator = GifAnimator(gif_file, position=(100, 100))
    
    if not animator.frames:
        print("Failed to load any frames from the GIF.")
        pygame.quit()
        return
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update animation
        dt = clock.tick(60) / 1000.0
        animator.update(dt)
        
        # Draw with black background
        screen.fill((255, 255, 255))  # Black background
        animator.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()