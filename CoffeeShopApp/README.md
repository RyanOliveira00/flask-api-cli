# ☕ Coffee Shop App - React Native

Este é um aplicativo React Native Expo com TypeScript que funciona como interface cliente para a API Coffee Shop.

## 🚀 Funcionalidades

- **Autenticação JWT**: Login e registro de usuários
- **Lista de Cafés**: Visualização de todos os cafés disponíveis
- **Compras**: Realizar compras de cafés
- **Histórico**: Visualizar histórico de compras
- **CRUD de Cafés** (Admin): Adicionar, editar e excluir cafés
- **Interface Responsiva**: Design moderno e intuitivo

## 📱 Telas

### Usuário Padrão
- **Login**: Autenticação com username e senha
- **Registro**: Criar nova conta
- **Lista de Cafés**: Ver cafés disponíveis e realizar compras
- **Histórico de Compras**: Ver todas as compras realizadas

### Usuário Admin
- Todas as funcionalidades do usuário padrão
- **Adicionar Café**: Criar novos cafés
- **Editar Café**: Modificar cafés existentes
- **Excluir Café**: Remover cafés da lista

## 🛠️ Tecnologias Utilizadas

- **React Native**: Framework para desenvolvimento mobile
- **Expo**: Plataforma para desenvolvimento React Native
- **TypeScript**: Tipagem estática para JavaScript
- **React Navigation**: Navegação entre telas
- **Axios**: Cliente HTTP para requisições à API
- **AsyncStorage**: Armazenamento local para tokens JWT

## 📋 Pré-requisitos

- Node.js (versão 14 ou superior)
- npm ou yarn
- Expo CLI (`npm install -g @expo/cli`)
- API Coffee Shop rodando (padrão: http://localhost:5001)

## 🔧 Instalação e Configuração

1. **Clone o repositório** (se ainda não foi feito):
   ```bash
   git clone <repository-url>
   cd CoffeeShopApp
   ```

2. **Instale as dependências**:
   ```bash
   npm install
   ```

3. **Configure a URL da API**:
   - Abra o arquivo `src/utils/config.ts`
   - Ajuste a `BASE_URL` para apontar para sua API:
   ```typescript
   export const API_CONFIG = {
     BASE_URL: 'http://localhost:5001', // Sua URL da API
     TIMEOUT: 10000,
   };
   ```

   **Importante**: Se você estiver testando em um dispositivo físico ou emulador, substitua `localhost` pelo IP da sua máquina:
   ```typescript
   BASE_URL: 'http://192.168.1.100:5001', // Exemplo com IP da máquina
   ```

4. **Inicie o servidor de desenvolvimento**:
   ```bash
   npx expo start
   ```

## 📱 Como Usar

### 1. Primeira Execução
- Certifique-se de que a API Coffee Shop está rodando
- Abra o app no seu dispositivo/emulador
- Use as credenciais padrão para testar:
  - **Admin**: `admin` / `admin123`
  - Ou crie uma nova conta

### 2. Funcionalidades Principais

#### Login/Registro
- Entre com uma conta existente ou crie uma nova
- O token JWT é armazenado automaticamente

#### Lista de Cafés
- Visualize todos os cafés disponíveis
- Veja preço, descrição e estoque
- Clique em "Comprar" para realizar uma compra

#### Histórico de Compras
- Acesse através do botão "Histórico" no cabeçalho
- Veja todas as suas compras com detalhes

#### Funcionalidades Admin
- Adicione novos cafés com o botão "+"
- Edite cafés existentes clicando em "Editar"
- Exclua cafés com o botão "Excluir"

## 🔗 Integração com a API

O app consome as seguintes rotas da API:

### Autenticação
- `POST /auth/login` - Login do usuário
- `POST /auth/register` - Registro de novo usuário

### Cafés
- `GET /coffee/` - Listar todos os cafés
- `POST /coffee/` - Adicionar novo café (admin)
- `PUT /coffee/:id` - Atualizar café (admin)
- `DELETE /coffee/:id` - Excluir café (admin)

### Compras
- `POST /purchase/` - Realizar compra
- `GET /purchase/` - Histórico de compras

## 🎨 Estrutura do Projeto

```
CoffeeShopApp/
├── src/
│   ├── components/          # Componentes reutilizáveis
│   ├── contexts/           # Contextos (Auth)
│   ├── screens/            # Telas do aplicativo
│   ├── services/           # Serviços (API)
│   ├── types/              # Tipos TypeScript
│   └── utils/              # Utilitários e configurações
├── App.tsx                 # Componente principal
└── README.md              # Este arquivo
```

## 🔐 Autenticação

O aplicativo usa JWT (JSON Web Tokens) para autenticação:
- Tokens são armazenados no AsyncStorage
- Incluídos automaticamente em requisições protegidas
- Usuário é redirecionado para login quando token expira

## 📝 Notas Importantes

1. **URL da API**: Certifique-se de ajustar a URL da API no arquivo de configuração
2. **Permissões**: Apenas usuários admin podem adicionar/editar/excluir cafés
3. **Conectividade**: O app requer conexão com a internet para funcionar
4. **Compatibilidade**: Testado no iOS e Android

## 🐛 Solução de Problemas

### Erro de Conexão
- Verifique se a API está rodando
- Confirme a URL da API no arquivo de configuração
- Em dispositivos físicos, use o IP da máquina, não localhost

### Erro de Token
- Faça logout e login novamente
- Verifique se o token não expirou

### Problemas de Navegação
- Reinicie o app com `npx expo start --clear`

## 🚀 Executando em Produção

Para criar um build de produção:

```bash
# Android
npx expo build:android

# iOS
npx expo build:ios
```

## 📄 Licença

Este projeto foi criado para fins educacionais e demonstração da integração entre React Native e APIs REST.

---

**Desenvolvido com ❤️ usando React Native e Expo** 