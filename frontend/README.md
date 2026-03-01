# SAP Process Discovery - React Frontend

A modern React frontend for the SAP Process Discovery Agent built with React, TypeScript, Vite, and Tailwind CSS.

## Features

- 💬 **Chat Interface** - Interactive chat with the SAP discovery agent
- 🎨 **Modern UI** - Clean, responsive design with Tailwind CSS
- ⚡ **Fast Development** - Vite for lightning-fast HMR
- 🔒 **Type Safety** - Full TypeScript support
- 🔄 **Real-time Status** - Live API health monitoring
- 📱 **Responsive** - Works on all screen sizes

## Architecture

### Components

- **App.tsx** - Main application component with state management
- **Header.tsx** - Top navigation with status indicator
- **ChatContainer.tsx** - Message display area
- **ChatMessage.tsx** - Individual message bubble
- **ChatInput.tsx** - Message input with send button
- **Sidebar.tsx** - Information and command reference panel
- **LoadingIndicator.tsx** - Loading animation

### Services

- **api.ts** - API client for backend communication
  - `/chat` - Send messages to agent
  - `/health` - Check API status
  - `/` - Get API info

### Types

- **ChatMessage** - Message structure
- **ChatRequest/Response** - API request/response types
- **SAPProcessMapping** - SAP discovery result structure

## Prerequisites

- Node.js 18+ or Bun
- Running backend API on `http://localhost:8001`

## Installation

```bash
# Install dependencies
npm install

# Or with bun
bun install
```

## Development

```bash
# Start development server (http://localhost:3000)
npm run dev

# Or with bun
bun dev
```

The frontend will proxy API requests from `/api/*` to `http://localhost:8001/*`.

## Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend-react/
├── src/
│   ├── components/          # React components
│   │   ├── ChatContainer.tsx
│   │   ├── ChatInput.tsx
│   │   ├── ChatMessage.tsx
│   │   ├── Header.tsx
│   │   ├── LoadingIndicator.tsx
│   │   └── Sidebar.tsx
│   ├── services/            # API services
│   │   └── api.ts
│   ├── types/               # TypeScript types
│   │   └── index.ts
│   ├── utils/               # Utility functions
│   │   └── formatContent.tsx
│   ├── styles/              # CSS files
│   │   └── index.css
│   ├── App.tsx              # Main app component
│   └── main.tsx             # Entry point
├── public/                  # Static assets
├── index.html               # HTML template
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

## Usage

1. **Start the backend API**
   ```bash
   cd ..
   python -m uvicorn api.main:app --reload --port 8001
   ```

2. **Start the frontend**
   ```bash
   npm run dev
   ```

3. **Open browser** to `http://localhost:3000`

4. **Start chatting** with the SAP discovery agent:
   - "Run SAP discovery"
   - "Display the results"
   - "Export to Excel"
   - "Run and print"

## API Integration

The frontend communicates with the FastAPI backend through a proxy:

- **Development**: `http://localhost:3000/api` → `http://localhost:8001`
- **Production**: Configure your reverse proxy or API gateway

### API Endpoints Used

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send message to agent |
| GET | `/health` | Check API health |
| GET | `/` | Get API information |

## Customization

### Theme Colors

Edit [tailwind.config.js](tailwind.config.js) to customize colors:

```js
theme: {
  extend: {
    colors: {
      primary: {
        500: '#0ea5e9', // Main brand color
        600: '#0284c7',
      },
    },
  },
}
```

### API URL

Edit [vite.config.ts](vite.config.ts) to change the backend URL:

```ts
server: {
  proxy: {
    '/api': {
      target: 'http://your-api-url:8001',
      changeOrigin: true,
    },
  },
}
```

## Troubleshooting

### Cannot connect to API

1. Make sure the backend is running on port 8001
2. Check CORS settings in backend `api/main.py`
3. Verify the proxy configuration in `vite.config.ts`

### Build errors

1. Clear node_modules: `rm -rf node_modules && npm install`
2. Clear Vite cache: `rm -rf node_modules/.vite`
3. Update dependencies: `npm update`

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons

## Performance

- Code splitting with Vite
- Lazy loading of components
- Optimized bundle size
- Fast refresh in development

## Future Enhancements

- [ ] Streaming SSE support for real-time responses
- [ ] Chat history persistence (localStorage)
- [ ] Export chat as PDF/Markdown
- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] Voice input support
- [ ] Keyboard shortcuts

## License

Part of the SAP Process Discovery Agent project.
