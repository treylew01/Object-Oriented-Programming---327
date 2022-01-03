import pytest
from machine import Enigma
from components import Rotor, Reflector, Plugboard, ROTOR_WIRINGS, ROTOR_NOTCHES, ALPHABET
import sys


def test_rotor_wirings():
    the_wirings = {
        'I': {'forward':'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
              'backward':'UWYGADFPVZBECKMTHXSLRINQOJ'},
        'II':{'forward':'AJDKSIRUXBLHWTMCQGZNPYFVOE',
              'backward':'AJPCZWRLFBDKOTYUQGENHXMIVS'},
        'III':{'forward':'BDFHJLCPRTXVZNYEIWGAKMUSQO',
               'backward':'TAGBPCSDQEUFVNZHYIXJWLRKOM'},
        'V':{'forward':'VZBRGITYUPSDNHLXAWMJQOFECK',
               'backward':'QCYLXWENFTZOSMVJUDKGIARPHB'}
    }
    assert ROTOR_WIRINGS == the_wirings

def test_rotor_notches():
    the_notches = {
        'I':'Q', # Next rotor steps when I moves from Q -> R
        'II':'E', # Next rotor steps when II moves from E -> F
        'III':'V', # Next rotor steps when III moves from V -> W
        'V':'Z' # Next rotor steps when V moves from Z -> A
        }
    assert ROTOR_NOTCHES == the_notches

def test_alphabet():
    the_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    assert ALPHABET == the_alphabet

def test_morning_messages():
    enigma = Enigma('ABC')
    enigma.encipher('GOODMORNINGSIR')
    enigma.encipher('PLANESOVERTHERHINETHISMORNING')
    enigma.encipher('BRITISHSHIPSWEREINTHEBALTIC')
    assert enigma.encipher('WEAREBEINGATTACKEDSENDBACKUPASSOONASPOSSIBLE') == 'OBIIGJPWQZZRPKZBOUEBOUWVYEOGNNFIIMVKNDQQEYJN'
    assert enigma.decipher('OBIIGJPWQZZRPKZBOUEBOUWVYEOGNNFIIMVKNDQQEYJN') == 'QCOPAUBKDAMDHRBOMFFCGHARDSSRYUHJSJGBUVBWGEBC'

def test_super_long_word_just_because():
    enigma = Enigma("XYZ")
    assert enigma.encipher('supercalifragilisticexpialidocioussupercalifragilisticexpialidocious\
supercalifragilisticexpialidocioussupercalifragilisticexpialidocioussupercalifragilisticexpialidocioussupercalifragilisticexpialidocioussupercalifragilisticexpialidocious ') == "JSDKZDUQZDOZZBXVGDDTNBRHSUMKDHOYKNBLXGNIEMXXGYQJDNHQRKWQHYEYJMFYSLBMPHGRNOCOOITWACPFLVHGYDNHBFFPYWTMSKOFFFSXFUHSJLNNHHILOFXVOPSFOVGUDYEDLKGLKTCPYZNXELPVAAHWAPAZVHKLRYKRTHPRK\
PIKPZAMJIUGZFFNQSRERPIAOWGODHTJMIESBWMZODIINOSMKJOAJBBWUZVZPSDIAW"

def test_hello_world_but_letter_by_letter():
    enigma = Enigma("ORT")
    assert enigma.encode_decode_letter('H') == 'T'
    assert enigma.encode_decode_letter('e') == 'U'
    assert enigma.encode_decode_letter('l') == 'Z'
    assert enigma.encode_decode_letter('l') == 'S'
    assert enigma.encode_decode_letter('l') == 'R'
    assert enigma.encode_decode_letter('o') == 'V'
    assert enigma.encode_decode_letter('w') == 'D'
    assert enigma.encode_decode_letter('o') == 'N'
    assert enigma.encode_decode_letter('r') == 'Y'
    assert enigma.encode_decode_letter('l') == 'B'
    assert enigma.encode_decode_letter('d') == 'T'




@pytest.fixture
def enigma():
    return Enigma()

def test_enigma_attributes(enigma):
    assert hasattr(enigma, 'key')
    assert hasattr(enigma, 'rotor_order')
    assert hasattr(enigma, 'set_rotor_order')
    assert hasattr(enigma, 'reflector')
    assert hasattr(enigma, 'plugboard')

