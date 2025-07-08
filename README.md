# 🕰️ ChronusPlanner

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Made with Flask](https://img.shields.io/badge/made%20with-Flask-blue)

> **ChronusPlanner** é uma aplicação web desenvolvida com Flask para gerenciamento de compromissos, ideal para agendas pessoais ou equipes organizadas.  
> Organize, edite e visualize seus eventos com uma interface simples, moderna e pronta para expansão com recursos como notificações e login.

---

## ✨ Funcionalidades

- 📅 Cadastro de compromissos com data, hora e descrição
- 🖊️ Edição e exclusão de eventos existentes
- 🔍 Visualização de eventos organizados por data
- 💡 Estrutura modular (routes, models, forms)
- 🧱 Pronto para escalabilidade (autenticação, FullCalendar, etc.)

---

## 🛠️ Tecnologias Utilizadas

| Ferramenta | Descrição |
|-----------|------------|
| 🐍 Python | Linguagem principal |
| 🌶️ Flask | Framework web |
| 🐘 SQLAlchemy | ORM para banco de dados |
| 💻 HTML + CSS | Estrutura e estilo das páginas |
| 🧪 Flask-WTF | Validação de formulários |

---

## 🗂️ Estrutura de Pastas

ChronusPlanner/
├── app/
│ ├── init.py
│ ├── models/
│ ├── routes/
│ ├── forms/
│ ├── templates/
│ ├── static/
├── run.py
├── config.py
├── requirements.txt
└── README.md


---

## ⚙️ Como Rodar o Projeto

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ChronusPlanner.git

# Acesse o diretório
cd ChronusPlanner

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute o projeto
python run.py
