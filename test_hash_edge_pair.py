import unittest
import sys
import os

sys.path.insert(0, os.getcwd())

from tabelaHash import TabelaHashSondagemLinear

class TestHashMCDC(unittest.TestCase):

    def test_inserir_posicao_vazia(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        self.assertEqual(tabela.buscar("ana"), 1)

    def test_inserir_posicao_removida(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        tabela.remover("ana")
        tabela.inserir("bia", 2)
        self.assertEqual(tabela.buscar("bia"), 2)

    def test_atualizar_posicao_ocupada(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        tabela.inserir("ana", 5)
        self.assertEqual(tabela.buscar("ana"), 5)

    def test_chaves_sem_removidos(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("a", 1)
        self.assertEqual(tabela.chaves(), ["a"])

    def test_chaves_com_removidos(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("a", 1)
        tabela.remover("a")
        self.assertEqual(tabela.chaves(), [])

    def test_contem_false(self):
        tabela = TabelaHashSondagemLinear(5)
        self.assertFalse(tabela.contem("x"))
        
    def test_edge_pair_sondagem_sucesso(self):
        self.th = TabelaHashSondagemLinear(capacidade=3)
        self.th.inserir(0, "A")
        self.th.inserir(3, "B")

        self.assertEqual(self.th.buscar(3), "B") [cite: 34]

    def test_edge_pair_circularidade(self):
        self.th = TabelaHashSondagemLinear(capacidade=3)
        self.th.inserir(2, "Fim")
        
        self.th.inserir(5, "Volta") 
        self.assertTrue(self.th.contem(5)) [cite: 34]

    def test_edge_pair_remocao_para_none(self):
        self.th = TabelaHashSondagemLinear(capacidade=3)
        self.th.inserir(0, "A")
        self.th.remover(0) 
        with self.assertRaises(KeyError):
            self.th.buscar(3) 

    def test_edge_pair_tabela_cheia_saida(self):
        self.th = TabelaHashSondagemLinear(capacidade=3)
        self.th.inserir(0, "V0")
        self.th.inserir(1, "V1")
        self.th.inserir(2, "V2")
        
        with self.assertRaises(KeyError):
            self.th.buscar(10)

if __name__ == "__main__":
    unittest.main()