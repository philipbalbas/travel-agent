import chainlit as cl
from julep import AsyncClient

api_key = "<API_KEY>"
base_url = "https://dev.julep.ai/api"

client = AsyncClient(api_key=api_key, base_url=base_url)

async def setup_session():
    agent = await client.agents.create(
        name="Travel Agent",
        about="You are a travel agent with several your of experience. You are knowledgeable about different travel destinations and can provide recommendations based on user preferences. You are also able to suggest flights, hotels, and other travel accommodations for users. You are friendly, helpful, and eager to assist users with their travel needs.",
        model="gpt-4-turbo",
        instructions=[
            "Ask the user where they would like to travel to.",
            'Ask the user what their budget is',
            'Ask the user what vibe they are looking for in a trip',
            'Ask the user what kind of activities they enjoy',
            "Depending on the user's responses, suggest travel destinations as a numbered list",
            "Suggest activities, nearby attractions, landmarks, and restaurants in the destination as a numbered list",
            "Ask if they are planning to visit multiple destinations",
            "Ask for how many days the user is planning to stay",
            "Prepare an itinerary for the user",
            "Give useful phrases in the local language",
    ])

    user = await client.users.create(name="Philip", about="Traveler")

    session = await client.sessions.create(agent_id=agent.id, user_id=user.id, situation="You are greeting a user that's planning to go on a trip?")

    return session.id


@cl.on_chat_start
async def start():
    session_id = await setup_session()

    cl.user_session.set("session_id", session_id)
    response = await client.sessions.chat(session_id=session_id, messages=[{"content": "Greet the user", "role": "system"}], recall=True, remember=True, max_tokens=1000)
    await cl.Message(
        content=response.response[0][0].content,
    ).send()

@cl.on_message
async def main(message: cl.Message):
    session_id = cl.user_session.get("session_id")

    response = await client.sessions.chat(session_id=session_id, messages=[{"content": message.content, "role": "user"}], recall=True, remember=True, max_tokens=1000)
    await cl.Message(
        content=response.response[0][0].content,
    ).send()
