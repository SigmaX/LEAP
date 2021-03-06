import io

from leap.probe import *
from leap import core, binary, data
from leap import operate as op


##############################
# Tests for CSVProbe
##############################
def test_CSVAttributesProbe_1():
    """When recording the attribute 'my_value' and leaving other arguments at their default,
    running CSVProbe on a population of individuals with just the attribute 'my_value' should
    produce the correct CSV-formatted output."""
    # Set up a population
    # TODO simplify this with a test fixture
    pop = data.test_population
    pop, _ = op.evaluate(pop)  # Evaluate its fitness

    # Assign distinct alues to an attribute on each individual
    attr = 'my_value'
    vals = ['GREEN', 15, 'BLUE', 72.81]
    for (ind, val) in zip(pop, vals):
        ind.attributes[attr] = val

    # Setup a probe that writes to a str in memory
    stream = io.StringIO()
    probe = CSVAttributesProbe(stream, ['my_value'])
    probe.set_step(10)

    # Execute
    probe(pop, None)
    result = stream.getvalue()
    stream.close()

    # Test
    expected = "step, my_value\n" + \
               "10, GREEN\n"  + \
               "10, 15\n" + \
               "10, BLUE\n" + \
               "10, 72.81\n"
    assert(result == expected)


def test_CSVAttributesProbe_2():
    """When recording the attribute 'my_value' and leaving other arguments at their default,
    running CSVProbe on a population of individuals with several attributes should
    produce CSV-formatted output that only records 'my_value'."""
    # Set up a population
    # TODO simplify this with a test fixture
    pop = data.test_population
    pop, _ = op.evaluate(pop)  # Evaluate its fitness

    # Assign distinct alues to an attribute on each individual
    attrs = [('foo', ['GREEN', 15, 'BLUE', 72.81]), \
             ('bar', ['Colorless', 'green', 'ideas', 'sleep']), \
             ('baz', [['a', 'b', 'c'], [1, 2, 3], [None, None, None], [0.1, 0.2, 0.3]])]
    for attr, vals in attrs:
        for (ind, val) in zip(pop, vals):
            ind.attributes[attr] = val

    # Setup a probe that writes to a str in memory
    stream = io.StringIO()
    probe = CSVAttributesProbe(stream, ['foo', 'bar'])
    probe.set_step(10)

    # Execute
    probe(pop, None)
    result = stream.getvalue()
    stream.close()

    # Test
    expected = "step, foo, bar\n" + \
               "10, GREEN, Colorless\n"  + \
               "10, 15, green\n" + \
               "10, BLUE, ideas\n" + \
               "10, 72.81, sleep\n"
    assert(result == expected)


def test_CSVAttributesProbe_3():
    """Changing the order of the attributes list changes the order of the columns."""
    # Set up a population
    # TODO simplify this with a test fixture
    pop = data.test_population
    pop, _ = op.evaluate(pop)  # Evaluate its fitness

    # Assign distinct alues to an attribute on each individual
    attrs = [('foo', ['GREEN', 15, 'BLUE', 72.81]), \
             ('bar', ['Colorless', 'green', 'ideas', 'sleep']), \
             ('baz', [['a', 'b', 'c'], [1, 2, 3], [None, None, None], [0.1, 0.2, 0.3]])]
    for attr, vals in attrs:
        for (ind, val) in zip(pop, vals):
            ind.attributes[attr] = val

    # Setup a probe that writes to a str in memory
    stream = io.StringIO()
    probe = CSVAttributesProbe(stream, ['bar', 'foo'])  # Passing params in reverse order from the other test above
    probe.set_step(10)

    # Execute
    probe(pop, None)
    result = stream.getvalue()
    stream.close()

    # Test
    expected = "step, bar, foo\n" + \
               "10, Colorless, GREEN\n"  + \
               "10, green, 15\n" + \
               "10, ideas, BLUE\n" + \
               "10, sleep, 72.81\n"
    assert(result == expected)


def test_CSVAttributesProbe_4():
    """Proving an attribute that contains list data should work flawlessly.."""
    # Set up a population
    # TODO simplify this with a test fixture
    pop = data.test_population
    pop, _ = op.evaluate(pop)  # Evaluate its fitness

    # Assign distinct alues to an attribute on each individual
    attrs = [('foo', ['GREEN', 15, 'BLUE', 72.81]), \
             ('bar', ['Colorless', 'green', 'ideas', 'sleep']), \
             ('baz', [['a', 'b', 'c'], [1, 2, 3], [None, None, None], [0.1, 0.2, 0.3]])]
    for attr, vals in attrs:
        for (ind, val) in zip(pop, vals):
            ind.attributes[attr] = val

    # Setup a probe that writes to a str in memory
    stream = io.StringIO()
    probe = CSVAttributesProbe(stream, ['bar', 'baz'])  # Passing params in reverse order from the other test above
    probe.set_step(10)

    # Execute
    probe(pop, None)
    result = stream.getvalue()
    stream.close()

    # Test
    expected = "step, bar, baz\n" + \
               "10, Colorless, ['a', 'b', 'c']\n"  + \
               "10, green, [1, 2, 3]\n" + \
               "10, ideas, [None, None, None]\n" + \
               "10, sleep, [0.1, 0.2, 0.3]\n"
    assert(result == expected)
