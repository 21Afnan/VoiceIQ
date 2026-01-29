from concurrent.futures import ThreadPoolExecutor, as_completed

from backend.core.rag import RAGRetriever
from backend.llms.gemini import GeminiLLM
from backend.llms.kimi import KimiLLM
from backend.llms.deepseek import DeepSeekLLM
from backend.voice.tts import text_to_speech


class AnswerEngine:
    def __init__(self):
        # -----------------------------
        # Initialize RAG
        # -----------------------------
        self.retriever = RAGRetriever()

        # -----------------------------
        # Initialize LLMs
        # -----------------------------
        self.llms = {
            "Gemini": GeminiLLM(),
            "Kimi": KimiLLM(),
            "DeepSeek": DeepSeekLLM(),
        }

    # -----------------------------
    # Generate answers + voice
    # -----------------------------
    def answer(self, question, top_k=5):
        #  Retrieve context
        chunks = self.retriever.retrieve(question, top_k=top_k)
        
        print(f"\n🔍 DEBUG: Question: {question}")
        print(f"🔍 DEBUG: Retrieved {len(chunks)} chunks")
        if chunks:
            print(f"🔍 DEBUG: First chunk preview: {chunks[0]['content'][:150]}...")

        if not chunks:
            return {
                "error": "No relevant context found on Sunmarke website"
            }

        # Merge chunks into context
        context = "\n\n".join(chunk["content"] for chunk in chunks)

        results = {}

        # -----------------------------
        # 2️ Run LLMs in parallel
        # -----------------------------
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_map = {
                executor.submit(llm.generate, question, context): name
                for name, llm in self.llms.items()
            }

            for future in as_completed(future_map):
                name = future_map[future]

                try:
                    text_answer = future.result()
                    print(f"✅ {name} Response: {text_answer[:100]}...")

                    # 3️⃣ Generate voice for each answer (MP3 bytes; avoids filesystem writes)
                    audio_bytes = text_to_speech(text_answer, return_bytes=True)

                    results[name] = {
                        "text": text_answer,
                        "audio": audio_bytes
                    }

                except Exception as e:
                    print(f"❌ {name} Exception: {str(e)}")
                    results[name] = {
                        "text": f"{name} failed: {e}",
                        "audio": None
                    }

        return results
