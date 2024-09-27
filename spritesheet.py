# evan genske, 12.5.2021

import pygame

class SpriteSheet:
    '''
    For full documentation of this module, visit GitHub:
    https://github.com/DavyJonesStockings/Pygame_spritesheet

    Make sure to read the license!
    '''

    def __init__(self, filepath):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filepath).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filepath}")
            raise SystemExit(e)


    def image_at(self, rectangle:tuple, scale:int = 1, colorkey:int = None) -> pygame.Surface:
        """Load a specific image from a specific rectangle.
        Returns a pygame surface.
        
        rectangle: a tuple in the format of (x, y, width, height). these are the dimensions for the image you want to load.
        colorkey: enter -1 to take the color code from (0,0) of the spritesheet,
        which will make all pixels of that exact color transparent. default 
        value leaves image as is
        scale: scale the image by a scalar
        """
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)

        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        size = image.get_size()
        size = (int(size[0] * scale), int(size[1] * scale))
        image = pygame.transform.scale(image, size)

        return image

    def images_at(self, rects:list, scale:int = 1, colorkey:int = None) -> list:
        """Load a whole bunch of images and return them as a list.
        
        rects: a list filled with rectangle tuples. see image_at() function
        for details on rectangle tuple format
        scale: see image_at()
        colorkey: see image_at()
        """
        return [self.image_at(rect, scale, colorkey) for rect in rects]

    def load_row(self, rect:tuple, image_count:int, scale:int = 1,colorkey:int = None) -> list:
        """Load a whole strip of images, and return them as a list.
        This function assumes equal size of each image within the row.

        rect: see image_at() for definition. This will be the first `rect` from which the positions of other sprites are derived.
        image_count: 
        scale: see image_at()
        colorkey: see image_at()
        """

        # rect: (x, y, width, height)
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, scale, colorkey)

    def load_column(self, rect:tuple, image_count:int, scale:int = 1, colorkey:int = None) -> list:
        """Load a whole strip of images, and return them as a list.
        This function assumes equal size of each image within the column.
        """

        # rect: (x, y, width, height)
        tups = [(rect[0], rect[1]+rect[3]*x, rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups,scale, colorkey)
