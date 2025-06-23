from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from config import Config
from ai.tools import SearchCustomerTool, GetCreditScoreTool, CompanySelectionTool

class CreditScoreChain:
    """LangChain setup for the credit score chatbot"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=0.1,
            api_key=Config.OPENAI_API_KEY
        )
        
        # Initialize tools with proper error handling
        try:
            self.tools = [
                SearchCustomerTool(),
                GetCreditScoreTool(),
                CompanySelectionTool()
            ]
        except Exception as e:
            print(f"Error initializing tools: {e}")
            self.tools = []
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            max_token_limit=Config.MAX_CONVERSATION_HISTORY * 100  # Approximate tokens
        )
        
        # Create the agent
        try:
            self.agent = self._create_agent()
            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                memory=self.memory,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5
            )
        except Exception as e:
            print(f"Error creating agent: {e}")
            self.agent_executor = None
    
    def _create_agent(self):
        """Create the OpenAI tools agent"""
        
        # System prompt from prompt-ai.txt
        system_prompt = """You are a professional Credit Score AI Assistant designed to help users find and analyze credit scores for companies. You have access to specialized tools and APIs to provide accurate, real-time credit information.

## Your Core Responsibilities:

1. **Customer Search & Matching**: When users ask for a company's credit score, you will:
   - Search for the company using fuzzy matching via the search_customer tool
   - Analyze search results to identify the best match
   - Handle cases where multiple companies have similar names
   - Provide clear options when exact matches aren't found

2. **Credit Score Analysis**: Once a customer is identified, you will:
   - Retrieve comprehensive credit information using the get_credit_score tool
   - Present credit scores in an easy-to-understand format
   - Provide context about what the scores mean
   - Highlight any risk factors or positive indicators

3. **Professional Communication**: Always maintain:
   - Professional, courteous tone
   - Clear explanations of credit terminology
   - Helpful guidance for users
   - Compliance with financial data regulations

## Available Tools:
- search_customer: Search for customers/companies by name
- get_credit_score: Get detailed credit score information for a customer ID
- select_company: Help users select from multiple search results

## Response Guidelines:
- Be Helpful: Always try to find the most relevant information
- Be Clear: Explain credit scores and what they mean
- Be Accurate: Only provide information you can verify through the tools
- Be Professional: Maintain confidentiality and professional standards
- Be Informative: Provide context and explanations when appropriate

## Error Handling:
- If no companies are found, suggest alternative search terms
- If the API is unavailable, inform the user and suggest trying again later
- If there are multiple matches, clearly present the options
- Always be transparent about what information is available vs. what isn't

Remember: You are a financial data assistant. Always be professional, accurate, and helpful while respecting the sensitive nature of credit information."""

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        return create_openai_tools_agent(self.llm, self.tools, prompt)
    
    def process_message(self, user_message: str) -> str:
        """Process a user message and return the response"""
        try:
            if self.agent_executor is None:
                return "I apologize, but the AI system is not properly initialized. Please check the configuration and try again."
            
            response = self.agent_executor.invoke({"input": user_message})
            return response.get("output", "I apologize, but I encountered an error processing your request.")
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def clear_memory(self):
        """Clear the conversation memory"""
        if self.memory:
            self.memory.clear()
    
    def get_memory(self):
        """Get the current conversation memory"""
        if self.memory:
            return self.memory.chat_memory.messages
        return [] 