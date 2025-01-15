This application enables users to interact with their documents through chat. Users can upload documents to a vector database using the LangChain framework, leveraging the OpenAI API to generate embeddings for the data, which is then stored in the vector database. Uploaded documents are also saved in a storage solution, such as AWS S3 or Azure Storage Accounts.

Users can select a specific document to chat within or interact with all their uploaded documents collectively. Each user’s documents are private, ensuring that users can only access and chat with their own documents. There is no visibility or interaction permitted with documents belonging to other users.

To use the application, users must create an account. Passwords are securely stored in an encrypted format, ensuring the safety and confidentiality of user credentials.

>_**Note**_: The application is currently in progress mode, indicating that it is under active development or enhancement.

# Architecture

## Auth (Clerk or User/Password in PostgreSQL database):

Handles authentication for the users.
It connects directly to the FrontEnd (Next.js) for user login or sign-up flows.
FrontEnd likely retrieves user authentication tokens and sends them to the BackEnd for secure API interactions.

## FrontEnd (Next.js):

Acts as the user-facing layer where users interact with the application.
Communicates with the BackEnd (FastAPI) for retrieving and sending data.
Retrieves authentication data from Clerk.

## BackEnd (FastAPI):

Handles the core business logic and processes requests from the FrontEnd.
Interacts with external services like OpenAI API for AI processing and Pinecone for vector database operations.
Stores and retrieves data/files in AWS S3.

## Database (PostgreSQL):

This layer serves as the backbone for storing and managing application data. It is where the core business schema resides, and it plays a critical role in ensuring data consistency, reliability, and security.

## OpenAI API:

Provides AI capabilities (e.g., natural language processing, text generation).
Communicates exclusively with the BackEnd.

## Vector Database (Pinecone or Qdrant):

Stores embeddings or vectorized representations of data.
Likely used for advanced search, similarity queries, or AI model-related tasks.
Managed by the BackEnd.

## Storage (AWS S3 or Azure Storage Account):

Stores larger files or raw data that may not fit in the database.
Accessed by the BackEnd for read/write operations.

# Project Structure
/.github
/backend
--/app
--/migrations
--/tests
----/units
----/integrations
/docs
/frontend
/infra
