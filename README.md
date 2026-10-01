# ⛪ ICM Algés & VFX — Portal Web Oficial & Backoffice

[![Vue 3](https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=flat&logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

Portal oficial da **Igreja Cristã Maranata — Algés e Vila Franca de Xira**. O projeto combina uma experiência moderna, responsiva e acessível para membros e visitantes com um painel de administração (**Backoffice**) e integração de pagamentos e donativos digitais (**MB WAY via IFTHENPAY** e **Transferência Bancária**).

---

## 🚀 Funcionalidades Principais

### 🌐 Área Pública (Website)
- **Design Moderno e Responsivo:** Desenvolvido com Vue 3, Tailwind CSS e DaisyUI, adaptado a smartphones, tablets e desktop.
- **Informações Institucionais:** Horários de cultos, moradas e mapas interativos das congregações de Algés e Vila Franca de Xira.
- **Módulo de Donativos:**
  - **MB WAY:** Pagamento instantâneo e seguro integrado com a gateway **IFTHENPAY**, com polling em tempo real do estado da transação e ecrãs de feedback.
  - **Transferência Bancária:** Exibição clara de IBAN e dados bancários, com formulário de recolha de dados para recibo fiscal (NIF, Nome, Morada).
- **Eventos e Transmissões:** Agenda de reuniões e ligação direta às transmissões e redes sociais.
- **Conformidade Legal & RGPD:**
  - Banner interativo de consentimento de cookies.
  - Páginas dedicadas de Termos de Utilização, Política de Privacidade e Política de Cookies.

### 🔐 Backoffice (Painel de Administração)
- **Autenticação Segura:** Sessões com tokens **JWT** (JSON Web Tokens), passwords cifradas com **bcrypt** e rate-limiting contra ataques de força bruta.
- **Gestão de Conteúdos:** Edição de textos, contactos, moradas e horários com reflexo imediato no site.
- **Configuração de Pagamentos:** Gestão das chaves de API e credenciais da IFTHENPAY (MB WAY).
- **Gestão de Cores e Temas:** Personalização dinâmica das cores de destaque do portal.

---

## 🛠️ Stack Tecnológica

### Frontend
- **Framework:** [Vue 3](https://vuejs.org/) (Composition API / `<script setup>`)
- **Build Tool:** [Vite](https://vitejs.dev/)
- **Estilos & UI:** [Tailwind CSS v4](https://tailwindcss.com/), [DaisyUI](https://daisyui.com/), [AOS](https://michalsnik.github.io/aos/) (animações ao rolar)
- **Ícones & Componentes:** [FontAwesome Free](https://fontawesome.com/), [Quill](https://quilljs.com/) (editor rich text), [vue-tel-input](https://github.com/iamstevendao/vue-tel-input)
- **Roteamento:** [Vue Router](https://router.vuejs.org/)

### Backend
- **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
- **Base de Dados & ORM:** [SQLModel](https://sqlmodel.tiangolo.com/) / [SQLAlchemy](https://www.sqlalchemy.org/) com [SQLite](https://sqlite.org/)
- **Segurança:** [PyJWT](https://pyjwt.readthedocs.io/), [bcrypt](https://pypi.org/project/bcrypt/)
- **Cliente HTTP Assíncrono:** [httpx](https://www.python-httpx.org/) (comunicação com a API IFTHENPAY)
- **Servidor ASGI:** [Uvicorn](https://www.uvicorn.org/)

### Deployment & Infraestrutura
- **Contentorização:** Docker (Multi-stage build)
- **Cloud:** Google Cloud Run / Google Cloud Build

---

## 📂 Estrutura do Projeto

```text
.
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth.py          # Endpoints de login e verificação JWT
│   │   │   ├── donations.py     # Endpoints de donativos e integração IFTHENPAY
│   │   │   └── settings.py      # Gestão de definições e conteúdos
│   │   ├── auth.py              # Lógica de segurança, hash e verificação de tokens
│   │   ├── colormanagement.py   # Gestão dinâmica de temas/cores
│   │   ├── crud.py              # Operações de base de dados
│   │   ├── database.py          # Configuração SQLite/SQLModel
│   │   ├── defaults.py          # Definições iniciais de conteúdos
│   │   ├── main.py              # Ponto de entrada FastAPI e montagem do frontend SPA
│   │   ├── models.py            # Modelos SQLModel
│   │   ├── schemas.py           # Esquemas Pydantic
│   │   └── validators.py        # Validação de payloads e configurações
│   └── requirements.txt         # Dependências Python
├── frontend/
│   ├── public/                  # Imagens, vídeos, logótipos e assets estáticos
│   ├── src/
│   │   ├── assets/              # Estilos globais
│   │   ├── components/          # Componentes reutilizáveis (Donations, Banner, Modais, etc.)
│   │   ├── router/              # Rotas da SPA (Home, Backoffice, Legal, etc.)
│   │   ├── services/            # Clientes de API (Auth, Settings, Donations)
│   │   ├── views/               # Vistas principais (Home, Admin, Privacy, Terms, Cookies)
│   │   ├── App.vue              # Componente raiz
│   │   └── main.js              # Ponto de entrada do Vue
│   ├── package.json
│   └── vite.config.js
├── Dockerfile                   # Dockerfile multi-stage pronto para Cloud Run
├── start-dev.ps1                # Script PowerShell para arranque local em simultâneo
└── README.md
```

---

## ⚙️ Instalação e Execução Local

### Pré-requisitos
- [Node.js](https://nodejs.org/) (versão 20 ou superior)
- [Python](https://www.python.org/) (versão 3.12 ou superior)
- [Git](https://git-scm.com/)

---

### Opção 1: Arranque Rápido no Windows (PowerShell)
Executa o script fornecido na raiz do projeto para arrancar o backend e o frontend em terminais separados:
```powershell
.\start-dev.ps1
```

---

### Opção 2: Arranque Manual

#### 1. Configurar e Iniciar o Backend
```bash
# Entrar na pasta do backend
cd backend

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows PowerShell)
.venv\Scripts\Activate.ps1
# No Linux/macOS: source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
O backend ficará acessível em: `http://localhost:8000` (Documentação Swagger: `http://localhost:8000/docs`).

#### 2. Configurar e Iniciar o Frontend
Em outro terminal:
```bash
# Entrar na pasta do frontend
cd frontend

# Instalar dependências
npm install

# Iniciar servidor Vite de desenvolvimento
npm run dev
```
O frontend ficará acessível em: `http://localhost:5173`.

---

## 🔒 Variáveis de Ambiente

Podes configurar variáveis de ambiente no teu ficheiro `.env` ou nas configurações do Cloud Run:

| Variável | Descrição | Padrão / Exemplo |
| :--- | :--- | :--- |
| `PORT` | Porta onde o Uvicorn escuta (injetado pelo Cloud Run) | `8080` / `8000` |
| `JWT_SECRET` | Chave secreta para assinatura dos tokens JWT | `icmav_jwt_secret_...` |
| `JWT_EXPIRE_MINUTES` | Duração dos tokens de autenticação em minutos | `120` |
| `ADMIN_USERNAME` | Nome de utilizador do Administrador | `SA` |
| `ADMIN_PASSWORD_HASH` | Hash bcrypt da password do Administrador | *(Hash por omissão no código)* |

*(As credenciais da Gateway IFTHENPAY podem ser configuradas diretamente através do Painel de Administração / Backoffice).*

---

## 🐳 Execução com Docker

Para testar a imagem de produção localmente ou criar a imagem para deployment:

```bash
# Construir a imagem Docker
docker build -t icmav-site:latest .

# Executar o contentor
docker run -p 8080:8080 -e PORT=8080 icmav-site:latest
```
Acede a `http://localhost:8080` no teu navegador.

---

## 📄 Licença e Direitos

Projeto desenvolvido para a **Igreja Cristã Maranata — Algés e VFX**. Todos os direitos reservados.
