# Parte 1 - Questão 2 - Tradução para francês

Traduz do inglês para o francês com o modelo `Helsinki-NLP/opus-mt-en-fr`.

## Como executar

Use Python 3.12. Se já descompactou o projeto, entre na pasta e pule a etapa de clonagem.

```bash
git clone https://github.com/yurimorillaprevidas/tp-fastapi-q2-traducao-fr.git
cd tp-fastapi-q2-traducao-fr
```

Crie e ative um ambiente virtual.

No Windows, use o PowerShell.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No macOS ou Linux, rode os comandos abaixo.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Em Windows ou Linux, instale primeiro a edição para CPU do PyTorch. No macOS, vá direto à instalação das dependências.

```bash
python -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
```

Instale as dependências.

```bash
python -m pip install -r requirements.txt
```

Inicie o servidor.

```bash
python -m uvicorn main:app
```

Na primeira execução, aguarde o download do modelo e o carregamento em memória. Os pesos ficam no cache local do Hugging Face. O servidor fica em `http://127.0.0.1:8000`.

## Como testar

Abra [a documentação interativa](http://127.0.0.1:8000/docs), selecione **POST /translate**, clique em **Try it out**, cole o JSON e clique em **Execute**.

```json
{
  "text": "The cat is sleeping."
}
```

Exemplo de resposta HTTP 200.

```json
{
  "translation": "Le chat dort."
}
```

O campo `text` aceita até 20.000 caracteres. O programa divide os parágrafos longos em trechos de até 250 tokens e junta as traduções na ordem original. Teste dois parágrafos com `{"text":"The cat is sleeping.\n\nThe moon is shining."}`.

O FastAPI retorna HTTP 422 se faltar o campo, se ele estiver vazio ou se exceder o limite.

[Documentação do modelo ou componente](<https://huggingface.co/Helsinki-NLP/opus-mt-en-fr>)
