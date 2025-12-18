# Project Plan: Physical AI & Humanoid Robotics — AI-Native Interactive Textbook

## 1. Phase 1: Core Textbook Development & Deployment

### 1.1 Setup Docusaurus Project

- Initialize Docusaurus project (`npx create-docusaurus@latest my-book classic`).
- Configure Docusaurus for basic site structure and navigation.
- Integrate Spec-Kit Plus for chapter/section management.

### 1.2 Initial Content Generation (Claude Code)

- Use Claude Code to generate initial chapters and sections for Physical AI & Humanoid Robotics.
- Structure content according to Spec-Kit Plus guidelines (e.g., Markdown/MDX files).
- Focus on foundational concepts first.

### 1.3 GitHub Pages Deployment

- Configure Docusaurus for deployment to GitHub Pages.
- Set up GitHub Actions or similar CI/CD for automated deployment on push to `main`.
- Verify public accessibility of the textbook.

## 2. Phase 2: RAG Chatbot Integration

### 2.1 Backend Development (FastAPI, Neon Postgres, Qdrant)

- Set up a FastAPI backend to handle RAG requests.
- Configure Neon Serverless Postgres for metadata and user data storage.
- Integrate Qdrant Cloud for vector database functionality.
- Develop API endpoints for:
  - Ingesting book content into Qdrant.
  - Performing similarity searches.
  - Handling RAG queries.

### 2.2 OpenAI Agents / ChatKit SDK Integration

- Integrate OpenAI Agents or ChatKit SDK with the FastAPI backend.
- Implement logic for generating responses based on retrieved information from Qdrant.

### 2.3 Docusaurus Frontend Integration

- Develop React components within Docusaurus to embed the chatbot UI.
- Implement client-side logic to interact with the FastAPI backend.
- Ensure natural embedding and user experience within the textbook.

### 2.4 "Answer Using Selected Text" Feature

- Implement frontend functionality to allow users to select text.
- Pass selected text as context to the RAG chatbot API.
- Ensure the chatbot strictly answers based on the provided selected text.

## 3. Phase 3: Bonus Deliverables (Concurrent/Sequential as feasible)

### 3.1 Reusable Intelligence (AI-Powered Tools)

- Identify key areas for AI tools (e.g., summarization, code generation, quiz generation).
- Develop Claude Code subagents or agent skills for each tool.
- Integrate these tools as reusable components within Docusaurus chapters.

### 3.2 Authentication System (`better-auth`)

- Implement user Signup/Signin using `better-auth`.
- Develop forms to collect Software Background, Hardware/Robotics Background, and Learning Preferences during signup.
- Store collected user data in Neon Postgres.

### 3.3 Personalized Content System

- Develop a "Personalize this Chapter" button for each chapter.
- Implement backend logic to retrieve user background from Neon Postgres.
- Dynamically regenerate chapter content based on user profiles (beginner/intermediate/advanced, software/hardware focus, learning style).

## 4. Deployment Strategy

- **Book**: GitHub Pages for static Docusaurus site.
- **Backend**: Railway/Render/Fly.io for FastAPI application.
- **Databases**: Qdrant Cloud and Neon managed cloud services.

## 5. Testing and Validation

- **Unit/Integration Tests**: For FastAPI endpoints, RAG logic, and Docusaurus components.
- **End-to-End Tests**: Verify full chatbot functionality, deployment, and personalization.
- **User Acceptance Testing**: Gather feedback on interactivity, content quality, and AI adaptation.

## 6. Continuous Improvement

- Establish a feedback loop for content improvement and AI model fine-tuning.
- Monitor deployment for performance and reliability.

## 7. Next Steps

- Create a detailed task breakdown using `/sp.tasks` based on this plan.
- Begin implementing Phase 1: Core Textbook Development.
