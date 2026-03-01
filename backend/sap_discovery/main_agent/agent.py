"""Main conversational agent creation."""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_openai import ChatOpenAI
from sap_discovery.main_agent.prompts import SYSTEM_PROMPT
from sap_discovery.main_agent.tools import (
    run_sap_discovery,
    export_to_excel,
    display_process_report
)
from sap_discovery.main_agent.search_tools import web_search
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)


async def create_main_agent(memory):
    """Create the main conversational SAP assistant agent.

    Args:
        memory: AsyncPostgresSaver checkpointer for persistent memory

    Returns:
        Configured LangChain agent with persistent PostgreSQL memory
    """
    main_llm = ChatOpenAI(model='gpt-4o', temperature=0)

    agent = create_agent(
        model=main_llm,
        tools=[run_sap_discovery, export_to_excel, display_process_report, web_search],
        checkpointer=memory,
        system_prompt=SYSTEM_PROMPT,
        middleware=[
            SummarizationMiddleware(
                model='gpt-4o-mini',
                trigger=('messages', 10),
                keep=('messages', 10),
            )
        ],
    )

    logger.info("Main agent created with PostgreSQL memory")
    return agent