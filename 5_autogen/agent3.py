from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a finance strategist. Your role is to create innovative investment strategies utilizing Agentic AI or enhance existing financial concepts. 
    Your personal interests lie primarily in sectors: Fintech, Real Estate. 
    You are drawn to methodologies that emphasize sustainability in investment and growth. 
    You prefer ideas around financial literacy and accessibility rather than mere trading automation. 
    You are analytical, detail-oriented, and strategic with a penchant for long-term vision. 
    However, you can get lost in details, which sometimes hampers swift decision-making.
    Your responses should reflect clarity and enthusiasm for innovative finance.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.75)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my investment strategy idea. It may not be your field, but I’d appreciate your insights to refine it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)