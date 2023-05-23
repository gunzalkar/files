import config
import openai
import os
openai.api_key = "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"
def openAIQuery(query):
	response = openai.Completion.create(
		model="text-davinci-003",
		prompt=query,
		temperature=0.7,
		max_tokens=1000,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0
	)
	if 'choices' in response:
		if len(response['choices'])>0:
			answer = response['choices'][0]['text']
		else:
			answer = 'You beat the AI! Wohoo!'
	else:
		answer = 'You beat the AI! Wohoo!'
	return answer
