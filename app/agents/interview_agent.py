from functools import lru_cache

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

from app.model.requests.interview import InterviewRequest, InterviewResponse


BEON_TECH_KNOWLEDGE_BASE = [
	"BEON.tech mission is to place the brightest tech talent in the most disruptive and innovative U.S. companies.",
	"BEON.tech offer IT staff augmentation services for every modern tech need, from backend and frontend to AI, machine learning, DevOps and QA.",
	"At BEON.tech, building software means far more than just filling roles — it's about creating strong relationships, empowering careers and helping people grow.",
]


class InterviewAgent:
	def __init__(self) -> None:
		embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
		self.vector_store = FAISS.from_texts(BEON_TECH_KNOWLEDGE_BASE, embedding=embeddings)
		self.request_parser = PydanticOutputParser(pydantic_object=InterviewRequest)
		self.response_parser = PydanticOutputParser(pydantic_object=InterviewResponse)
		self.prompt = ChatPromptTemplate.from_messages(
			[
				(
					"system",
					"You answer interview questions about BEON.tech using only the provided context. "
					"If the context is not enough, say so clearly and keep the answer grounded in the provided information.\n\n"
					"Relevant matches:\n{context}\n\n"
					"Return the response using this format:\n{format_instructions}",
				),
				("human", "Question: {question}"),
			]
		)
		self.llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)
		self.chain = self.prompt | self.llm

	def get_vector_store(self) -> FAISS:
		return self.vector_store

	def answer(self, payload: InterviewRequest) -> InterviewResponse:
		parsed_request = self.request_parser.parse(payload.model_dump_json())
		matches = self.vector_store.similarity_search(parsed_request.prompt, k=3)
		context = "\n".join(f"- {match.page_content}" for match in matches)
		response = self.chain.invoke(
			{
				"question": parsed_request.prompt,
				"context": context,
				"format_instructions": self.response_parser.get_format_instructions(),
			}
		)
  
		return self.response_parser.parse(response.content)


@lru_cache(maxsize=1)
def get_interview_agent() -> InterviewAgent:
	return InterviewAgent()
