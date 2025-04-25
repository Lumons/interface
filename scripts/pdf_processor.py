import json
import uuid
import re
import lmstudio as lms
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceWindowNodeParser, MarkdownNodeParser
from docling.document_converter import DocumentConverter
from llama_index.core.node_parser.interface import Document
from supabase import create_client, Client
from datetime import datetime



SUPABASE_URL = "https://fhfxgqlmmzccbqfvcxum.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZoZnhncWxtbXpjY2JxZnZjeHVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI1OTUyODMsImV4cCI6MjA1ODE3MTI4M30._OmwDs08TLE5-nLj8eNZoWDfZFgcEPZ12hsKG1yT7GM"

# Initialize Supabase client
client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



source = "/home/luke/repos/seshat/EXPORT/Clark and Chalmers - 1998 - The Extended Mind.pdf"  # document per local path or URL
converter = DocumentConverter()
result = converter.convert(source)
print(result)
markdown_content = result.document.export_to_markdown()
print(markdown_content)
# Initialize LM Studio Embedding Model
model = lms.embedding_model("nomic-embed-text-v1.5")


# Check that conversion produced a markdown document
if result is not None and hasattr(result, 'document'):
    markdown_content = result.document.export_to_markdown()
    print("Markdown Export:\n", markdown_content[:500]) # Preview first 500 chars

    # Initialize LM Studio Embedding Model
    model = lms.embedding_model("nomic-embed-text-v1.5")

    # Create document object with markdown content
    document = Document(text=markdown_content)

    # Initialize node parser with default settings
    # Hypothetical API - adjust based on actual library support
    node_parser = MarkdownNodeParser()


    # Node parsing from document
    nodes = node_parser.get_nodes_from_documents([document], show_progress=True)
    print(f"Nodes created: {len(nodes)}")

    # Initialize GraphRAGExtractor
    extractor = GraphRAGExtractor(
        llm=llm,
        extract_prompt=DEFAULT_KG_TRIPLET_EXTRACT_PROMPT,
        parse_fn=default_parse_triplets_fn,
        max_paths_per_chunk=10,
    )

    # Extract features from nodes
    nodes_with_features = extractor(nodes)
    print(f"Nodes with features extracted: {len(nodes_with_features)}")

    # Initialize list for nodes with embeddings
    nodes_embedded = []

    # Loop over each node, retrieve embeddings, and store these nodes
    for node in nodes:
        chunk = node.text
        if chunk:
            embedding = model.embed(chunk)
            nodes_embedded.append({
                "id": node.id_,
                "chunk": chunk,
                "embedding": embedding,
                "metadata": node.metadata
            })

    # Save nodes with embeddings as JSON
    with open('embedded_nodes.json', 'w') as f:
        json.dump(nodes_embedded, f, indent=4)
    print("Embedded Nodes saved to embedded_nodes.json")
else:
    print(f"No valid document conversion for source: {source}")



def insert_nodes_to_supabase(file_path, nodes_embedded):
    """Insert node data into Supabase."""
    date_time_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i, node in enumerate(nodes_embedded):
        data = {
            "file_path": file_path,
            "created_at": date_time_added,
            "chunk_number": i,
            "chunk_content": node["chunk"],
            "embeddings": node["embedding"]
        }
        response = client.table('paper-library').insert(data).execute()
        if response.data:
            print(f"Inserted node {i} into Supabase.")
        else:
            print(f"Failed to insert node {i}. Error: {response.error}")

insert_nodes_to_supabase(source, nodes_embedded)
