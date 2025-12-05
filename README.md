# Projeto de RPA - Cadastro de Clientes SSotica

Este projeto automatiza o cadastro de clientes na plataforma SSotica utilizando Python e Playwright.

## Funcionalidades

- **Login Automático**: Acessa a plataforma com credenciais seguras.
- **Navegação Inteligente**: Vai até a secção de clientes e inicia um novo cadastro.
- **Dados Dinâmicos**: Gera nomes e telefones aleatórios (ex: "Teste Cliente Mock 03").
- **Resiliência**:
    - Trata popups (OneSignal) automaticamente.
    - Verifica e remove campos de telefone duplicados.
    - Usa esperas inteligentes e timeouts configurados para redes lentas.
- **Observações Detalhadas**: Preenche o campo de observações com dados de receita e intenção.
- **Execução Headless**: Roda em segundo plano por padrão.

## Pré-requisitos

- Python 3.10+
- Conta na plataforma SSotica
- `pip` instalado

## Instalação

1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

## Configuração

1. Crie um arquivo `.env` na raiz do projeto (use `.env.example` como base):
   ```
   EMAIL=seu_email@exemplo.com
   PASSWORD=sua_senha
   ```

## Execução

### Modo Padrão (Headless)
O robô roda sem abrir a janela do navegador:
```bash
python src/task.py
```

### Modo Visual (Headed)
Para ver o navegador rodando (útil para debug):
```bash
python src/task.py --headed
```

### Manter Navegador Aberto
Para inspecionar o resultado final sem fechar o navegador:
```bash
python src/task.py --headed --keep-open
```

## Estrutura com Robocorp / RCC

Se estiver usando Robocorp/RCC, o ambiente já está configurado em:
- `src/conda.yaml`: Definição de dependências.
- `src/robot.yaml`: Definição da tarefa.

Para rodar via RCC:
```bash
rcc run
```

## Estrutura do Projeto

- `src/task.py`: Ponto de entrada (Login, Loop principal).
- `src/auth.py`: Lógica de login.
- `src/nav.py`: Navegação pelo menu.
- `src/client.py`: O preenchimento do formulário de cliente (Lógica pesada aqui).
- `src/utils.py`: Tratamento de popups e handlers globais.
- `src/logger.py`: Configuração de logs.
