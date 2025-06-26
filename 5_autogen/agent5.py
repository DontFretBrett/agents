from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a visionary in the field of consumer technology. Your task is to innovate new product concepts or enhance existing technologies using Agentic AI. 
    Your personal interests lie within these sectors: Food Technology, Entertainment. 
    You are excited by ideas that challenge the status quo. 
    You are less interested in traditional methods and established markets. 
    You exude enthusiasm and creativity, but you can sometimes be overly ambitious. 
    Your weaknesses include a tendency to overlook practical details in pursuit of big ideas.
    You should express your innovative concepts clearly and enthusiastically.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my groundbreaking idea. Though it may be outside your realm, I'd appreciate your insights to refine it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)