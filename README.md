# Sistema de Gerenciamento e Precificação de Produtos

## Descrição

Este projeto consiste em um sistema de gerenciamento de produtos desenvolvido em Python utilizando Oracle Database. O sistema permite realizar operações de cadastro, consulta, atualização e exclusão de produtos, além de calcular automaticamente o preço de venda com base nos custos e margem de lucro desejada.

Além disso, as descrições dos produtos são armazenadas de forma criptografada utilizando uma implementação baseada em criptografia matricial.

---

## Funcionalidades

### Cadastro de Produtos

* Inserção de novos produtos no banco de dados.
* Armazenamento das seguintes informações:

  * Código do produto
  * Nome
  * Descrição (criptografada)
  * Custo de aquisição
  * Custo fixo (%)
  * Comissão de vendas (%)
  * Impostos sobre vendas (%)
  * Margem de lucro (%)

### Cálculo de Preço de Venda

O sistema calcula:

* Preço de venda (PV)
* Receita bruta (RB)
* Custos fixos
* Comissão de vendas
* Impostos
* Outros custos
* Rentabilidade

Classificação da margem de lucro:

* Alta (> 20%)
* Média (10% a 20%)
* Baixa (0% a 10%)
* Equilíbrio (= 0%)
* Prejuízo (< 0%)

### Atualização de Produtos

Permite alterar:

* Nome
* Descrição
* Custo do produto
* Custo fixo
* Comissão de vendas
* Impostos sobre vendas
* Margem de lucro

### Exclusão de Produtos

Remoção de produtos através do código identificador.

### Visualização de Produtos

Exibe todos os produtos cadastrados com:

* Dados armazenados
* Descrição descriptografada
* Informações financeiras calculadas

### Visualização de Preços

Apresenta relatório detalhado de precificação de cada produto.

---

## Tecnologias Utilizadas

* Python 3
* Oracle Database XE
* Biblioteca oracledb

---

## Estrutura da Tabela

Tabela utilizada:

```sql
CREATE TABLE produtos_pi (
    CODIGO NUMBER PRIMARY KEY,
    NOME VARCHAR2(100),
    DESCRICAO VARCHAR2(255),
    CP NUMBER,
    CF NUMBER,
    CV NUMBER,
    IV NUMBER,
    ML NUMBER
);
```

---

## Instalação

### 1. Instalar dependências

```bash
pip install oracledb
```

### 2. Configurar conexão

No código, altere:

```python
connection = oracledb.connect(
    user="SEU_USUARIO",
    password="SUA_SENHA",
    dsn="BD-ACD/XE"
)
```

### 3. Executar o sistema

```bash
python main.py
```

---

## Menu Principal

```text
1 - Inserir produto
2 - Calcular preço de produto
3 - Modificar produto
4 - Apagar produto
5 - Visualizar produtos
6 - Visualizar preços
7 - Sair do sistema
```

---

## Segurança

As descrições dos produtos são armazenadas utilizando um algoritmo de criptografia baseado em matrizes 2x2, permitindo:

* Criptografia no momento do cadastro.
* Descriptografia durante a consulta.

---

## Autores

Projeto desenvolvido para a disciplina de Projeto Integrador, com foco em:

* Banco de Dados Oracle
* Programação em Python
* Operações CRUD
* Cálculo de precificação de produtos
* Criptografia básica de dados

## Observação Importante

Este repositório não contém a implementação completa do projeto original.

Durante o desenvolvimento, parte do controle de versões e do gerenciamento das alterações foi realizado diretamente em hardware e em ambientes locais da equipe, não sendo totalmente integrado ao sistema de versionamento do código-fonte.

Por esse motivo, algumas funcionalidades, ajustes e versões intermediárias desenvolvidas ao longo do projeto podem não estar presentes nesta versão disponibilizada no repositório.

O código disponibilizado representa a versão final funcional utilizada para demonstração das principais características do sistema, incluindo:

* Integração com Oracle Database;
* Operações de CRUD de produtos;
* Cálculo de precificação;
* Relatórios de preços;
* Criptografia e descriptografia de descrições.

Eventuais diferenças entre esta versão e a apresentada durante o desenvolvimento decorrem do processo de controle de versões adotado pela equipe durante a execução do projeto.

