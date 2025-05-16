import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from app.config import settings
from bson import ObjectId

MONGODB_URI = settings.MONGODB_URI
DB_NAME = "god_talk"

# Sample questions for different gods
QUESTIONS = [
    {
        "question": "How can I find peace amidst chaos?",
        "god_id": "Shiva",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What does it mean to destroy ego?",
        "god_id": "Shiva",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why is detachment important in life?",
        "god_id": "Shiva",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How can I balance meditation and action?",
        "god_id": "Shiva",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the path to self-realization?",
        "god_id": "Shiva",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why do you hold the Ganga in your hair?",
        "god_id": "Shiva",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the story behind your Tandava dance?",
        "god_id": "Shiva",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why did you consume the poison during Samudra Manthan?",
        "god_id": "Shiva",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Who is your consort Parvati and how did you meet?",
        "god_id": "Shiva",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why do you reside in cremation grounds?",
        "god_id": "Shiva",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the true meaning of karma yoga?",
        "god_id": "Krishna",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How can I stay detached from results?",
        "god_id": "Krishna",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why is devotion the highest path?",
        "god_id": "Krishna",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is your advice for handling moral dilemmas?",
        "god_id": "Krishna",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How to balance love and duty in life?",
        "god_id": "Krishna",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why did you steal butter as a child?",
        "god_id": "Krishna",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the story of your Ras Leela?",
        "god_id": "Krishna",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How did you lift the Govardhan hill?",
        "god_id": "Krishna",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What was your role in the Mahabharata?",
        "god_id": "Krishna",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why did you not prevent the war of Kurukshetra?",
        "god_id": "Krishna",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How can I overcome obstacles in life?",
        "god_id": "Ganesh",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why is focus important in learning?",
        "god_id": "Ganesh",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How to stay grounded while achieving success?",
        "god_id": "Ganesh",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the power of beginnings?",
        "god_id": "Ganesh",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How can I develop wisdom and clarity?",
        "god_id": "Ganesh",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why do you have an elephant head?",
        "god_id": "Ganesh",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the story behind your broken tusk?",
        "god_id": "Ganesh",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How did you become the scribe of the Mahabharata?",
        "god_id": "Ganesh",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why do people worship you before starting anything new?",
        "god_id": "Ganesh",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What happened in the race with your brother Kartikeya?",
        "god_id": "Ganesh",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the purpose of creation?",
        "god_id": "Brahma",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How is knowledge related to spiritual growth?",
        "god_id": "Brahma",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why is it important to stay humble despite wisdom?",
        "god_id": "Brahma",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the role of time in creation and destruction?",
        "god_id": "Brahma",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How to cultivate a creative mindset?",
        "god_id": "Brahma",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why are there so few temples dedicated to you?",
        "god_id": "Brahma",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Who are the four Kumaras you created?",
        "god_id": "Brahma",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why did you sprout four heads?",
        "god_id": "Brahma",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What happened in your rivalry with Shiva?",
        "god_id": "Brahma",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Who is Saraswati and what is her role in your life?",
        "god_id": "Brahma",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What does it mean to live with dharma?",
        "god_id": "Ram",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How can I remain righteous during hardships?",
        "god_id": "Ram",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why is loyalty important in relationships?",
        "god_id": "Ram",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How to lead with compassion and strength?",
        "god_id": "Ram",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the value of sacrifice for the greater good?",
        "god_id": "Ram",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why did you go to exile for 14 years?",
        "god_id": "Ram",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the story behind building the bridge to Lanka?",
        "god_id": "Ram",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How did you defeat Ravana?",
        "god_id": "Ram",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why did you leave Sita after the war?",
        "god_id": "Ram",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the significance of your return as Ram Rajya?",
        "god_id": "Ram",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How can I develop unshakable devotion?",
        "god_id": "Hanuman",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the secret to inner strength?",
        "god_id": "Hanuman",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How do I serve selflessly?",
        "god_id": "Hanuman",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why is humility important even with great power?",
        "god_id": "Hanuman",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How to stay fearless in difficult times?",
        "god_id": "Hanuman",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "How did you leap across the ocean to Lanka?",
        "god_id": "Hanuman",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why did you tear open your chest to show Ram and Sita?",
        "god_id": "Hanuman",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the story of your childhood mischief?",
        "god_id": "Hanuman",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "What is the significance of Hanuman Chalisa?",
        "god_id": "Hanuman",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "question": "Why are you considered immortal?",
        "god_id": "Hanuman",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

async def init_questions():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    
    # Get all gods to map names to ObjectIds
    gods = await db["gods"].find().to_list(length=None)
    if not gods:
        print("No gods found in the database. Please initialize gods first.")
        return
        
    god_name_to_id = {god["name"]: god["_id"] for god in gods}
    
    # Replace god names with ObjectIds
    questions_with_ids = []
    for question in QUESTIONS:
        god_name = question["god_id"]
        if god_name in god_name_to_id:
            question_copy = question.copy()
            question_copy["god_id"] = god_name_to_id[god_name]
            questions_with_ids.append(question_copy)
        else:
            print(f"Warning: God '{god_name}' not found in database, skipping question: {question['question']}")
    
    # Optionally clear existing questions
    await db["questions"].delete_many({})
    
    # Insert new questions
    if questions_with_ids:
        await db["questions"].insert_many(questions_with_ids)
        print(f"Database initialized with {len(questions_with_ids)} predefined questions.")
    else:
        print("No questions were added. Make sure gods exist in the database first.")

if __name__ == "__main__":
    asyncio.run(init_questions()) 