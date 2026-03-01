FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Accept build argument and set as env var for Vite
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build for production (VITE_API_URL is now available)
RUN npm run build

# Expose port
EXPOSE 3000

# Serve with preview server
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]