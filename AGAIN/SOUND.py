import pygame as pg

pg.init()
pg.mixer.init()

def play_sound(sound_file):
    pg.mixer.music.load(sound_file)
    pg.mixer.music.play()
    # while pg.mixer.music.get_busy():
    #     pg.time.Clock().tick(10)

def play_music_loop(music_file, loops=-1):  
    pg.mixer.music.load(music_file)
    pg.mixer.music.play(loops=loops)

def stop_music():
    pg.mixer.music.stop()

if __name__ == "__main__":
    play_sound(r"D:\Yugiohohoh\DRIVE\Sound-Theme song\Akeno.mp3")
