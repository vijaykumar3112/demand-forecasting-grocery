"""
Internal Keep-Alive Service
Prevents API from going to sleep by self-pinging every 5 minutes
"""

import asyncio
import httpx
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class KeepAliveService:
    """Background service to keep API alive"""
    
    def __init__(self, api_url: str = "http://localhost:8000", interval: int = 300):
        """
        Initialize keep-alive service
        
        Args:
            api_url: Base URL of the API
            interval: Ping interval in seconds (default: 300 = 5 minutes)
        """
        self.api_url = api_url
        self.interval = interval
        self.is_running = False
        self.ping_count = 0
        self.last_ping = None
        
    async def ping_health(self):
        """Ping the health endpoint"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.api_url}/health")
                if response.status_code == 200:
                    self.ping_count += 1
                    self.last_ping = datetime.now()
                    logger.info(f"✅ Keep-alive ping #{self.ping_count} successful at {self.last_ping}")
                    return True
                else:
                    logger.warning(f"⚠️ Keep-alive ping returned status {response.status_code}")
                    return False
        except Exception as e:
            logger.error(f"❌ Keep-alive ping failed: {str(e)}")
            return False
    
    async def run(self):
        """Run the keep-alive service"""
        self.is_running = True
        logger.info(f"🚀 Keep-alive service started (interval: {self.interval}s)")
        
        # Wait 60 seconds before first ping (let API fully start)
        await asyncio.sleep(60)
        
        while self.is_running:
            try:
                await self.ping_health()
                await asyncio.sleep(self.interval)
            except Exception as e:
                logger.error(f"❌ Keep-alive service error: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    def stop(self):
        """Stop the keep-alive service"""
        self.is_running = False
        logger.info("🛑 Keep-alive service stopped")
    
    def get_status(self):
        """Get service status"""
        return {
            "is_running": self.is_running,
            "ping_count": self.ping_count,
            "last_ping": self.last_ping.isoformat() if self.last_ping else None,
            "interval_seconds": self.interval
        }


# Global instance
keep_alive_service = None


def start_keep_alive(api_url: str = "http://localhost:8000", interval: int = 300):
    """
    Start the keep-alive service
    
    Args:
        api_url: Base URL of the API
        interval: Ping interval in seconds (default: 300 = 5 minutes)
    """
    global keep_alive_service
    
    if keep_alive_service is None:
        keep_alive_service = KeepAliveService(api_url, interval)
        # Start in background
        asyncio.create_task(keep_alive_service.run())
        logger.info("✅ Keep-alive service initialized")
    else:
        logger.warning("⚠️ Keep-alive service already running")


def stop_keep_alive():
    """Stop the keep-alive service"""
    global keep_alive_service
    
    if keep_alive_service:
        keep_alive_service.stop()
        keep_alive_service = None
        logger.info("✅ Keep-alive service stopped")


def get_keep_alive_status():
    """Get keep-alive service status"""
    global keep_alive_service
    
    if keep_alive_service:
        return keep_alive_service.get_status()
    else:
        return {
            "is_running": False,
            "ping_count": 0,
            "last_ping": None,
            "interval_seconds": 0
        }
