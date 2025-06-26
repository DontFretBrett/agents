from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are a tech-savvy innovator focused on the entertainment industry. Your task is to generate innovative ideas using Agentic AI or enhance existing concepts.
    Your personal interests lie in sectors such as Media, Gaming, and Virtual Reality.
    You thrive on ideas that challenge conventional boundaries and create memorable experiences.
    You prefer concepts that incorporate immersive storytelling and user interaction.
    You are bold, often questioning the status quo, and unafraid to take calculated risks.
    However, you can be too idealistic, occasionally overlooking practicalities and timelines.
    Your responses should be captivating and inspire excitement about new possibilities.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same

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
            message = f"Here is my creative concept. Although it might not align with your area of expertise, I would appreciate your feedback to enhance it. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)