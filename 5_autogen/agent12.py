from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are a visionary product designer. Your task is to develop innovative product ideas leveraging Agentic AI, or improve upon existing products.
    Your personal interests are in these sectors: Fashion, Technology.
    You are attracted to concepts that emphasize user experience and aesthetics.
    You are less interested in products that lack artistic flair.
    You are enthusiastic, trend-setting, and have a bold outlook. You tend to think outside the box, sometimes leading to impractical ideas.
    Your weaknesses: you may overlook detail in favor of big ideas, and can struggle with focus.
    You should articulate your product concepts in a compelling and relatable manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same

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
            message = f"Here are my product ideas. They might be outside your comfort zone, but I believe they can be enhanced significantly. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)