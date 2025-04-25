![](documentation/media/lumo9838_epistemic_interface._Neo-renaissance_cyberpunk_knowled_9be5ed1a-efea-4f54-9916-eab2f338459d.png)

# Epistemic Interface

**Overview**

In Clark and Chalmers' vision of the extended mind, they describe epistemic actions as follows:

> "Epistemic actions alter the world so as to aid and augment cognitive processes such as recognition and search."

In our increasingly complex world of data, knowledge, and interconnected ideas, Epistemic Interface extends this concept, providing a tool to help users manipulate and structure knowledge in a way that offloads mental burdens, augments cognitive capabilities, and enables more efficient recognition, search, and insight generation.

The Epistemic Interface enables knowledge manipulation through a variety of externalized tools—such as building knowledge graphs, processing and visualizing data, and creating dynamic, interactive environments for cognitive exploration. These actions help users externalize their thought processes, much like using a calculator to augment mathematical cognition or a map to navigate spatially.

By interacting with the Epistemic Interface, you engage in epistemic actions that make complex data more accessible, facilitate a deeper understanding of the relationships between pieces of information, and help you navigate vast knowledge systems in an intuitive, interactive way.

**Epistemic Actions as Cognitive Security**

In addition to augmenting cognitive processes, epistemic actions are also vital to cognitive security—the protection and enhancement of how we think, recognize, and act upon information. As knowledge becomes more intricate and complex, it’s easy to become overwhelmed or misled by false or incomplete data.

The Epistemic Interface mitigates these risks by providing a structured, externalized framework for organizing, visualizing, and verifying knowledge. By ensuring that your cognitive tools are accurate, secure, and transparent, the interface helps preserve the integrity of the knowledge you work with, reducing cognitive overload and preventing errors in judgment that arise from chaos or misinformation.

In this way, Epistemic Interface not only aids in knowledge management but also strengthens the cognitive security of your processes—ensuring that external tools are used to safeguard the reliability and validity of your insights, while also providing a secure space for exploring complex systems of knowledge.

**Key Features of Epistemic Interface**

- *Multi-Modal Knowledge Processing*: Organize, process, and manipulate different forms of data—text, documents, and more—through an integrated, high-tech interface.

- *Dynamic Knowledge Graphs*: Visualize relationships between ideas, concepts, and data points in real-time, supported by advanced AI and algorithmic tools for pattern recognition and insight generation.

- *Interactive Search & Querying*: Easily search and interact with complex data, instantly extracting relevant insights or verifying information across multiple sources.

- *Cognitive Security Framework*: Designed with features to help ensure that your knowledge processes remain accurate, transparent, and free from cognitive overload or misinformation.

## Scripts

### record_audio.py

- When run, checks for the existence of a state file which, if non-existent, creates, and then begins recording. If state indicates recording, then recording is stopped and the state file changed. Saves recording as date-time (`recording_%Y-%m-%d_%H-%M-%S.wav`)


### transcriber.py

- Checks an index file `transcription_index.txt` against available files. Transcribes using whisper, saves as txt file in the same folder and adds names to the index. Whisper model size can be changed with speed/ quality tradeoffs. Currently specified as latest and largest - intended function is a scheduled overnight job so not worried about how long it will take. May take a while if a batch have been added in bulk. 


### Audio Log Processor.py

The audio_log_processor.py script automates the process of transcribing audio files, generating embeddings from the transcriptions, and storing the results both locally and in a Supabase database. This is achieved through the following steps:

**1. Environment Setup:**

The script initializes necessary configurations by loading environment variables for secure access to Supabase, avoiding any hardcoded credentials.

**2. Model Initialization:**

It checks for a CUDA-enabled GPU to take advantage of hardware acceleration and loads the Whisper model, which is utilized for transcription tasks.

**3. Audio Transcription:**

The script processes audio files found in a specified directory, transcribing them into text. It supports common audio formats such as .wav, .mp3, and .m4a.
It tracks which files have already been transcribed using an index file (transcription_index.txt), ensuring that each file is only processed once.
  
**4. Text Embedding:**

For each transcribed audio file, the script generates embeddings using LM Studio's embedding model. These embeddings represent the transcriptions in a numerical form that captures the semantic content, useful for machine learning and data retrieval tasks.

**5. Local Storage:**

Metadata about each transcription, including the file name and the transcription text, is stored in a CSV file (audio_transcriptions.csv). This step facilitates easy access to transcription records in a tabular format.

**6. Database Integration:**

The script inserts each transcription, along with its embedding and relevant metadata, into a Supabase database table called 'log-entries'. This enables efficient storage and retrieval of the audio data for various applications, such as content analysis and data mining.

**7. Index Maintenance:**

Each transcribed file is added to an index to prevent repetitive processing in future runs, promoting efficient resource utilization and streamlined operation.


### PDF_processor.py

The script processes a document specified by the user, converting it into a markdown format, extracting text content from this format, embedding the text using a language model, and then storing the processed data in a Supabase database. Here's how it achieves this:

**1. Document Conversion:**

The script begins by loading a document from a specified file path or URL.
Using the DocumentConverter, it converts the document into a markdown format. This step is essential for standardizing the document's formatting, making it easier to parse and analyze the text.

**2. Markdown Extraction:**

The converted document's content is exported to markdown and printed to the console for preview.
The markdown content is then used to create a Document object.

**3. Node Parsing:**

A node parser, specifically a `MarkdownNodeParser`, is initialized to extract discrete text segments or "nodes" from the markdown content. These nodes represent chunks of text parsed from the document.

**4. Text Embedding:**

For each text node, the script uses the LM Studio's embedding model, `nomic-embed-text-v1.5`, to generate embeddings. Embeddings are numerical representations of the text that capture semantic meaning, useful in various machine learning applications like similarity searches.

**5. Data Storage:**

The script prepares a list of these text nodes, including their embeddings and metadata, and saves this list to a JSON file named `embedded_nodes.json`.

It further inserts each node along with its embedding and other relevant metadata into a Supabase database. Each entry in the database corresponds to a node from the document, allowing for robust storage and retrieval capabilities for future applications or analyses.