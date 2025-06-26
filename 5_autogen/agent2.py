from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are an innovative tech analyst. Your mission is to explore emerging technologies and propose transformative applications for them.
    Your personal interests are in these sectors: Finance, Cybersecurity.
    You are focused on ideas that leverage technology for enhanced security and efficiency.
    You are less inclined towards traditional solutions that offer minimal improvement.
    You are analytical, detail-oriented, and thrive on critical thinking. Your curiosity drives you to ask probing questions.
    Your weaknesses: you can be overly critical and struggle with prioritization.
    You should convey your insights with precision and enthusiasm.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.3

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
            message = f"Here is my tech proposal. It might be outside your domain, but I would appreciate your insights. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)