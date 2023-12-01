import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextEmbedding
from semantic_kernel.connectors.memory.chroma import ChromaMemoryStore
import os
import shutil
import asyncio

api_key="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"

kernel = sk.Kernel()
kernel.add_text_completion_service("openai-completion", OpenAIChatCompletion("gpt-3.5-turbo-0301", api_key))
kernel.add_text_embedding_generation_service("openai-embedding", OpenAITextEmbedding("text-embedding-ada-002", api_key))

dir_path = "memories"
shutil.rmtree(dir_path)
print("Memory cleared and reset")
kernel.register_memory_store(memory_store=ChromaMemoryStore(persist_directory='memories'))

strength_questions = ["What unique recipes or ingredients does the pizza shop use?","What are the skills and experience of the staff?","Does the pizza shop have a strong reputation in the local area?","Are there any unique features of the shop or its location that attract customers?", "Does the pizza shop have a strong reputation in the local area?", "Are there any unique features of the shop or its location that attract customers?"]
weakness_questions = ["What are the operational challenges of the pizza shop? (e.g., slow service, high staff turnover)","Are there financial constraints that limit growth or improvements?","Are there any gaps in the product offering?","Are there customer complaints or negative reviews that need to be addressed?"]
opportunities_questions = ["Is there potential for new products or services (e.g., catering, delivery)?","Are there under-served customer segments or market areas?","Can new technologies or systems enhance the business operations?","Are there partnerships or local events that can be leveraged for marketing?"]
threats_questions = ["Who are the major competitors and what are they offering?","Are there potential negative impacts due to changes in the local area (e.g., construction, closure of nearby businesses)?","Are there economic or industry trends that could impact the business negatively (e.g., increased ingredient costs)?","Is there any risk due to changes in regulations or legislation (e.g., health and safety, employment)?"]

strengths = [ "Unique garlic pizza recipe that wins top awards","Owner trained in Sicily at some of the best pizzerias","Strong local reputation","Prime location on university campus" ]
weaknesses = [ "High staff turnover","Floods in the area damaged the seating areas that are in need of repair","Absence of popular calzones from menu","Negative reviews from younger demographic for lack of hip ingredients" ]
opportunities = [ "Untapped catering potential","Growing local tech startup community","Unexplored online presence and order capabilities","Upcoming annual food fair" ]
threats = [ "Competition from cheaper pizza businesses nearby","There's nearby street construction that will impact foot traffic","Rising cost of cheese will increase the cost of pizzas","No immediate local regulatory changes but it's election season" ]

async def save_information_async(kernel, memoryCollectionName, strength_questions, strengths):
    for i in range(len(strengths)):
        await kernel.memory.save_information_async(memoryCollectionName, id=f"strength-{i}", text=f"Internal business strength (S in SWOT) that makes customers happy and satisfied Q&A: Q: {strength_questions[i]} A: {strengths[i]}")

memoryCollectionName = "SWOT"

async def save_memory():
    for i in range(len(strengths)):
        await kernel.memory.save_information_async(memoryCollectionName, id=f"strength-{i}", text=f"Internal business strength (S in SWOT) that makes customers happy and satisfied Q&A: Q: {strength_questions[i]} A: {strengths[i]}")
    for i in range(len(weaknesses)):
        await kernel.memory.save_information_async(memoryCollectionName, id=f"weakness-{i}", text=f"Internal business weakness (W in SWOT) that makes customers unhappy and dissatisfied Q&A: Q: {weakness_questions[i]} A: {weaknesses[i]}")
    for i in range(len(opportunities)):
        await kernel.memory.save_information_async(memoryCollectionName, id=f"opportunity-{i}", text=f"External opportunity (O in SWOT) for the business to gain entirely new customers Q&A: Q: {opportunities_questions[i]} A: {opportunities[i]}")
    for i in range(len(threats)):
        await kernel.memory.save_information_async(memoryCollectionName, id=f"threat-{i}", text=f"External threat (T in SWOT) to the business that impacts its survival Q&A: Q: {threats_questions[i]} A: {threats[i]}")
    
asyncio.run(save_memory())

# potential_question = "What are the easiest ways to make more money?"
# counter = 0

# async def retrieve_memory():
#     memories = await kernel.memory.search_async(memoryCollectionName,potential_question, limit=5, min_relevance_score=0.5)
#     print(memories)
#     return memories

# memories = asyncio.run(retrieve_memory())

# for memory in memories:
#     if counter == 0:
#         related_memory = memory.text
#     counter += 1
#     print(f"Similarity result {counter}:\n  >> ID: {memory.id}\n  Text: {memory.text}  Relevance: {memory.relevance}\n")

what_if_scenario = "How can the business owner save time?"
counter = 0

gathered_context = []
max_memories = 3

async def retrieve_memory():
    memories = await kernel.memory.search_async(memoryCollectionName, what_if_scenario, limit=max_memories, min_relevance_score=0.77)
    return memories
memories = asyncio.run(retrieve_memory())

for memory in memories:
    if counter == 0:
        related_memory = memory.text
    counter += 1
    gathered_context.append(memory.text + "\n")
    print(f"Hit {counter}: {memory.id} ")

skillsDirectory = "plugins-sk"
pluginFC = kernel.import_semantic_skill_from_directory(skillsDirectory, "FriendlyConsultant");

my_context = kernel.create_new_context()
my_context['input'] = what_if_scenario
my_context['context'] = "\n".join(gathered_context)

async def write_presentation():
    presentation = await kernel.run_async(pluginFC["Presentation"], input_context=my_context)
    return presentation

print(asyncio.run(write_presentation()))
