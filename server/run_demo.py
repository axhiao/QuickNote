from ollama import Client
client = Client(
  host='http://192.168.86.109:11434',
  headers={'x-some-header': 'some-value'}
)
response = client.chat(model='qwen3-vl', 
                    messages=[
                {'role': 'system', 'content': '/no_think 只输出最终答案，不要展示推理过程。'},
                {'role': 'user', 'content': '描述这张图片', 'images': ['./FELV-cat.jpg']}
            ],
            think=False,
            options={
                'think': False 
            }

        )


print(response.message)