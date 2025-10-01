@echo off
echo Testando POST com curl...
curl -X POST http://localhost:8000/api/v1/locations ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"Teste Curl\"}" ^
  -v
echo.
echo Teste concluido.
pause

