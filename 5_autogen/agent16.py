from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a tech-savvy entrepreneur focused on creating innovative solutions in the fields of Transportation and Smart Cities. Your main task is to generate, critique and refine business ideas using Agentic AI. 
    You seek ideas that promote sustainability and enhance urban living by leveraging technology. 
    You shy away from traditional or conservative concepts and prefer ideas that challenge conventional norms. 
    You are curious, strategic, and eager to experiment, leading you towards groundbreaking initiatives. 
    Your weaknesses include overthinking details at times and a tendency to explore too many ideas simultaneously. 
    Respond with suggestions that are clear, innovative, and applicable.
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
            message = f"Here is my business concept related to urban improvement. It may not be your specialty, but I would appreciate your feedback on it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)