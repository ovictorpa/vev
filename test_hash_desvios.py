import unittest
import sys
import os

sys.path.insert(0, os.getcwd())

from tabelaHash import TabelaHashSondagemLinear

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

    def test_init_arestas(self):
        with self.assertRaises(ValueError):
            TabelaHashSondagemLinear(0)
        th = TabelaHashSondagemLinear(11)
        self.assertEqual(th.capacidade, 11)

    def test_funcao_hash_tipos(self):
        th = TabelaHashSondagemLinear(10)
        self.assertEqual(th.funcao_hash(15), 5)
        self.assertEqual(th.funcao_hash("a"), ord("a") % 10)
        self.assertEqual(th.funcao_hash(1.5), sum(ord(c) for c in str(1.5)) % 10)

    def test_inserir_e_overflow(self):
        th = TabelaHashSondagemLinear(1)
        th.inserir("A", 1) 
        with self.assertRaises(OverflowError):
            th.inserir("B", 2)
        th.inserir("A", 10)
        self.assertEqual(th.buscar("A"), 10)

    def test_buscar_e_remover_inexistente(self):
        th = TabelaHashSondagemLinear(5)
        with self.assertRaises(KeyError):
            th.buscar("chave_que_nao_existe")
        with self.assertRaises(KeyError):
            th.remover("chave_que_nao_existe")

    def test_procurar_posicao_casos(self):
        th = TabelaHashSondagemLinear(3)
        th.inserir("A", 1) 
        th.remover("A")   
        th.inserir("B", 2) 
        
        self.assertFalse(th.contem("C"))

    def test_metodos_iteradores(self):
        th = TabelaHashSondagemLinear(3)
        th.inserir("A", 1)
        th.inserir("B", 2)
        th.remover("A")
        self.assertEqual(th.chaves(), ["B"])
        self.assertEqual(th.valores(), [2])
        self.assertEqual(len(th.itens()), 1)

    def test_str_completo(self):
        th = TabelaHashSondagemLinear(3)
        th.inserir("A", 1)
        th.remover("A")
        th.inserir("B", 2)
        res = str(th)
        self.assertIn("VAZIO", res)
        self.assertIn("REMOVIDO", res)
        self.assertIn("B -> 2", res)

if __name__ == "__main__":
    unittest.main()