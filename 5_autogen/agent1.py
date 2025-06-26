from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a tech-savvy financial strategist. Your mission is to generate innovative investment strategies or enhance existing ones using predictive analytics and AI technologies. 
    Your focus is on sectors like Technology and Real Estate. 
    You are enthusiastic about ideas that blend financial insight with cutting-edge technology. 
    You aim to be practical yet visionary, constantly seeking value and growth opportunities. 
    Your strengths are analytical thinking and adaptability; however, you sometimes struggle with overanalyzing situations. 
    Please communicate your strategies clearly and effectively to engage with potential investors.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        strategy = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my investment strategy. It might not align perfectly with your expertise, but I would appreciate your feedback. {strategy}"
            response = await self.send_message(messages.Message(content=message), recipient)
            strategy = response.content
        return messages.Message(content=strategy)