This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Folder Structure
```
/frontend
├── app/                # Next.js app directory (Routing and Layouts)
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   ├── about/page.tsx  # About page
│   ├── pricing/page.tsx # Pricing page
│   ├── auth/           # Auth pages (login, register)
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   ├── dashboard/      # User dashboard pages
│   │   ├── layout.tsx  # Dashboard layout (with Sidebar, etc.)
│   │   ├── page.tsx    # Dashboard home
│   │   ├── documents/page.tsx  # List documents page
│   │   ├── chat/page.tsx       # Chat page
│   │   ├── settings/           # User settings
│   │   │   ├── page.tsx        # General settings page
│   │   │   ├── account/page.tsx # Account settings
│   │   │   ├── usage/page.tsx   # Usage and quota page
│   ├── admin/          # Admin dashboard pages
│       ├── layout.tsx  # Admin layout
│       ├── page.tsx    # Admin home
│       ├── users/page.tsx # List users and subscriptions
│       ├── subscriptions/page.tsx # Create/manage subscriptions
│       ├── settings/page.tsx # List parameters
├── components/         # Reusable UI components (from shadcn/ui and custom)
│   ├── ui/             # Components from shadcn/ui
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── modal.tsx
│   ├── layout/         # Layout components
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Sidebar.tsx
│   ├── dashboard/      # Components specific to the dashboard
│   │   ├── DocumentCard.tsx
│   │   ├── ChatWindow.tsx
│   ├── admin/          # Components specific to the admin panel
│       ├── UserListTable.tsx
│       ├── SubscriptionForm.tsx
├── lib/                # Utilities, helpers, and API calls
│   ├── api/            # API call abstractions
│   │   ├── auth.ts     # Auth API (login, register)
│   │   ├── documents.ts # Documents API (CRUD operations)
│   │   ├── chat.ts     # Chat API
│   │   ├── admin.ts    # Admin API
│   ├── utils.ts        # Shared utilities (e.g., date formatting, error handling)
│   ├── routes.ts       # Centralized route definitions
├── styles/             # Styling files
│   ├── globals.css     # Global CSS file
│   ├── tailwind.css    # Tailwind configuration
├── public/             # Public assets
│   ├── logo.png
│   ├── favicon.ico
├── middleware.ts       # Middleware for route protection
├── hooks/              # Custom hooks
│   ├── useAuth.ts      # Authentication logic
│   ├── useChat.ts      # Chat logic
│   ├── useDocuments.ts # Document management logic
│   ├── useAdmin.ts     # Admin-related logic
├── contexts/           # React Contexts for global state
│   ├── AuthContext.tsx # Authentication context
│   ├── ChatContext.tsx # Chat state management
├── config/             # Configuration files
│   ├── constants.ts    # Shared constants (e.g., API URLs, limits)
│   ├── routes.ts       # Centralized route definitions

```

## Getting Started

### Install packages
Set the cursor on frontend folder and execute:

```bash
npm install
```

### Run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.


## Add Packages:
- add packages
```bash
npm install @shadcn@latest/ui
npm install lucide-react
# npm install drizzle-orm @neondatabase/serverless
# npm install -D drizzle-kit
# npm install -D pg
npm install react-dropzone
# npm install aws-sdk
npm install @tanstack/react-query
npm install -D @tanstack/react-query-devtools
npm install react-toastify
npm install axios
# npm install @pinecone-database/pinecone
# npm install langchain
# npm install @langchain/core
# npm install pdf-parse
# npm install @langchain/openai
# npm install @langchain/pinecone
# npm install @tanstack/react-table
# npm install ai
# npm install openai
# npm install react-markdown
# npm install react-wrap-balancer
# npm install nltk
# npm install compromise
```

- Init shadcn
```bash
npx shadcn@latest init
```

- Components

* add component
```bash
cd apps/frontend
npx shadcn@latest add label
npx shadcn@latest add button
npx shadcn@latest add dialog
npx shadcn@latest add alert
npx shadcn@latest add card
npx shadcn@latest add form
npx shadcn@latest add input
npx shadcn@latest add alert-dialog
npx shadcn@latest add avatar
npx shadcn@latest add dropdown-menu
npx shadcn@latest add select
npx shadcn@latest add table
npx shadcn@latest add tabs
npx shadcn@latest add sheet
npx shadcn@latest add accordion
npx shadcn@latest add scroll-area
npx shadcn@latest add popover
npx shadcn@latest add progress
npx shadcn@latest add skeleton
npx shadcn@latest add toast
```