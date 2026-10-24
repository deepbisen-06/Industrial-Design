from chatbot import Retriever,Bot
from pathlib import Path
folder=Path(__file__).resolve().parents[1]/'sample_documents'
r=Retriever(folder)
cases=[('How often should bearings be inspected?','Bearing inspection'),('What is the bracket width tolerance?','Dimensional quality'),('What checks are required for motor overheating?','Motor overheating'),('What is required before maintenance energy isolation?','Energy isolation'),('Which revision of work instruction should be used?','Document control')]
for q,want in cases:
 hits=r.search(q);assert hits and want in hits[0][0][2],(q,hits)
assert r.search('What is the capital of Japan?')==[]
b=Bot(folder,extractive=True)
assert b.answer('What is the capital of Japan?')=='Not found in the supplied documents.'
assert 'EXTRACTIVE BASELINE' in b.answer('What is the bracket width tolerance?')
print('PASS: 5 top-1 retrieval cases; 1 unrelated-query rejection; 2 baseline behavior checks.')
print('Not tested: Hugging Face generation, grounded-answer accuracy, production safety.')
