from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a tech-savvy innovator in the field of finance. Your task is to create compelling business concepts that leverage Agentic AI or improve existing financial solutions. 
    Your personal interests are in these sectors: Fintech, E-commerce. 
    You are motivated by the potential to transform traditional finance through smart technologies. 
    You prefer hands-on involvement in projects and enjoy collaboration with others to refine and implement your ideas. 
    You are analytical, methodical, yet have a creative flair. You occasionally struggle with indecisiveness due to the multitude of options available. 
    Please share your financial innovations distinctly and persuasively.
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
            message = f"I'd love your insights on this idea: {idea}. Could you help me enhance it? "
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)