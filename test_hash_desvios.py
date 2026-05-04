import unittest
from tabelaHash import TabelaHashSondagemLinear, REMOVIDO

class TestTabelaHashSondagemLinear(unittest.TestCase):

    def test_init_valid_invalid(self):
        tabela = TabelaHashSondagemLinear(5)
        self.assertEqual(tabela.capacidade, 5)
        
        with self.assertRaises(ValueError):
            TabelaHashSondagemLinear(0)
            

    def test_funcao_hash_tipos(self):
        tabela = TabelaHashSondagemLinear(10)

        self.assertEqual(tabela.funcao_hash(10), 0)

        self.assertEqual(tabela.funcao_hash("A"), ord("A") % 10)

        val_float = 1.5
        soma_esperada = sum(ord(c) for c in str(val_float)) % 10
        self.assertEqual(tabela.funcao_hash(val_float), soma_esperada)
        

    def test_inserir_e_buscar_sucesso(self):
        tabela = TabelaHashSondagemLinear(10)
        tabela.inserir("key1", "val1")
        self.assertEqual(tabela.buscar("key1"), "val1")
        self.assertTrue(tabela.contem("key1"))

        tabela.inserir("key1", "val2")
        self.assertEqual(tabela.buscar("key1"), "val2")
        

    def test_colisao_linear_e_tabela_cheia(self):
        tabela = TabelaHashSondagemLinear(2)
        tabela.inserir(0, "zero")
        tabela.inserir(2, "dois") 
        
        self.assertEqual(tabela.buscar(2), "dois")
        
        with self.assertRaises(OverflowError):
            tabela.inserir(4, "quatro")
            

    def test_remover_e_sondagem_com_removido(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir(0, "A")
        tabela.inserir(3, "B") 
        tabela.inserir(6, "C") 

        tabela.remover(3)
        self.assertFalse(tabela.contem(3))
        
        with self.assertRaises(KeyError):
            tabela.buscar(9)

        tabela.inserir(3, "B-novo")
        self.assertEqual(tabela.buscar(3), "B-novo")
        

    def test_buscar_remover_inexistente(self):
        tabela = TabelaHashSondagemLinear(5)

        with self.assertRaises(KeyError):
            tabela.buscar("nada")

        with self.assertRaises(KeyError):
            tabela.remover("nada")
            

    def test_metodos_de_listagem(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("a", 1)
        tabela.inserir("b", 2)
        tabela.remover("a")
        
        self.assertEqual(tabela.chaves(), ["b"])
        self.assertEqual(tabela.valores(), [2])
        self.assertEqual(tabela.itens(), [("b", 2)])
        self.assertEqual(len(tabela), 1)
        

    def test_string_representation(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir(0, "A")
        tabela.remover(0)

        res = str(tabela)
        self.assertIn("REMOVIDO", res)
        self.assertIn("VAZIO", res)
        
        tabela.inserir(1, "B")
        self.assertIn("1: 1 -> B", str(tabela))
        

    def test_procurar_posicao_casos_especificos(self):
        tabela = TabelaHashSondagemLinear(2)
        tabela.tabela = [REMOVIDO, REMOVIDO]
        tabela.quantidade = 2

        pos = tabela._procurar_posicao(10, para_insercao=True)
        self.assertIsNotNone(pos)
        
        
    def test_valores_iteracao_com_filtro_de_vazios_e_removidos(self):
        tabela_vazia_no_fim = TabelaHashSondagemLinear(2)
        tabela_vazia_no_fim.inserir("a", 10)

        self.assertEqual(tabela_vazia_no_fim.valores(), [10])

        tabela_removido_no_fim = TabelaHashSondagemLinear(2)
        tabela_removido_no_fim.inserir(0, "valor0")
        tabela_removido_no_fim.inserir(1, "valor1")
        tabela_removido_no_fim.remover(1)
        
        self.assertEqual(tabela_removido_no_fim.valores(), ["valor0"])

        tabela_valido_no_fim = TabelaHashSondagemLinear(1)
        tabela_valido_no_fim.inserir("unico", "sucesso")

        self.assertEqual(tabela_valido_no_fim.valores(), ["sucesso"])
        
        tabela_vazia = TabelaHashSondagemLinear(3)

        self.assertEqual(tabela_vazia.valores(), [])
        
    
    def test_chaves_cobertura_arestas_finais(self):
        tabela_pequena = TabelaHashSondagemLinear(1)

        self.assertEqual(tabela_pequena.chaves(), [])
        
        tabela_fim_removido = TabelaHashSondagemLinear(2)

        tabela_fim_removido.inserir("A", "valor_qualquer") 
        tabela_fim_removido.inserir("B", "outro_valor")
        tabela_fim_removido.remover("B") 

        self.assertEqual(tabela_fim_removido.chaves(), ["A"])

        tabela_fim_valido = TabelaHashSondagemLinear(1)
        tabela_fim_valido.inserir("unico", 100) 
        self.assertEqual(tabela_fim_valido.chaves(), ["unico"])
        
        
    def test_itens_iteracao_com_filtro_de_vazios_e_removidos(self):
        tabela_fim_vazio = TabelaHashSondagemLinear(2)
        tabela_fim_vazio.inserir("a", 100)

        self.assertEqual(tabela_fim_vazio.itens(), [("a", 100)])

        tabela_fim_removido = TabelaHashSondagemLinear(2)
        tabela_fim_removido.inserir(0, "val0")
        tabela_fim_removido.inserir(1, "val1")
        tabela_fim_removido.remover(1)
        
        self.assertEqual(tabela_fim_removido.itens(), [(0, "val0")])

        tabela_fim_valido = TabelaHashSondagemLinear(1)
        tabela_fim_valido.inserir("unico", "par")

        self.assertEqual(tabela_fim_valido.itens(), [("unico", "par")])

        tabela_vazia = TabelaHashSondagemLinear(3)
        
        self.assertEqual(tabela_vazia.itens(), [])
        
        
    def test_chaves_fluxo_finalizacao_loop(self):
        tabela_vazia = TabelaHashSondagemLinear(3)
        
        self.assertEqual(tabela_vazia.chaves(), [])

        tabela_ultimo = TabelaHashSondagemLinear(1) 
        tabela_ultimo.inserir("fim", 100) 

        self.assertEqual(tabela_ultimo.chaves(), ["fim"])
        
        
    def test_str_fluxo_finalizacao_arestas(self):
        tabela_vazia = TabelaHashSondagemLinear(1)
        self.assertEqual(tabela_vazia.__str__(), "0: VAZIO")

        tabela_fim_removido = TabelaHashSondagemLinear(2)
        tabela_fim_removido.inserir(0, "val0")
        tabela_fim_removido.inserir(1, "val1")
        tabela_fim_removido.remover(1)  
        resultado = tabela_fim_removido.__str__()
        
        self.assertIn("1: REMOVIDO", resultado)

        tabela_fim_valido = TabelaHashSondagemLinear(1)
        tabela_fim_valido.inserir("fim", "valor")
        
        self.assertEqual(tabela_fim_valido.__str__(), "0: fim -> valor")


    def test_str_saida_imediata_loop(self):
        tabela_vazia = TabelaHashSondagemLinear(1)
        tabela_vazia.tabela = []
        
        self.assertEqual(tabela_vazia.__str__(), "")
        
        
    def test_chaves_saida_imediata_loop(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.tabela = []

        self.assertEqual(tabela.chaves(), [])
        
        
    def test_itens_saida_imediata_loop(self):
        tabela = TabelaHashSondagemLinear(10)
        tabela.tabela = []
        
        self.assertEqual(tabela.itens(), [])
        
    
    def test_valores_saida_imediata_loop(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.tabela = []
        
        self.assertEqual(tabela.valores(), [])    
            
        
    def test_funcao_hash_saida_imediata_primeiro_for(self):
        tabela = TabelaHashSondagemLinear(10)
        chave_vazia = ""

        self.assertEqual(tabela.funcao_hash(chave_vazia), 0)
        
        
    def test_funcao_hash_saida_imediata_segundo_for(self):
        tabela = TabelaHashSondagemLinear(10)
        class ObjetoVazio:
            def __str__(self):
                return ""
                
        chave_vazia = ObjetoVazio()
        
        self.assertEqual(tabela.funcao_hash(chave_vazia), 0)
        
        
if __name__ == '__main__':
    unittest.main()