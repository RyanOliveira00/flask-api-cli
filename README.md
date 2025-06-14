# ☕ Coffee Shop - Sistema Completo

Um sistema completo de cafeteria composto por uma API RESTful em Flask e um aplicativo mobile em React Native.

## 🏗️ Arquitetura do Projeto

Este repositório contém dois projetos principais:

- **`CoffeeShopApi/`** - API REST em Flask com autenticação JWT
- **`CoffeeShopApp/`** - Aplicativo mobile em React Native Expo

## 🚀 Funcionalidades Principais

### 🔐 Autenticação
- Sistema de login/registro com JWT
- Controle de acesso por roles (usuário/admin)
- Tokens seguros com expiração

### ☕ Gestão de Cafés
- CRUD completo de produtos
- Controle de estoque
- Preços e descrições detalhadas

### 🛒 Sistema de Compras
- Carrinho de compras
- Histórico de transações
- Controle de estoque automático

### 📱 Interface Mobile
- App nativo para iOS e Android
- Interface moderna e intuitiva
- Sincronização em tempo real com a API

## 📖 Documentação da API

### 🌐 Documentação Online (Swagger)
Acesse a documentação interativa da API:
**[https://flask-api-cli.onrender.com/docs/](https://flask-api-cli.onrender.com/docs/)**

### 🔧 Documentação Local
Quando rodando localmente, acesse: `http://localhost:5001/docs/`

## 🚀 Quick Start

### 1. Clone o Repositório
```bash
x
```

### 2. Configure a API (Flask)
```bash
cd CoffeeShopApi

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
# Crie um arquivo .env com:
# DATABASE_URL=sqlite:///coffee_shop.db
# JWT_SECRET_KEY=your-secret-key

# Execute a API
python app.py
```

A API estará disponível em `http://localhost:5001`

### 3. Configure o App Mobile (React Native)
```bash
cd ../CoffeeShopApp

# Instale as dependências
npm install

# Configure a URL da API em src/utils/config.ts
# BASE_URL: 'http://localhost:5001'

# Execute o app
npx expo start
```

## 📁 Estrutura do Projeto

```
casseb/
├── CoffeeShopApi/          # API Flask
│   ├── app.py             # Aplicação principal
│   ├── models.py          # Modelos do banco de dados
│   ├── routes.py          # Rotas da API
│   ├── routes_swagger.py  # Rotas com documentação Swagger
│   ├── requirements.txt   # Dependências Python
│   └── tests/             # Testes unitários
│
├── CoffeeShopApp/          # App React Native
│   ├── src/
│   │   ├── components/    # Componentes reutilizáveis
│   │   ├── screens/       # Telas do aplicativo
│   │   ├── services/      # Serviços de API
│   │   └── contexts/      # Contextos (Auth)
│   ├── App.tsx           # Componente principal
│   └── package.json      # Dependências Node.js
│
└── README.md             # Este arquivo
```

## 🔧 Tecnologias Utilizadas

### Backend (API)
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **JWT** - Autenticação stateless
- **Swagger/OpenAPI** - Documentação interativa
- **pytest** - Testes unitários

### Frontend (Mobile)
- **React Native** - Framework mobile multiplataforma
- **Expo** - Plataforma de desenvolvimento
- **TypeScript** - Tipagem estática
- **React Navigation** - Navegação entre telas
- **Axios** - Cliente HTTP

## 🔗 Endpoints Principais da API

### Autenticação
- `POST /auth/register` - Registro de usuário
- `POST /auth/login` - Login e obtenção do token JWT

### Cafés
- `GET /coffee` - Listar todos os cafés
- `POST /coffee` - Adicionar café (admin apenas)
- `GET /coffee/<id>` - Detalhes do café
- `PUT /coffee/<id>` - Atualizar café (admin apenas)
- `DELETE /coffee/<id>` - Excluir café (admin apenas)

### Compras
- `POST /purchase` - Realizar compra
- `GET /purchase` - Histórico de compras

## 🧪 Executando Testes

### Testes da API
```bash
cd CoffeeShopApi
pytest -s tests/ -v
```

## 🚀 Deploy

### API
A API está deployada no Render:
- **URL de Produção**: `https://flask-api-cli.onrender.com`
- **Documentação**: `https://flask-api-cli.onrender.com/docs/`

### App Mobile
Para build de produção:
```bash
cd CoffeeShopApp

# Android
npx expo build:android

# iOS
npx expo build:ios
```

## 👥 Credenciais de Teste

Para testar o sistema, use:
- **Admin**: `admin` / `admin123`
- Ou crie uma nova conta através do registro

## 📝 CI/CD

O projeto inclui pipeline GitHub Actions que:
- Executa linting com flake8
- Roda testes unitários com pytest
- Ativa automaticamente em push/PR para main

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e demonstração de integração entre APIs REST e aplicações mobile.

---

**Desenvolvido com ❤️ usando Flask e React Native** 