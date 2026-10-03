# ⛪ ICMAV — Portal Web Oficial & Backoffice da ICMAV - Igreja Cristã Manancial de Águas Vivas

[![Vue 3](https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=flat&logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

Portal oficial da **Igreja Cristã Manancial de Águas Vivas — ICMAV**. O projeto combina uma experiência moderna, responsiva e acessível para membros e visitantes com um painel de administração (**Backoffice**) e integração de pagamentos e donativos digitais (**MB WAY via IFTHENPAY** e **Transferência Bancária**).

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

# Criar credenciais locais privadas (recusa substituir ficheiros existentes)
python scripts/init_secrets.py

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

Por padrão, o frontend usa `/api` na mesma origem do website. Em desenvolvimento,
o Vite encaminha `/api` e `/uploads` para `http://127.0.0.1:8000`.
Para usar uma API noutro domínio, define `VITE_API_BASE_URL` antes do build.

Para validar o encaminhamento da API e gerar o frontend de produção:
```bash
cd frontend
npm test
npm run build
```

---

## 🔒 Variáveis de Ambiente

Podes configurar variáveis de ambiente no teu ficheiro `.env` ou nas configurações do Cloud Run:

| Variável | Descrição | Padrão / Exemplo |
| :--- | :--- | :--- |
| `PORT` | Porta onde o Uvicorn escuta (injetado pelo Cloud Run) | `8080` / `8000` |
| `JWT_SECRET` | Segredo aleatório obrigatório para assinatura JWT | Gerado localmente, nunca partilhado |
| `ADMIN_USERNAME` | Utilizador administrativo obrigatório | `admin` |
| `ADMIN_PASSWORD_HASH` | Hash bcrypt obrigatório da password privada | Gerado localmente |
| `SETTINGS_ENCRYPTION_KEY` | Chave Fernet para cifrar credenciais de pagamento | Guardar em backup privado |
| `ICMAV_DATA_DIR` | Diretório privado e persistente da base de dados e uploads | Fora de `public_html` |
| `JWT_EXPIRE_MINUTES` | Duração dos tokens de autenticação em minutos | `120` |

O comando `python scripts/init_secrets.py` cria `backend/.env` e
`.local-state/admin-login.txt` com permissões privadas, sem imprimir segredos.
Os ficheiros estão excluídos do Git. A aplicação recusa arrancar com credenciais
em falta ou com os antigos valores de exemplo.

As credenciais IFTHENPAY configuradas no Backoffice são cifradas na base de dados.
Ao arrancar, os campos antigos em texto simples são cifrados numa transação;
se a chave faltar ou não corresponder, o arranque falha sem apagar os dados.
Guarda uma cópia privada de `SETTINGS_ENCRYPTION_KEY`: a sua perda impede recuperar
as credenciais cifradas. Backups antigos também devem permanecer privados.

Para executar os testes de segurança a partir da raiz:
```bash
PYTHONPATH=backend backend/.venv/bin/python -m unittest discover -s backend/tests -v
```

O diretório configurado por `ICMAV_DATA_DIR` deve ser persistente. Ao mudar de
caminho, copia primeiro a base de dados existente e os uploads. Um caminho novo
não migra os dados automaticamente. O sistema de ficheiros efémero do Cloud Run
não serve para preservar estes dados.

Os pedidos MB WAY exigem um cabeçalho `Idempotency-Key` UUID v4. A aplicação
reserva cada tentativa na base de dados antes de contactar o fornecedor. Repetir
a mesma tentativa não volta a iniciar o pagamento; dados diferentes com a mesma
chave são rejeitados. O navegador conserva a chave durante a sessão e recupera o
estado após recarregar. Um erro de transporte não significa que não houve débito:
confirma primeiro na app MB WAY e com a tesouraria. Só uma resposta explícita
`X-Payment-Attempt-State: not-sent` permite corrigir/repetir, sempre com a mesma
chave e respeitando `Retry-After`. Não apagues o registo de tentativas para resolver
erros. Este registo requer SQLite persistente; não uses réplicas com discos separados.

Existem limites de iniciação por telefone, IP e globais, e de consulta de estado.
Guarda uma cópia consistente da base de dados e da chave de cifragem antes de
migrações. Os formulários de ajuda/grupos ainda não enviam pedidos para um backend;
a emissão automática de recibos também não está implementada.

A auditoria npm ainda identifica um aviso upstream de baixa gravidade no Quill
2.0.3, sem versão corrigida publicada. Os formatos vulneráveis de vídeo/fórmula
estão desativados e todo o HTML do editor e dos componentes é sanitizado; os testes
cobrem estes limites. Reavaliar a dependência quando existir uma correção oficial.

---

## 🐳 Execução com Docker

Para testar a imagem de produção localmente ou criar a imagem para deployment:

```bash
# Construir a imagem Docker
docker build -t icmav-site:latest .

# Executar o contentor
docker run -p 8080:8080 --env-file backend/.env -e PORT=8080 \
  -e ICMAV_DATA_DIR=/data -v icmav-data:/data icmav-site:latest
```
Acede a `http://localhost:8080` no teu navegador. O volume local `icmav-data`
preserva os dados entre contentores; faz backups privados desse volume e da chave
de cifragem. Os ficheiros `.env`, backups, bases de dados e uploads são excluídos
da imagem.

O script FTP local publica apenas conteúdo estático. O plano WebHS HS S verificado
não tem Python, Passenger nem SSH ativos. O backend exige ativação adequada pela
WebHS ou outro alojamento; copiar ficheiros Python para `public_html` não o executa.
O script mantém as credenciais no `.env` privado original, verifica o certificado
FTPS, faz backup antes de escrever e publica os recursos antes de `index.html`.
Não elimina ficheiros remotos. `--project CAMINHO --dry-run` seleciona um projeto
estático e valida sem publicar; projetos com backend são bloqueados antes do build
ou da ligação à rede. O script e as credenciais não devem ser versionados.

---

## 📄 Licença e Direitos

Projeto desenvolvido para a **ICMAV - Igreja Cristã Manancial de Águas Vivas**. Todos os direitos reservados.
