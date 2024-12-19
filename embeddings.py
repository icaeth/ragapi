import os
import uuid
import traceback
from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PDFMinerLoader
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

class RAGEmbedding:
    def __init__(self):
        self.connection = "postgresql+psycopg://esvanguardia:papitas@pgvector:5432/1vectordb"
        self.alternative_db_connection = "postgresql+psycopg://esvanguardia:papitas@pgvector:5432/1transcriptdb"
        
        #Acá se configuran los embeddings en openai
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        
        self.vector_store = PGVector(
            embeddings=self.embeddings,
            connection=self.connection,
            use_jsonb=True,
        )
        
        self.alternative_vector_store = PGVector(
            embeddings=self.embeddings,
            connection=self.alternative_db_connection,
            use_jsonb=True,
        )

    
    def similarity_search(self, query):
            # Create unique IDs for each page using filename and page number
            query = query
            print(f"{query}")
            return self.alternative_vector_store.similarity_search(query, k=10)
            
    def coursedescriptions(self, docs):
        try:
            self.vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise


    def add_documents(self, docs):
        try:
            print(f"Adding {len(docs)} documents to vector store")
            self.alternative_vector_store.add_documents(
                documents=docs,
                ids=[doc.metadata["chunk_id"] for doc in docs]
            )
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise

    async def vector_pdf(self, file: UploadFile):
        temp_file_path = os.path.join('/tmp', file.filename)
        try:
            # Save the uploaded file temporarily
            content = await file.read()
            with open(temp_file_path, "wb") as buffer:
                buffer.write(content)
            
            print(f"Attempting to process PDF: {file.filename}")
            
            # Try multiple PDF loaders
            docs = []
            exceptions = []
            
            # Try PyPDF loader first
            try:
                print("Attempting PyPDFLoader...")
                loader = PyPDFLoader(temp_file_path)
                docs = loader.load()
                print(f"PyPDFLoader extracted {len(docs)} pages")
            except Exception as e:
                print(f"PyPDFLoader failed: {str(e)}")
                exceptions.append(str(e))
            
            # If PyPDF fails, try PDFMiner
            if not docs:
                try:                    
                    print("Attempting PDFMinerLoader...")
                    loader = PDFMinerLoader(temp_file_path)
                    docs = loader.load()
                    print(f"PDFMinerLoader extracted {len(docs)} pages")
                except Exception as e:
                    print(f"PDFMinerLoader failed: {str(e)}")
                    exceptions.append(str(e))
            
            # If both fail, try PDFPlumber as last resort
            if not docs:
                try:
                    print("Attempting PDFPlumberLoader...")
                    loader = PDFPlumberLoader(temp_file_path)
                    docs = loader.load()
                    print(f"PDFPlumberLoader extracted {len(docs)} pages")
                except Exception as e:
                    print(f"PDFPlumberLoader failed: {str(e)}")
                    exceptions.append(str(e))
            
            # If no loader worked, raise error with details
            if not docs:
                error_msg = "Failed to extract text using any PDF loader. Errors:\n"
                error_msg += "\n".join(exceptions)
                raise ValueError(error_msg)
            
            # Validate and clean extracted text
            processed_docs = []
            for i, doc in enumerate(docs):
                if hasattr(doc, 'page_content') and doc.page_content.strip():
                    # Clean the text content
                    cleaned_content = doc.page_content.strip()
                    # Skip if content is too short or appears invalid
                    if len(cleaned_content) > 10:  # Adjust minimum length as needed
                        doc.page_content = cleaned_content
                        processed_docs.append(doc)
                        print(f"Page {i+1}: Extracted {len(cleaned_content)} characters")
                else:
                    print(f"Page {i+1}: No valid content found")
            
            if not processed_docs:
                raise ValueError("No valid text content could be extracted from the PDF")
            
            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            all_splits = text_splitter.split_documents(processed_docs)
            
            if not all_splits:
                raise ValueError("No text chunks could be created from the extracted content")
            
            print(f"Successfully created {len(all_splits)} text chunks")
            
            # Add metadata and store
            for i, doc in enumerate(all_splits):
                doc.metadata.update({
                    "chunk_id": str(uuid.uuid4()),
                    "source_file": file.filename,
                    "chunk_index": i,
                    "total_chunks": len(all_splits),
                    "extraction_method": loader.__class__.__name__
                })
            
            self.add_documents(docs=all_splits)
            return True
                
        except Exception as e:
            print(f"Error processing PDF: {e}")
            print(f"Stack trace: {traceback.format_exc()}")
            raise ValueError(f"Failed to process PDF: {str(e)}")
            
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


# Instantiate the class
embedding = RAGEmbedding()
