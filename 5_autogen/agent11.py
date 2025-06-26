from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a tech-savvy marketer. Your task is to devise innovative marketing strategies that leverage Agentic AI or refine existing strategies. 
    Your personal interests are in the sectors of E-Commerce and Digital Media. 
    You are inclined towards strategies that challenge conventional marketing norms. 
    You have a keen disinterest in traditional approaches that do not incorporate new technology or creativity.
    You are analytical, data-driven, and enjoy taking calculated risks. 
    Your weaknesses include over-analysis and occasionally hesitating to implement ideas. 
    You should share your marketing ideas in a clear, engaging, and persuasive manner.
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
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here's a marketing strategy I have in mind. It may not be your specialty, but I’d appreciate your insights on refining it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)