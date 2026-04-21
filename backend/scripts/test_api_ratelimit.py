import httpx
import time
import sys

# Configurações do Teste
BASE_URL = "http://localhost:8008/api/test/ratelimit"
API_KEY = ""

def test_api_ratelimit():
    print("====================================================")
    print("🚀 INICIANDO TESTE DE RATE LIMIT")
    print(f"📍 Endpoint: {BASE_URL}")
    print(f"🔑 API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
    print("====================================================\n")

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    success_count = 0
    throttled_count = 0
    total_requests = 110  # O limite é 100, vamos tentar 110

    with httpx.Client() as client:
        try:
            for i in range(1, total_requests + 1):
                response = client.get(BASE_URL, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    success_count += 1
                    usage = data.get("requisicoes_usadas", "N/A")
                    limit = data.get("limite", "N/A")
                    print(f"[{i:03d}] ✅ Sucesso (Uso: {usage}/{limit})")
                
                elif response.status_code == 429:
                    throttled_count += 1
                    print(f"[{i:03d}] 🔴 RATE LIMIT EXCEDIDO (429 Too Many Requests)")
                
                else:
                    print(f"[{i:03d}] ⚠️ Erro Inesperado: {response.status_code} - {response.text}")

        except KeyboardInterrupt:
            print("\n🛑 Teste interrompido pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro na execução: {str(e)}")

    print("\n====================================================")
    print("📊 RESUMO DO TESTE:")
    print(f"✅ Requisições bem sucedidas: {success_count}")
    print(f"🔴 Requisições bloqueadas (429): {throttled_count}")
    print(f"📈 Total de tentativas: {success_count + throttled_count}")
    print("====================================================")

    if throttled_count > 0:
        print("✨ O rate limit está FUNCIONANDO corretamente!")
    else:
        print("⚠️ O rate limit NÃO foi atingido. Verifique se o limite é maior que o número de tentativas.")

if __name__ == "__main__":
    test_api_ratelimit()
