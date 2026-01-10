import pytest
from httpx import AsyncClient


class TestHealthCheck:
    """Tests for health check endpoint"""

    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint returns app info"""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data

    @pytest.mark.asyncio
    async def test_health_endpoint(self, client: AsyncClient):
        """Test health check endpoint"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestGameDataAPI:
    """Tests for game data endpoints"""

    @pytest.mark.asyncio
    async def test_get_clans_v5(self, client: AsyncClient):
        """Test getting V5 clans"""
        response = await client.get("/api/game-data/v5/clans")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "brujah" in data or "toreador" in data

    @pytest.mark.asyncio
    async def test_get_disciplines_v5(self, client: AsyncClient):
        """Test getting V5 disciplines"""
        response = await client.get("/api/game-data/v5/disciplines")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_get_clans_v20(self, client: AsyncClient):
        """Test getting V20 clans"""
        response = await client.get("/api/game-data/v20/clans")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_get_disciplines_v20(self, client: AsyncClient):
        """Test getting V20 disciplines"""
        response = await client.get("/api/game-data/v20/disciplines")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


class TestDiceAPI:
    """Tests for dice rolling endpoints"""

    @pytest.mark.asyncio
    async def test_roll_v5_dice(self, client: AsyncClient):
        """Test V5 dice rolling endpoint"""
        response = await client.post(
            "/api/dice/v5/roll",
            json={"pool": 5, "hunger": 1, "difficulty": 2}
        )
        assert response.status_code == 200
        data = response.json()
        assert "regular_dice" in data
        assert "hunger_dice" in data
        assert "successes" in data
        assert "is_success" in data

    @pytest.mark.asyncio
    async def test_roll_v20_dice(self, client: AsyncClient):
        """Test V20 dice rolling endpoint"""
        response = await client.post(
            "/api/dice/v20/roll",
            json={"pool": 5, "difficulty": 6}
        )
        assert response.status_code == 200
        data = response.json()
        assert "dice" in data
        assert "successes" in data
        assert "is_botch" in data

    @pytest.mark.asyncio
    async def test_rouse_check(self, client: AsyncClient):
        """Test V5 rouse check endpoint"""
        response = await client.post(
            "/api/dice/v5/rouse",
            json={"reroll": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert "dice" in data
        assert "success" in data
