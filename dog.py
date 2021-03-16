from scene import *
from time import time
from random import randrange, uniform, choice

class Ground (object):
    def __init__(self, parent):
        ground = SpriteNode(parent = parent)
        ground.z_position = -1
        ground.size = Size(parent.size.w, parent.size.h / 3)
        ground.color = '#bfffbf'
        ground.anchor_point = (0, 0)
        self._grasses = []
        for i in range(16):
            x = randrange(int(ground.size.w))
            y = randrange(int(ground.size.h))
            grass = SpriteNode('GRASS.PNG', parent = ground, position = (x, y))
            self._grasses.append(grass)
        self._xx = 0

    def set_xx(self, xx):
        self._xx = xx

    def update(self):
        for grass in self._grasses:
            grass.position = grass.position - (self._xx, 0)
            (x, y) = grass.position
            if x < 0:
                grass.position = (grass.parent.size.w + x, y)
            elif x >= grass.parent.size.w:
                grass.position = (x - grass.parent.size.w, y)

class Score (object):
    def __init__(self, parent):
        self._parent = parent
        self._o_pos = Point(parent.size.w / 2 - 144, parent.size.h - 32)
        self._sprites = []

    def reset(self):
        self._times = 0
        self._score = 0
        for sp in self._sprites:
            sp.remove_from_parent()
        self._sprites = []

    def get_times(self):
        return self._times

    def get_score(self):
        return self._score

    def add_times(self):
        self._times = self._times + 1
        pos = self._o_pos + ((self._times - 1) * 32, 0)
        sp = SpriteNode('SCORE0.PNG', parent = self._parent, position = pos)
        self._sprites.append(sp)

    def add_score(self):
        self._score = self._score + 1
        pos = self._o_pos + ((self._times - 1) * 32, -32)
        sp = SpriteNode('SCORE1.PNG', parent = self._parent, position = pos)
        self._sprites.append(sp)

class Dog (object):
    STATE_LEFT_STAY  = 1
    STATE_LEFT_RUN   = 2
    STATE_LEFT_SIT   = 3
    STATE_LEFT_DOWN  = 4
    STATE_LEFT_JUMP  = 5
    STATE_RIGHT_STAY = 6
    STATE_RIGHT_RUN  = 7
    
    SPRITE_NAME = 'DOG{0}.PNG'
    SPRITE_NUM = 11

    def __init__(self, parent):
        self._sp_dog = SpriteNode(parent = parent, z_position = 1)
        self._sp_sha = SpriteNode('DOG_SHADOW.PNG', parent = parent)
        self._tx_dogs = []
        for i in range(Dog.SPRITE_NUM):
            tx = Texture(Dog.SPRITE_NAME.format(i))
            self._tx_dogs.append(tx)
        self._sp_dog.texture = self._tx_dogs[0]
        self._s_pos = Point(parent.size.w / 2, parent.size.h / 6)
        self._sha_y = self._s_pos.y - 28
        self.reset()

    def reset(self):
        self.set_position(self._s_pos)
        self._state = Dog.STATE_LEFT_STAY
        self._xxyy = Point(0, 0)
        self._before_time = None

    def get_state(self):
        return self._state

    def get_rect(self):
        sp_rect = self._sp_dog.frame
        return Rect(sp_rect.x,  sp_rect.y + sp_rect.h / 2, sp_rect.w / 2, sp_rect.h / 2)

    def get_position(self):
        return self._sp_dog.position

    def set_position(self, pos):
        self._sp_dog.position = pos
        self._sp_sha.position = (pos.x, self._sha_y)

    def set_xxyy(self, xxyy):
        self._xxyy = Point(*xxyy)

    def wait(self):
        if self._before_time == None:
            self._before_time = time()
            return
        if time() - self._before_time < 0.2:
            return
        self._state = choice([Dog.STATE_LEFT_STAY,
                              Dog.STATE_LEFT_JUMP,
                              Dog.STATE_LEFT_SIT])
        self.update_pose()
        self._before_time = None

    def start(self):
        self.reset()
        self.update_pose()

    def update(self):
        pos = self._sp_dog.position
        pos = pos + (0, self._xxyy.y)
        if pos.y > self._s_pos.y:
            self._state = Dog.STATE_LEFT_JUMP
        else:
            pos.y = self._s_pos.y
            if self._xxyy.x > 0:
                self._state = Dog.STATE_RIGHT_RUN
            elif self._xxyy.x < 0:
                self._state = Dog.STATE_LEFT_RUN
            else:
                if self._state == Dog.STATE_RIGHT_RUN or self._state == Dog.STATE_RIGHT_STAY:
                    self._state = Dog.STATE_RIGHT_STAY
                else:
                    self._state = Dog.STATE_LEFT_STAY
        self.set_position(pos)
        self.update_pose()

    def update_pose(self):
        sp_num = 0
        timing = int(time() * 4) % 2
        if self._state == Dog.STATE_LEFT_STAY:
            sp_num = timing
        elif self._state == Dog.STATE_LEFT_RUN:
            sp_num = 2 + timing
        elif self._state == Dog.STATE_LEFT_SIT:
            sp_num = 4
        elif self._state == Dog.STATE_LEFT_DOWN:
            sp_num = 5
        elif self._state == Dog.STATE_LEFT_JUMP:
            sp_num = 6
        elif self._state == Dog.STATE_RIGHT_STAY:
            sp_num = 7 + timing
        elif self._state == Dog.STATE_RIGHT_RUN:
            sp_num = 9 + timing
        self._sp_dog.texture = self._tx_dogs[sp_num]

    def down(self):
        if self._before_time == None:
            self._before_time = time()
            self._state = Dog.STATE_LEFT_SIT
            self.update_pose()
            return
        t = time() - self._before_time
        if t < 1:
            return
        elif t < 3:
            self._state = Dog.STATE_LEFT_DOWN
            self.update_pose()
            return
        self._state = Dog.STATE_LEFT_STAY
        self._before_time = None

