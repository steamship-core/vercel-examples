# AI Chat GPT-3 with Persistence using LangChain and Steamship

This example shows how to implement a persistent chat bot using Next.js, API Routes, and [OpenAI API](https://beta.openai.com/docs/api-reference/completions/create).

### Components

- Next.js
- OpenAI API (REST endpoint)
- API Routes (Edge runtime)
- Steamship API (AI orchestration stack)

## How to Use

You can choose from one of the following two methods to use this repository:

### Deploy your Steamship API

Steamship is an AI orchestration stack that auto-manages prompts, image generation, embeddings, vector search, and more.
Think of it as a host for Vercel-style API functions, but with a managed, stateful, AI stack built-in.

Deploy your **chatbot with persistence** endpoints here:

```bash
pip install steamship
cd steamship
ship deploy
```

### One-Click Deploy

Deploy the example using [Vercel](https://vercel.com?utm_source=github&utm_medium=readme&utm_campaign=vercel-examples):

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/steamship-core/examples/tree/main/vercel/ai-chatgpt-with-persistence&project-name=ai-chatgpt-with-steamship&repository-name=ai-chatgpt-with-persistence&env=STEAMSHIP_API_KEY,STEAMSHIP_PACKAGE_HANDLE)

### Clone and Deploy

Execute [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app) with [npm](https://docs.npmjs.com/cli/init) or [Yarn](https://yarnpkg.com/lang/en/docs/cli/create/) to bootstrap the example:

```bash
npx create-next-app --example https://github.com/steamship-core/examples/tree/main/vercel/ai-chatgpt-with-persistence
# or
yarn create next-app --example https://github.com/steamship-core/examples/tree/main/vercel/ai-chatgpt-with-persistence
```

#### Set up environment variables

Rename [`.env.example`](.env.example) to `.env.local`:

```bash
cp .env.example .env.local
```

Then:

1. update `STEAMSHIP_API_KEY` with your [Steamship API Key](https://steamship.com/account/api).
2. update `STEAMSHIP_PACKAGE_HANDLE` with the package name you selected when deploying your Steamship API

Next, run Next.js in development mode:

```bash
npm install
npm run dev

# or

yarn
yarn dev
```

The app should be up and running at http://localhost:3000.

Deploy it to the cloud with [Vercel](https://vercel.com/new?utm_source=github&utm_medium=readme&utm_campaign=steamship-ai-chatgpt) ([Documentation](https://nextjs.org/docs/deployment)).
