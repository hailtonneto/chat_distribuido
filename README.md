# 💬 Sistema de Chat Distribuído — Cliente-Servidor com Threads e Processos

Este projeto implementa um sistema de chat distribuído utilizando a arquitetura cliente-servidor. A solução aplica conceitos de concorrência e paralelismo com uso de threads e processos, permitindo comunicação simultânea entre múltiplos clientes.

---

## 📌 Funcionalidades

- Arquitetura distribuída baseada em cliente-servidor
- Comunicação via protocolo TCP com mensagens em JSON
- Suporte a múltiplos clientes simultâneos com `threading`
- Simulação de paralelismo com `multiprocessing` para testes de carga
- Autenticação simples para administrador com senha
- Comando `/encerrar` para desligar o servidor remotamente
- Comando `/limparlog` para apagar o conteúdo do log do servidor
- Logs de eventos e mensagens no servidor
- Controle de conexões e sincronização com `Lock`

---

## 🧱 Estrutura do Projeto

```
chat_distribuido/
├── server.py           # Servidor com threads e controle de clientes
├── client.py           # Cliente com envio/recebimento de mensagens
├── config.py           # Configurações de rede e autenticação
├── utils.py            # Funções auxiliares (formatação, validação)
├── tests/
│   └── stress_test.py  # Simulação de múltiplos clientes com multiprocessing
├── logs/
│   └── server.log      # Arquivo de log do servidor
└── README.md           # Documentação do projeto
```

---

## 🚀 Como Executar

### 1. Iniciar o servidor

```bash
python server.py
```

### 2. Iniciar um cliente

```bash
python client.py
```

Digite seu nome de usuário e, se for `admin`, insira a senha definida em `config.py`.

### 3. Teste de carga (opcional)

```bash
python tests/stress_test.py
```

---

## 🔐 Comando Especiais (somente para administrador)

- `/encerrar` → Encerra o servidor e desconecta todos os clientes
- `/limparlog` → Apaga o conteúdo do arquivo server.log

---

## 🧠 Conceitos Aplicados

- **Concorrência:** Threads para múltiplos clientes simultâneos
- **Paralelismo:** Processos para simular múltiplos clientes
- **Sincronização:** `threading.Lock()` para proteger recursos compartilhados
- **Comunicação:** Sockets TCP e mensagens em formato JSON
- **Segurança:** Autenticação simples com verificação de senha para comandos críticos

---

## 🛠 Requisitos

- Python 3.8+
- Bibliotecas padrão: `socket`, `threading`, `multiprocessing`, `json`, `logging`

---

## 📄 Licença

Este projeto é acadêmico e livre para uso educacional.

---

