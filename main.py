import asyncio, os
from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig


class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant that can answer questions and help with tasks.")
    async def on_enter(self): await self.session.say("Hello! How can I help?")
    async def on_exit(self): await self.session.say("Goodbye!")
    
    
async def start_session(context: JobContext):
    # Initialize Model
    model = GeminiRealtime(
        model="gemini-2.0-flash-live-001",
        api_key=os.getenv("GOOGLE_API_KEY"), 
        config=GeminiLiveConfig(           
            voice="Leda", # Puck, Charon, Kore, Fenrir, Aoede, Leda, Orus, and Zephyr.
            response_modalities=["AUDIO"]
        )
    )


    # Create pipeline
    pipeline = RealTimePipeline(
        model=model
    )

    session = AgentSession(
        agent=MyVoiceAgent(),
        pipeline=pipeline
    )

    try:
        await context.connect()
        await session.start()
        await asyncio.Event().wait()
    finally:
        # Clean up resources when done
        await session.close()
        await context.shutdown()

def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id=os.getenv(""),
        auth_token=os.getenv("VIDEOSDK_AUTH_TOKEN"),
        name="VideoSDK Realtime Agent",
        playground=True
    )

    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()