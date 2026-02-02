"""
Vector Store for Semantic Search
Uses sentence-transformers for embeddings and ChromaDB for vector storage
"""
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
from datetime import datetime

class VectorStore:
    def __init__(self, persist_directory="/mnt/data/chroma_db"):
        """Initialize vector store with persistent storage"""
        print("🔧 Initializing Vector Store...")
        
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize embedding model (downloads once, ~80MB)
        print("📦 Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded (384 dimensions)")
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="intelligence_documents",
            metadata={"description": "External intelligence documents and articles"}
        )
        
        print(f"✅ Vector store initialized ({self.collection.count()} documents indexed)")
    
    def add_document(self, doc_id, text, metadata):
        """
        Add document to vector store
        
        Args:
            doc_id: Unique document ID
            text: Full document text
            metadata: Dict with title, source, url, date, etc.
        """
        try:
            # Generate embedding
            embedding = self.embedding_model.encode(text).tolist()
            
            # Store in ChromaDB
            self.collection.add(
                ids=[str(doc_id)],
                embeddings=[embedding],
                documents=[text[:2000]],  # Store first 2000 chars for preview
                metadatas=[{
                    'title': metadata.get('title', ''),
                    'source': metadata.get('source', ''),
                    'url': metadata.get('url', ''),
                    'date': metadata.get('date', ''),
                    'doc_type': metadata.get('doc_type', 'article'),
                    'indexed_at': datetime.now().isoformat()
                }]
            )
            
            return True
        except Exception as e:
            print(f"❌ Error adding document {doc_id}: {e}")
            return False
    
    def update_document(self, doc_id, text, metadata):
        """Update existing document"""
        try:
            # Delete old version
            self.collection.delete(ids=[str(doc_id)])
            
            # Add new version
            return self.add_document(doc_id, text, metadata)
        except Exception as e:
            print(f"❌ Error updating document {doc_id}: {e}")
            return False
    
    def delete_document(self, doc_id):
        """Delete document from vector store"""
        try:
            self.collection.delete(ids=[str(doc_id)])
            return True
        except Exception as e:
            print(f"❌ Error deleting document {doc_id}: {e}")
            return False
    
    def search(self, query, n_results=10, filter_metadata=None):
        """
        Semantic search for similar documents
        
        Args:
            query: Search query string
            n_results: Number of results to return
            filter_metadata: Optional filters (e.g., {'source': 'TechCrunch'})
        
        Returns:
            Dict with documents, metadatas, distances
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata  # ChromaDB filter format
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i],
                    'similarity': 1 - results['distances'][0][i]  # Convert distance to similarity
                })
            
            return {
                'success': True,
                'results': formatted_results,
                'count': len(formatted_results)
            }
        except Exception as e:
            print(f"❌ Search error: {e}")
            return {
                'success': False,
                'error': str(e),
                'results': []
            }
    
    def get_document(self, doc_id):
        """Get specific document by ID"""
        try:
            result = self.collection.get(
                ids=[str(doc_id)],
                include=['documents', 'metadatas']
            )
            
            if result['ids']:
                return {
                    'success': True,
                    'document': result['documents'][0],
                    'metadata': result['metadatas'][0]
                }
            else:
                return {'success': False, 'error': 'Document not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def count(self):
        """Get total document count"""
        return self.collection.count()
    
    def reindex_all(self, documents):
        """
        Re-index all documents (useful after model upgrade)
        
        Args:
            documents: List of dicts with 'id', 'text', 'metadata'
        """
        print(f"🔄 Re-indexing {len(documents)} documents...")
        
        success_count = 0
        for doc in documents:
            if self.add_document(doc['id'], doc['text'], doc['metadata']):
                success_count += 1
        
        print(f"✅ Re-indexed {success_count}/{len(documents)} documents")
        return success_count
    
    def reset(self):
        """Reset the vector store (delete all documents)"""
        try:
            self.client.delete_collection(name="intelligence_documents")
            self.collection = self.client.get_or_create_collection(
                name="intelligence_documents",
                metadata={"description": "External intelligence documents and articles"}
            )
            print("✅ Vector store reset")
            return True
        except Exception as e:
            print(f"❌ Error resetting vector store: {e}")
            return False


# Global instance
_vector_store = None

def get_vector_store():
    """Get or create global vector store instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store


if __name__ == "__main__":
    # Test the vector store
    print("Testing Vector Store...")
    
    vs = VectorStore()
    
    # Test adding documents
    test_docs = [
        {
            'id': 'test1',
            'text': 'Artificial intelligence is transforming healthcare through machine learning and deep learning.',
            'metadata': {'title': 'AI in Healthcare', 'source': 'Test'}
        },
        {
            'id': 'test2',
            'text': 'Digital transformation is reshaping business operations across industries.',
            'metadata': {'title': 'Digital Transformation', 'source': 'Test'}
        }
    ]
    
    for doc in test_docs:
        vs.add_document(doc['id'], doc['text'], doc['metadata'])
    
    # Test search
    print("\nSearching for 'healthcare technology'...")
    results = vs.search('healthcare technology', n_results=2)
    
    if results['success']:
        for r in results['results']:
            print(f"\n✅ Found: {r['metadata']['title']}")
            print(f"   Similarity: {r['similarity']:.3f}")
            print(f"   Text: {r['document'][:100]}...")
    
    print(f"\n📊 Total documents: {vs.count()}")
