from app import main


try:
    main()
except Exception as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Interrupted")
