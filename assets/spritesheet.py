# evan genske, 12.5.2021

import pygame

class SpriteSheet:

    def __init__(self, filepath):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filepath).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filepath}")
            raise SystemExit(e)


    def image_at(self, rectangle:tuple, colorkey:int = None, scale:int = 1) -> pygame.Surface:
        """Load a specific image from a specific rectangle.
        Returns a pygame surface.
        
        rectangle: a tuple in the format of (x, y, width, height)
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

    def images_at(self, rects:list, colorkey:int = None) -> list:
        """Load a whole bunch of images and return them as a list.
        
        rects: a list filled with rectangle tuples. see image_at() function
        for details on rectangle tuple format
        colorkey: see image_at()
        """
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_horizontal_strip(self, rect, image_count, colorkey = None) -> list:
        """Load a whole strip of images, and return them as a list.
        This function assumes equal size of each image within the row.
        rect:
        """

        # rect: (x, y, width, height)
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_vertical_strip(self, rect, image_count, colorkey = None) -> list:
        """Load a whole strip of images, and return them as a list.
        This function assumes equal size of each image within the column.
        rect:
        """

        # rect: (x, y, width, height)
        tups = [(rect[0], rect[1]+rect[3]*x, rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
