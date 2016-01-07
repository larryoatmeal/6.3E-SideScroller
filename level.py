from pygame import image, Surface, PixelArray

'''
The Level class will read a 'pixmap', an image where the pixels correspond to
certain entities at locations in the world for easy level creation.

Level provides the load() method, which will fill a World with Entities as
defined by the color_mapping dictionary.
'''
class Level:
    '''
    level_file is the location of the image file that describes the level by
    pixel.

    color_mapping is a dictionary that maps colors in (r, g, b) format to
    functions accepting a World object and a (x, y) position. This would
    typically be used to construct Sprites by color.

    For example, this mapping would construct Players of size (50, 75) at the
    position specified by red pixel locations:
        def red_func(world, pos):
            player = Player(world, pos, (50, 75))
            world.addPlayer(player)
        color_mapping = {(255, 0, 0): red_func}
    '''
    def __init__(self, level_file, color_mapping):
        self.color_mapping = color_mapping

        # Load image from file and store dimensions
        pixmap = image.load(level_file)
        self.width, self.height = pixmap.get_size()

        # Convert pixels to colors
        def index_to_color(i):
            color = pixmap.unmap_rgb(i)
            return (color.r, color.g, color.b)
        self.color_array = list(map(
                               lambda index: list(map(
                                   index_to_color, index)), PixelArray(pixmap)))

    '''
    Iterates over the pixel array and calls the function defined in
    color_mapping corresponding to the color at that location, passing that
    function the pixel position and the world.
    '''
    def load(self, world):
        for i in range(self.width):
            for j in range(self.height):
                color = self.color_array[i][j]
                try:
                    function = self.color_mapping[color]
                    function(world, (i, j))
                except KeyError:
                    print('KeyError in Level.load(): Color', str(color),
                          'does not map to a function in color_mapping.')

if __name__ == '__main__':
    print('Testing Level.py class')
    level = Level('level_test.png', {
        (255, 255, 255): lambda world, pos: print('white', pos),
        (0, 0, 0): lambda world, pos: print('black', pos)
    })
    level.load(None)