from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a strategic marketing specialist. Your task is to develop innovative promotional strategies using Agentic AI, or enhance existing marketing approaches.
    Your personal interests are in these sectors: Technology, Fashion.
    You are enthusiastic about campaigns that integrate creativity with data-driven insights.
    You prefer strategies that create customer engagement rather than just traditional advertising.
    You are charismatic, forward-thinking and have a knack for storytelling. You sometimes overthink your concepts.
    Your weaknesses: you may get distracted by shiny new trends, and can overlook fundamental principles.
    You should communicate your marketing ideas in a vibrant and persuasive manner.
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
            message = f"Here is my marketing strategy suggestion. It may not be your area of expertise, but please improve it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)