"""
Long Context Client for Production RAG Applications

This module provides a production-ready client for using long-context LLMs
as an alternative to traditional RAG systems.

Usage:
    config = LongContextConfig(model="claude-3-5-sonnet-20241022")
    analyzer = LongContextAnalyzer(config)
    result = analyzer.analyze_documents(
        query="What are the termination conditions?",
        documents=[contract_text]
    )
"""

import os
from dataclasses import dataclass
from typing import List, Dict, Optional
import anthropic
import tiktoken


@dataclass
class LongContextConfig:
    """Configuration for long context analysis."""
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 128_000
    # Leave 20% buffer for response + system prompt
    context_budget: int = 102_000  # 80% of max
    temperature: float = 0.1  # Consistent for analysis
    
    # Cost tracking (update with current pricing)
    input_cost_per_1k: float = 0.003  # $3/million for Claude 3.5
    output_cost_per_1k: float = 0.015
    
    def __post_init__(self):
        """Validate configuration."""
        if self.context_budget > self.max_tokens:
            raise ValueError("context_budget cannot exceed max_tokens")


class LongContextAnalyzer:
    """
    Production-grade analyzer using long-context LLMs.
    
    This is a simpler, more maintainable alternative to complex RAG systems
    for document corpora under ~100K tokens.
    """
    
    def __init__(self, config: Optional[LongContextConfig] = None):
        """
        Initialize the analyzer.
        
        Args:
            config: Configuration object. Uses defaults if not provided.
        """
        self.config = config or LongContextConfig()
        
        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable required")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        
        # Initialize tokenizer for cost estimation
        try:
            self.tokenizer = tiktoken.encoding_for_model("gpt-4")
        except Exception:
            # Fallback to cl100k_base
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count
        """
        return len(self.tokenizer.encode(text))
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate estimated API cost.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Estimated cost in USD
        """
        input_cost = input_tokens * self.config.input_cost_per_1k / 1000
        output_cost = output_tokens * self.config.output_cost_per_1k / 1000
        return input_cost + output_cost
    
    def analyze_documents(
        self, 
        query: str, 
        documents: List[str],
        system_prompt: Optional[str] = None
    ) -> Dict:
        """
        Analyze documents using long context.
        
        This method combines all documents into the context window and
        queries the LLM with the full context available.
        
        Args:
            query: User question or analysis request
            documents: List of document texts to analyze
            system_prompt: Optional system instructions for the LLM
            
        Returns:
            Dictionary containing:
                - response: The LLM's text response
                - input_tokens: Token count of input
                - output_tokens: Token count of output
                - cost_usd: Estimated API cost
                - context_utilization: Percentage of context window used
                
        Raises:
            ValueError: If documents exceed context budget
            anthropic.APIError: If API call fails
        """
        # Build context with document separators
        doc_sections = []
        for i, doc in enumerate(documents, 1):
            doc_sections.append(f"Document {i}:\n{doc}")
        
        context = "\n\n---\n\n".join(doc_sections)
        
        # Build full prompt
        full_prompt = f"""Context:
{context}

User Question: {query}

Provide a detailed analysis based on the context above."""
        
        # Check context budget
        token_count = self.count_tokens(full_prompt)
        if token_count > self.config.context_budget:
            raise ValueError(
                f"Context too large: {token_count} tokens exceeds "
                f"budget of {self.config.context_budget}. "
                f"Consider using RAG or reducing document count."
            )
        
        # Call LLM
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=4096,
            temperature=self.config.temperature,
            system=system_prompt or "You are a precise document analyzer. Answer based only on the provided context.",
            messages=[{"role": "user", "content": full_prompt}]
        )
        
        # Calculate metrics
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = self.estimate_cost(input_tokens, output_tokens)
        utilization = token_count / self.config.max_tokens
        
        return {
            "response": response.content[0].text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": round(cost, 4),
            "context_utilization": round(utilization, 2),
            "model_used": self.config.model
        }
    
    def batch_analyze(
        self,
        queries: List[str],
        documents: List[str],
        system_prompt: Optional[str] = None
    ) -> List[Dict]:
        """
        Run multiple queries against the same document set.
        
        Args:
            queries: List of queries to run
            documents: Documents to analyze
            system_prompt: Optional system instructions
            
        Returns:
            List of result dictionaries (one per query)
        """
        results = []
        total_cost = 0
        
        for query in queries:
            result = self.analyze_documents(query, documents, system_prompt)
            results.append(result)
            total_cost += result["cost_usd"]
        
        # Add summary
        return {
            "results": results,
            "total_cost_usd": round(total_cost, 4),
            "query_count": len(queries),
            "avg_cost_per_query": round(total_cost / len(queries), 4)
        }


# Example usage and testing
if __name__ == "__main__":
    # Example: Analyze a simple contract
    sample_docs = [
        """TERMINATION CLAUSE
        This agreement may be terminated by either party with 30 days written notice.
        However, if the service level falls below 99.9% uptime for 3 consecutive months,
        the client may terminate immediately without penalty.""",
        
        """PAYMENT TERMS
        Monthly fee of $5000 due on the 1st of each month.
        Late payments subject to 1.5% monthly service charge."""
    ]
    
    try:
        config = LongContextConfig()
        analyzer = LongContextAnalyzer(config)
        
        result = analyzer.analyze_documents(
            query="What are the termination conditions?",
            documents=sample_docs
        )
        
        print("Response:", result["response"])
        print(f"Cost: ${result['cost_usd']}")
        print(f"Context utilization: {result['context_utilization']*100:.1f}%")
        
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {e}")