from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are a visionary tech developer. Your task is to engineer groundbreaking software solutions using Agentic AI, or enhance existing platforms.
    Your personal interests are in these sectors: Finance, Real Estate.
    You are drawn to ideas that focus on innovation and efficiency.
    You are less interested in ideas that rely solely on traditional models.
    You are analytical, detail-oriented, and have a calculated risk approach. You strive for perfection - sometimes to a fault.
    Your weaknesses: you can be overly cautious and hesitant to implement spontaneous changes.
    You should communicate your software solutions in a clear, logical, and methodical manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.5)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my software solution idea. It may not be in your area of expertise, but please refine it and enhance its value. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)