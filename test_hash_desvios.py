import unittest
import sys
import os

sys.path.insert(0, os.getcwd())

from VEV.vev.tabelaHash import TabelaHashSondagemLinear

class TestHashDesvios(unittest.TestCase):

    def test_capacidade_invalida(self):
        with self.assertRaises(ValueError):
            TabelaHashSondagemLinear(0)

    def test_inserir_e_buscar(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 10)
        self.assertEqual(tabela.buscar("ana"), 10)

    def test_atualizar_valor_existente(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 10)
        tabela.inserir("ana", 20)
        self.assertEqual(tabela.buscar("ana"), 20)

    def test_buscar_inexistente(self):
        tabela = TabelaHashSondagemLinear(5)
        with self.assertRaises(KeyError):
            tabela.buscar("x")

    def test_remover_existente(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 10)
        tabela.remover("ana")
        self.assertFalse(tabela.contem("ana"))

    def test_remover_inexistente(self):
        tabela = TabelaHashSondagemLinear(5)
        with self.assertRaises(KeyError):
            tabela.remover("x")

    def test_reutilizar_posicao_removida(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        tabela.remover("ana")
        tabela.inserir("bia", 2)
        self.assertTrue(tabela.contem("bia"))

if __name__ == "__main__":
    unittest.main()