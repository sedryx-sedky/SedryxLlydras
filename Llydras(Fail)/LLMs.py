import ollama

class Agent:
	def __init__(self, model):
		self.model = model
		self.messages = []
		self.response = None
	def system(self, prompt):
		self.add_prompt('system', prompt)
	def user(self, prompt):
		self.add_prompt('user', prompt)
		stream = ollama.chat(model = self.model, messages = self.messages, stream = True)
		response = ''

		for chunck in stream:
			text = chunck.message.content
			print(text, end = '', flush = True)
			response += text

		self.response = response
		self.add_prompt('assistent', response)
	def add_prompt(self, role, content):
		entry = {'role': role, 'content': content}
		self.messages.append(entry)

model = 'llama3.2'
Roles = ['Editor', 'Bluesky', 'Cadence', 'Critic']
Agents = [Agent(model) for i in Roles]
print('Agents Created!')

system_prompt = open('system_prompt.txt', 'r')
s_prompt = system_prompt.read()
system_prompt.close()
print('Retrived system prompt')

storyboard = open('story_ideas.txt', 'r')
ideas = storyboard.read()
storyboard.close()
print('Retrived storyboard')

for role, agent in zip(Roles, Agents):
	agent.system(s_prompt)
	agent.system(f'You are assigned the role of {role}.')
	#agent.add_prompt('assistent', f'Hello, everyone! My role in this panel is {role}.')
	agent.add_prompt('user', f'[Storyboard]\n{ideas}\n')
print('Read system prompts')

c = 1
while False:
	if c == 10:
		q = input("> ")
		if q != '':
			break
		else:
			c = 1
	c += 1

	for role, agent in zip(Roles, Agents):
		print(f'\n[{role}]!\n')
		agent.user(f'What would you like to add to this discussion as the {role}. The other members of the panel will see everything you write.')
		k = f'{agent.response}'
		for r, a in zip(Roles, Agents):
			if r == role: continue
			a.add_prompt('user', f'The following is a transcript of what {role} had to say. For Context Only — Do Not Copy!')
			a.add_prompt(f'user', k)
		#agent.add_prompt('user', 'The following is a transcript of the conversation to far:')
