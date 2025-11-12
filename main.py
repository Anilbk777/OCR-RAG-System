from app.use_cases.rag_qa_usecase import run_pipeline

API_KEY = "AIzaSyB_MD1bo1nDCdUw7Gy4-8S7rvnt61zTY9A"

if __name__ == "__main__":
    outputs = run_pipeline(API_KEY)
    for o in outputs:
        print(o)
