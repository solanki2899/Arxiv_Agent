import arxiv

# 1. Fetch the 5 most recent papers in AI
client = arxiv.Client()
results = client.results(arxiv.Search(query="category:cs.AI"))

print("--- ArXiv Watchdog Papers Fetched ---")
for paper in results:
    # 2. Extract Title and Summary
    title = paper.title
    abstract = paper.summary
