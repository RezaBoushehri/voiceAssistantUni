def voice_assistant():
    # Step 1: Record and recognize speech (offline)
    recognized_text = recognize_speech()
    
    if recognized_text:
        # Step 2: Process recognized text with NLTK
        processed_text = process_text(recognized_text)
        print(f"Processed Text: {processed_text}")
        
        # Step 3: Perform NLP tasks with BERT (offline)
        question = "What is the capital of France?"  # Example question
        context = recognized_text  # Use recognized text as context
        answer = get_answer_from_bert(question, context)
        print(f"Assistant Answer: {answer}")
    else:
        print("Sorry, I couldn't understand that.")

# Run the voice assistant
voice_assistant()
