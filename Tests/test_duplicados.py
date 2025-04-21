import os
import shutil
import unittest
from duplicados import calcular_hash, buscar_duplicados, eliminar_duplicados, mover_duplicados

class TestDuplicados(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/temp"
        os.makedirs(self.test_dir, exist_ok=True)

        # Crear archivos duplicados
        with open(os.path.join(self.test_dir, "archivo1.txt"), "w") as f:
            f.write("contenido de prueba")

        shutil.copy(
            os.path.join(self.test_dir, "archivo1.txt"),
            os.path.join(self.test_dir, "archivo2.txt")
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_calcular_hash(self):
        archivo = os.path.join(self.test_dir, "archivo1.txt")
        hash1 = calcular_hash(archivo)
        self.assertIsInstance(hash1, str)
        self.assertEqual(hash1, calcular_hash(os.path.join(self.test_dir, "archivo2.txt")))

    def test_buscar_duplicados(self):
        duplicados = buscar_duplicados(self.test_dir)
        self.assertTrue(any("archivo2.txt" in dup[0] for dup in duplicados))

    def test_eliminar_duplicados(self):
        duplicados = buscar_duplicados(self.test_dir)
        eliminar_duplicados(duplicados)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "archivo1.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "archivo2.txt")))

    def test_mover_duplicados(self):
        duplicados = buscar_duplicados(self.test_dir)
        mover_duplicados(duplicados, self.test_dir)
        moved_path = os.path.join(self.test_dir, "Duplicados", "archivo2.txt")
        self.assertTrue(os.path.exists(moved_path))

if __name__ == '__main__':
    unittest.main()
