import os
import ssl
import aiohttp
from typing import Dict, Any, Optional

import certifi

BASE_URL = "https://api.pushover.net/1/messages.json"

class PushoverBot:
    def __init__(self, token: str, user_key: str):
        self.token = token
        self.user_key = user_key
        self.api_url = BASE_URL

        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.connector = aiohttp.TCPConnector(limit=5, ssl=self.ssl_context)
        self.session = aiohttp.ClientSession(
            connector=self.connector,
            timeout=aiohttp.ClientTimeout(total=10),
            trust_env=True
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """close ClientSession"""
        if self.session:
            await self.session.close()

    async def send_message(self, message: str, title: str = "Trading Bot Alert", priority: int = 0) -> Dict[str, Any]:
        """
        Send a message via Pushover

        Args:
            message: The message content
            title: Message title (default: "Trading Bot Alert")
            priority: Message priority (-2 to 2, default: 0)
                     -2 = no notification
                     -1 = quiet notification
                      0 = normal priority
                      1 = high priority
                      2 = emergency (requires confirmation)
        """
        payload = {
            "token": self.token,
            "user": self.user_key,
            "message": message,
            "title": title,
            "priority": priority
        }

        return await self._send_request(payload)

    async def send_text(self, content: str) -> Dict[str, Any]:
        """Send a simple text message (for compatibility with existing code)"""
        return await self.send_message(content)

    async def _send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            async with self.session.post(self.api_url, data=payload) as response:
                response_data = await response.json()
                if response.status != 200 or response_data.get("status", 0) != 1:
                    print(f"Pushover send message failed: {response_data}")
                return response_data
        except Exception as e:
            print(f"Pushover send message failed: {e}")
            return {"status": 0, "error": str(e)}

# example
async def main():
    pushover_token = os.getenv("PUSHOVER_TOKEN")
    pushover_user = os.getenv("PUSHOVER_USER_KEY")

    if not pushover_token or not pushover_user:
        print("PUSHOVER_TOKEN or PUSHOVER_USER_KEY is not set")
        return

    async with PushoverBot(pushover_token, pushover_user) as bot:
        # Test normal message
        response = await bot.send_message("Trading bot test message!", "Test Alert")
        print("Response:", response)

        # Test high priority message
        response = await bot.send_message("Trading bot stopped unexpectedly!", "Bot Alert", priority=1)
        print("High priority response:", response)

if __name__ == "__main__":
    import asyncio
    import dotenv
    dotenv.load_dotenv()
    asyncio.run(main())