def test_enigma_begin(capfd):
    with pytest.raises(ValueError):
        enigma = Enigma(key = 'AAAA')
        out,err=capfd.readouterr()
        assert out.err=="Please provide a three letter position key such as AAA."

def test_enigma_output(enigma):
    first_part = "Keyboard <-> Plugboard <->  Rotor I <-> Rotor  II <-> Rotor  III <-> Reflector "
    key = "Key:  + AAA"
    assert enigma.__repr__() == f"{first_part}\n{key}"

def test_encipher(enigma):
    code = "ILBDAAMTAZ"
    assert enigma.encipher("Hello World") == code

def test_bad_encipher(enigma, capfd):
    with pytest.raises(ValueError):
        enigma.encipher("Hello World!")
        out,err=capfd.readouterr()
        assert out.err=="Please provide a string containing only the characters a-zA-Z and spaces."

def test_decipher(enigma):
    decode = "HELLOWORLD"
    assert enigma.decipher("ILBDAAMTAZ") == decode

def test_encode_decode_letter(enigma):
    assert enigma.encode_decode_letter("A") == "B"

def test_bad_encode_decode_letter(enigma, capfd):
    with pytest.raises(ValueError):
        enigma.encode_decode_letter("1")
        out,err=capfd.readouterr()
        assert out.err=="Please provide a string containing only the characters a-zA-Z and spaces."

def test_set_rotor_position(enigma, capfd):
    enigma.set_rotor_position("AAA", printIt=True)
    out,err=capfd.readouterr()
    assert out=="Rotor position successfully updated. Now using AAA.\n"

def test_set_rotor_position2(enigma, capfd):
    enigma.set_rotor_position("XYZ", printIt=True)
    out,err=capfd.readouterr()
    assert out=="Rotor position successfully updated. Now using XYZ.\n"

def test_bad_set_rotor_position(enigma, capfd):
    enigma.set_rotor_position("AAAA", printIt=True)
    out,err=capfd.readouterr()
    assert out=="Please provide a three letter position key such as AAA.\n"

def test_bad_set_rotor_position1(enigma):
    enigma.set_rotor_position("ABC")
    assert enigma.decipher("Hello") == "ROMUL"

def test_set_plugs(enigma):
    enigma.set_plugs(['AB', 'CD', 'XR'])
    new_enigma = Enigma(swaps=['AB', 'CD', 'XR'])
    assert enigma.decipher('ILBDAAMTAZ') == new_enigma.decipher('ILBDAAMTAZ')

def test_set_plugs_printed(enigma, capfd):
    #Plugboard successfully updated. New swaps are:
    swap3 = "A <-> B"
    swap2 = "C <-> D"
    swap1 = "X <-> R"
    enigma.set_plugs(['AB', 'CD', 'XR'], printIt=True)
    out,err=capfd.readouterr()
    assert out==f"Plugboard successfully updated. New swaps are:\n{swap3}\n{swap2}\n{swap1}\n"


### CAPITAL R Rotor is the class!
### SMALL r rotor is the rotor for this instance!
@pytest.fixture
def rotor():
    return Rotor('I', 'A')

def test_rotor_attributes(rotor):
    assert hasattr(rotor, 'rotor_num')
    assert hasattr(rotor, 'wiring')
    assert hasattr(rotor, 'notch')
    assert hasattr(rotor, 'window')
    assert hasattr(rotor, 'offset')
    assert hasattr(rotor, 'next_rotor')
    assert hasattr(rotor, 'prev_rotor')

def test_bad_rotor(capfd):
    with pytest.raises(ValueError):
        rotor = Rotor('A', 'I')
        out,err=capfd.readouterr()
        assert out.err=="Please select I, II, III, or V for your rotor number and provide the initial window setting (i.e. the letter on the wheel initially visible to the operator."

def test_rotor_output(rotor):
    forward = '{\'forward\': \'EKMFLGDQVZNTOWYHXUSPAIBRCJ\''
    backward = '\'backward\': \'UWYGADFPVZBECKMTHXSLRINQOJ\'}'
    window = 'Window: A'
    assert rotor.__repr__() == f"Wiring:\n{forward}, {backward}\n{window}"

