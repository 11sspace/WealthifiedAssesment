from app import create_app
app=create_app()
# Run this to test
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
