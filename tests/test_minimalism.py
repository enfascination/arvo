import pytest
from music21 import converter
from arvo import minimalism
from arvo import sequences
from arvo import tools


@pytest.fixture
def example_stream():
    s = converter.parse("tinyNotation: C D E F G A B c d e f g")
    return s


# Additive Process Tests


def test_additive_process(example_stream):
    result = minimalism.additive_process(example_stream)
    expected_result = converter.parse(
        """tinyNotation: 
        C
        C D 
        C D E 
        C D E F 
        C D E F G 
        C D E F G A 
        C D E F G A B 
        C D E F G A B c
        C D E F G A B c d
        C D E F G A B c d e
        C D E F G A B c d e f
        C D E F G A B c d e f g
    """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


@pytest.mark.parametrize(
    "direction,expected_result",
    [
        (
            minimalism.Direction.BACKWARD,
            converter.parse(
                """tinyNotation: 
        g
        f g  
        e f g  
        d e f g  
        c d e f g  
        B c d e f g  
        A B c d e f g  
        G A B c d e f g   
        F G A B c d e f g   
        E F G A B c d e f g   
        D E F G A B c d e f g  
        C D E F G A B c d e f g      
    """
            ),
        ),
        (
            minimalism.Direction.INWARD,
            converter.parse(
                """tinyNotation: 
        C g
        C D f g  
        C D E e f g   
        C D E F d e f g
        C D E F G c d e f g 
        C D E F G A B c d e f g   
    """
            ),
        ),
        (
            minimalism.Direction.OUTWARD,
            converter.parse(
                """tinyNotation: 
        A B
        G A B c
        F G A B c d
        E F G A B c d e
        D E F G A B c d e f
        C D E F G A B c d e f g
    """
            ),
        ),
    ],
)
def test_additive_process_direction(example_stream, direction, expected_result):
    result = minimalism.additive_process(example_stream, direction=direction)
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_additive_process_step_int(example_stream):
    result = minimalism.additive_process(example_stream, step=2)
    expected_result = converter.parse(
        """tinyNotation: 
        C D 
        C D E F 
        C D E F G A 
        C D E F G A B c
        C D E F G A B c d e
        C D E F G A B c d e f g
    """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_additive_process_step_sequence(example_stream):
    result = minimalism.additive_process(example_stream, step=[1, 2, 3])
    expected_result = converter.parse(
        """tinyNotation: 
        C
        C D E 
        C D E F G A 
        C D E F G A B 
        C D E F G A B c d
        C D E F G A B c d e f g
        """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_additive_process_step_sequence_absolute(example_stream):
    result = minimalism.additive_process(
        example_stream, step=sequences.PRIMES, step_mode=minimalism.StepMode.ABSOLUTE
    )
    expected_result = converter.parse(
        """tinyNotation: 
        C D 
        C D E 
        C D E F G 
        C D E F G A B 
        C D E F G A B c d e f
        C D E F G A B c d e f g
        """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_additive_process_step_sequence_absolute_infinite_loop(example_stream):
    result = minimalism.additive_process(
        example_stream, step=[1, 2, 3], step_mode=minimalism.StepMode.ABSOLUTE
    )
    expected_result = converter.parse(
        """tinyNotation: 
        C
        C D 
        C D E 
        """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_additive_process_repetitions_int(example_stream):
    result = minimalism.additive_process(example_stream, repetitions=2)
    expected_result = converter.parse(
        """tinyNotation: 
        C
        C
        C D 
        C D 
        C D E 
        C D E 
        C D E F 
        C D E F 
        C D E F G 
        C D E F G 
        C D E F G A 
        C D E F G A 
        C D E F G A B 
        C D E F G A B 
        C D E F G A B c
        C D E F G A B c
        C D E F G A B c d
        C D E F G A B c d
        C D E F G A B c d e
        C D E F G A B c d e
        C D E F G A B c d e f
        C D E F G A B c d e f
        C D E F G A B c d e f g
        C D E F G A B c d e f g
    """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_additive_process_repetitions_sequence(example_stream):
    result = minimalism.additive_process(example_stream, repetitions=[1, 2, 3])
    expected_result = converter.parse(
        """tinyNotation: 
        C
        C D 
        C D 
        C D E 
        C D E 
        C D E 
        C D E F 
        C D E F G 
        C D E F G 
        C D E F G A 
        C D E F G A 
        C D E F G A 
        C D E F G A B 
        C D E F G A B c
        C D E F G A B c
        C D E F G A B c d
        C D E F G A B c d
        C D E F G A B c d
        C D E F G A B c d e
        C D E F G A B c d e f
        C D E F G A B c d e f
        C D E F G A B c d e f g
        C D E F G A B c d e f g
        C D E F G A B c d e f g
    """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_additive_process_iterations(example_stream):
    result = minimalism.additive_process(example_stream, iterations=8)
    expected_result = converter.parse(
        """tinyNotation: 
        C
        C D 
        C D E 
        C D E F 
        C D E F G 
        C D E F G A 
        C D E F G A B 
        C D E F G A B c
    """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_additive_process_nonlinear(example_stream):
    result = minimalism.additive_process(
        example_stream,
        step=sequences.kolakoski(),
        step_mode=minimalism.StepMode.ABSOLUTE,
        iterations=8,
    )
    expected_result = converter.parse(
        """tinyNotation: 
        C
        C D     
        C D     
        C
        C
        C D     
        C
        C D     
        """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


# Subtractive Process Tests


def test_subtractive_process(example_stream):
    result = minimalism.subtractive_process(example_stream)
    expected_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        E F G A B c d e f g   
        F G A B c d e f g   
        G A B c d e f g   
        A B c d e f g  
        B c d e f g  
        c d e f g  
        d e f g  
        e f g  
        f g  
        g
    """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


@pytest.mark.parametrize(
    "direction,expected_result",
    [
        (
            minimalism.Direction.BACKWARD,
            converter.parse(
                """tinyNotation: 
        C D E F G A B c d e f g
        C D E F G A B c d e f
        C D E F G A B c d e
        C D E F G A B c d
        C D E F G A B c
        C D E F G A B 
        C D E F G A 
        C D E F G 
        C D E F 
        C D E 
        C D 
        C   
    """
            ),
        ),
        (
            minimalism.Direction.INWARD,
            converter.parse(
                """tinyNotation: 
        C D E F G A B c d e f g
        D E F G A B c d e f
        E F G A B c d e
        F G A B c d
        G A B c
        A B
        """
            ),
        ),
        (
            minimalism.Direction.OUTWARD,
            converter.parse(
                """tinyNotation: 
        C D E F G A B c d e f g   
        C D E F G c d e f g 
        C D E F d e f g
        C D E e f g   
        C D f g  
        C g
    """
            ),
        ),
    ],
)
def test_subtractive_process_direction(example_stream, direction, expected_result):
    result = minimalism.subtractive_process(example_stream, direction=direction)
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_subtractive_process_step_int(example_stream):
    result = minimalism.subtractive_process(example_stream, step=2)
    expected_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        E F G A B c d e f g   
        G A B c d e f g   
        B c d e f g  
        d e f g  
        f g  
    """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_subtractive_process_step_sequence(example_stream):
    result = minimalism.subtractive_process(example_stream, step=[1, 2, 3])
    expected_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        F G A B c d e f g   
        B c d e f g  
        c d e f g  
        e f g  
        """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_subtractive_process_step_sequence_absolute(example_stream):
    result = minimalism.subtractive_process(
        example_stream, step=sequences.PRIMES, step_mode=minimalism.StepMode.ABSOLUTE
    )
    expected_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        E F G A B c d e f g   
        F G A B c d e f g   
        A B c d e f g  
        c d e f g  
        g
        """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_subtractive_process_step_sequence_absolute_infinite_loop(example_stream):
    result = minimalism.subtractive_process(
        example_stream, step=[1, 2, 3], step_mode=minimalism.StepMode.ABSOLUTE
    )
    expected_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        E F G A B c d e f g   
        F G A B c d e f g   
        """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_subtractive_process_repetitions_int(example_stream):
    result = minimalism.subtractive_process(example_stream, repetitions=2)
    expected_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        D E F G A B c d e f g  
        E F G A B c d e f g   
        E F G A B c d e f g   
        F G A B c d e f g   
        F G A B c d e f g   
        G A B c d e f g   
        G A B c d e f g   
        A B c d e f g  
        A B c d e f g  
        B c d e f g  
        B c d e f g  
        c d e f g  
        c d e f g  
        d e f g  
        d e f g  
        e f g  
        e f g  
        f g  
        f g  
        g   
        g
        """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_subtractive_process_repetitions_sequence(example_stream):
    result = minimalism.subtractive_process(example_stream, repetitions=[1, 2, 3])
    expected_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        D E F G A B c d e f g  
        E F G A B c d e f g   
        E F G A B c d e f g   
        E F G A B c d e f g   
        F G A B c d e f g   
        G A B c d e f g   
        G A B c d e f g   
        A B c d e f g  
        A B c d e f g  
        A B c d e f g  
        B c d e f g  
        c d e f g  
        c d e f g  
        d e f g  
        d e f g  
        d e f g  
        e f g  
        f g  
        f g  
        g
        g
        g
    """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_subtractive_process_iterations(example_stream):
    result = minimalism.subtractive_process(example_stream, iterations=8)
    expected_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        E F G A B c d e f g   
        F G A B c d e f g   
        G A B c d e f g   
        A B c d e f g  
        B c d e f g  
        c d e f g  
        d e f g  
    """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)


def test_subtractive_process_nonlinear(example_stream):
    result = minimalism.subtractive_process(
        example_stream,
        step=sequences.kolakoski(),
        step_mode=minimalism.StepMode.ABSOLUTE,
        iterations=8,
    )
    expected_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        E F G A B c d e f g   
        E F G A B c d e f g   
        D E F G A B c d e f g  
        D E F G A B c d e f g  
        E F G A B c d e f g   
        D E F G A B c d e f g  
        E F G A B c d e f g   
        """
    )
    assert tools.stream_to_notes(result) == tools.stream_to_notes(expected_result)
