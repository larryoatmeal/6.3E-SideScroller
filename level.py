from pygame import image
from pygame import Surface
from pygame import PixelArray

# The Level class will read a "pixmap", an image where the pixels correspond to
# certain entities at locations in the world for easy level creation.
#
# Level provides the load() method, which will fill a World with Entities as
# defined by the color_mapping dictionary.
class Level:
    # level_file is the location of the image file that describes the level by
    # pixel.
    #
    # color_mapping is a dictionary that maps colors in (r, g, b) format to
    # functions accepting a (x, y) position and a World object. This would
    # typically be used to construct Sprites by color. For example, this mapping
    # would construct Players of size (50, 75) at the position specified by
    # red pixel locations:
    #     def red_func(pos, world):
    #         player = Player(world, pos, (50, 75))
    #         world.addPlayer(player)
    #     color_mapping = {(255, 0, 0): red_func}
    def __init__(self, level_file, color_mapping):
    self.color_mapping = color_mapping

    # Load image from file and store dimensions
    pixel_map = image.load(level_file)
    self._width = pixel_map.get_width()
    self._height = pixel_map.get_height()

    # Convert image surface to pixel array (lighter)
    self.pixel_array = map(PixelArray(pixel_map),
                        lambda x: map(Surface.unmap_rgb, x))

    # Iterates over the pixel array and calls the function defined in
    # color_mapping corresponding to the color at that location, passing that
    # function the pixel position and the world.
    def load(self, world):
        for i in range(self.width):
            for j in range(self.height):
                color = self.pixel_array[i, j]
                function = self.color_mapping[color]
                function((i, j), world)