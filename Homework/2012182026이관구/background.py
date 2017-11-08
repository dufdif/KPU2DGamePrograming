import json
from pico2d import *
class tile:
    def __init__(self,filename):
        f=open(filename)
        self.map=json.load(f)
        self.x=0
        self.y=0
        self.image=load_image('tmw_desert_spacing.png')


    def draw(self):
        map_width=self.map['width']
        map_height=self.map['height']
        tileset=self.map['tilesets'][0]
        margin=tileset['margin']
        columns=tileset['columns']
        rows=-(-tileset['tilecount']//columns)
        dx,dy=0+tileset['tilewidth']/2,0+tileset['tileheight']/2
        desty=dy
        for y in range(50):
            destx=dx
            for x in range(100):
                index=(map_height-y-1)*map_width
                tn=self.map['layers'][0]['data'][index]
                tx=tn%8
                ty=tn//8
                srcx=margin+tx*(tileset['tilewidth']+tileset['spacing'])
                srcy=margin+ty*(tileset['tileheight']+tileset['spacing'])
                self.image.clip_draw(srcx,srcy,tileset['tilewidth'],tileset['tileheight'],destx,desty)
                destx+=tileset['tilewidth']
            desty+=tileset['tileheight']

