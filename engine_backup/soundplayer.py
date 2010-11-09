import pyglet, util, random

class SoundPlayer(object):

    def _init_(self):

        self.sound_path = util.respath_func_with_base_path('music')
        self.count = 0
        self.random_timer = random.randrange(500, 3000)

    def play_sound(self, load_sound):
        self.sound = pyglet.resource.media(self.sound_path(load_sound))
        self.sound.play()

    def play_track(self, load_track):
        self.track = pyglet.resource.media(self.sound_path(load_track))
        self.track.eos_action = "loop"
        self.track.play()

    def pause_track(self):
        if(self.track.playing):
            self.track.pause()
        else:
            self.track.play()

    def ambient_sounds(self):
        self.ambient = pyglet.resource.media(self.sound_path("Train_Loop1.ogg"))
        self.ambient.eos_action = "stop"
        print "play sound"
        self.ambient.play()

    def update(self):
        if (self.count > self.random_timer):
            self.random_timer = random.randrange(500, 3000)
            print "I am inside the loop"
            self.ambient_sounds()
            self.count = 0
        else:
            self.count += 1
        
