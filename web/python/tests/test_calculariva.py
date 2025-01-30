import unittest

def calcularIVA(precio):
    return precio * 0.21

class TestCalcularIVA(unittest.TestCase):
    def test_calculariva(self):
        self.assertEqual(calcularIVA(100), 21)
        self.assertEqual(calcularIVA(200), 42)
        self.assertEqual(calcularIVA(0), 0)
        self.assertEqual(calcularIVA(-100), -21)

if __name__ == '__main__':
    unittest.main()
