from robot_hat import Music,TTS
from time import sleep

m = Music()
t = TTS()

def sound():
    sound_effect = './sounds/sign.wav'
    m.sound_effect_play(sound_effect)

def background_music():
    music = './musics/slow-trail-Ahjay_Stelino.mp3'	
    m.music_set_volume(50)
    m.background_music(music)	

def tts():
    t.say("timing begins")
    sleep(1)
    t.say("three")
    sleep(1)
    t.say("two")
    sleep(1)
    t.say("one")
    sleep(1)
    t.say("Stop music")
	
if __name__ == "__main__":
    background_music()
    sleep(10)	
    while True:
        sound()
        tts()
        m.music_pause()
        sleep(1)
        m.music_unpause()
        sleep(10)
        		
