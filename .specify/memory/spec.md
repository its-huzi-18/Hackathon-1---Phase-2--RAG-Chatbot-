Project Constitution
Physical AI & Humanoid Robotics — AI-Native Interactive Textbook

Purpose of the Project
The goal of this project is to create a fully AI-native, interactive, and intelligent textbook for the course Physical AI & Humanoid Robotics.
The textbook will be generated using Spec-Kit Plus and Claude Code, published using Docusaurus, and deployed publicly through GitHub Pages.

This project goes beyond a simple book. It aims to demonstrate a next-generation learning model in which:

The book is interactive

The content is AI-adaptive

Readers can ask the book questions

The book can personalize itself

The book can translate itself

The book becomes a digital intelligent tutor

This aligns with the vision of Panaversity: building AI-native educational platforms for the next era.

Core Deliverables (Mandatory)

2.1 Textbook Creation

Write a complete textbook covering Physical AI & Humanoid Robotics from fundamentals to advanced concepts.

Structure the book using Spec-Kit Plus, including chapters, sections, and metadata.

Use Claude Code for content writing, automation, and agent-based workflows.

Implement the book as a Docusaurus documentation website.

Deploy the final book publicly using GitHub Pages.

2.2 RAG Chatbot Integration
Build and embed a Retrieval-Augmented Generation chatbot inside the textbook using:

OpenAI Agents / ChatKit SDK

FastAPI backend

Qdrant Cloud (vector database)

Neon Serverless Postgres (metadata + user data)

The integrated assistant must:

Answer questions strictly based on book content.

Support “answer using only selected text” functionality.

Embed naturally within Docusaurus.

Bonus Deliverables (Optional but Worth +150 Points Total)

3.1 Reusable Intelligence (+50 Points)
Create novel AI-powered tools using Claude Code subagents and agent skills, such as:

Chapter Summarizer Agent

Robotics Code Example Generator Agent

Chapter Quiz/MCQ Generator Agent

Concept Explainer Agent

Hardware Diagram Creator Agent

These tools should become reusable components inside the book.

3.2 Authentication System (+50 Points)

Implement Signup/Signin using better-auth.

Ask users at signup:

Software Background

Hardware/Robotics Background

Learning Preferences

Store this information in Neon Postgres for personalized learning.

3.3 Personalized Content System (+50 Points)
Add a “Personalize this Chapter” button to each chapter.

Upon click:

Retrieve user background

Regenerate the chapter dynamically

Adapt content based on:

Beginner level

Intermediate level

Advanced robotics experience

Software development focus

Hardware engineering focus

Preferred learning style

Technology Stack

4.1 Book Development

Spec-Kit Plus

Claude Code

Docusaurus

React Components

Markdown/MDX

4.2 Backend / AI

FastAPI

OpenAI Agents / ChatKit SDK

Qdrant Cloud (vector storage)

Neon Serverless Postgres

PyPDF / text pipeline as needed

4.3 Deployment

GitHub Pages (book)

Railway/Render/Fly.io (backend)

Qdrant + Neon managed cloud services

Success Criteria
The project will be considered successful if:

A complete textbook is authored and deployed using Docusaurus.

The RAG chatbot answers queries accurately using vectorized content.

The “selected text answering” feature works inside the live book.

The backend integrates seamlessly with the frontend.

(Bonus) The AI subagents function reliably.

(Bonus) Signup/Signin works using better-auth.

(Bonus) Personalization and Urdu translation buttons function correctly.

Project Vision
This project is a demonstration of the future of textbooks:
AI-powered, dynamic, multilingual, adaptive, and deeply interactive.
