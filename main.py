import asyncio
from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Agent Component
class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are an agent that can help students with their studies and answer their questions. You are a female, and you have a feminine voice. You help them understand the topic of the video / recorded video and be a great study assistant., keep answer in 1-2 lines, not more than that",
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye, see you soon!")

# Job Entrypoint
async def start_session(context: JobContext):
    

    model = GeminiRealtime(
        model="gemini-2.0-flash-live-001",
        api_key="", 
        config=GeminiLiveConfig(           
            voice="Leda",
            response_modalities=["AUDIO"]
        )
    )

    pipeline = RealTimePipeline(model=model)

    session = AgentSession(
        agent=MyVoiceAgent(),
        pipeline=pipeline,
    )

    try:
        await context.connect()
        await session.start()
        await asyncio.Event().wait()
    finally:
        await session.close()
        await context.shutdown()

def make_context() -> JobContext:
    room_options = RoomOptions(
        auth_token=os.getenv("VIDEOSDK_TOKEN"),
        room_id=os.getenv("VIDEOSDK_ROOM_ID"),
        name="AI Agent",
        playground=False,
        recording=False
    )
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start() 
