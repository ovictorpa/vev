import unittest
import sys
import os

sys.path.insert(0, os.getcwd())

from VEV.vev.tabelaHash import TabelaHashSondagemLinear

class TestHashEdgePair(unittest.TestCase):

    def test_inserir_colisao(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir(1, "a")
        tabela.inserir(4, "b")  # colisão
        self.assertEqual(tabela.buscar(4), "b")

    def test_remover_e_reinserir(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        tabela.remover("ana")
        tabela.inserir("bia", 2)
        self.assertTrue(tabela.contem("bia"))

    def test_buscar_existente(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("x", 9)
        self.assertEqual(tabela.buscar("x"), 9)

    def test_buscar_inexistente(self):
        tabela = TabelaHashSondagemLinear(5)
        with self.assertRaises(KeyError):
            tabela.buscar("y")

    def test_tabela_cheia(self):
        tabela = TabelaHashSondagemLinear(2)
        tabela.inserir(1, "a")
        tabela.inserir(2, "b")
        with self.assertRaises(OverflowError):
            tabela.inserir(3, "c")

    def test_itens(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("a", 1)
        tabela.inserir("b", 2)
        self.assertEqual(len(tabela.itens()), 2)

if __name__ == "__main__":
    unittest.main()