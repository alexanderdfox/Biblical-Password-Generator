import os
import random
import hashlib
import datetime

# Path to Bible root folder
BIBLE_ROOT = "bible"  # Repo includes lowercase bible/ next to this script

# Leet speak mapping
LEET_MAP = {
	'a':'4','b':'8','c':'(','d':'d','e':'3','f':'f','g':'6','h':'#','i':'1',
	'j':'j','k':'k','l':'1','m':'m','n':'n','o':'0','p':'p','q':'q','r':'r',
	's':'5','t':'7','u':'u','v':'v','w':'w','x':'x','y':'y','z':'2',' ':'_'
}

def to_leet(text):
	return "".join(LEET_MAP.get(c.lower(), c) for c in text)

def pick_random_verse(root_folder):
	"""Pick a random book -> chapter -> verse using 'Chapter (n).txt' naming."""
	# Find all book folders
	books = [d for d in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, d))]
	if not books:
		raise ValueError("No book folders found!")
	book = random.choice(books)
	book_path = os.path.join(root_folder, book)

	# Find all chapter files named 'Chapter n.txt'
	chapters = [f for f in os.listdir(book_path) if f.startswith("Chapter ") and f.endswith(".txt")]
	if not chapters:
		raise ValueError(f"No chapters found in book {book}!")

	chapter_file = random.choice(chapters)
	chapter_path = os.path.join(book_path, chapter_file)

	# Pick a random verse from the chapter
	with open(chapter_path, encoding="utf-8") as f:
		verses = [line.strip() for line in f if line.strip()]
		if not verses:
			raise ValueError(f"No verses in {book}/{chapter_file}!")
		verse = random.choice(verses)

	# Reference for display
	ref = f"{book} {chapter_file.replace('.txt','')}"
	return ref, verse

def generate_password(ref, verse):
	leetverse = to_leet(f"{ref} {verse}")
	raw = f"{datetime.date.today().isoformat()}-{leetverse}"
	hashed = hashlib.sha256(raw.encode()).hexdigest()
	return hashed[:16]  # 16-character password

if __name__ == "__main__":
	ref, verse_text = pick_random_verse(BIBLE_ROOT)
	password = generate_password(ref, verse_text)

	print("Random Verse:")
	print(f"{ref} — {verse_text}\n")

	print("Leet Verse:")
	print(to_leet(f"{ref} {verse_text}") + "\n")

	print("Generated Password:")
	print(password)