class Frisbee (object):
    SPRITE_NAME = 'FRISBEE{0}.PNG'
    SPRITE_NUM = 3

    def __init__(self, parent):
        self._sp_fri = SpriteNode(parent = parent, z_position = 2)
        self._sp_sha = SpriteNode('FRISBEE_SHADOW.PNG', parent = parent)
        self._tx_fris = []
        for i in range(Frisbee.SPRITE_NUM):
            tx = Texture(Frisbee.SPRITE_NAME.format(i))
            self._tx_fris.append(tx)
        self._sp_fri.texture = self._tx_fris[1]
        self._s_pos = Point(-32, parent.size.h / 2)
        self._sha_y = parent.size.h / 6 - 32
        self.reset()

    def reset(self):
        self.set_position(self._s_pos)
        self._xxyy = Point(0, 0)
        self._xxxyyy = Point(0, 0)
        self._xx = 0
        self._is_frying = False

    def start(self):
        self.reset()
        self._xxyy = Point(8, uniform(2, 4))
        self._xxxyyy = Point(uniform(-0.01, 0.01), -0.02)
        self._is_frying = True

    def get_rect(self):
        return self._sp_fri.frame

    def is_frying(self):
        return self._is_frying

    def set_position(self, pos):
        self._sp_fri.position = pos
        self._sp_sha.position = (pos.x, self._sha_y)

    def set_xx(self, xx):
        self._xx = xx

    def catch(self):
        self._sp_fri.texture = self._tx_fris[1]        

    def update(self):
        pos = self._sp_fri.position
        pos = pos + self._xxyy
        pos = pos - (self._xx, 0)
        if pos.y <= self._sha_y + 4:
            pos.y = self._sha_y + 4
            self._xxyy = Point(0, 0)
            self._xxxyyy = Point(0, 0)
            self._is_frying = False
        self.set_position(pos)
        sp_num = 1
        if self._xxyy.y > 2:
            sp_num = 0
        elif self._xxyy.y < -2:
            sp_num = 2
        self._sp_fri.texture = self._tx_fris[sp_num]
        self._xxyy = self._xxyy + self._xxxyyy

