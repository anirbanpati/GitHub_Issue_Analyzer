"""LLM client for analyzing GitHub issues using LangChain."""

from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from app.config import settings
from app.exceptions import LLMError


class LLMClient:
    """Client for LLM-based issue analysis using LangChain."""
    
    def __init__(self):
        self.llm = None
        if settings.OPENAI_API_KEY:
            self.llm = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=settings.LLM_MODEL,
                temperature=0.7,
                max_tokens=2000
            )
    
    def _format_issues_as_documents(self, issues: List[dict]) -> List[Document]:
        """Convert issues to LangChain Document objects."""
        documents = []
        for issue in issues:
            body = issue.get("body", "") or "No description provided"
            if len(body) > 500:
                body = body[:500] + "..."
            
            content = f"""Title: {issue['title']}
Created: {issue['created_at']}
URL: {issue['html_url']}
Description: {body}"""
            
            doc = Document(
                page_content=content,
                metadata={
                    "id": issue.get("id"),
                    "title": issue.get("title"),
                    "url": issue.get("html_url")
                }
            )
            documents.append(doc)
        return documents
    
    def _chunk_documents(self, documents: List[Document], chunk_size: int = 25) -> List[List[Document]]:
        """Split documents into smaller chunks."""
        return [documents[i:i + chunk_size] for i in range(0, len(documents), chunk_size)]
    
    async def analyze(self, prompt: str, issues: List[dict]) -> str:
        """
        Analyze issues using LangChain with map-reduce pattern.
        Handles large issue sets by chunking and summarizing.
        """
        if not self.llm:
            raise LLMError("OpenAI API key not configured")
        
        if not issues:
            raise LLMError("No issues to analyze")
        
        documents = self._format_issues_as_documents(issues)
        
        if len(documents) <= 20:
            return await self._direct_analysis(prompt, documents)
        
        return await self._map_reduce_analysis(prompt, documents)
    
    async def _direct_analysis(self, prompt: str, documents: List[Document]) -> str:
        """Analyze a small set of issues directly."""
        context = "\n\n---\n\n".join([doc.page_content for doc in documents])
        
        analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an experienced open-source maintainer and software engineer.
You are analyzing GitHub issues for a repository. Provide clear, actionable insights based on the issues provided.
Be specific about patterns, priorities, and recommendations."""),
            ("user", """User Request: {user_prompt}

Here are the GitHub issues to analyze:

{context}

Please provide a comprehensive analysis addressing the user's request.""")
        ])
        
        chain = analysis_prompt | self.llm | StrOutputParser()
        
        try:
            result = await chain.ainvoke({
                "user_prompt": prompt,
                "context": context
            })
            return result
        except Exception as e:
            raise LLMError(f"LLM analysis failed: {str(e)}")
    
    async def _map_reduce_analysis(self, prompt: str, documents: List[Document]) -> str:
        """Analyze large issue sets using map-reduce pattern."""
        chunks = self._chunk_documents(documents, chunk_size=25)
        
        map_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are analyzing a batch of GitHub issues.
Summarize the key themes, common problems, and notable patterns in these issues.
Be concise but comprehensive. Focus on actionable insights."""),
            ("user", """Analyze these GitHub issues and identify key themes:

{context}

User's focus: {user_prompt}

Provide a concise summary (max 300 words) of the main themes and insights.""")
        ])
        
        map_chain = map_prompt | self.llm | StrOutputParser()
        
        chunk_summaries = []
        try:
            for i, chunk in enumerate(chunks):
                context = "\n\n---\n\n".join([doc.page_content for doc in chunk])
                summary = await map_chain.ainvoke({
                    "context": context,
                    "user_prompt": prompt
                })
                chunk_summaries.append(f"Batch {i+1} Summary:\n{summary}")
        except Exception as e:
            raise LLMError(f"LLM chunk analysis failed: {str(e)}")
        
        while len(chunk_summaries) > 5:
            chunk_summaries = await self._reduce_summaries(chunk_summaries, prompt)
        
        return await self._final_reduce(chunk_summaries, prompt)
    
    async def _reduce_summaries(self, summaries: List[str], prompt: str) -> List[str]:
        """Reduce multiple summaries into fewer summaries."""
        reduce_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are synthesizing multiple analysis summaries.
Combine the key insights, identify common patterns, and highlight priorities.
Be concise and focus on the most important findings."""),
            ("user", """Combine these batch summaries into a unified summary:

{summaries_text}

Focus on: {user_prompt}

Provide a concise synthesis (max 400 words).""")
        ])
        
        reduce_chain = reduce_prompt | self.llm | StrOutputParser()
        
        reduced = []
        batch_size = 5
        try:
            for i in range(0, len(summaries), batch_size):
                batch = summaries[i:i + batch_size]
                summaries_text = "\n\n---\n\n".join(batch)
                result = await reduce_chain.ainvoke({
                    "summaries_text": summaries_text,
                    "user_prompt": prompt
                })
                reduced.append(result)
        except Exception as e:
            raise LLMError(f"Summary reduction failed: {str(e)}")
        
        return reduced
    
    async def _final_reduce(self, summaries: List[str], prompt: str) -> str:
        """Final reduction to produce the analysis result."""
        final_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an experienced open-source maintainer providing the final analysis.
Synthesize all insights into a clear, actionable response.
Be specific about patterns, priorities, and recommendations."""),
            ("user", """I analyzed a large set of GitHub issues in batches. Here are the summaries:

{summaries_text}

Please provide a comprehensive final analysis addressing this request:
"{user_prompt}"

Include:
1. Key themes and patterns identified
2. Priority issues or areas needing attention
3. Specific recommendations for maintainers""")
        ])
        
        final_chain = final_prompt | self.llm | StrOutputParser()
        
        try:
            summaries_text = "\n\n---\n\n".join(summaries)
            result = await final_chain.ainvoke({
                "summaries_text": summaries_text,
                "user_prompt": prompt
            })
            return result
        except Exception as e:
            raise LLMError(f"Final analysis failed: {str(e)}")


# Singleton instance
llm_client = LLMClient()
