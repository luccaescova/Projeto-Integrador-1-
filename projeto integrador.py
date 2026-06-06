import oracledb
from abc import ABC, abstractmethod
from typing import List, Optional

# ==========================================
# 1. CAMADA DE DOMÍNIO (Interfaces e Entidades)
# ==========================================

class ICryptography(ABC):
    @abstractmethod
    def encrypt(self, text: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, text: str) -> str:
        pass


class Product:
    """Entidade de Domínio representando o Produto e suas regras financeiras."""
    def __init__(self, codigo: int, nome: str, descricao: str, cp: float, 
                 cf: float, cv: float, iv: float, ml: float):
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.cp = cp  # Custo de Aquisição
        self.cf = cf  # Custo Fixo (%)
        self.cv = cv  # Comissão de Vendas (%)
        self.iv = iv  # Imposto sobre Vendas (%)
        self.ml = ml  # Margem de Lucro (%)

    def calculate_financials(self) -> dict:
        """Centraliza a lógica de cálculo de precificação (Clean Code: Sem duplicação)"""
        try:
            pv = self.cp / (1 - ((self.cf + self.cv + self.iv + self.ml) / 100))
        except ZeroDivisionError:
            pv = 0.0

        cf_val = (self.cf / 100) * pv
        cv_val = (self.cv / 100) * pv
        iv_val = (self.iv / 100) * pv
        oc = cf_val + cv_val + iv_val
        rb = pv - self.cp
        ra = rb - oc

        return {
            "pv": pv, "cf_val": cf_val, "cv_val": cv_val,
            "iv_val": iv_val, "oc": oc, "rb": rb, "ra": ra
        }

    def get_margin_classification(self) -> str:
        if self.ml > 20: return "Alta"
        if 10 <= self.ml <= 20: return "Média"
        if 0 < self.ml < 10: return "Baixa"
        if self.ml == 0: return "Em Equilíbrio"
        return "Prejuízo"


class IProductRepository(ABC):
    """Interface abstrata para o Banco de Dados (SOLID: DIP)"""
    @abstractmethod
    def save(self, product: Product) -> None: pass
    
    @abstractmethod
    def find_by_id(self, codigo: int) -> Optional[Product]: pass
    
    @abstractmethod
    def update_field(self, codigo: int, field: str, value: any) -> None: pass
    
    @abstractmethod
    def delete(self, codigo: int) -> None: pass
    
    @abstractmethod
    def find_all(self) -> List[Product]: pass

# ==========================================
# 2. SERVIÇOS E SEGURANÇA (Padrão GoF: Strategy)
# ==========================================

class MatrixCryptography(ICryptography):
    """Implementação da Criptografia Matricial original encapsulada."""
    def __init__(self):
        self.letras = {i: chr(64 + i) for i in range(1, 27)}
        self.letras[27] = ' '
        self.letras_inv = {v: k for k, v in self.letras.items()}

    def _transform(self, text: str, mode: int) -> str:
        text = text.upper()
        m1, m2 = [], []
        
        for n, char in enumerate(text):
            if char not in self.letras_inv:
                continue
            if n % 2 == 0: m1.append(self.letras_inv[char])
            else: m2.append(self.letras_inv[char])
            
        if len(text) % 2 != 0:
            m2.append(27)

        m3, m4 = ([4, 3], [1, 2]) if mode == 1 else ([22, -33], [-11, 44])
        encrypted = []
        
        for n in range(len(m1)):
            for key_matrix in [m3, m4]:
                x = (key_matrix[0] * m1[n]) + (key_matrix[1] * m2[n])
                x = x % 27 if (x <= 0 or x > 27) else x
                encrypted.append(x)

        result = [self.letras.get(x, ' ') for x in encrypted]
        return ''.join(result).strip()

    def encrypt(self, text: str) -> str:
        return self._transform(text, mode=1)

    def decrypt(self, text: str) -> str:
        return self._transform(text, mode=0)

# ==========================================
# 3. INFRAESTRUTURA (Banco de Dados Oracle)
# ==========================================

class OracleProductRepository(IProductRepository):
    """Implementação concreta do Repositório para Oracle DB."""
    def __init__(self, connection_string: dict):
        self.conn = oracledb.connect(**connection_string)

    def save(self, p: Product) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO produtos_pi VALUES (:1, :2, :3, :4, :5, :6, :7, :8)",
                [p.codigo, p.nome, p.descricao, p.cp, p.cf, p.cv, p.iv, p.ml]
            )
            self.conn.commit()

    def find_by_id(self, codigo: int) -> Optional[Product]:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM produtos_pi WHERE CODIGO = :1", [codigo])
            row = cursor.fetchone()
            if row:
                return Product(*row)
        return None

    def update_field(self, codigo: int, field: str, value: any) -> None:
        # Mapeamento seguro de colunas para evitar SQL Injection dinâmico estrutural
        fields_map = {1: "NOME", 2: "DESCRICAO", 3: "CP", 4: "CF", 5: "CV", 6: "IV", 7: "ML"}
        col_name = fields_map.get(int(field))
        if not col_name: return
        
        with self.conn.cursor() as cursor:
            cursor.execute(f"UPDATE produtos_pi SET {col_name} = :1 WHERE CODIGO = :2", [value, codigo])
            self.conn.commit()

    def delete(self, codigo: int) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM produtos_pi WHERE CODIGO = :1", [codigo])
            self.conn.commit()

    def find_all(self) -> List[Product]:
        products = []
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM produtos_pi")
            for row in cursor.fetchall():
                products.append(Product(*row))
        return products

