"""" WORLD COLOR ACCORDING TO MENNING """

UNEXPLORATED = "2"
EXPLORATED = "3"
START = "1"

class Colormap(object):

    """ Basic color map class"""

    def __init__(self):
        """ Create the color map """
        pass

    def __call__(self, state):
        return self.state2color(state)


class NoColor(Colormap):

    """Docstring for NoColor. """

    def __init__(self):
        """TODO: to be defined. """
        Colormap.__init__(self)

    def state2color(self, state):
        return "lightblue"


class ClassicColor(Colormap):

    """ Classic color scheme"""

    def __init__(self):
        """ Create the colormap """
        Colormap.__init__(self)

    def state2color(self, state):
        """Convert state to color

        :state: TODO
        :returns: TODO

        """
        if state == UNEXPLORATED:
            return "red"

        if state == EXPLORATED:
            return "green"

        if state == START:
            return "blue"

