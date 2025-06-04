# zbx-server-provisioning

> Script de provisionamento automatizado para o Zabbix Server 7 no Ubuntu Server 24.04 com Apache2 e MySQL.

## 📋 Descrição

Este script automatiza a instalação e configuração do **Zabbix Server 7.0 LTS** utilizando **Apache2** como servidor web e **MySQL** como banco de dados no **Ubuntu Server 24.04**. Ele é útil para ambientes de testes, laboratórios ou configurações locais rápidas.

## ⚙️ Requisitos

- Python 3.x
- Sistema: Ubuntu Server 24.04
- Permissões de superusuário (root)

## 📦 Dependências

O script utiliza o módulo `subprocess` para executar comandos do sistema. Nenhuma biblioteca externa é necessária.

## 🚀 Como Usar

### 1. Clone o repositório:

```bash
git clone https://github.com/VJorgeNeto/zbx-server-provisioning.git
cd zbx-server-provisioning
```
### 2. Dê permissão de execução e execute:

```bash
python3 zabbix-server.py
```
🧪 O que o script faz?
Instala dependências do Zabbix

Instala e configura o MySQL Server

Instala e configura o Apache2

Baixa o pacote oficial do Zabbix

Realiza a configuração inicial do Zabbix Server

Habilita os serviços para inicialização automática

📁 Estrutura
```bash
.
├── zabbix-server.py
└── README.md
```

📄 Licença
Distribuído sob a licença MIT.
Desenvolvido por @VJorgeNeto 🚀