# ==========================================
# 4. INTERFACE DE USUÁRIO (Console Driver)
# ==========================================

class ConsoleInterface:
    def __init__(self, repository: IProductRepository, crypto: ICryptography):
        self.repo = repository
        self.crypto = crypto

    def show_menu(self):
        while True:
            print("\n=== GERENCIAMENTO DE PRODUTOS ===")
            print("1 - Inserir produto\n2 - Calcular preço em tempo de execução\n3 - Modificar produto")
            print("4 - Apagar produto\n5 - Visualizar Produtos\n6 - Visualizar Preços\n7 - Sair do sistema")
            try:
                op = int(input("Escolha uma opção: "))
                if op == 7: break
                self._execute_option(op)
            except ValueError:
                print("Por favor, insira um número válido.")

    def _execute_option(self, op: int):
        if op == 1: self._insert_product()
        elif op == 2: self._calculate_runtime_price()
        elif op == 3: self._update_product()
        elif op == 4: self._delete_product()
        elif op == 5: self._list_products(show_details=False)
        elif op == 6: self._list_products(show_details=True)
        else: print("Opção inválida.")

    def _insert_product(self):
        print("\n-- Cadastro de Produto --")
        id_prod = int(input("ID do produto: "))
        nome = input("Nome: ")
        desc = self.crypto.encrypt(input("Descrição: "))
        cp = float(input("Custo base (CP): "))
        cf = float(input("Custo Fixo (%): "))
        cv = float(input("Comissão de Vendas (%): "))
        iv = float(input("Impostos (%): "))
        ml = float(input("Margem de Lucro desejada (%): "))
        
        product = Product(id_prod, nome, desc, cp, cf, cv, iv, ml)
        self.repo.save(product)
        print("Produto salvo com sucesso!")

    def _calculate_runtime_price(self):
        print("\n-- Simulação de Cálculo de Preço --")
        nome = input("Nome do produto: ")
        cp = float(input("Custo do produto: "))
        cf = float(input("Custo fixo (%): "))
        cv = float(input("Comissão de vendas (%): "))
        iv = float(input("Impostos (%): "))
        ml = float(input("Margem de lucro (%): "))
        
        dummy_product = Product(0, nome, "", cp, cf, cv, iv, ml)
        self._print_financial_report(dummy_product)

    def _update_product(self):
        id_update = int(input("Insira o ID do produto que deseja alterar: "))
        product = self.repo.find_by_id(id_update)
        if not product:
            print("Produto não encontrado.")
            return

        print("1-Nome | 2-Descrição | 3-CP | 4-CF | 5-CV | 6-IV | 7-ML")
        field = int(input("O que deseja alterar? "))
        novo_valor = input("Insira o novo valor: ")
        
        if field == 2:  # Re-criptografar se for alterada a descrição
            novo_valor = self.crypto.encrypt(novo_valor)
        elif field in [3, 4, 5, 6, 7]:
            novo_valor = float(novo_valor)

        self.repo.update_field(id_update, field, novo_valor)
        print("Produto atualizado!")

    def _delete_product(self):
        id_del = int(input("Insira o ID do produto que deseja apagar: "))
        self.repo.delete(id_del)
        print("Operação concluída.")

    def _list_products(self, show_details: bool):
        products = self.repo.find_all()
        for p in products:
            p.descricao = self.crypto.decrypt(p.descricao) # Descriptografa ao exibir
            if show_details:
                self._print_financial_report(p)
            else:
                print(f"ID: {p.codigo} | Nome: {p.nome} | Desc: {p.descricao} | CP: {p.cp:.2f} | ML: {p.ml}%")

    def _print_financial_report(self, p: Product):
        f = p.calculate_financials()
        print(f"\nRelatório do Produto: {p.nome} (Margem: {p.get_margin_classification()})")
        print(f"Preço de Venda:      R$ {f['pv']:.2f}")
        print(f"Custo de Aquisição:  R$ {p.cp:.2f} ({(p.cp/f['pv']*100 if f['pv']>0 else 0):.1f}%)")
        print(f"Receita Bruta:       R$ {f['rb']:.2f}")
        print(f"Custos Fixos:        R$ {f['cf_val']:.2f}")
        print(f"Rentabilidade:       R$ {f['ra']:.2f}")


# ==========================================
# 5. EXECUÇÃO PRINCIPAL (Configuração / Injeção)
# ==========================================

if __name__ == "__main__":
    db_config = {
        "user": "seu_usuario",
        "password": "sua_senha",
        "dsn": "BD-ACD/XE"
    }
    
    try:
        # Injeção de Dependências pura
        crypto_service = MatrixCryptography()
        product_repository = OracleProductRepository(db_config)
        
        app = ConsoleInterface(product_repository, crypto_service)
        app.show_menu()
        
    except Exception as e:
        print(f"Erro crítico na execução do sistema: {e}")