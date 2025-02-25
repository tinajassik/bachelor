from dotenv import load_dotenv
from fastapi import FastAPI
from src.api.skraafoto import router as skraafoto_router
from fastapi.middleware.cors import CORSMiddleware




# Initialize FastAPI app
app = FastAPI()

# Include API routes
app.include_router(skraafoto_router, prefix="/api/skraafoto")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Backend"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allow Angular frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
    """
    Main entry point for testing the project setup.
    """
    print("Testing imports and setup...")

    # Load environment variables
    load_dotenv() # might need to be moved as the first executed step since the FastAPI might need the environment variables. 
                  # Might cause issues

    print("Project setup looks good HUHU!")

    print("FastAPI app is set up and ready!")

# Run the test function if executed directly
if __name__ == "__main__":
    main()