def test_rotor_step(capfd):
    rotor1 = Rotor('I', 'X')
    rotor2 = Rotor('V', 'X', next_rotor=rotor1)
    rotor2.step()
    rotor2.step()
    rotor1.step()
    x = rotor1.encode_letter('R')
    y = rotor2.encode_letter('Z')
    print(x, y)
    out,err =capfd.readouterr()
    assert out=="9 12\n"

def test_rotor_step2():
    rotor1 = Rotor('I','A')
    rotor2 = Rotor('V','Z', next_rotor=rotor1)
    rotor2.step()
    assert rotor1.window == 'B'
    #assert rotor2.next_rotor.window == 'A'

def test_rotor_step3():
    rotor1 = Rotor('I','Q')
    rotor2 = Rotor('V','A', next_rotor=rotor1)
    rotor1.step()
    assert rotor1.window == 'R'


def test_ecode_letter(rotor, capfd):
    x = rotor.encode_letter('A', return_letter=True)
    print(x)
    out,err =capfd.readouterr()
    assert out=="E\n"

def test_ecode_letter2(capfd):
    rotor1 = Rotor('I', 'X')
    rotor2 = Rotor('V', 'Y', next_rotor=rotor1)
    rotor2.change_setting('Z')
    rotor2.encode_letter('A', printit = True)
    out,err =capfd.readouterr()
    assert out=="Rotor V: input = Z, output = K\n"

### CAPITAL R Reflector is the class!
### SMALL r reflector is the reflector for this instance!
@pytest.fixture
def reflector():
    return Reflector()

def test_reflector_attributes(reflector):
    assert hasattr(reflector, 'wiring')

def test_reflector_wiring(reflector):
    assert reflector.wiring == {'A': 'Y', 'B': 'R', 'C': 'U', 'D': 'H', 'E': 'Q', 'F': 'S', 'G': 'L', 'H': 'D',
                 'I': 'P', 'J': 'X', 'K': 'N', 'L': 'G', 'M': 'O', 'N': 'K', 'O': 'M', 'P': 'I',
                 'Q': 'E', 'R': 'B', 'S': 'F', 'T': 'Z', 'U': 'C', 'V': 'W', 'W': 'V', 'X': 'J',
                 'Y': 'A', 'Z': 'T'
                 }

def test_reflector_output(reflector):
    wires = {'A': 'Y', 'B': 'R', 'C': 'U', 'D': 'H', 'E': 'Q', 'F': 'S', 'G': 'L', 'H': 'D', 'I': 'P', 'J': 'X', 'K': 'N', 'L': 'G', 'M': 'O', 'N': 'K', 'O': 'M', 'P': 'I', 'Q': 'E', 'R': 'B', 'S': 'F', 'T': 'Z', 'U': 'C', 'V': 'W', 'W': 'V', 'X': 'J', 'Y': 'A', 'Z': 'T'}
    assert reflector.__repr__() == f"Reflector wiring: \n{wires}"

### CAPITAL P Plugboard is the class!
### SMALL p plugboards is the plugboard for this fixture
@pytest.fixture
def plugboard():
    return Plugboard(['AB', 'XR'])

def test_plugboard_attributes(plugboard):
    assert hasattr(plugboard, 'swaps')

def test_plugboard_output(plugboard):
    swap1 = "A <-> B"
    swap2 = "X <-> R"
    assert plugboard.__repr__() == f"{swap1}\n{swap2}"

def test_update_plugboard_true(plugboard):
    plugboard.update_swaps(['AB', 'FX'],  replace=True)
    swap1 = "A <-> B"
    swap2 = "F <-> X"
    assert plugboard.__repr__() == f"{swap1}\n{swap2}"

def test_update_plugboard_false(plugboard):
    plugboard.update_swaps(['AB', 'FX'],  replace=False)
    swap1 = "A <-> B"
    swap2 = "X <-> F"
    swap3 = "R <-> X"
    assert plugboard.__repr__() == f"{swap1}\n{swap2}\n{swap3}"

def test_plugboard_limit(plugboard, capfd):
    plugboard.update_swaps(['AB', 'FX', 'DE', 'FG', 'HI', 'JK', 'LM', 'NO', 'PQ'],  replace=True)
    out,err=capfd.readouterr()
    assert out=="Only a maximum of 6 swaps is allowed.\n"

def test_plugboard_NULL(plugboard,capfd):
    plugboard.update_swaps(None)
    out,err=capfd.readouterr()
    assert out==""
