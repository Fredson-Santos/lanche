# Dockerfile para o frontend React + Vite (Desenvolvimento)
FROM node:20-alpine

WORKDIR /app

# Garantir que os binários do npm estejam no PATH
ENV PATH /app/node_modules/.bin:$PATH

# Copiar arquivos de dependências
COPY package*.json ./

# Instalar TODAS as dependências (incluindo Vite)
RUN npm install

# Copiar o resto dos arquivos
COPY . .

# Expor a porta do Vite
EXPOSE 5173

# Comando para desenvolvimento
CMD ["npm", "run", "dev", "--", "--host"]
