# AI Chat GPT-3 with Persistence using LangChain and Steamship

[![Steamship](https://raw.githubusercontent.com/steamship-core/python-client/main/badge.svg)](https://www.steamship.com/build/langchain-on-vercel?utm_source=github&utm_medium=badge&utm_campaign=github_repo&utm_id=github_vercel_repo_ai_chatgpt)

This example shows how to implement a persistent chat bot using Next.js, API Routes, [OpenAI](https://beta.openai.com/docs/api-reference/completions/create), and [Steamship](https://www.steamship.com).

![Screen Shot](https://steamship.com/data/templates/langchain-on-vercel/chatbot-card.png)

### Components

- Next.js
- OpenAI API (REST endpoint)
- API Routes (Edge runtime)
- Steamship API (AI orchestration stack)

## How to Use

### Run create-next-app

Execute [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app) with [npm](https://docs.npmjs.com/cli/init) or [Yarn](https://yarnpkg.com/lang/en/docs/cli/create/) to bootstrap the example:

```bash
npx create-next-app --example https://github.com/steamship-core/vercel-examples/tree/main/ai-chatgpt
# or
yarn create-next-app --example https://github.com/steamship-core/vercel-examples/tree/main/ai-chatgpt
```

### Deploy your Steamship Stack

Steamship is an AI orchestration stack that auto-manages prompts, image generation, embeddings, vector search, and more.
Think of it as a host for Vercel-style API functions, but with a managed, stateful, AI stack built-in.

Deploy your Steamship stack from this project's root folder with:

```bash
pip install steamship
cd steamship
ship deploy
```

### Set your environment variables

Rename [`.env.example`](.env.example) to `.env.local`:

```bash
cp .env.example .env.local
```

Then:

1. update `STEAMSHIP_API_KEY` with your [Steamship API Key](https://www.steamship.com/account/api).
2. update `STEAMSHIP_PACKAGE_HANDLE` with the package name you selected when deploying your Steamship Stack

### Run or Deploy your Next.js Stack

Run your Next.js stack in development mode:

```bash
npm install
npm run dev

# or

yarn
yarn dev
```

The app should be up and running at http://localhost:3000.

When you like what you see, deploy it to the cloud with [Vercel](https://vercel.com/new?utm_source=github&utm_medium=readme&utm_campaign=steamship-ai-chatgpt) ([Documentation](https://nextjs.org/docs/deployment)).
