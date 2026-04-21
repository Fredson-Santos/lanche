from fastapi import APIRouter, Depends
from app.api.deps import verify_api_key
from app.models.api_key import APIKey

router = APIRouter()

@router.get("/ratelimit")
async def test_ratelimit(api_key: APIKey = Depends(verify_api_key)):
    """
    Endpoint de teste para verificar o rate limit de API Keys.
    Requer uma API Key válida no header Authorization: Bearer <KEY>
    """
    return {
        "status": "success",
        "message": "API Key válida e dentro do limite",
        "api_key_id": api_key.id,
        "descricao": api_key.descricao,
        "requisicoes_usadas": api_key.requisicoes_usadas,
        "limite": api_key.limite_requisicoes
    }