class Game (Scene):
    TITLE_SHOW = 1
    TITLE_WAIT = 2
    TITLE_HIDE = 3
    START      = 4
    INTERVAL   = 5
    PLAY       = 6
    CATCH      = 7
    BRING      = 8
    MISS       = 9
    DOWN       = 10
    OVER       = 11

    def setup(self):
        self.background_color = '#bfffff'
        self.ground = Ground(self)
        self.score = Score(self)
        self.dog = Dog(self)
        self.frisbee = Frisbee(self)
        self.label1 = None
        self.label2 = None
        self.t_begin = None
        self.l_begin = None
        self.start_t = None
        self.interval_t = None
        self.xx = 0
        self.xxx = 0
        self.yy = 0
        self.yyy = 0
        self.state = Game.TITLE_SHOW

    def update(self):
        if self.state == Game.TITLE_SHOW:
            self.title_show()
        elif self.state == Game.TITLE_WAIT:
            self.title_wait()
        elif self.state == Game.TITLE_HIDE:
            self.title_hide()
        elif self.state == Game.START:
            self.start()
        elif self.state == Game.INTERVAL:
            self.interval()
        elif self.state == Game.PLAY:
            self.play()
        elif self.state == Game.CATCH:
            self.catch()
        elif self.state == Game.BRING:
            self.bring()
        elif self.state == Game.MISS:
            self.miss()
        elif self.state == Game.DOWN:
            self.down()
        elif self.state == Game.OVER:
            self.over()

    def update_ground(self):
        self.ground.set_xx(self.xx)
        self.ground.update()

    def update_dog(self):
        self.dog.set_xxyy((self.xx, self.yy))
        self.dog.update()
        if self.xxx != 0:
            self.xx = self.xx - self.xxx
            if (self.xxx > 0 and self.xx < 0) or (self.xxx < 0 and self.xx > 0):
                self.xx = 0
                self.xxx = 0
        if self.yyy != 0:
            self.yy = self.yy - self.yyy
            if self.dog.get_state() != Dog.STATE_LEFT_JUMP:
                self.yy = 0
                self.yyy = 0

    def update_frisbee(self):
        self.frisbee.set_xx(self.xx)
        self.frisbee.update()

    def title_show(self):
        self.label1 = LabelNode(parent = self)
        self.label1.position = (self.size.w / 2, self.size.h / 2)
        self.label1.color = 'blue'
        self.label1.font = ('<System-Bold>', 32)
        self.label1.text = 'Frisbee Dog'
        self.label2 = LabelNode(parent = self)
        self.label2.position = (self.size.w / 2, self.size.h / 2 - 40)
        self.label2.color = 'blue'
        self.label2.font = ('<System-Bold>', 24)
        self.label2.text = 'Tap to start'
        self.state = Game.TITLE_WAIT

    def title_wait(self):
        self.dog.wait()

    def title_hide(self):
        self.label1.remove_from_parent()
        self.label1 = None
        self.label2.remove_from_parent()
        self.label2 = None
        self.score.reset()
        self.state = Game.START

    def start(self):
        self.xx = 0
        self.yy = 0
        self.xxx = 0
        self.yyy = 0
        self.score.add_times()
        self.dog.start()
        self.frisbee.start()
        self.state = Game.INTERVAL

    def interval(self):
        if self.start_t == None or self.interval_t == None:
            self.start_t = self.t
            self.interval_t = uniform(1, 5)
            return
        self.dog.update_pose()
        if self.t - self.start_t < self.interval_t:
            return
        self.start_t = None
        self.interval_t = None
        self.state = Game.PLAY

    def play(self):
        self.update_ground()
        self.update_dog()
        self.update_frisbee()
        if self.dog.get_state() == Dog.STATE_LEFT_JUMP and \
        self.frisbee.get_rect().intersects(self.dog.get_rect()):
            self.frisbee.catch()
            self.state = Game.CATCH
        elif self.frisbee.is_frying() == False:
            self.state = Game.MISS

    def catch(self):
        self.update_ground()
        self.update_dog()
        self.frisbee.set_position(self.dog.get_position() + (-44, 20))
        if self.dog.get_state() != Dog.STATE_LEFT_JUMP:
            self.score.add_score()
            self.frisbee.set_position(self.dog.get_position() + (-44, 0))
            self.state = Game.BRING

    def bring(self):
        dog_pos = self.dog.get_position() - (4, 0)
        self.dog.set_position(dog_pos)
        self.dog.update_pose()
        self.frisbee.set_position(dog_pos + (-44, 0))
        if dog_pos.x < -32:
            if self.score.get_times() < 10:
                self.state = Game.START
            else:
                self.state = Game.OVER

    def miss(self):
        self.update_ground()
        self.update_dog()
        self.update_frisbee()
        if self.dog.get_state() != Dog.STATE_LEFT_JUMP:
            self.state = Game.DOWN

    def down(self):
        self.dog.down()
        if self.dog.get_state() != Dog.STATE_LEFT_SIT and \
        self.dog.get_state() != Dog.STATE_LEFT_DOWN:
            if self.score.get_times() < 10:
                self.state = Game.START
            else:
                self.state = Game.OVER

    def over(self):
        self.dog.reset()
        self.frisbee.reset()
        self.label1 = LabelNode(parent = self)
        self.label1.position = (self.size.w / 2, self.size.h / 2)
        self.label1.color = 'blue'
        self.label1.font = ('<System-Bold>', 24)
        self.label1.text = 'Score : ' + str(self.score.get_score()) + ' point(s)'
        self.label2 = LabelNode(parent = self)
        self.label2.position = (self.size.w / 2, self.size.h / 2 - 32)
        self.label2.color = 'blue'
        self.label2.font = ('<System-Bold>', 24)
        self.label2.text = 'Tap to new game'
        self.state = Game.TITLE_WAIT

    def touch_began(self, touch):
        if self.state == Game.PLAY:        
            if self.dog.get_state() == Dog.STATE_LEFT_JUMP:
                return
            self.t_begin = self.t
            self.l_begin = touch.location
            self.xx = 0
            self.xxx = 0

    def touch_moved(self, touch):
        if self.state == Game.PLAY:
            if self.t_begin == None or self.l_begin == None:
                return
            if self.dog.get_state() == Dog.STATE_LEFT_JUMP:
                return
            dt = self.t - self.t_begin
            if dt == 0:
                return
            dx = touch.location.x - self.l_begin.x
            self.xx = -dx / (dt * 60)
            if self.xx > 16:
                self.xx = 16
            elif self.xx < -16:
                self.xx = -16
            self.xxx = self.xx / 128
            dy = touch.location.y - self.l_begin.y
            if dx >= 0 or abs(dx) >= abs(dy) or dy < 12:
                self.yy = 0
                self.yyy = 0
            else:
                self.xx = -self.xx
                self.xxx = -self.xxx
                self.yy = dy / (dt * 60)
                if self.yy > 16:
                    self.yy = 16
                self.yyy = 1
            self.t_begin = self.t
            self.l_begin = touch.location

    def touch_ended(self, touch):
        if self.state == Game.TITLE_WAIT:
            self.state = Game.TITLE_HIDE

if __name__ == '__main__':
  run(Game(), LANDSCAPE)
