# Quick Start Guide - React Frontend

Get the SAP Process Discovery React frontend running in 3 steps.

## Step 1: Install Dependencies

```bash
cd frontend-react

# Using npm
npm install

# Or using bun (faster)
bun install
```

## Step 2: Start the Backend API

In a separate terminal:

```bash
cd ..
python -m uvicorn api.main:app --reload --port 8001
```

Wait for the message: **"API Ready! Agent initialized successfully."**

## Step 3: Start the Frontend

```bash
# Using npm
npm run dev

# Or using bun
bun dev
```

Open your browser to: **http://localhost:3000**

## What You'll See

1. **Header** - Shows connection status and clear chat button
2. **Chat Area** - Main conversation interface
3. **Input Box** - Send messages to the agent
4. **Sidebar** - Commands and information

## Try These Commands

### Run SAP Discovery
```
Run SAP discovery
```

### Display Results
```
Display the results
```

### Export to Excel
```
Export to Excel
```

### Combined Command
```
Run and print
```

## Troubleshooting

### "Cannot connect to API"

✅ **Solution**: Make sure the backend is running on port 8001

```bash
# In the project root directory
python -m uvicorn api.main:app --reload --port 8001
```

### Port 3000 already in use

✅ **Solution**: Change the port in `vite.config.ts`:

```ts
server: {
  port: 3001, // or any other available port
  // ...
}
```

### Dependencies not installing

✅ **Solution**: Try clearing the cache:

```bash
# Remove node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                     │
│                 (localhost:3000)                     │
│                                                      │
│  ┌────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Header   │  │ ChatContainer│  │  Sidebar   │ │
│  └────────────┘  └──────────────┘  └────────────┘ │
│                         │                           │
│                    ┌────▼────┐                      │
│                    │ api.ts  │ (Axios)              │
│                    └────┬────┘                      │
└─────────────────────────┼───────────────────────────┘
                          │ HTTP Proxy (/api -> :8001)
                          ▼
┌─────────────────────────────────────────────────────┐
│                FastAPI Backend                       │
│                 (localhost:8001)                     │
│                                                      │
│  POST /chat      - Send message                     │
│  GET  /health    - Check status                     │
│  GET  /          - API info                         │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│           SAP Discovery Agent (LangGraph)            │
│                                                      │
│  • Main Agent with Memory                           │
│  • Subagent Workflow                                │
│  • SAP Help Portal (MCP)                            │
│  • Web Search (Serper)                              │
└─────────────────────────────────────────────────────┘
```

## Key Features

✅ Real-time chat interface
✅ Health status monitoring
✅ Auto-scroll to latest messages
✅ Markdown-like formatting
✅ Loading indicators
✅ Error handling
✅ Responsive design
✅ TypeScript type safety

## Next Steps

1. **Explore the UI** - Try different commands
2. **Customize** - Edit colors in `tailwind.config.js`
3. **Extend** - Add new components in `src/components/`
4. **Build** - Run `npm run build` for production

## Development Tips

### Hot Module Replacement (HMR)

Changes to `.tsx` files will instantly reflect in the browser without full reload.

### Component Structure

```typescript
// Example: Adding a new component
import React from 'react';

interface Props {
  title: string;
}

export const MyComponent: React.FC<Props> = ({ title }) => {
  return <div className="card">{title}</div>;
};
```

### Styling with Tailwind

```typescript
// Use Tailwind utility classes
<div className="flex items-center gap-4 p-6 bg-white rounded-lg shadow-sm">
  <span className="text-gray-700 font-medium">Hello</span>
</div>
```

### API Calls

```typescript
// Add new API method in src/services/api.ts
export const api = {
  async myNewEndpoint(): Promise<MyType> {
    const response = await apiClient.get<MyType>('/my-endpoint');
    return response.data;
  },
};
```

## Resources

- [React Docs](https://react.dev)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

**Need help?** Check the main [README.md](README.md) or the project documentation.
