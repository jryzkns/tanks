import pygame as pg

class score_keeper:
    
    def __init__(self, gamex, gamey):
        
        self.gamewidth, self.gameheight = gamex, gamey
        
        self.show, self.drawx, self.drawy = False, 0, 0
        self.wave = pg.image.load('assets\\Wave.png')
        self.buffer, self.text = [], [ pg.image.load('assets\\'+str(i)+'.png') for i in range(9+1)]
        self.wavelen, self.numberlen = self.wave.get_rect().size[0], self.text[0].get_rect().size[0]

    def update(self, score):
        self.buffer = [self.wave] + [self.text[int(dig)] for dig in str(score)]
        display_buffer_length = self.wavelen + self.numberlen*(len(self.buffer)-1)
        self.drawx = (self.gamewidth - display_buffer_length) >> 1

    def draw(self, surface):

        surface.blit(self.wave, (self.drawx, self.drawy))
        for i in range(1, len(self.buffer)):
            surface.blit(self.buffer[i], (self.drawx + self.wavelen +(i-1)*self.numberlen , self.drawy))