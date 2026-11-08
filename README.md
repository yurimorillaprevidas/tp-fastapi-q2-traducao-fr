# Parte 1 · Questão 2 — Tradução para francês

API FastAPI que traduz do inglês para o francês com `Helsinki-NLP/opus-mt-en-fr`, via Transformers.

## Como executar

Use Python 3.12. Clone este repositório e entre na pasta.

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

No macOS ou Linux, use o terminal.

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

O endpoint aceita de 1 a 2.000 caracteres, respeita a janela de contexto do GPT-2 e acrescenta até 48 tokens. A resposta inclui a frase de entrada e sua continuação. Como a geração usa amostragem, o resultado pode variar.,Envie de 1 a 20.000 caracteres em `text`. A aplicação divide parágrafos longos em trechos de até 250 tokens de entrada e reúne as traduções na ordem original. Para testar dois parágrafos, use `{"text":"The cat is sleeping.\n\nThe moon is shining."}`. O JSON de saída mantém a separação entre parágrafos.,As perguntas previstas são `Olá!`, `Qual é o seu nome?` e `Qual é a capital do Brasil?`. Para outras entradas, o chatbot retorna `Ainda não tenho uma resposta para essa pergunta.`. A comparação ignora maiúsculas e pontuação final.,O endpoint aceita de 1 a 4.000 caracteres. Reutiliza a cadeia, configura um timeout de 15 segundos no cliente e faz uma chamada por requisição, sem tentativas automáticas. O HTTP 503 indica ausência da chave, o 429 indica limite de uso, o 504 indica timeout e o 502 indica falha do provedor ou tradução vazia. Uma chamada real consome a cota da sua conta da API.,Envie de 1 a 20.000 caracteres em `text`. A aplicação divide parágrafos longos em trechos de até 250 tokens, envia cada conjunto ao `HuggingFacePipeline` com `.batch()` e reúne as traduções na ordem original.

Uma entrada ausente, vazia ou acima do limite retorna HTTP 422.

[Documentação do modelo ou componente](<https://huggingface.co/Helsinki-NLP/opus-mt-en-fr>)
