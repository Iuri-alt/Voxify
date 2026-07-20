# Voxify

Voxify é uma plataforma SaaS que utiliza o Azure-Speech para transformar arquivos de áudio em texto de forma rápida, segura e intuitiva, oferecendo uma experiência moderna para a transcrição.

# 🛠️ Tecnologias Utilizadas

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)

![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=for-the-badge&logo=fastapi)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql)

![Supabase](https://img.shields.io/badge/Supabase-Cloud-3ECF8E?style=for-the-badge&logo=supabase)

![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript)

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)

![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

![JWT](https://img.shields.io/badge/JWT-Authentication-orange?style=for-the-badge)

</p>

# ✨ Principais Funcionalidades

## 👤 Usuários
- Cadastro de usuários
- Login
- Autenticação utilizando JWT
- Sessões protegidas
- Controle de acesso
---
## 🎙️ Transcrição de Áudios
- Upload de arquivos de áudio
- Integração com a Azure-speech
- Conversão de áudio para texto
- Armazenamento das transcrições
- Histórico individual por usuário
---
## ☁️ Banco de Dados
- Persistência das informações
- Armazenamento em nuvem utilizando Supabase
- PostgreSQL
---
## 🎨 Interface
- Landing Page moderna
- Dashboard do usuário
- Sistema de Login
- Sistema de Cadastro
- Layout totalmente responsivo
- Interface intuitiva e amigável

# 🏗️ Arquitetura do Sistema

O Voxify foi desenvolvido seguindo uma arquitetura desacoplada (Frontend + Backend), separando completamente a interface do usuário da lógica de negócio. Essa abordagem facilita a manutenção, escalabilidade e futuras integrações com aplicações mobile ou outros clientes.

```text
                Frontend

       HTML + CSS + JavaScript
                 │
                 │
        Requisições HTTP (Fetch API)
                 │
                 ▼
             FastAPI (Python)
                 │
      ┌──────────┴──────────┐
      │                     │
   Routers              Services
      │                     │
      │             OpenAI Service
      │                     │
      └──────────┬──────────┘
                 │
          PostgreSQL (Supabase)
```
---
# 🔄 Fluxo da Aplicação

O fluxo completo do sistema acontece conforme ilustrado abaixo.
```text
Usuário
↓
Landing Page
↓
Cadastro/Login
↓
JWT Authentication
↓
Dashboard
↓
Upload de Áudio
↓
FastAPI
↓
Validação do Arquivo
↓
OpenAI API
↓
Transcrição
↓
PostgreSQL (Supabase)
↓
Resposta da API
↓
Dashboard
↓
Visualização da Transcrição
```
---
# 📂 Estrutura do Projeto

A organização do projeto foi dividida entre Frontend e Backend, permitindo maior desacoplamento entre interface e API.
```text
voxify/

├── .github/
│
├── Back/
│   ├── .idea/
│   ├── .venv/
│   ├── alembic/
│   ├── app/
│   ├── routers/
│   ├── services/
│   ├── uploads/
│   ├── .env
│   ├── .env.example
│   ├── alembic.ini
│   └── requirements.txt
│
├── Front/
│   ├── assets/
│   ├── script/
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── config.js
│   │   ├── dashboard.js
│   │   ├── login.js
│   │   ├── register.js
│   │   ├── registro.js
│   │   └── upload.js
│   │
│   ├── style/
│   │
│   ├── Dashboard.html
│   ├── index.html
│   ├── login.html
│   └── registro.html
│
├── .gitignore
└── README.md
```
---
# ⚙️ Organização do Backend

O Backend foi desenvolvido utilizando FastAPI seguindo uma arquitetura em camadas.

| Pasta   | Responsabilidade |
|---------|------------------|
| app     | Inicialização da aplicação |
| routers | Endpoints da API |
| services| Regras de negócio |
| uploads | Armazenamento temporário dos arquivos |
| alembic | Controle de migrações |
| .env    | Variáveis de ambiente |
| requirements.txt | Dependências do projeto |
---
# 🎨 Organização do Frontend
O Frontend foi desenvolvido utilizando HTML, CSS e JavaScript puro.
Sua estrutura foi organizada para manter uma clara separação entre interface, estilos e scripts.

| Pasta | Responsabilidade |
|--------|------------------|
| assets | Logos, imagens e ícones |
| script | Comunicação com a API e lógica da interface |
| style | Arquivos CSS |
| *.html | Páginas da aplicação |
---
# 🗄️ Banco de Dados
O projeto utiliza PostgreSQL hospedado no Supabase para armazenar todas as informações da aplicação.
Atualmente o banco é responsável por armazenar:
- Usuários
- Credenciais de acesso
- Histórico de transcrições
- Informações dos arquivos enviados
---
## Modelo Conceitual
```text
Usuário
───────────────
id
nome
email
senha

        │ 1
        │
        │
        │ N

Transcrição
────────────────────────
id
nome_arquivo
texto
data_upload
usuario_id
```
---
# ☁️ Infraestrutura
O Voxify utiliza serviços em nuvem para garantir maior disponibilidade e escalabilidade.
### Backend
- FastAPI
- Python
### Banco de Dados
- PostgreSQL
- Supabase Cloud
### Trascrição
- Azure-speech
### Frontend
- HTML5
- CSS3
- JavaScript
