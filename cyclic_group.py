class CyclicGroup:
    def __init__(self, order, generator):
        """
        Initialize a cyclic group of given order with a generator element.
        :param order: The order (size) of the cyclic group.
        :param generator: The generator element of the group.
        """
        if order <= 0:
            raise ValueError("Order of the cyclic group must be a positive integer.")

        self.order = order
        self.generator = generator

    def element(self, exponent):
        """
        Compute the element in the cyclic group given an exponent.
        :param exponent: The exponent to raise the generator to.
        :return: The element in the cyclic group.
        """
        return pow(self.generator, exponent, self.order)

    def exponentiate(self, num, power):
        return pow(num, power, self.order)

    def elements(self):
        """
        Generate all elements of the cyclic group.
        :return: A set of all elements.
        """
        return {self.element(i) for i in range(self.order)}

    def is_member(self, value):
        """
        Check if a given value is a member of the cyclic group.
        :param value: The value to check.
        :return: True if the value belongs to the group, False otherwise.
        """
        return value in self.elements()

    @staticmethod
    def find_generator(order):
        """
        Find a generator for the cyclic group of given order.
        :param order: The order of the cyclic group.
        :return: A generator element if found, otherwise None.
        """
        if order <= 0:
            raise ValueError("Order must be a positive integer.")

        def finder():
            for g in range(1, order):
                elements = {(g**i) % order for i in range(order)}
                if len(elements) == order - 1:
                    yield g

        g = None
        for _, g in zip(range(10), finder()):
            pass
        else:
            return g

    @classmethod
    def new(cls, order, generator):
        if generator:
            return cls(order, generator)
        return cls(order, cls.find_generator(order))

    def __repr__(self):
        return f"CyclicGroup(order={self.order}, generator={self.generator})"
